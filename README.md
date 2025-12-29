# 🚀 GraphMind: Advanced RAG-Powered AI Agent

**GraphMind** is a full-stack AI application designed to provide intelligent, context-aware responses using Retrieval-Augmented Generation (RAG). By combining a structured Python backend with graph-based logic, this agent can maintain complex conversation states and retrieve information from a private knowledge base in real-time.

---

## 🌟 Highlights
- **Stateful Logic:** Utilizes `graph.py` to manage complex decision-making and agentic workflows.
- **RAG Integration:** Connects to a `vector_db` to perform semantic search across uploaded documents.
- **Persistent Memory:** Uses an SQLite database (`chatbot.db`) to ensure conversation history is never lost.
- **Clean Architecture:** Separation of concerns between the API logic (Backend) and the UI (Frontend).

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.9+ |
| **AI Framework** | LangGraph / LangChain |
| **API Layer** | FastAPI / Flask |
| **Database** | SQLite & Vector Storage (Chroma/FAISS) |
| **Frontend** | HTML5, CSS3, JavaScript |

---

## 📂 Project Structure

```text
LG_CB/
├── backend/
│   ├── graph.py          # State-machine logic and agent workflows
│   ├── main.py           # API endpoints and server configuration
│   ├── schemas.py        # Data models and validation
│   └── __init__.py       # Package initialization
├── frontend/
│   └── index.html        # Main web interface
├── uploads/              # Local storage for user-uploaded documents
├── vector_db/            # Persistent storage for document embeddings
├── .env                  # Secure environment variables (Hidden)
├── chatbot.db            # SQLite database for session history
└── requirements.txt      # Dependency list
