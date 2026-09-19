from pathlib import Path

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

load_dotenv()


CHROMA_DIR = "chroma_db"


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


vector_store = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings,
)


retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
)


prompt = ChatPromptTemplate.from_template("""
You are a helpful and expert Singapore Travel Assistant.
Answer the user's question using ONLY the provided context below.

Context:
{context}

Question:
{question}

Instructions:
1. Provide accurate, clear, and relevant information derived strictly from the context.
2. If the answer is not contained within the provided context, politely state:
   "I don't have enough information in my database to answer that question."
3. Keep your response friendly, clear, and well-formatted using Markdown bullet points where applicable.
""")


def retrieve_documents(question: str):
    logger.info("[RAG] Searching knowledge base")
    documents = retriever.invoke(question)
    logger.info("[RAG] Retrieved %d documents", len(documents))
    return documents


def format_context(documents):
    parts = []
    for index, document in enumerate(documents, start=1):
        source_title = document.metadata.get("source_title", "Unknown source")
        source_url = document.metadata.get("source_url", "")
        parts.append(
            f"SOURCE {index}\n"
            f"Title: {source_title}\n"
            f"URL: {source_url}\n"
            f"Content: {document.page_content}"
        )
    return "\n\n".join(parts)

# --------------------------------------------------
# RAG chain
# --------------------------------------------------

rag_chain = (
    {
        "context": retriever | format_context,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)



def answer_from_rag(question: str,):

    logger.info("[RAG] RAG called")
    logger.info("[RAG] Question: %s", question)

    documents = retrieve_documents(question)

    answer = rag_chain.invoke(question)

    sources = []

    for document in documents:
     source = {
        "title": document.metadata.get("source_title", "Unknown"),
        "url": document.metadata.get("source_url", ""),
     }
     if source not in sources:
         sources.append(source)

    return {
        "answer": answer,
        "sources": sources,
    }
