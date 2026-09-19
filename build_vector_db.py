from pathlib import Path

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


KNOWLEDGE_DIR = Path("knowledge_base")
CHROMA_DIR = "chroma_db"

SOURCE = {
    "singapore_basic_info.txt": {
        "title": "Singapore - Wikivoyage Travel Guide",
        "url": "https://en.wikivoyage.org/wiki/Singapore",
    },
    "singapore_things_to_do.txt": {
        "title": "Singapore - Things To Do",
        "url": "https://www.visitsingapore.com/things-to-do/top-things-to-do/",
    },
    "singapore_itinerary.txt": {
        "title": "Visit Singapore - Itineraries",
        "url": "https://www.visitsingapore.com/travel-tips/travelling-to-singapore/itineraries/",
    },
}


def load_documents():

    documents = []

    for filename, metadata in SOURCE.items():

        path = KNOWLEDGE_DIR / filename

        if not path.exists():
            print(f"Missing: {path}")
            continue

        text = path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source_title": metadata["title"],
                    "source_url": metadata["url"],
                },
            )
        )

    return documents


def main():

    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} source documents.")

    if not documents:
        raise RuntimeError("No knowledge-base documents found.")

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Gemini embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    print("Creating Chroma vector store...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    print("Knowledge base created successfully!")


if __name__ == "__main__":
    main()
