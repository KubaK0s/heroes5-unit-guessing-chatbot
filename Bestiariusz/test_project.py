import os
from main import load_bestiary
from langchain_text_splitters import RecursiveCharacterTextSplitter

def test_pdf_exists():
    assert os.path.exists("Heroes5_bestiary.pdf")

def test_load_bestiary_missing_file():
    splitter = RecursiveCharacterTextSplitter(chunk_size=100)
    try:
        load_bestiary("nieistniejacy_plik.pdf", splitter)
        assert False 
    except FileNotFoundError:
        assert True   
