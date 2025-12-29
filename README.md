# 🚀 GraphMind: Advanced RAG-Powered AI Agent

**GraphMind** is a full-stack AI application designed to provide intelligent, context-aware responses using Retrieval-Augmented Generation (RAG). By combining a structured Python backend with graph-based logic, this agent can maintain complex conversation states and retrieve information from a private knowledge base in real-time.

---

## 🌟 Highlights
- **Stateful Logic:** Utilizes `graph.py` to manage complex decision-making and agentic workflows.
- **RAG Integration:** Connects to a `vector_db` to perform semantic search across uploaded documents.
- **Persistent Memory:** Uses an SQLite database (`chatbot.db`) to ensure conversation history is never lost.
- **Clean Architecture:** Separation of concerns between the API logic (Backend) and the UI (Frontend).


## 💎 Advanced Features

### 🔌 Model Context Protocol (MCP) Implementation
Unlike traditional hard-coded tools, GraphMind leverages the **MCP standard**, allowing for:
* **Dynamic Tool Discovery:** Seamlessly connect to external data sources (GitHub, Google Drive, Local Filesystem) using a unified protocol.
* **Contextual Intelligence:** Only relevant tools are invoked based on the conversation state, reducing latency and cost.

### ⚡ Real-Time Streaming (UX First)
The application is optimized for responsiveness:
* **Token-by-Token Rendering:** Experience instant feedback as the LLM generates responses.
* **Agentic Step Visualization:** The UI tracks the agent's "thought process" as it transitions between graph nodes (e.g., *Retrieval* -> *Reasoning* -> *Responding*).

### 🧠 Persistent State & Session Management
Built to handle real-world interruptions:
* **Chat Resuming:** Leveraging LangGraph's `Checkpointer`, the agent can resume a conversation even after a server restart or browser refresh.
* **Automatic Chat Saving:** Every turn is serialized into the `chatbot.db` (SQLite), ensuring no data loss and allowing for historical session review.

---
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
