"""Test script to check PDF content"""
from langchain_community.document_loaders import PyPDFLoader

pdf_path = "Tafseer Ibn-e-Kaseer 01.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"Total pages: {len(documents)}")
print(f"\nFirst page content length: {len(documents[0].page_content)}")
print(f"\nFirst 500 characters of page 1:")
print(documents[0].page_content[:500])
print(f"\nLast 500 characters of page 1:")
print(documents[0].page_content[-500:])

# Check a few more pages
for i in [0, 1, 2, 10, 50]:
    if i < len(documents):
        print(f"\n--- Page {i+1} ---")
        print(f"Content length: {len(documents[i].page_content)}")
        print(f"Sample: {documents[i].page_content[:200]}")
