# 🧠 LangGraph Conversational Bot

An **advanced, production-ready conversational AI system** built using **LangGraph**, **LangChain**, **FastAPI**, and **WebSockets**, supporting **tool calling, RAG (Retrieval-Augmented Generation), persistent memory, and MCP (Model Context Protocol) integrations**.

This project demonstrates how to build a **stateful, streaming, multi-tool AI chatbot** with real-world capabilities like document search, knowledge storage, calculators, stock prices, and timezone-aware system utilities.

---

## 🚀 Features

### 🔁 Stateful Conversations (LangGraph)
- Graph-based agent workflow
- Persistent conversation memory using SQLite
- Thread-based chat history with summaries

### 🧰 Tool Calling (Local + Remote)
- Arithmetic calculator
- Percentage calculator
- System date & time (timezone-aware)
- Stock price lookup (Alpha Vantage)
- DuckDuckGo web search
- Knowledge base search & save
- **MCP remote tools integration**

### 📚 Retrieval-Augmented Generation (RAG)
- Document embeddings using OpenAI Embeddings
- Vector storage via **ChromaDB**
- Semantic search over uploaded documents & saved notes

### 🔌 Real-Time Streaming
- WebSocket-based chat
- Token-level streaming responses
- Live tool execution status updates

### 🗂️ Thread Management
- Automatic conversation summaries
- Thread listing & persistence
- SQLite-backed checkpointing

---

## 🏗️ Project Structure

```text
LG_CB/
├── backend/
│   ├── graph.py          # LangGraph state machine, tools & agent logic
│   ├── main.py           # FastAPI app, WebSocket routes, server startup
│   ├── schemas.py        # Pydantic models & request/response schemas
│   └── __init__.py
├── frontend/
│   └── index.html        # Simple web-based chat UI
├── uploads/              # User-uploaded documents (PDFs, notes, etc.)
├── vector_db/            # ChromaDB persistent embeddings
├── .env                  # Environment variables (not committed)
├── chatbot.db            # SQLite database (chat memory & summaries)
└── requirements.txt      # Python dependencies
````

---

## ⚙️ Tech Stack

| Layer           | Technology             |
| --------------- | ---------------------- |
| LLM             | OpenAI (GPT-4o-mini)   |
| Agent Framework | LangGraph              |
| Tooling         | LangChain              |
| Backend         | FastAPI                |
| Transport       | WebSockets             |
| Vector DB       | Chroma                 |
| Embeddings      | OpenAI Embeddings      |
| Storage         | SQLite                 |
| MCP             | MultiServer MCP Client |
| Frontend        | HTML + JS              |

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

> ⚠️ Never commit `.env` files to GitHub

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/LG_CB.git
cd LG_CB
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Start Backend Server

```bash
uvicorn backend.main:app --reload
```

* WebSocket endpoint: `ws://localhost:8000/chat`
* API server runs on: `http://localhost:8000`

### Open Frontend

Open `frontend/index.html` in your browser.

---

## 🧠 How It Works

1. **User sends a message** via WebSocket
2. Message enters **LangGraph state machine**
3. LLM decides:

   * Respond directly **OR**
   * Call a tool (calculator, RAG, search, MCP, etc.)
4. Tool results are injected back into the graph
5. Response is streamed token-by-token to frontend
6. Conversation state is checkpointed in SQLite
7. First message auto-generates a thread summary

---

## 🧪 Example Tool Calls

* “What’s today’s date?”
* “Increase 5000 by 12%”
* “Search my documents for Docker”
* “Save this note for later”
* “Get stock price of AAPL”

---

## 🛠️ MCP Integration

This project supports **remote MCP servers**:

```python
MultiServerMCPClient({
  "expense": {
    "transport": "sse",
    "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
  }
})
```

MCP tools are dynamically discovered and merged with local tools at runtime.

---

## 🗄️ Persistence & Memory

* **Chat History** → SQLite checkpoints
* **Thread Summaries** → SQLite table
* **Documents & Notes** → ChromaDB
* **Uploads** → Local filesystem

---

## 📌 Future Enhancements

* Authentication & user-based threads
* File upload via frontend
* Advanced RAG (chunking, re-ranking)
* Observability (LangSmith / OpenTelemetry)
* Deployment (Docker + AWS / GCP)

---

## 👤 Author

**Keshav Reddy**
Data Analyst | GenAI | LangGraph | MLOps

---

## ⭐ If you find this useful

Give this repo a ⭐ and feel free to fork or extend it!
