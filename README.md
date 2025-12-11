# OmniMind - Comprehensive Project Documentation

<p align="center">
  <img src="./assets/gradient_flow_logo_1764409055594.png" alt="OmniMind Logo" width="200">
</p>

<p align="center">
  <strong>Privacy-First AI-Native Local Workspace Platform</strong>
</p>

<p align="center">
  <a href="https://github.com/zengyuzhi/omnimind"><img src="https://img.shields.io/badge/GitHub-Repository-blue?logo=github" alt="GitHub"></a>
  <a href="https://github.com/GradientHQ/parallax"><img src="https://img.shields.io/badge/Powered%20by-Parallax-green" alt="Parallax"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"></a>
</p>

---

## Table of Contents

1. [What is OmniMind?](#what-is-omnimind)
2. [The Problem We Solve](#the-problem-we-solve)
3. [Key Features](#key-features)
4. [System Architecture](#system-architecture)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Installation and Setup](#installation-and-setup)
8. [Configuration Guide](#configuration-guide)
9. [API Reference](#api-reference)
10. [Agent System](#agent-system)
11. [RAG Knowledge Base](#rag-knowledge-base)
12. [MCP Integration](#mcp-integration)
13. [Security](#security)
14. [Troubleshooting](#troubleshooting)

---

## What is OmniMind?

**OmniMind** is a **privacy-first, AI-native local workspace platform** designed to empower teams and individuals with secure, intelligent collaboration. Unlike cloud-based AI solutions that send your data to third-party servers, OmniMind runs entirely on **YOUR infrastructure** using local LLM inference powered by [Parallax](https://github.com/GradientHQ/parallax).

### Core Philosophy

- **Privacy First**: All data stays on your hardware - chat history, documents, and vector embeddings never leave your infrastructure
- **Zero Token Costs**: After initial setup, there are no pay-per-token fees - you own the compute
- **Low Latency**: Local inference ensures millisecond-level responses
- **Full Control**: You own the models, the data, and the entire infrastructure

---

## The Problem We Solve

### Current Pain Points with Cloud AI Solutions

| Problem                 | Cloud AI Reality                          | OmniMind Solution                               |
| ----------------------- | ----------------------------------------- | ----------------------------------------------- |
| **Data Privacy**        | Sensitive data sent to external servers   | All data processed locally on YOUR hardware     |
| **Cost Explosion**      | Pay-per-token pricing accumulates rapidly | Zero inference costs after hardware setup       |
| **Latency Issues**      | Network round-trips add 200-500ms+ delay  | Local inference = instant responses             |
| **Vendor Lock-in**      | Dependent on provider API availability    | Complete ownership of models and infrastructure |
| **Context Isolation**   | Each conversation starts fresh            | Persistent context with RAG knowledge base      |
| **Passive Interaction** | Traditional bots only respond when asked  | Agents proactively participate in discussions   |

### Who Is This For?

- **Enterprise Teams** needing secure internal AI assistants without data leakage
- **Research Organizations** handling sensitive/proprietary information
- **Startups** wanting AI capabilities without recurring API costs
- **Developers** building AI-powered applications with full control
- **Privacy-Conscious Users** who refuse to share data with cloud providers

---

## Key Features

### Multi-Agent System

OmniMind supports multiple AI agents running simultaneously:

```
@AI-Assistant  -> General Q&A, code help, document analysis
@Writer        -> Content creation, editing, summarization
@Researcher    -> Web search, academic paper retrieval
```

**Agent Capabilities:**

- **Passive Response**: Reply when @mentioned
- **Proactive Response**: Actively participate without being mentioned
- **Emoji Reactions**: React to messages with contextual emojis
- **Summarization**: Generate conversation summaries on demand

### RAG Knowledge Base

Upload your documents and the AI gains access to your private knowledge:

- **Supported Formats**: PDF, DOCX, PPTX, TXT, Markdown
- **Semantic Search**: ChromaDB vector database with cosine similarity
- **Auto-Chunking**: Intelligent document splitting with overlap
- **Deduplication**: Hash-based document tracking

### MCP Tool Integration

Extend AI capabilities through Model Context Protocol:

- **Web Research**: Real-time web search and content extraction
- **Custom Tools**: Add your own tools via MCP servers
- **Function Calling**: Structured tool invocation with validation

### Real-Time Collaboration

- **Multiple Chat Rooms**: Create unlimited rooms for different topics
- **User Presence**: See who is online and typing in real-time
- **Message Threading**: Reply to specific messages with context
- **Reactions**: Add emoji reactions to messages

---

## System Architecture

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|   React Frontend | <-> |  Express Backend | <-> |   Parallax LLM   |
|   (Vite + TS)    |     |   (Node.js)      |     |  (Local Model)   |
|                  |     |                  |     |                  |
+------------------+     +--------+---------+     +------------------+
                                 |
         +-----------------------+-----------------------+
         |                       |                       |
         v                       v                       v
+------------------+    +------------------+    +------------------+
|                  |    |                  |    |                  |
|   RAG Service    |    |  Agent Service   |    |   MCP Server     |
|  (Flask+Chroma)  |    |  (Multi-Agent)   |    | (Research Tools) |
|                  |    |                  |    |                  |
+------------------+    +------------------+    +------------------+
```

### Data Flow

1. **User Input**: User sends message in React frontend
2. **Backend Processing**: Express server receives and validates
3. **Agent Detection**: Checks for @mentions or proactive triggers
4. **RAG Enhancement**: Retrieves relevant context from knowledge base
5. **LLM Inference**: Parallax generates response locally
6. **Response Delivery**: Real-time WebSocket update to all clients

---

## Technology Stack

### Frontend

| Technology       | Purpose                        |
| ---------------- | ------------------------------ |
| React 18.3       | Modern React with hooks        |
| TypeScript 5.8   | Type-safe development          |
| Vite 6.3         | Fast build tool and dev server |
| Framer Motion    | Smooth animations              |
| Socket.IO Client | Real-time communication        |

### Backend

| Technology  | Purpose                      |
| ----------- | ---------------------------- |
| Node.js 18+ | JavaScript runtime           |
| Express.js  | Web framework                |
| Socket.IO   | WebSocket server             |
| UUID        | Unique identifier generation |

### AI/ML Services

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Parallax   | Local LLM inference engine   |
| ChromaDB   | Vector database for RAG      |
| Flask      | Python web framework for RAG |

---

## Project Structure

```
OmniMind/
├── src/                          # Frontend source code
│   ├── components/               # React components
│   │   ├── MessageBubble/        # Chat message display
│   │   ├── ChatSidebar.tsx       # Room navigation
│   │   ├── MessageInput.tsx      # Message composition
│   │   └── MessageList.tsx       # Message display
│   ├── api/                      # API client
│   ├── context/                  # React contexts
│   ├── hooks/                    # Custom hooks
│   └── types/                    # TypeScript types
├── server/                       # Backend server
│   ├── server.js                 # Express + Socket.IO
│   └── data.json                 # Local data storage
├── agents/                       # AI agent services
│   ├── agent_service.py          # Main agent runner
│   ├── base_agent.py             # Agent base class
│   ├── core/                     # Agent core modules
│   ├── rag/                      # RAG service
│   └── mcp/                      # MCP server
└── package.json                  # Node.js dependencies
```

---

## Installation and Setup

### Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.10+** - [Download](https://python.org/)
- **Parallax** - [Installation Guide](https://github.com/GradientHQ/parallax)
- **Git** - [Download](https://git-scm.com/)

### Step 1: Clone Repository

```bash
git clone https://github.com/ayusingh-54/OmniMind---Comprehensive-Project-Documentation.git
cd OmniMind
```

### Step 2: Install Node.js Dependencies

```bash
npm install
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r agents/rag/requirements.txt
pip install -r agents/requirements.txt
```

### Step 4: Start Parallax

```bash
parallax serve --model llama3.2:3b
```

### Step 5: Start All Services

Open 5 terminal windows:

**Terminal 1 - Backend Server:**

```bash
npm run server
# Runs on http://localhost:4000
```

**Terminal 2 - RAG Service:**

```bash
cd agents/rag
python rag_service.py --port 4001
# Runs on http://localhost:4001
```

**Terminal 3 - MCP Server:**

```bash
cd agents/mcp
python mcp_research_server.py
# Runs on http://localhost:3001
```

**Terminal 4 - Agent Service:**

```bash
cd agents
python agent_service.py
```

**Terminal 5 - Frontend:**

```bash
npm run dev
# Runs on http://localhost:5173
```

### Step 6: Access Application

Open browser: **http://localhost:5173**

**Default Credentials:**

- Email: `root@example.com`
- Password: `1234567890`

---

## Configuration Guide

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
PORT=4000
CLIENT_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Parallax Configuration
PARALLAX_HOST=http://127.0.0.1:11434
PARALLAX_MODEL=llama3.2:3b

# RAG Service
RAG_SERVICE_URL=http://localhost:4001
CHROMA_PERSIST_DIR=./chroma_db

# MCP Server
MCP_SERVER_URL=http://localhost:3001
```

---

## API Reference

### REST Endpoints

#### Messages

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| GET    | `/api/messages/:roomId` | Get messages for a room |
| POST   | `/api/messages`         | Send a new message      |
| PUT    | `/api/messages/:id`     | Update a message        |
| DELETE | `/api/messages/:id`     | Delete a message        |

#### Rooms

| Method | Endpoint         | Description       |
| ------ | ---------------- | ----------------- |
| GET    | `/api/rooms`     | Get all rooms     |
| POST   | `/api/rooms`     | Create a new room |
| DELETE | `/api/rooms/:id` | Delete a room     |

#### RAG

| Method | Endpoint                 | Description          |
| ------ | ------------------------ | -------------------- |
| POST   | `/api/rag/upload`        | Upload document      |
| POST   | `/api/rag/query`         | Query knowledge base |
| GET    | `/api/rag/documents`     | List documents       |
| DELETE | `/api/rag/documents/:id` | Delete document      |

### WebSocket Events

**Client to Server:**

```javascript
socket.emit("join_room", { roomId: "room-123" });
socket.emit("send_message", { roomId: "room-123", content: "Hello!" });
socket.emit("typing", { roomId: "room-123", isTyping: true });
```

**Server to Client:**

```javascript
socket.on("new_message", (message) => {
  /* handle */
});
socket.on("user_typing", ({ userId, isTyping }) => {
  /* handle */
});
socket.on("user_presence", ({ userId, status }) => {
  /* handle */
});
```

---

## Agent System

### Creating Custom Agents

```python
from base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CustomBot",
            personality="Helpful and friendly",
            capabilities=["task1", "task2"]
        )

    async def process_message(self, message, context):
        response = await self.generate_response(message, context)
        return response
```

---

## RAG Knowledge Base

### Uploading Documents

**Via API:**

```bash
curl -X POST http://localhost:4001/upload \
  -F "file=@document.pdf" \
  -F "collection=default"
```

**Via Chat:**

Simply ask questions - the RAG system automatically retrieves relevant context:

```
User: What are the company vacation policies?
AI: Based on the company handbook, employees receive...
    [Sources: company_policies.pdf, page 12]
```

---

## MCP Integration

### Available Tools

| Tool         | Description                     |
| ------------ | ------------------------------- |
| `web_search` | Search the web using DuckDuckGo |
| `fetch_url`  | Extract content from a URL      |
| `wikipedia`  | Search Wikipedia articles       |

---

## Security

### Data Privacy

- All data stored locally in `server/data.json`
- No external API calls for inference (uses Parallax)
- Vector embeddings stored in local ChromaDB
- No telemetry or analytics

### Best Practices

1. **Change default credentials** after first login
2. **Use HTTPS** in production
3. **Restrict network access** to trusted IPs
4. **Regular backups** of `data.json` and `chroma_db/`

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using the port (Windows)
netstat -ano | findstr :4000

# Kill the process
taskkill /F /PID <PID>
```

### CORS Errors

Add your frontend URL to `CLIENT_ORIGINS` in `server/server.js`:

```javascript
const CLIENT_ORIGINS = ["http://localhost:5173", "http://your-ip:5173"];
```

### ChromaDB Installation Issues

For Python 3.12+:

```bash
pip install chromadb --no-deps
pip install numpy pydantic tokenizers
```

### Parallax Connection Failed

1. Ensure Parallax is running: `parallax serve`
2. Check the port: default is 11434
3. Test: `curl http://localhost:11434/api/tags`

---

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and test: `npm test`
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Open a Pull Request

---

## License

MIT License - see [LICENSE](./LICENSE) for details.

---

## Acknowledgments

- [Parallax](https://github.com/GradientHQ/parallax) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Socket.IO](https://socket.io/) - Real-time communication
- [React](https://react.dev/) - UI framework

---

<p align="center">
  <strong>Built with privacy in mind</strong>
</p>

<p align="center">
  <a href="https://github.com/ayusingh-54/OmniMind---Comprehensive-Project-Documentation">Star this repo</a> |
  <a href="https://github.com/ayusingh-54/OmniMind---Comprehensive-Project-Documentation/issues">Report Bug</a> |
  <a href="https://github.com/ayusingh-54/OmniMind---Comprehensive-Project-Documentation/issues">Request Feature</a>
</p>
