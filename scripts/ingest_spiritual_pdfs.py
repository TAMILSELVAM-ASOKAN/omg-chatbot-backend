from langchain_community.document_loaders import PyPDFLoader
from utils.vector_store import embedding_model
from utils.postgres_connector import get_db_connection
import os


PDF_PATHS = [
    r"C:\GWC\OMG_CHATBOT\backend\documents\story_diwali.pdf",
    r"C:\GWC\OMG_CHATBOT\backend\documents\story_ganesha.pdf",
    r"C:\GWC\OMG_CHATBOT\backend\documents\story_shivaratri.pdf",
]


def store_documents(texts: list[str], source: str):
    embeddings = embedding_model.embed_documents(texts)

    sql = """
    INSERT INTO spiritual_documents (source, content, embedding)
    VALUES (%s, %s, %s)
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for text, emb in zip(texts, embeddings):
                cur.execute(sql, (source, text, emb))
        conn.commit()


def load_pdf(path: str) -> list[str]:
    loader = PyPDFLoader(path)
    docs = loader.load()
    return [d.page_content for d in docs]


def ingest_pdf(pdf_path: str):
    source_name = os.path.basename(pdf_path)
    texts = load_pdf(pdf_path)
    store_documents(texts, source=source_name)
    print(f"Ingested: {source_name}")

def ingest_all_pdfs(pdf_paths: list[str]):
    for path in pdf_paths:
        ingest_pdf(path)

