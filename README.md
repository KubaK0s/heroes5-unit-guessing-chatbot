# 🏰 Heroes V Unit Guesser - AI Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-v0.3-green)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.0-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Heroes V Unit Guesser** to inteligentny agent konwersacyjny oparty na modelu językowym (LLM) oraz technice RAG (Retrieval-Augmented Generation). Aplikacja służy do interaktywnej gry, w której użytkownik opisuje jednostkę z gry *Heroes of Might and Magic V*, a AI próbuje ją zgadnąć, posiłkując się wiedzą z załączonego bestiariusza PDF.

Projekt zrealizowany w ramach zaliczenia przedmiotów: **Projekt z PPP** oraz **OiRPOS**.

---

## 📑 Spis treści
1. [Opis projektu](#-opis-projektu)
2. [Technologie](#-technologie)
3. [Funkcjonalności](#-funkcjonalności)
4. [Struktura Projektu](#-struktura-projektu)
5. [Instrukcja Uruchomienia (Developer)](#-instrukcja-uruchomienia-developer)
6. [Instrukcja Użytkowania](#-instrukcja-użytkowania)
7. [Opis API i Architektura](#-opis-api-i-architektura)
8. [Autorzy](#-autorzy)

---

## 📝 Opis projektu

Celem aplikacji jest demonstracja możliwości nowoczesnych frameworków AI (LangChain, LangGraph) w tworzeniu agentów posiadających "pamięć" oraz dostęp do zewnętrznych źródeł danych (narzędzi).

Aplikacja symuluje eksperta gry Heroes V. Agent:
- Analizuje opis użytkownika w języku naturalnym.
- Wyszukuje pasujące jednostki w wektorowej bazie danych (stworzonej z pliku PDF).
- Zadaje pytania doprecyzowujące.
- Finalizuje grę poprzez wywołanie specjalnego narzędzia do "zgadywania".

---

## 🛠 Technologie

W projekcie wykorzystano następujące biblioteki i narzędzia Open Source:

* **[Python 3.10+](https://www.python.org/)**: Język programowania.
* **[LangChain](https://www.langchain.com/)**: Framework do budowania aplikacji opartych na LLM.
* **[LangGraph](https://langchain-ai.github.io/langgraph/)**: Biblioteka do tworzenia stanowych, wieloetapowych agentów (cykle decyzyjne).
* **[Google Gemini](https://ai.google.dev/)**: Model językowy (LLM) `gemini-2.0-flash` oraz model embedingów `embedding-001`.
* **[ChromaDB](https://www.trychroma.com/)**: Wektorowa baza danych do przechowywania i przeszukiwania treści bestiariusza.
* **[PyMuPDF](https://pymupdf.readthedocs.io/)**: Narzędzie do ekstrakcji tekstu z plików PDF.

---

## 🚀 Funkcjonalności

- **RAG (Retrieval-Augmented Generation)**: Agent nie zgaduje "na ślepo", lecz sprawdza fakty w załączonym dokumencie `Heroes5_bestiary.pdf`.
- **Pamięć konwersacji**: Dzięki `MemorySaver`, agent pamięta kontekst rozmowy i poprzednie wskazówki gracza.
- **Narzędzia (Tools)**:
    - `read_bestiary`: Wyszukiwanie semantyczne w bazie wektorowej.
    - `submit_final_guess`: Oficjalne zgłoszenie odpowiedzi i zakończenie pętli gry.
- **Interfejs konsolowy**: Prosta i czytelna interakcja w terminalu.

---

## 📂 Struktura Projektu

```bash
HeroesV-Guesser/
│
├── main.py                  # Główny plik uruchomieniowy aplikacji
├── requirements.txt         # Lista wymaganych bibliotek Python
├── Heroes5_bestiary.pdf     # Źródłowy plik wiedzy (Baza wiedzy RAG)
├── .env                     # Plik konfiguracyjny (Klucze API - ignorowany przez git)
├── chroma_heroes5_bestiary/ # Folder lokalnej bazy wektorowej (generowany automatycznie)
└── README.md                # Dokumentacja projektu
```

## ⚙️ Instrukcja Uruchomienia (Developer)

Aby uruchomić projekt lokalnie, upewnij się, że masz zainstalowane niezbędne narzędzia.

### 📋 Wymagania wstępne
* **Python 3.10** lub nowszy
* Konto Google z dostępem do **Google AI Studio** (dla modelu Gemini)
* Zainstalowany **Git**

### 📥 Instalacja krok po kroku

**1. Sklonuj repozytorium:**
Pobierz kod źródłowy na swój komputer i przejdź do katalogu projektu.
```bash
git clone [https://github.com/twoj-nick/HeroesV-Guesser.git](https://github.com/twoj-nick/HeroesV-Guesser.git)
cd HeroesV-Guesser
```
**2. Zainstaluj wymagane zależności: Zalecamy użycie wirtualnego środowiska (venv), a następnie instalację bibliotek z pliku requirements.txt.
pip install -r requirements.txt**
```bash
pip install -r requirements.txt
```
**3. Skonfiguruj klucze API: Utwórz plik o nazwie .env w głównym katalogu projektu i wklej do niego swój klucz (bez cudzysłowów):**
```bash
GOOGLE_API_KEY=TwojKlucz
```
**4. Uruchom aplikację:**
```bash
python main.py
```

## 🎮 Instrukcja Użytkowania

Interakcja z agentem odbywa się w konsoli. Poniżej znajduje się typowy przebieg sesji:

1.  **Start Gry:**
    Po uruchomieniu programu (`python main.py`) rozpocznie się inicjalizacja bazy wiedzy. Zobaczysz komunikat:
    > *Type your unit clues. Type 'exit' or 'quit' to stop.*

2.  **Rozgrywka:**
    * **Krok 1:** Opisz wybraną jednostkę z *Heroes of Might and Magic V*. Możesz podać jej frakcję, poziom, wygląd lub unikalne zdolności.
    * **Krok 2:** Agent przeanalizuje Twoją odpowiedź. Jeśli nie jest pewien, zada pytanie uściślające lub przeszuka bestiariusz.
    * **Krok 3:** Odpowiadaj na pytania Agenta, aż zgromadzi wystarczająco dużo informacji.

3.  **Zakończenie Rundy:**
    Gdy Agent nabierze pewności, zgłosi ostateczną odpowiedź w formacie:
    > *Gracz1, my final guess is: [Nazwa Jednostki]*

4.  **Wyjście:**
    Aby przerwać działanie programu w dowolnym momencie, wpisz komendę: `exit` lub `quit`.

---

## 🧠 Opis API i Architektura Systemu

Aplikacja została zbudowana w oparciu o architekturę agentową z wykorzystaniem frameworków **LangChain** oraz **LangGraph**. System nie wystawia publicznego API REST, lecz działa jako autonomiczna pętla decyzyjna (Agent Loop).

### 🏗 Schemat działania (Agent Flow)

```mermaid
graph TD
    Start([Start: Input Użytkownika]) --> Agent{Agent AI<br>Gemini 2.5 Flash}
    
    Agent -->|Decyzja: Potrzebuję wiedzy| ToolRead[Tool: read_bestiary]
    ToolRead -->|Zapytanie wektorowe| ChromaDB[(ChromaDB<br>Vector Store)]
    ChromaDB -->|Zwrot fragmentów PDF| ToolRead
    ToolRead -->|Kontekst| Agent
    
    Agent -->|Decyzja: Pytanie do gracza| Output[Pytanie doprecyzowujące]
    Output --> Start
    
    Agent -->|Decyzja: Mam pewność| ToolGuess[Tool: submit_final_guess]
    ToolGuess --> End([Koniec Gry / Wynik])

