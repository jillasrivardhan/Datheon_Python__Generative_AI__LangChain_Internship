# Generative AI Projects: RAG Document Q&A Assistant & JSON Extractor

A collection of two practical Generative AI projects exploring how language models can retrieve information from documents and transform unstructured text into structured data.

## 📌 Projects Overview

### 1. RAG Document Q&A Assistant

A document question-answering application that allows users to upload PDF or TXT files and ask questions about their content.

**Features**
- Upload PDF and TXT documents.
- Extract and split document text into manageable chunks.
- Generate embeddings using Google Gemini.
- Store and retrieve document vectors using FAISS.
- Retrieve relevant passages for each question.
- Generate context-based answers using a Gemini language model.
- Display source information where available.

**Workflow**

1. Upload a document.
2. Extract and split the document text.
3. Generate embeddings and create a FAISS vector index.
4. Ask a question about the document.
5. Retrieve relevant passages and generate an answer.

### 2. JSON Extractor

A text-to-JSON utility designed to extract useful information from unstructured text and organize it into a structured JSON object.

**Potential features**
- Extract specified fields from text.
- Convert unstructured information into JSON.
- Produce consistent data structures for further processing.
- Support workflows such as data cleaning, reporting, and API integration.

*Note: Update this section to match the actual fields, model, validation rules, and features supported by your implementation.*

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive interface for the RAG application |
| LangChain | LLM integration and document processing |
| Google Gemini | Embeddings and answer generation |
| FAISS | Vector similarity search |
| JSON | Structured data representation |

## 📁 Suggested Project Structure

```text
generative-ai-projects/
├── document_qa_rag/
│   ├── app.py
│   ├── rag_pipeline.py
│   ├── requirements.txt
│   ├── .env.example
│   └── examples/
│       └── example_document.txt
│
├── json_extractor/
│   ├── extractor.py
|    |__ ui.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md
```

Adjust the structure to match your actual files and folders.

## ⚙️ Getting Started

### Requirements

- Python 3.10 or newer, compatible with your dependencies.
- Google Gemini API key for the RAG application.
- Git (optional).

### 1. Clone the repository

Replace the placeholders with your repository details.

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
```

### 2. Run the RAG Document Q&A Assistant

Navigate to the project folder:

```bash
cd document_qa_rag
```

Create and activate a virtual environment.

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get an API key from [Google AI Studio](https://aistudio.google.com/apikey).

Start the application:

```bash
streamlit run app.py
```

### 3. Run the JSON Extractor

Navigate to the extractor directory:

```bash
cd ../json_extractor
```

If a `requirements.txt` file is available, install its dependencies:

```bash
pip install -r requirements.txt
```

Run the entry point appropriate to your implementation.

For a Streamlit application:

```bash
streamlit run app.py
```

For a Python script:

```bash
python <your_extractor_file>.py
```

If the extractor uses an external LLM API, configure its required environment variables locally.

## 🧪 JSON Extractor Example

**Input**

```text
Name: Ananya Rao. She is a Python developer and has
2 years of experience.
```

**Illustrative output**

```json
{
  "name": "Ananya Rao",
  "skills": ["Python"],
  "experience_years": 2
}
```

This is an example of the expected type of transformation, not a guarantee of your application's exact output schema.

## 🔐 Security and Best Practices

- Never commit API keys or credentials to GitHub.
- Keep secrets in a local `.env` file and add it to `.gitignore`.
- Commit a `.env.example` containing placeholders instead of real secrets.
- Verify important answers against the original document.
- Validate extracted JSON before using it in another application.
- Avoid processing sensitive documents without appropriate authorization.

## 🚀 Future Improvements

- Support additional document formats.
- Add document validation and configurable retrieval settings.
- Introduce JSON schema validation and improved error handling.
- Add automated tests and sample datasets.
- Improve logging, evaluation, and user feedback.

## 🤝 Contributing

Contributions and suggestions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request explaining your improvements.

For bugs or feature requests, open an issue with the relevant steps and error details. Never include API keys or private document contents.

## 📄 License

Choose a license, such as MIT, before publishing the repository, and include the corresponding `LICENSE` file.

## 👤 Author

**Srivardhan Jilla**

- LinkedIn: [linkedin.com/in/jilla-srivardhan](https://linkedin.com/in/jilla-srivardhan)
- GitHub: [github.com/jillasrivardhan](https://github.com/jillasrivardhan)

---

**About this repository:** These projects demonstrate two useful Generative AI workflows: retrieving relevant information from documents and converting unstructured text into structured data.
