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

### Wymagania
- Python 3.10 lub nowszy
- Konto Google z dostępem do Google Generative AI (Gemini)

### Instalacja

*  1. Sklonuj repozytorium:
  git clone <adres_repozytorium> cd HeroesV-Guesser
*  2.Zainstaluj wymagane zależności:
  pip install -r requirements.txt
*  3. Utwórz plik .env i uzupełnij klucz API:
  GOOGLE_API_KEY=twoj_klucz_api
*  4. Uruchom aplikację:
  python main.py


---

### 🎮 Instrukcja Użytkowania

```md
## 🎮 Instrukcja Użytkowania

1. Po uruchomieniu programu rozpoczyna się sesja gry.
2. Użytkownik opisuje wybraną jednostkę z gry Heroes V (np. frakcję, zdolności, styl walki).
3. Agent analizuje odpowiedź, zadaje pytania doprecyzowujące i korzysta z bestiariusza.
4. Po uzyskaniu wysokiej pewności agent zgłasza ostateczną odpowiedź.
5. Aby zakończyć działanie programu, należy wpisać `exit` lub `quit`.

## 🧠 Opis API i Architektura

Aplikacja została zbudowana w oparciu o architekturę agentową z wykorzystaniem
frameworków LangChain oraz LangGraph.

### Główne komponenty:
- **LLM (Google Gemini)** – analiza języka naturalnego i generowanie odpowiedzi.
- **Vector Store (ChromaDB)** – przechowywanie wektorowych reprezentacji jednostek.
- **Tools**:
  - `read_bestiary` – wyszukiwanie semantyczne w bazie wiedzy.
  - `submit_final_guess` – zakończenie gry i zgłoszenie odpowiedzi.
- **MemorySaver** – przechowywanie kontekstu rozmowy.

Każda jednostka w pliku PDF jest traktowana jako osobny dokument semantyczny,
co zapobiega mieszaniu informacji między jednostkami.




