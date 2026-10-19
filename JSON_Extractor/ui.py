
import json
import streamlit as st

from extractor import analyze_document


st.set_page_config(
    page_title="JSON Extractor",
    page_icon="📄",
    layout="wide",
)

# -----------------------------
# Page styling
# -----------------------------

st.title("📄 AI JSON Extractor")
st.caption(
    "Extract structured information from invoices and resumes "
    "using LangChain, Gemini, and Pydantic."
)

st.divider()

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("⚙️ Settings")

    document_type = st.selectbox(
        "Document Type",
        ["invoice", "resume"],
        format_func=lambda x: x.title(),
    )

    st.info(
        "The selected document type determines how the "
        "document is analyzed."
    )

    st.markdown("### Technology Stack")
    st.markdown(
        "- Streamlit\n"
        "- LangChain\n"
        "- Google Gemini\n"
        "- Pydantic\n"
        "- JSON"
    )

# -----------------------------
# Main input area
# -----------------------------

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("📝 Document Input")

    with st.form("document_form"):
        document_content = st.text_area(
            "Paste your document content",
            height=350,
            placeholder=(
                "Paste invoice or resume text here..."
            ),
        )

        analysis_requirements = st.text_input(
            "Analysis Requirements",
            value=(
                "Extract all relevant information from "
                "the document."
            ),
            help="Specify the fields you want to extract.",
        )

        submitted = st.form_submit_button(
            "🚀 Analyze Document",
            type="primary",
            use_container_width=True,
        )

with right:
    st.subheader("📊 Analysis Results")

    if submitted:
        if not document_content.strip():
            st.warning(
                "Please paste some document content first."
            )

        else:
            with st.spinner(
                "Analyzing your document with Gemini..."
            ):
                try:
                    result = analyze_document(
                        document_type=document_type,
                        document_content=document_content,
                        analysis_requirements=analysis_requirements,
                    )

                    result_data = result.model_dump(
                        mode="json"
                    )

                    st.session_state["result_data"] = result_data

                except Exception as exc:
                    st.error(
                        "Document analysis failed. "
                        "Check your API key, model availability, "
                        "network connection, and structured-output "
                        "compatibility."
                    )

                    with st.expander("Technical error details"):
                        st.code(str(exc))

    # Show the latest result, including after reruns
    result_data = st.session_state.get("result_data")

    if result_data:
        if result_data.get("status") == "success":
            st.success("Analysis completed successfully!")
        else:
            st.warning("The document could not be analyzed.")

        st.json(result_data)

        json_text = json.dumps(
            result_data,
            indent=2,
            ensure_ascii=False,
        )

        st.download_button(
            label="⬇️ Download JSON",
            data=json_text,
            file_name=f"{result_data['document_type']}_analysis.json",
            mime="application/json",
            use_container_width=True,
        )

    else:
        st.info(
            "Your extracted JSON will appear here after "
            "you analyze a document."
        )

st.divider()

st.caption(
    "Built with Streamlit, LangChain, Google Gemini, and Pydantic."
)
