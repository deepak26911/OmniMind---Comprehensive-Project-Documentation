# Active LLM Group Chat System - Developer Documentation

This document focuses on architecture design, data contracts, and extension development guidelines as a supplementary reference to the README.

---

## 1. Project Structure & Dependencies

### Directory Structure

```
openai-groupchat/
├── src/                        # React + TypeScript + Vite Frontend
│   ├── api/
│   │   └── client.ts           # API client wrapper (HTTP+JSON communication layer)
│   ├── components/
│   │   ├── MessageBubble/      # Message components (MessageContent, ReactionList, etc.)
│   │   ├── AuthScreen.tsx      # Authentication page
│   │   ├── Layout.tsx          # Main layout framework
│   │   ├── Sidebar.tsx         # Sidebar (channels, member list)
│   │   ├── ChatSidebar.tsx     # Chat info sidebar (content, tasks, participants)
│   │   ├── MessageList.tsx     # Message list (virtualized)
│   │   ├── MessageInput.tsx    # Message input box
│   │   ├── MessageStatus.tsx   # Message status indicator
│   │   ├── DateSeparator.tsx   # Date separator
│   │   ├── AgentConfigPanel.tsx # Agent configuration panel
│   │   ├── AboutModal.tsx      # About modal
│   │   ├── EmojiPicker.tsx     # Emoji picker
│   │   └── ErrorBoundary.tsx   # Error boundary
│   ├── context/
│   │   ├── ChatContext.tsx     # Global chat state (useReducer)
│   │   ├── TypingContext.tsx   # Typing indicator state (performance optimization)
│   │   └── UsersLookupContext.tsx # User quick lookup
│   ├── hooks/
│   │   ├── useNetworkStatus.ts # Network status monitoring
│   │   ├── useDevicePerformance.ts # Device performance detection
│   │   └── useReducedMotion.ts # Reduced motion preference
│   ├── types/
│   │   └── chat.ts             # Shared TS type definitions
│   ├── i18n/                   # Internationalization (Chinese/English)
│   └── constants/
│       ├── animations.ts       # Framer Motion animation config
│       └── ui.ts               # UI constants
│
├── server/
│   ├── server.js               # Express API server (~1400 lines)
│   ├── data.json               # Persistent data (users/messages/agents)
│   └── chroma_rag_db/          # ChromaDB vector database directory
│
├── agents/
│   ├── base_agent.py           # Agent abstract base class
│   ├── agent_service.py        # Core Agent service (polling + response)
│   ├── multi_agent_manager.py  # Multi-Agent concurrent manager
│   ├── mcp_research_server.py  # MCP research assistant service (FastMCP)
│   ├── tools.py                # Tool library (context, search, RAG)
│   ├── query.py                # LLM client (dynamic configuration)
│   ├── rag_service.py          # RAG vector retrieval service (Flask + ChromaDB)
│   ├── core.py                 # Core configuration and utility classes
│   ├── requirements.txt        # Python base dependencies
│   └── requirements-rag.txt    # RAG service dependencies
│
└── Config Files
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    └── CLAUDE.md
```

### Main Dependencies

| Category | Dependencies |
|----------|--------------|
| Frontend Framework | React 18, TypeScript, Vite |
| UI Libraries | framer-motion, lucide-react, clsx |
| Utility Libraries | react-virtuoso, react-markdown, react-hot-toast, dayjs |
| Backend | Express, lowdb, bcryptjs, jsonwebtoken, cookie-parser, cors |
| Agent Service | Python requests, openai |
| RAG Service | chromadb, flask, flask-cors |

---

## 2. Data Models (`src/types/chat.ts`)

### User
```typescript
interface User {
  id: string;
  name: string;
  avatar: string;
  isLLM: boolean;
  status: 'online' | 'offline' | 'busy';
  type?: 'human' | 'agent' | 'system';
  agentId?: string;           // Associated Agent ID
  email?: string;
  createdAt?: number;
}
```

### Agent
```typescript
interface Agent {
  id: string;
  userId?: string;            // Associated User ID
  name: string;
  description?: string;
  avatar?: string;
  status?: 'active' | 'inactive';
  systemPrompt?: string;      // LLM system prompt
  capabilities?: AgentCapabilities;
  tools?: string[];           // Available tools list
  model?: AgentModelConfig;
  runtime?: AgentRuntimeConfig;
  createdAt?: number;
  updatedAt?: number;
}

interface AgentCapabilities {
  answer_active?: boolean;    // Proactively participate in conversations
  answer_passive?: boolean;   // Only respond to @mentions
  like?: boolean;             // Add emoji reactions
  summarize?: boolean;        // Generate summaries
}

interface AgentModelConfig {
  provider: string;           // openai, parallax, azure, etc.
  name: string;
  temperature?: number;       // 0-2
  maxTokens?: number;         // 64-16000
}

interface AgentRuntimeConfig {
  type: string;
  endpoint?: string;          // API endpoint
  apiKeyAlias?: string;       // API key alias
  proactiveCooldown?: number; // Proactive response cooldown (seconds)
}
```

### Message
```typescript
interface Message {
  id: string;
  content: string;
  senderId: string;
  timestamp: number;
  reactions: Reaction[];
  conversationId: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  replyToId?: string;         // ID of replied message
  mentions?: string[];        // @mentioned user/agent IDs
  metadata?: Record<string, unknown>;
  status?: MessageStatus;     // Message send status
  editHistory?: MessageEditMetadata[]; // Edit history
  editedAt?: number;          // Last edit time
}

interface Reaction {
  emoji: string;
  count: number;
  userIds: string[];
}

// Message status types
type MessageStatus =
  | { type: 'sending' }
  | { type: 'sent'; sentAt: number }
  | { type: 'delivered'; deliveredAt: number }
  | { type: 'read'; readAt: number }
  | { type: 'failed'; error: string };

interface MessageEditMetadata {
  content: string;
  editedAt: number;
}
```

### ChatState (Global State)
```typescript
interface ChatState {
  currentUser: User | null;
  users: User[];
  agents: Agent[];
  messages: Message[];
  typingUsers: string[];
  replyingTo?: Message;
  authStatus: 'loading' | 'authenticated' | 'unauthenticated';
}
```

---

## 3. Frontend Workflow

### Authentication & Initialization (`App.tsx`)
1. On mount, call `/auth/me`
2. On success, fetch `/users` + `/messages`, dispatch `HYDRATE`
3. On failure, enter `AuthScreen`

### Polling Mechanism
| Data | Interval | Description |
|------|----------|-------------|
| Messages | ~4 sec | `GET /messages` (since parameter for incremental), merge and dedupe |
| Typing Status | ~2.5 sec | `GET /typing`, update `typingUsers` |

### Message Sending (`MessageInput.tsx`)
1. Text box auto-grows, `Enter` to send, `Shift+Enter` for newline
2. Lightweight @mention suggestions (real-time calculation, not persisted)
3. `POST /messages` submit, dispatch `SEND_MESSAGE`
4. API response may include updated users → `SET_USERS`
5. Typing indicator: `POST /typing { isTyping: true/false }`

### Message Rendering (`MessageList` / `MessageBubble`)
- **Virtualized list** (`react-virtuoso`) efficiently handles large message volumes
- Grouped timestamps, reply preview, reaction aggregation, hover actions
- Markdown rendering support (`react-markdown`)

---

## 4. Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `AuthScreen.tsx` | Login/register form, calls `/auth/register` + `/auth/login` |
| `Layout.tsx` | Overall framework, mobile top bar sidebar toggle, offline banner |
| `Sidebar.tsx` | Channel placeholder, current user card, member list (online status + BOT badge) |
| `ChatSidebar.tsx` | Chat info sidebar (content tab, tasks tab, participants tab, AI summary generation) |
| `MessageList.tsx` | Virtualized scroll container, auto-scroll to latest, typing indicator row, date separators |
| `MessageBubble/` | Message component directory |
| ├─ `index.tsx` | Message main container |
| ├─ `MessageContent.tsx` | Markdown rendering |
| ├─ `ReactionList.tsx` | Reaction display |
| ├─ `ReactionPanel.tsx` | Reaction panel (quick selection) |
| ├─ `ActionButtons.tsx` | Hover actions (reply, react, delete) |
| ├─ `DeleteConfirmDialog.tsx` | Delete confirmation dialog |
| ├─ `ReplyContext.tsx` | Reply context |
| └─ `AgentSelector.tsx` | Agent selection dropdown |
| `MessageInput.tsx` | Multi-line editor, reply tag, attachment button, input dispatch |
| `SettingsModal.tsx` | LLM configuration settings (endpoint, model, API Key) |
| `SimulatedChat.tsx` | Simulated chat demo component |
| `MessageStatus.tsx` | Message send status indicator (sending, sent, delivered, read, failed) |
| `DateSeparator.tsx` | Date separator (Today, Yesterday, date format) |
| `AgentConfigPanel.tsx` | Agent configuration UI |
| `AboutModal.tsx` | About modal (project info, features) |
| `EmojiPicker.tsx` | Emoji picker |
| `ErrorBoundary.tsx` | Catches render errors, displays fallback UI |

### Context Responsibilities

| Context | Responsibility |
|---------|----------------|
| `ChatContext` | Global state management, Actions: `HYDRATE`, `SET_AUTH_STATUS`, `SET_USERS`, `SET_MESSAGES`, `SEND_MESSAGE`, `DELETE_MESSAGE`, `SET_REPLY`, `UPDATE_REACTIONS` |
| `TypingContext` | Typing indicator state (separate to avoid re-renders) |
| `UsersLookupContext` | User quick lookup (ID → User mapping) |

---

## 5. Backend Overview (`server/server.js`)

### Tech Stack
- Express + lowdb (JSONFile adapter)
- bcryptjs password hashing
- jsonwebtoken JWT
- cookie-parser + cors

### Storage
- Default `server/data.json`
- Ensures default Bot users exist on startup

### Sessions
- JWT stored as httpOnly Cookie
- Also supports Authorization Bearer

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `4000` | API port |
| `CLIENT_ORIGIN` | `http://localhost:5173` | CORS whitelist (comma-separated) |
| `JWT_SECRET` | - | JWT signing key |
| `DB_PATH` | `server/data.json` | Data storage path |
| `AGENT_API_TOKEN` | - | Agent API authentication token |
| `RAG_SERVICE_URL` | `http://localhost:4001` | RAG service URL |

### API Routes

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

#### Messages
- `GET /messages` - Get message list (supports `limit`, `before`, `since`, `conversationId`)
- `POST /messages` - Send message
- `POST /messages/summarize` - AI-generated conversation summary (SSE streaming response)
- `DELETE /messages/:id` - Delete message (cascades to replies)
- `POST /messages/:id/reactions` - Add/toggle emoji reaction

#### Users
- `GET /users` - Get all users

#### Agent Configuration
- `GET /agents` - Get all Agent configurations
- `GET /agents/configs` - Same as above (alias)
- `POST /agents/configs` - Create new Agent
- `PATCH /agents/configs/:agentId` - Update Agent
- `DELETE /agents/configs/:agentId` - Delete Agent

#### Agent Runtime API (Token Authentication)
- `POST /agents/:id/messages` - Agent sends message
- `POST /agents/:id/reactions` - Agent adds reaction
- `POST /agents/:id/heartbeat` - Agent heartbeat signal
- `POST /agents/:id/looking` - Agent "looking" status
- `GET /agents/looking` - Query active Agents
- `GET /agents/status` - Get all Agent status

#### Agent Context Tools
- `GET /agents/:id/context` - Get message surrounding context
- `GET /agents/:id/long-context` - Get full conversation history
- `GET /agents/:id/history` - Get recent history

#### Tool APIs
- `POST /agents/:id/tools/web-search` - DuckDuckGo search
- `POST /agents/:id/tools/local-rag` - Knowledge base query

#### Knowledge Base Management
- `POST /knowledge-base/upload` - Upload document
- `GET /knowledge-base/documents` - List documents
- `DELETE /knowledge-base/documents/:id` - Delete document

#### Typing Status
- `POST /typing` - Set typing status
- `GET /typing` - Query typing status

#### LLM Configuration
- `GET /llm/config` - Get LLM config (endpoint, model, has API Key)
- `POST /llm/config` - Save LLM config

---

## 6. Agent Service (`agents/`)

### Core Service (`agent_service.py`)

Python service bridging chat backend and LLM:

```bash
cd agents && pip install -r requirements.txt
python agent_service.py --email root@example.com --password 1234567890
```

#### Workflow
1. Login to chat backend (get JWT)
2. Start heartbeat thread (every 5 seconds)
3. Poll `/messages` (every 1 second)
4. Detect @mentions (via `mentions` field or `@AgentName`)
5. Build context: last 10 messages, format `<Name: User>: content`
6. Call LLM, clean `<think>` tags and special tokens
7. Send reply via `/agents/:agentId/messages`

#### Tool Support
| Tool | Format | Description |
|------|--------|-------------|
| Get Context | `[GET_CONTEXT:msg_id]` | Get message surrounding context |
| Full History | `[GET_LONG_CONTEXT]` | Get full conversation history |
| Web Search | `[WEB_SEARCH:query]` | DuckDuckGo search |
| Knowledge Base Query | `[LOCAL_RAG:query]` | Local vector retrieval |
| Emoji Reaction | `[REACT:emoji:msg_id]` | Add emoji reaction |

#### Message Format Handling
- Direction tags: `[TO: YOU]`, `[TO: @Other]`, `[TO: everyone]`
- Special tag cleanup: `<think>`, `<|channel|>`, etc.
- Keyword extraction

#### Configuration Parameters
| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE` | `http://localhost:4000` | Chat backend |
| `AGENT_TOKEN` | `dev-agent-token` | Must match `AGENT_API_TOKEN` env var |
| `AGENT_ID` | `helper-agent-1` | Agent config ID |
| `AGENT_USER_ID` | `llm1` | Agent user ID |
| `POLL_INTERVAL` | `1` | Message polling interval (seconds) |
| `HEARTBEAT_INTERVAL` | `5` | Heartbeat interval (seconds) |

### Multi-Agent Manager (`multi_agent_manager.py`)

Run multiple Agents concurrently:

```bash
python multi_agent_manager.py --email root@example.com --password 1234567890
```

#### Features
- Single login to get JWT
- Auto-fetch all Agent configs and sync
- Concurrent threads for each Agent
- Auto-skip inactive Agents
- Auto-restart on failure
- **Sequential tool calls**: Supports sequential execution for multi-round tool calls
- **Max rounds control**: Configurable maximum rounds for Agent responses

### Base Agent Class (`base_agent.py`)

Abstract base class for Agent service, providing common functionality:

- API client management
- Mention detection (@ detection)
- Heartbeat management
- Main loop structure
- Message processing framework
- Message cancellation support

Subclasses must implement:
- `generate_reply()`: LLM response generation
- `build_system_prompt()`: System prompt building
- `_init_llm()`: LLM client initialization

### MCP Research Service (`mcp_research_server.py`)

Model Context Protocol server based on FastMCP framework:

```bash
# Install dependencies
pip install fastmcp requests beautifulsoup4 feedparser

# stdio mode (for Claude Desktop)
python mcp_research_server.py

# SSE mode (HTTP access)
python mcp_research_server.py --transport sse --port 3001

# With API Key authentication
python mcp_research_server.py --transport sse --port 3001 --auth

# Generate API Keys
python mcp_research_server.py --generate-keys 3
```

#### Features
- Academic search (arXiv, PubMed, etc.)
- Web content fetching
- API Key management and authentication
- Supports both stdio and SSE transport modes

### Tool Library (`tools.py`)

`AgentTools` class provides:
- `get_context()` - Get message context
- `get_long_context()` - Get full history
- `compress_context()` - Compress conversation history
- `format_context_for_llm()` - LLM formatting
- `web_search()` - Web search
- `local_rag()` - Knowledge base query
- `parse_tool_calls()` - Parse tool calls
- `remove_tool_calls()` - Clean tool markers

### LLM Client (`query.py`)

Dynamic configuration, supports multiple providers:
- `openai` - OpenAI API
- `azure` - Azure OpenAI
- `anthropic` - Anthropic Claude
- `parallax` - Custom OpenAI-compatible endpoint
- `custom` - Custom endpoint

```python
from query import configure, chat_with_history

configure(provider="parallax", endpoint="http://localhost:8000/v1", model="gpt-4")
response = chat_with_history(messages, system_prompt="...")
```

---

## 7. RAG Service (`agents/rag_service.py`)

Vector retrieval service based on ChromaDB:

```bash
cd agents
pip install -r requirements-rag.txt
python rag_service.py              # Default port 4001
python rag_service.py --port 5000  # Custom port
python rag_service.py --test       # Run tests
```

### Flask API Endpoints
| Endpoint | Description |
|----------|-------------|
| `POST /rag/upload` | Upload document |
| `POST /rag/search` | Search query |
| `GET /rag/stats` | Knowledge base statistics |
| `POST /rag/delete` | Delete document |
| `POST /rag/clear` | Clear knowledge base |
| `GET /health` | Health check |

### ChromaDB Configuration
| Config | Value |
|--------|-------|
| Storage Location | `server/chroma_rag_db/` |
| Collection Name | `knowledge_base` |
| Embedding Model | `all-MiniLM-L6-v2` (automatic) |
| Similarity Metric | Cosine |
| Chunk Size | 500 characters |

### Workflow
1. User uploads document → `POST /knowledge-base/upload`
2. Backend forwards to RAG service
3. ChromaDB chunks + vectorizes
4. Agent queries → `[LOCAL_RAG:query]` → semantic search
5. Returns relevant passages

---

## 8. Development Scripts & Commands

```bash
# Node.js
npm install          # Install dependencies
npm run dev          # Start frontend dev server
npm run server       # Start backend API
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run test         # Run Vitest tests

# Python Agent
cd agents
pip install -r requirements.txt
python agent_service.py       # Single Agent
python multi_agent_manager.py # Multi-Agent

# Python RAG
pip install -r requirements-rag.txt
python rag_service.py
```

### Data Reset
1. Stop all services
2. Delete `server/data.json`
3. Restart services (automatically rebuilds default data)

---

## 9. Key Design Patterns

### State Management
- React Context + useReducer (ChatContext central management)
- Separate TypingContext to avoid unnecessary re-renders

### Performance Optimization
- Message virtualization (react-virtuoso)
- Message deduplication and merging
- Device performance detection (useDevicePerformance)

### Error Handling
- ErrorBoundary component
- Offline status monitoring (useNetworkStatus)

### Animation
- Framer Motion configuration management
- Reduced motion preference detection (useReducedMotion)

### Agent Tool Execution
- Multi-round tool calls: get context → call LLM again → final reply
- Supports standard format and native model formats
- **Sequential tool calls**: Execute in order when tools have dependencies
- **Max rounds limit**: Prevents infinite tool call loops

### Internationalization
- Supports Chinese/English interface switching
- Component-level localization support

### Agent Selection
- Dropdown menu to select online Agents
- Keyboard navigation support (arrow keys, Enter, Escape)
- Sorted by status (online first)

---

## 10. Extension Suggestions

### Near-term
- Replace polling with WebSocket/SSE for lower latency
- Implement LLM streaming responses (display as generated)
- ~~Add message edit history~~ (completed)

### Mid-term
- Add multi-channel/private messaging model (filter by `channelId`)
- ~~Add multiple Agents with different personalities/capabilities~~ (completed)
- File attachment upload

### Long-term
- Production hardening: HTTPS, secure SameSite Cookies, rate limiting, input validation
- Audit logs and monitoring
- Migrate to real database (PostgreSQL/MongoDB)

### Completed Features
- ✅ MCP (Model Context Protocol) integration
- ✅ Agent selection dropdown
- ✅ LLM configuration settings UI
- ✅ Chinese localization
- ✅ Sequential tool call support
- ✅ Max rounds configuration
- ✅ Agent auto-sync
