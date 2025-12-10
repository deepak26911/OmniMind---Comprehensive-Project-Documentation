# OmniMind - Comprehensive Project Documentation

<p align="center">
  <img src="./assets/gradient_flow_logo_1764409055594.png" alt="OmniMind Logo" width="200">
</p>

<p align="center">
  <strong>🏆 Privacy-First AI-Native Local Workspace Platform</strong>
</p>

<p align="center">
  <a href="https://github.com/zengyuzhi/omnimind"><img src="https://img.shields.io/badge/GitHub-Repository-blue?logo=github" alt="GitHub"></a>
  <a href="https://github.com/GradientHQ/parallax"><img src="https://img.shields.io/badge/Powered%20by-Parallax-green" alt="Parallax"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"></a>
</p>

---

## 📋 Table of Contents

1. [What is OmniMind?](#-what-is-omnimind)
2. [The Problem We Solve](#-the-problem-we-solve)
3. [Key Features](#-key-features)
4. [System Architecture](#-system-architecture)
5. [Technology Stack](#-technology-stack)
6. [Project Structure](#-project-structure)
7. [Installation & Setup](#-installation--setup)
8. [Configuration Guide](#-configuration-guide)
9. [API Reference](#-api-reference)
10. [Agent System](#-agent-system)
11. [RAG Knowledge Base](#-rag-knowledge-base)
12. [MCP Integration](#-mcp-integration)
13. [Security](#-security)
14. [Troubleshooting](#-troubleshooting)

---

## 🎯 What is OmniMind?

**OmniMind** is a **privacy-first, AI-native local workspace platform** designed to empower teams and individuals with secure, intelligent collaboration. Unlike cloud-based AI solutions that send your data to third-party servers, OmniMind runs entirely on **YOUR infrastructure** using local LLM inference powered by [Parallax](https://github.com/GradientHQ/parallax).

### Core Philosophy

- **🔒 Privacy First**: All data stays on your hardware - chat history, documents, and vector embeddings never leave your infrastructure
- **💰 Zero Token Costs**: After initial setup, there are no pay-per-token fees - you own the compute
- **⚡ Low Latency**: Local inference ensures millisecond-level responses
- **🎛️ Full Control**: You own the models, the data, and the entire infrastructure

---

## 🔥 The Problem We Solve

### Current Pain Points with Cloud AI Solutions

| Problem                 | Cloud AI Reality                                                               | OmniMind Solution                                      |
| ----------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| **Data Privacy**        | Sensitive conversations, documents, and business data sent to external servers | All data processed and stored locally on YOUR hardware |
| **Cost Explosion**      | Pay-per-token pricing accumulates rapidly for teams                            | Zero inference costs after hardware setup              |
| **Latency Issues**      | Network round-trips add 200-500ms+ delay                                       | Local inference = instant responses                    |
| **Vendor Lock-in**      | Dependent on provider's API availability and pricing changes                   | Complete ownership of models and infrastructure        |
| **Context Isolation**   | Each conversation starts fresh, no memory across sessions                      | Persistent context with RAG knowledge base             |
| **Passive Interaction** | Traditional bots only respond when asked                                       | Agents proactively participate in discussions          |

### Who Is This For?

- **Enterprise Teams** needing secure internal AI assistants without data leakage
- **Research Organizations** handling sensitive/proprietary information
- **Startups** wanting AI capabilities without recurring API costs
- **Developers** building AI-powered applications with full control
- **Privacy-Conscious Users** who refuse to share data with cloud providers

---

## ✨ Key Features

### 🤖 Multi-Agent System

OmniMind supports multiple AI agents running simultaneously, each with distinct personalities, capabilities, and tools:

```
@AI-Assistant  → General Q&A, code help, document analysis
@Writer        → Content creation, editing, summarization
@Researcher    → Web search, academic paper retrieval, fact-checking
```

**Agent Capabilities:**

- **Passive Response**: Reply when @mentioned
- **Proactive Response**: Actively participate without being mentioned
- **Emoji Reactions**: React to messages with contextual emojis
- **Summarization**: Generate conversation summaries on demand

### 📚 RAG Knowledge Base (Retrieval-Augmented Generation)

Upload your documents and the AI gains access to your private knowledge:

- **Supported Formats**: PDF, DOCX, PPTX, TXT, Markdown
- **Semantic Search**: ChromaDB vector database with cosine similarity
- **Auto-Chunking**: Intelligent document splitting with overlap for context preservation
- **Deduplication**: Hash-based document tracking to prevent duplicates

### 🔍 Built-in Tools

| Tool               | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `GET_CONTEXT`      | Retrieve messages around a specific point in conversation |
| `GET_LONG_CONTEXT` | Get full conversation history for deep understanding      |
| `WEB_SEARCH`       | Real-time web search for current information              |
| `LOCAL_RAG`        | Search your uploaded knowledge base                       |
| `MCP Tools`        | Extensible Model Context Protocol integration             |

### 💬 Modern Chat Experience

- **Smart Context Management**: Fine-tuned context engineering for @mentions, reply threads, and conversation history
- **Rich Text Support**: Markdown rendering with code syntax highlighting
- **Interactive Features**: Emoji reactions, quote replies, typing indicators
- **Real-time Sync**: Live message updates across all connected clients
- **File Attachments**: Upload and share documents directly in chat

### 🔌 MCP (Model Context Protocol) Integration

Extend agent capabilities with external tools via MCP servers:

```python
# Example: Research MCP Server provides:
- arxiv_search      # Search academic papers
- semantic_scholar  # Find research by topic
- paper_details     # Get paper metadata
- summarize_paper   # Generate paper summaries
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER / BROWSER                               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     REACT FRONTEND (Vite + TypeScript)              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │  ChatContext │ │ MessageList │ │ MessageInput│ │ AgentConfig │   │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     EXPRESS BACKEND (Node.js)                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │  Auth/JWT   │ │  Messages   │ │   Agents    │ │  LLM Config │   │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
│                          │                                           │
│                          ▼                                           │
│                   ┌─────────────┐                                    │
│                   │  LowDB JSON │                                    │
│                   └─────────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌───────────────────────┐ ┌───────────────┐ ┌───────────────────────┐
│   AGENT SERVICE       │ │  RAG SERVICE  │ │    MCP SERVICE        │
│   (Python)            │ │  (Python)     │ │    (Python)           │
│ ┌───────────────────┐ │ │ ┌───────────┐ │ │ ┌───────────────────┐ │
│ │ Multi-Agent Mgr   │ │ │ │ ChromaDB  │ │ │ │ Research Tools    │ │
│ │ Tool Executor     │ │ │ │ Embeddings│ │ │ │ Web Search        │ │
│ │ Harmony Parser    │ │ │ │ Doc Parser│ │ │ │ Paper Retrieval   │ │
│ └───────────────────┘ │ │ └───────────┘ │ │ └───────────────────┘ │
└───────────────────────┘ └───────────────┘ └───────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PARALLAX LOCAL LLM INFERENCE                      │
│              (Llama 3 / Mistral / Qwen / GPT-OSS 20B)               │
└─────────────────────────────────────────────────────────────────────┘
```

### Service Communication Flow

1. **User sends message** → Frontend → Backend API
2. **Backend stores message** → Notifies Agent Service
3. **Agent detects @mention** → Fetches context → Queries RAG if needed
4. **Agent calls LLM** → Local Parallax inference
5. **LLM may use tools** → Web search, RAG lookup, MCP tools
6. **Agent posts response** → Backend → Frontend updates

---

## 🛠️ Technology Stack

### Frontend

| Technology         | Purpose                                  |
| ------------------ | ---------------------------------------- |
| **React 18**       | UI framework with hooks and context      |
| **TypeScript**     | Type safety and better DX                |
| **Vite**           | Fast dev server and build tool           |
| **Framer Motion**  | Smooth animations                        |
| **React Virtuoso** | Virtualized message list for performance |
| **Lucide React**   | Icon library                             |

### Backend

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| **Express.js** | REST API server               |
| **LowDB**      | JSON file-based database      |
| **JWT**        | Authentication tokens         |
| **bcrypt**     | Password hashing              |
| **Multer**     | File upload handling          |
| **CORS**       | Cross-origin resource sharing |

### AI/ML Services

| Technology     | Purpose                                      |
| -------------- | -------------------------------------------- |
| **OpenAI SDK** | LLM client (compatible with local endpoints) |
| **ChromaDB**   | Vector database for RAG                      |
| **FastMCP**    | Model Context Protocol server                |
| **Parallax**   | Local LLM inference engine                   |

### Python Services

| Technology                        | Purpose                   |
| --------------------------------- | ------------------------- |
| **Flask**                         | RAG service HTTP API      |
| **Requests**                      | HTTP client for API calls |
| **PyPDF/python-docx/python-pptx** | Document parsing          |

---

## 📁 Project Structure

```
OmniMind/
├── 📁 src/                          # Frontend React application
│   ├── 📁 api/
│   │   └── client.ts                # API client for backend communication
│   ├── 📁 components/
│   │   ├── AgentConfigPanel.tsx     # Agent creation/editing UI
│   │   ├── AuthScreen.tsx           # Login/Register forms
│   │   ├── ChatSidebar.tsx          # Conversation list
│   │   ├── EmojiPicker.tsx          # Emoji selection widget
│   │   ├── Layout.tsx               # Main app layout
│   │   ├── MessageBubble/           # Message display components
│   │   ├── MessageInput.tsx         # Chat input with mentions
│   │   ├── MessageList.tsx          # Virtualized message list
│   │   ├── SettingsModal.tsx        # LLM configuration
│   │   └── Sidebar.tsx              # Navigation sidebar
│   ├── 📁 context/
│   │   ├── ChatContext.tsx          # Global chat state management
│   │   ├── TypingContext.tsx        # Typing indicators
│   │   └── UsersLookupContext.tsx   # User data cache
│   ├── 📁 hooks/
│   │   ├── useDevicePerformance.ts  # Performance detection
│   │   ├── useNetworkStatus.ts      # Online/offline detection
│   │   └── useReducedMotion.ts      # Accessibility
│   ├── 📁 types/
│   │   └── chat.ts                  # TypeScript type definitions
│   ├── App.tsx                      # Main application component
│   └── main.tsx                     # Application entry point
│
├── 📁 server/
│   ├── server.js                    # Express backend (3000+ lines)
│   └── data.json                    # LowDB database file
│
├── 📁 agents/                       # Python AI services
│   ├── agent_runner.py              # Entry point for agent service
│   ├── agent_service.py             # Main agent logic (~1000 lines)
│   ├── base_agent.py                # Base agent class
│   ├── multi_agent_manager.py       # Concurrent agent management
│   ├── 📁 core/
│   │   ├── config.py                # Environment configuration
│   │   ├── llm_client.py            # OpenAI-compatible LLM client
│   │   ├── tool_executor.py         # Built-in tool implementations
│   │   ├── tool_formatters.py       # Tool prompt formatting
│   │   ├── harmony_parser.py        # GPT-OSS response parsing
│   │   └── response_cleaner.py      # Output sanitization
│   ├── 📁 rag/
│   │   ├── rag_service.py           # RAG API server (~550 lines)
│   │   ├── document_parser.py       # PDF/DOCX/PPTX parsing
│   │   └── requirements.txt         # RAG dependencies
│   └── 📁 mcp/
│       ├── mcp_research_server.py   # Research tools MCP server
│       └── requirements.txt         # MCP dependencies
│
├── 📁 public/                       # Static assets
├── 📁 assets/                       # Images and media
├── package.json                     # Node.js dependencies
├── vite.config.ts                   # Vite configuration
├── tsconfig.json                    # TypeScript configuration
└── README.md                        # Main documentation
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Node.js 18+** - JavaScript runtime
- **Python 3.10-3.12** - For AI services (3.14 has compatibility issues)
- **Parallax** - Local LLM inference engine ([Installation Guide](https://github.com/GradientHQ/parallax))
- **GPU (Recommended)** - NVIDIA GPU with 8GB+ VRAM for local LLM

### Step 1: Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/zengyuzhi/omnimind.git
cd omnimind

# Install Node.js dependencies
npm install

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Install Python dependencies for all services
pip install -r agents/requirements.txt
pip install -r agents/rag/requirements.txt
pip install -r agents/mcp/requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the project root:

```env
# Server Configuration
PORT=4000
JWT_SECRET=your-secure-secret-key-change-this

# Client Origins (for CORS)
CLIENT_ORIGIN=http://localhost:5173,http://localhost:5174

# Agent Configuration
AGENT_API_TOKEN=dev-agent-token

# LLM Configuration (Parallax endpoint)
LLM_ENDPOINT=http://localhost:8080/v1
LLM_API_KEY=not-needed
LLM_MODEL=gpt-oss-20b

# RAG Service
RAG_SERVICE_URL=http://localhost:4001
CHROMA_DB_PATH=./server/chroma_rag_db
```

### Step 3: Start All Services

You need to start **5 services** in separate terminals:

**Terminal 1 - Backend API Server:**

```bash
npm run server
# Runs on http://localhost:4000
```

**Terminal 2 - RAG Knowledge Base:**

```bash
cd agents/rag
python rag_service.py --port 4001
# Runs on http://localhost:4001
```

**Terminal 3 - MCP Research Service (Optional):**

```bash
cd agents/mcp
python mcp_research_server.py --transport sse --port 3001
# Runs on http://localhost:3001
```

**Terminal 4 - Agent Service:**

```bash
cd agents
python agent_runner.py
# Connects to backend on port 4000
```

**Terminal 5 - Frontend Dev Server:**

```bash
npm run dev
# Runs on http://localhost:5173
```

### Step 4: Access the Application

Open your browser and navigate to: **http://localhost:5173**

Login with default credentials:

- **Email**: `root@example.com`
- **Password**: `1234567890`

---

## ⚙️ Configuration Guide

### LLM Configuration (Settings → AI Settings)

Configure your LLM endpoint through the UI:

| Setting      | Description               | Example                      |
| ------------ | ------------------------- | ---------------------------- |
| **Endpoint** | OpenAI-compatible API URL | `http://localhost:8080/v1`   |
| **Model**    | Model identifier          | `gpt-oss-20b`, `llama-3-70b` |
| **API Key**  | Authentication key        | `not-needed` for local       |

### Agent Configuration

Create and configure agents through the Agent Config Panel:

```typescript
interface AgentConfig {
  name: string; // Display name
  description: string; // Agent purpose
  avatar: string; // Avatar URL
  status: "active" | "inactive";

  // Behavior settings
  capabilities: {
    answer_passive: boolean; // Reply when @mentioned
    answer_active: boolean; // Proactive participation
    like: boolean; // Emoji reactions
    summarize: boolean; // Summarization ability
  };

  // Model settings
  model: {
    provider: string; // 'openai', 'parallax', etc.
    name: string; // Model name
    temperature: number; // 0.0 - 2.0
    maxTokens: number; // Max response length
  };

  // Tool configuration
  tools: string[]; // Enabled tools
  mcp?: {
    url: string; // MCP server URL
    enabledTools: string[];
  };
}
```

### RAG Knowledge Base Configuration

Upload documents through the UI or API:

```bash
# Upload via API
curl -X POST http://localhost:4001/rag/upload-file \
  -F "file=@document.pdf"

# Search knowledge base
curl -X POST http://localhost:4001/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "topK": 5}'
```

---

## 📡 API Reference

### Authentication Endpoints

| Method | Endpoint         | Description        |
| ------ | ---------------- | ------------------ |
| POST   | `/auth/register` | Create new account |
| POST   | `/auth/login`    | Login and get JWT  |
| POST   | `/auth/logout`   | Clear session      |
| GET    | `/auth/me`       | Get current user   |

### Message Endpoints

| Method | Endpoint                  | Description               |
| ------ | ------------------------- | ------------------------- |
| GET    | `/messages`               | List messages (paginated) |
| POST   | `/messages`               | Create new message        |
| DELETE | `/messages/:id`           | Delete message            |
| POST   | `/messages/:id/reactions` | Add emoji reaction        |

### Agent Endpoints

| Method | Endpoint      | Description       |
| ------ | ------------- | ----------------- |
| GET    | `/agents`     | List all agents   |
| POST   | `/agents`     | Create new agent  |
| GET    | `/agents/:id` | Get agent details |
| PUT    | `/agents/:id` | Update agent      |
| DELETE | `/agents/:id` | Delete agent      |

### RAG Endpoints

| Method | Endpoint           | Description                   |
| ------ | ------------------ | ----------------------------- |
| POST   | `/rag/upload`      | Upload text content           |
| POST   | `/rag/upload-file` | Upload file (PDF, DOCX, etc.) |
| POST   | `/rag/search`      | Semantic search               |
| GET    | `/rag/files`       | List uploaded documents       |
| POST   | `/rag/delete`      | Delete document               |
| GET    | `/rag/stats`       | Get knowledge base stats      |

---

## 🤖 Agent System

### How Agents Work

1. **Polling**: Agent service polls backend for new messages every 1-2 seconds
2. **Detection**: Checks for @mentions or proactive triggers
3. **Context Building**: Fetches relevant conversation history
4. **RAG Integration**: Searches knowledge base if `LOCAL_RAG` tool enabled
5. **LLM Call**: Sends context to local LLM via Parallax
6. **Tool Execution**: Executes any tool calls in response
7. **Response Posting**: Sends final response back to chat

### Multi-Agent Manager

```python
manager = MultiAgentManager(
    api_base="http://localhost:4000",
    agent_token="dev-agent-token",
    auto_sync=True  # Hot-reload agent configs
)

manager.login("root@example.com", "password")
manager.start_all_agents()  # Start all active agents

# Agents run in separate threads
# Hot-reload: New agents auto-start, deactivated agents auto-stop
```

### Harmony Format (GPT-OSS)

For GPT-OSS models, OmniMind uses a special "Harmony" format for function calling:

```
<|channel|>commentary to=WEB_SEARCH
<|message|>{"query": "latest AI news"}
```

The `harmony_parser.py` handles parsing and building these special formatted messages.

---

## 📚 RAG Knowledge Base

### Architecture

```
Document Upload → Text Extraction → Chunking → Embedding → ChromaDB
                         ↓
                  Query → Embedding → Vector Search → Top-K Results
```

### Chunking Strategy

- **Chunk Size**: 500 characters (configurable)
- **Overlap**: 50 characters to preserve context
- **Boundary Respect**: Tries to split on paragraphs, then sentences

### Supported Formats

| Format     | Extension | Parser      |
| ---------- | --------- | ----------- |
| PDF        | `.pdf`    | PyPDF       |
| Word       | `.docx`   | python-docx |
| PowerPoint | `.pptx`   | python-pptx |
| Plain Text | `.txt`    | Native      |
| Markdown   | `.md`     | Native      |

### Usage in Chat

When an agent has `tools.local_rag` enabled, users can ask questions about uploaded documents:

```
User: @AI-Assistant What does our company policy say about remote work?

AI-Assistant: Based on the company handbook, remote work is allowed
up to 3 days per week with manager approval. [Source: company_handbook.pdf]
```

---

## 🔌 MCP Integration

### What is MCP?

Model Context Protocol (MCP) is a standard for extending LLM capabilities with external tools. OmniMind includes a research-focused MCP server.

### Available MCP Tools

| Tool                      | Description             |
| ------------------------- | ----------------------- |
| `arxiv_search`            | Search arXiv papers     |
| `semantic_scholar_search` | Search Semantic Scholar |
| `get_paper_details`       | Get paper metadata      |
| `summarize_paper`         | Generate paper summary  |
| `get_citations`           | Get paper citations     |

### Connecting MCP Server

1. Start the MCP server:

   ```bash
   python mcp_research_server.py --transport sse --port 3001
   ```

2. In Agent Config Panel, add MCP connection:
   - URL: `http://localhost:3001`
   - Select which tools to enable

---

## 🔐 Security

### Authentication

- **JWT Tokens**: 7-day expiry, httpOnly cookies
- **Password Hashing**: bcrypt with salt rounds
- **Session Management**: Secure cookie handling

### CORS Configuration

```javascript
// Allowed origins (configurable via CLIENT_ORIGIN env var)
const CLIENT_ORIGINS = [
  "http://localhost:5173",
  "http://localhost:5174",
  "http://172.20.48.82:5173", // Local network
];
```

### Agent API Security

- **Agent Token**: Required for agent-to-backend communication
- **Separate Authentication**: Agents use X-Agent-Token header

### Data Privacy

- **Local Storage**: All data stored in local JSON/ChromaDB files
- **No Telemetry**: ChromaDB telemetry disabled
- **No External Calls**: LLM inference runs locally via Parallax

---

## 🐛 Troubleshooting

### Common Issues

#### 1. CORS Error: "Access-Control-Allow-Origin"

**Solution**: Add your IP to `CLIENT_ORIGIN` in `.env` or `server.js`:

```javascript
CLIENT_ORIGIN=http://localhost:5173,http://YOUR_IP:5173
```

#### 2. "ModuleNotFoundError: No module named 'flask'"

**Solution**: Install dependencies in your virtual environment:

```bash
.\.venv\Scripts\Activate.ps1
pip install -r agents/rag/requirements.txt
```

#### 3. Port Already in Use (EADDRINUSE)

**Solution**: Kill the process using the port:

```bash
# Windows
netstat -ano | findstr :4000
taskkill /F /PID <PID>

# Linux/Mac
lsof -i :4000
kill -9 <PID>
```

#### 4. ChromaDB Build Errors on Python 3.14

**Solution**: Use Python 3.10-3.12 instead:

```bash
py -3.12 -m venv .venv
```

#### 5. Agent Not Responding

**Checklist**:

1. Is agent service running? (`python agent_runner.py`)
2. Is agent status "active" in config?
3. Is LLM endpoint configured correctly?
4. Check agent service logs for errors

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow existing code style
4. Test your changes
5. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

- **[Parallax](https://github.com/GradientHQ/parallax)** - Local LLM inference engine
- **[ChromaDB](https://www.trychroma.com/)** - Vector database for RAG
- **[FastMCP](https://github.com/jlowin/fastmcp)** - Model Context Protocol framework
- **Gradient Network Community** - For the hackathon opportunity

---

<p align="center">
  <strong>Built with ❤️ for the Gradient Network Community</strong>
</p>

<p align="center">
  <code>#BuildYourOwnAILab #Parallax #GradientNetwork #PrivacyFirst</code>
</p>
#   O m n i M i n d - - - C o m p r e h e n s i v e - P r o j e c t - D o c u m e n t a t i o n  
 