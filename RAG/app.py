import streamlit as st
from pathlib import Path
from rag_pipeline import build_vector_store, answer_question

st.set_page_config(page_title="Document Q&A | RAG", page_icon="📚", layout="wide")

st.title("📚 Document Q&A Assistant")
st.caption("Ask questions about your PDF or TXT documents. Answers are grounded in the uploaded content and include page/source references.")

with st.sidebar:
    st.header("📄 Your documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files. PDF page numbers are preserved for citations.",
    )
    st.info("For best results, ask specific questions about the uploaded documents.")
    if st.button("Clear session", use_container_width=True):
        for key in ("vector_store", "document_names", "chat_history"):
            st.session_state.pop(key, None)
        st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_files:
    current_signature = tuple((f.name, len(f.getvalue())) for f in uploaded_files)
    if st.session_state.get("upload_signature") != current_signature:
        with st.spinner("Reading documents, splitting text, and creating embeddings..."):
            try:
                store, names = build_vector_store(uploaded_files)
                st.session_state.vector_store = store
                st.session_state.document_names = names
                st.session_state.upload_signature = current_signature
                st.session_state.chat_history = []
                st.success(f"Indexed {len(names)} document(s). You can ask questions now.")
            except Exception as exc:
                st.error(f"Could not process the documents: {exc}")
                st.stop()

if st.session_state.get("document_names"):
    st.success("Ready: " + ", ".join(st.session_state.document_names))
else:
    st.warning("Upload one or more PDF/TXT documents in the sidebar to get started.")
    st.markdown("### Try the included example")
    st.write("This project includes `examples/example_document.txt`. Upload it using the sidebar, or replace it with your own document.")

for item in st.session_state.chat_history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
        if item.get("sources"):
            with st.expander("Sources"):
                for source in item["sources"]:
                    st.write(f"**{source['source']}** — {source['page']}")
                    if source.get("snippet"):
                        st.caption(source["snippet"])

question = st.chat_input("Ask a question about your uploaded documents...", disabled=not bool(st.session_state.get("vector_store")))
if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching your document and preparing an answer..."):
            try:
                result = answer_question(st.session_state.vector_store, question)
                st.markdown(result["answer"])
                if result["sources"]:
                    with st.expander("Sources"):
                        for source in result["sources"]:
                            st.write(f"**{source['source']}** — {source['page']}")
                            if source.get("snippet"):
                                st.caption(source["snippet"])
                st.session_state.chat_history.append({
                    "role": "assistant", "content": result["answer"], "sources": result["sources"]
                })
            except Exception as exc:
                st.error(f"Question answering failed: {exc}")
