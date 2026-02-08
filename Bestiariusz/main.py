import os
import sys
# Usunęliśmy import time, bo nie jest już potrzebny do spowalniania
from typing import Any, List, Optional, Dict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage, AIMessage
from langchain_core.vectorstores import VectorStore
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.tools import BaseTool, tool, ToolRuntime
from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

# Convenience typedefs
AgentType = CompiledStateGraph[Any, Any, Any, Any]
TodoType = Dict[str, Any]


def player_chat_conversation(agent: AgentType, player_name: str) -> Optional[str]:
    config = {
        "configurable": {
            "player_name": player_name,
            "thread_id": f"session-{player_name.replace(' ', '_')}",
        }
    }

    final_guess: Optional[str] = None
    print(f"\n--- Rozpoczęto grę: Zgadywanie jednostki Heroes V ---")
    print("Opisz jednostkę (statystyki, wygląd, umiejętności). Wpisz 'exit' by zakończyć.\n")

    while True:
        try:
            user_input: str = input(f"{player_name}: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                break

            # Usunęliśmy sztuczne "Agent myśli..." i sleep

            for event in agent.stream(
                    {"messages": [{"role": "user", "content": user_input}]},
                    config=config,
                    stream_mode="values",
            ):
                msg = event["messages"][-1]

                if not isinstance(msg, AIMessage):
                    continue

                if isinstance(msg.content, str) and msg.content:
                    print(f"Agent: {msg.content}")
                elif isinstance(msg.content, list):
                    for block in msg.content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            print(f"Agent: {block['text']}")

            state = agent.get_state(config)
            guess = state.values.get("final_unit_guess")

            if guess is not None:
                final_guess = guess
                break

        except KeyboardInterrupt:
            print("\nPrzerwano przez użytkownika.")
            break
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    return final_guess


def load_bestiary(document_path: str, text_splitter: TextSplitter, skip_pages: int = 0) -> List[Document]:
    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Nie znaleziono pliku bestiariusza: {document_path}")

    pdf_loader = PyMuPDFLoader(document_path)
    docs = pdf_loader.load()
    docs_to_split = docs[skip_pages:] if skip_pages > 0 else docs
    return text_splitter.split_documents(docs_to_split)


def prepare_vector_store(encyclopedia_chunks: List[Document], embeddings: Embeddings) -> VectorStore:
    persist_dir = "./chroma_heroes5_bestiary"

    vectorstore = Chroma(
        collection_name="heroes5_units",
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    if vectorstore._collection.count() == 0:
        print("Indeksowanie bestiariusza... (to może chwilę potrwać)")
        vectorstore.add_documents(encyclopedia_chunks)
        print("Zakończono indeksowanie.")

    return vectorstore


def guess_unit_agent_setup(
        document_path: str,
        skip_pages: int = 0,
        # Teraz, gdy masz płatne konto, ten model powinien działać najlepiej:
        model_name: str = "gemini-2.0-flash"
) -> AgentType:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        add_start_index=True
    )

    try:
        bestiary_chunks = load_bestiary(document_path, text_splitter, skip_pages)
    except FileNotFoundError as e:
        print(f"Błąd krytyczny: {e}")
        sys.exit(1)

    bestiary_vector_store = prepare_vector_store(bestiary_chunks, embeddings)

    @tool(response_format="content_and_artifact")
    def read_bestiary(query: str):
        """Retrieve information from the Heroes V bestiary PDF to verify unit details."""
        # Zwiększamy k do 3, bo masz większe limity i możesz przetworzyć więcej tekstu
        retrieved_docs = bestiary_vector_store.similarity_search(query, k=3)

        serialized = "\n\n".join(
            f"Source Page: {doc.metadata.get('page', 'Unknown')}\nContent: {doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    @tool
    def submit_final_guess(runtime: ToolRuntime[TodoType, TodoType], unit: str) -> Command:
        """Submit the final unit guess when you are 100% sure. Ends the game."""
        config = runtime.config or {}
        configurable = config.get("configurable") or {}
        player_name = configurable.get("player_name", "Player")

        msg = ToolMessage(
            content=f"Gratulacje {player_name}! Moja ostateczna odpowiedź to: {unit}",
            tool_call_id=runtime.tool_call_id,
            name="submit_final_guess",
        )

        return Command(
            update={
                "messages": [msg],
                "final_unit_guess": unit,
            }
        )

    tools = [read_bestiary, submit_final_guess]

    system_prompt = (
        "Jesteś inteligentnym detektywem w świecie Heroes of Might and Magic V. "
        "Twoim celem jest jak najszybsze zgadnięcie jednostki, o której myśli gracz. "

        "STRATEGIA DZIAŁANIA (Postępuj krok po kroku):"
        "1. ELIMINACJA: Jeśli nie znasz Frakcji (Zamek/Town), zapytaj o nią w pierwszej kolejności (np. 'Czy twoja jednostka należy do Przystani lub Inferno?')."
        "2. ROLA: Zapytaj o typ jednostki (Strzelec, Latająca, Piechota, Magiczna)."
        "3. POZIOM: Zapytaj o Tier (Poziom) jednostki (np. 'Czy to jednostka wysokiego poziomu 5-7?')."
        "4. SZCZEGÓŁY: Dopiero gdy masz 2-3 kandydatów, pytaj o konkretne umiejętności lub statystyki, używając narzędzia 'read_bestiary'."

        "ZASADY:"
        "- NIE zgaduj 'na ślepo'. Zgaduj tylko, gdy jesteś na 90% pewien."
        "- Zadawaj pytania, na które łatwo odpowiedzieć TAK/NIE."
        "- Analizuj poprzednie odpowiedzi. Jeśli gracz powiedział, że jednostka NIE lata, nie pytaj czy to Gryf."
        "- Jeśli używasz narzędzia 'read_bestiary', szukaj ogólnych haseł, np. 'Inferno units list' zamiast konkretnych statystyk na początku."

        "Kiedy będziesz pewny w 100%, użyj narzędzia 'submit_final_guess' z dokładną nazwą jednostki."

        "FORMAT ODPOWIEDZI:"
        "Zawsze zaczynaj od krótkiej analizy w nawiasie, np.:"
        "(Gracz potwierdził Inferno. Odrzucam Impa bo nie strzela. Zostają Sukub i Zmora. Muszę zapytać o strzelanie.)"
        "Twoje pytanie do gracza..."
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=MemorySaver()
    )

    return agent


def main():
    if not load_dotenv():
        print("Ostrzeżenie: Nie znaleziono pliku .env lub jest pusty.")

    if not os.getenv("GOOGLE_API_KEY"):
        print("Błąd: Brak klucza GOOGLE_API_KEY w zmiennych środowiskowych.")
        return

    pdf_path = os.path.join(os.path.dirname(__file__), "Heroes5_bestiary.pdf")

    agent = guess_unit_agent_setup(
        document_path=pdf_path,
        skip_pages=8,
    )

    final_guess = player_chat_conversation(
        agent=agent,
        player_name="Gracz1",
    )

    if final_guess:
        print(f"\n--- KONIEC GRY ---\nZgadnięta jednostka: {final_guess}")
    else:
        print("\nGra zakończona bez odgadnięcia.")


if __name__ == "__main__":
    main()