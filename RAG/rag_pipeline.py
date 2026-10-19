
from pathlib import Path
import os
import tempfile

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

load_dotenv()


def _get_api_key():
    """Read the Gemini API key from environment variables or .env."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Add GEMINI_API_KEY=your_key "
            "to your .env file."
        )

    return api_key


def _load_uploaded_file(uploaded_file):
    """Load an uploaded PDF or TXT file with source metadata."""
    name = uploaded_file.name
    content = uploaded_file.getvalue()
    suffix = Path(name).suffix.lower()

    if suffix == ".pdf":
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".pdf"
            ) as tmp:
                tmp.write(content)
                temp_path = tmp.name

            docs = PyPDFLoader(temp_path).load()

            for doc in docs:
                # Keep the original uploaded filename for citations.
                doc.metadata["source"] = name

                # Convert zero-based PDF page indices to 1-based pages.
                doc.metadata["page"] = (
                    int(doc.metadata.get("page", 0)) + 1
                )

            return docs

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    elif suffix == ".txt":
        text = content.decode("utf-8", errors="replace")

        return [
            Document(
                page_content=text,
                metadata={"source": name, "page": 1},
            )
        ]

    else:
        raise ValueError(
            f"Unsupported file type: {suffix}. Upload a PDF or TXT file."
        )


def build_vector_store(uploaded_files):
    """Load documents, split them, embed chunks and create a FAISS index."""
    all_docs = []
    names = []

    for uploaded_file in uploaded_files:
        docs = _load_uploaded_file(uploaded_file)

        if not any(doc.page_content.strip() for doc in docs):
            continue

        all_docs.extend(docs)
        names.append(uploaded_file.name)

    if not all_docs:
        raise ValueError(
            "No readable text found. Check your files. "
            "Scanned PDFs may require OCR."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        add_start_index=True,
    )

    chunks = splitter.split_documents(all_docs)

    if not chunks:
        raise ValueError("No text chunks could be created.")

    api_key = _get_api_key()

    # Gemini embeddings convert document chunks into vectors.
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key,
    )

    # Store vectors locally in a FAISS index.
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store, names


def _extract_plain_text(content):
    """Convert Gemini response content into ordinary readable text."""

    # Most common case: response.content is already a string.
    if isinstance(content, str):
        return content.strip()

    # Some model responses contain a list of content blocks.
    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                if (
                    block.get("type") == "text"
                    and isinstance(block.get("text"), str)
                ):
                    text_parts.append(block["text"])

            else:
                # Support content block objects with a text attribute.
                block_text = getattr(block, "text", None)

                if isinstance(block_text, str):
                    text_parts.append(block_text)

        return "\n".join(text_parts).strip()

    # Avoid displaying raw dictionaries or metadata to the user.
    return ""


def answer_question(vector_store, question: str):
    """Retrieve relevant document chunks and answer using Gemini."""

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question about your document.",
            "sources": [],
        }

    # Retrieve the four most relevant chunks.
    retrieved = vector_store.similarity_search(question, k=4)

    if not retrieved:
        return {
            "answer": (
                "I couldn't find relevant information "
                "in the uploaded documents."
            ),
            "sources": [],
        }

    context_parts = []
    sources = []
    seen = set()

    for doc in retrieved:
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", 1)

        context_parts.append(
            f"[Source: {source}, page {page}]\n"
            f"{doc.page_content}"
        )

        source_key = (source, page)

        if source_key not in seen:
            sources.append(
                {
                    "source": source,
                    "page": f"Page {page}",
                    "snippet": doc.page_content[:280].replace(
                        "\n", " "
                    ),
                }
            )
            seen.add(source_key)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a document question-answering assistant.

Rules:
1. Answer using ONLY the retrieved document context.
2. Do not use outside knowledge or make up facts.
3. If the answer is not present in the context, say:
   "I couldn't find that information in the uploaded document."
4. Respond in normal, readable text.
5. Never return JSON, Python dictionaries, metadata,
   content-block structures, or signature information.
6. Use simple paragraphs or bullet points when appropriate.
7. Include relevant source citations in this format:
   (filename.pdf, page 2)
8. Be clear, concise, and directly answer the question.
                """,
            ),
            (
                "human",
                """
Question:
{question}

Retrieved document context:
{context}

Write the answer as plain, readable text.
                """,
            ),
        ]
    )

    api_key = _get_api_key()

    # Gemini generates the final answer.
    model = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
        max_output_tokens=2048,
        api_key=api_key,
    )

    chain = prompt | model

    response = chain.invoke(
        {
            "question": question,
            "context": "\n\n---\n\n".join(context_parts),
        }
    )

    # Extract only text, never the full response object or metadata.
    answer = _extract_plain_text(response.content)

    if not answer:
        answer = (
            "I couldn't generate a readable answer. "
            "Please try asking the question again."
        )

    return {
        "answer": answer,
        "sources": sources,
    }
