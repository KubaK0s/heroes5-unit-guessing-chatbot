import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'Bestiariusz'))

from main import load_bestiary
from langchain_text_splitters import RecursiveCharacterTextSplitter

def test_pdf_exists():
    # Sprawdzamy ścieżkę wewnątrz folderu
    expected_path = os.path.join("Bestiariusz", "Heroes5_bestiary.pdf")
    assert os.path.exists(expected_path), f"Nie znaleziono pliku PDF w: {expected_path}"

def test_load_bestiary_missing_file():
    splitter = RecursiveCharacterTextSplitter(chunk_size=100)
    try:
        load_bestiary("nieistniejacy_plik.pdf", splitter)
        assert False  
    except FileNotFoundError:
        assert True  
