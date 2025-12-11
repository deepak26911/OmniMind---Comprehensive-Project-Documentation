# CLAUDE.md

This file provides project development guidelines for Claude Code (claude.ai/code).

## Project Overview

Active LLM Group Chat System - An intelligent group chat application built with React + TypeScript frontend and Express + lowdb backend. Supports multi-agent collaboration, RAG knowledge base retrieval, web search, and more. UI design inspired by Telegram/Discord.

## General Principles

- Prefer small, focused changes unless explicitly requested for large-scale refactoring
- Keep UX consistent with modern chat applications (including LLM Bots)
- Follow existing React + TypeScript patterns, avoid introducing unnecessary complex patterns
- Design features with LLM-friendliness in mind (clear APIs, structured JSON, stable contracts)

## Quick Start (Full Services)

Running the complete service requires 4 terminals:

```bash
# Terminal 1: Frontend Development Server
npm run dev

# Terminal 2: Backend API Server
npm run server

# Terminal 3: RAG Knowledge Base Service (optional but recommended)
cd agents
pip install -r requirements-rag.txt  # First run only
python rag_service.py --port 4001

# Terminal 4: Agent Service
cd agents
pip install -r requirements.txt  # First run only
python multi_agent_manager.py --email root@example.com --password 1234567890
```

**Startup Order**: Backend → RAG Service → Agent Service → Frontend

## Development Commands

### Frontend (React + Vite)

```bash
npm run dev          # Start dev server http://localhost:5173
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run test         # Run Vitest tests
```

### Backend (Express)

```bash
npm run server       # Start API server http://localhost:4000
```

### Agent Service (Python)

```bash
cd agents
pip install -r requirements.txt
python multi_agent_manager.py --email root@example.com --password 1234567890
```

### RAG Service (Python - ChromaDB)

```bash
cd agents
pip install -r requirements-rag.txt  # chromadb, flask, flask-cors
python rag_service.py --port 4001    # Start http://localhost:4001
python rag_service.py --test         # Run quick test
```

## Environment Variables

| Variable          | Default                 | Description                                 |
| ----------------- | ----------------------- | ------------------------------------------- |
| `VITE_API_URL`    | `http://localhost:4000` | Frontend API URL                            |
| `PORT`            | `4000`                  | Backend port                                |
| `CLIENT_ORIGIN`   | `http://localhost:5173` | CORS whitelist (comma-separated)            |
| `JWT_SECRET`      | -                       | JWT signing key (must change in production) |
| `DB_PATH`         | `server/data.json`      | Data storage path                           |
| `AGENT_API_TOKEN` | -                       | Agent API authentication token              |
| `RAG_SERVICE_URL` | `http://localhost:4001` | RAG service URL                             |

## Architecture & Key Patterns

### Frontend Architecture

- **State Management**: `ChatContext` (React Context + useReducer) for central management
- **Performance Optimization**: `TypingContext` manages input state separately to avoid re-renders
- **API Communication**: Unified through `src/api/client.ts`
- **Message Rendering**: react-virtuoso for virtualized scrolling
- **Real-time Updates**: Polling mechanism (messages ~4s, typing status ~2.5s)

### Backend Architecture

- **Tech Stack**: Express + lowdb (JSON storage)
- **Authentication**: JWT (httpOnly Cookie + Bearer token)
- **Data Storage**: `server/data.json`

### Agent Service

- **Core**: `agents/agent_service.py` - Polls messages, detects @mentions, calls LLM
- **Multi-Agent**: `agents/multi_agent_manager.py` - Manages multiple agents concurrently
- **Tool Library**: `agents/tools.py` - Context retrieval, web search, RAG queries
- **LLM Client**: `agents/query.py` - Supports OpenAI/Azure/Anthropic/custom endpoints

### RAG Service

- **Tech Stack**: Flask + ChromaDB
- **Features**: Document upload, vectorization, semantic retrieval
- **Storage**: `server/chroma_rag_db/`

## API Routes Overview

### Authentication

- `POST /auth/register`, `/auth/login`, `/auth/logout`, `GET /auth/me`

### Messages

- `GET /messages` - Get messages (supports since, limit, conversationId)
- `POST /messages` - Send message
- `DELETE /messages/:id` - Delete message (cascades to replies)
- `POST /messages/:id/reactions` - Emoji reactions

### Agent

- `GET /agents` - Get configurations
- `POST /agents/configs` - Create Agent
- `PATCH /agents/configs/:id` - Update Agent
- `POST /agents/:id/messages` - Agent sends message
- `POST /agents/:id/heartbeat` - Heartbeat
- `POST /agents/:id/tools/web-search` - Web search
- `POST /agents/:id/tools/local-rag` - Knowledge base query

### Knowledge Base

- `POST /knowledge-base/upload` - Upload document
- `GET /knowledge-base/documents` - List documents
- `DELETE /knowledge-base/documents/:id` - Delete document

## Key Type Definitions (src/types/chat.ts)

- `User`: Contains type (human/agent/system), agentId
- `Agent`: Contains capabilities, model, runtime, systemPrompt, tools
- `Message`: Contains role, conversationId, reactions, mentions, replyToId
- `ChatState`: Global state (currentUser, users, agents, messages, typingUsers)

## Frontend Development Guidelines

### UI Style

- **Animation**: Smooth but quick, avoid overly long or distracting transitions
- **Visual**: Minimalist style with high-quality details (subtle shadows, gradients, hover states)
- **Layout**: Keep it clean, focus on micro-interactions and spacing
- **Components**: Keep focused and reusable, extract cross-cutting logic into hooks

### File Structure

- Components: `src/components/`
- Hooks: `src/hooks/`
- Types: `src/types/`
- API: `src/api/`
- Constants: `src/constants/`
- Context: `src/context/`

## Backend Development Guidelines

- Design LLM-friendly features (clear APIs, structured JSON, stable contracts)
- Keep chat room logic LLM Bot-friendly (predictable message structures, tool metadata)
- Avoid breaking existing API contracts unless coordinated with frontend

## Important Implementation Notes

1. **Message Virtualization**: MessageList uses react-virtuoso for large message histories
2. **Markdown Support**: react-markdown renders message content
3. **Typing Indicator**: Polling + TTL cleanup mechanism
4. **Reply System**: References other messages via replyToId
5. **Emoji Reactions**: Aggregated reactions + user tracking
6. **Error Boundary**: ErrorBoundary component catches render errors
7. **Network Status**: Offline/online detection + banner notification
8. **Agent Tools**: Supports [GET_CONTEXT], [WEB_SEARCH], [LOCAL_RAG], [REACT], etc.

## Test Account (Development Only)

- Email: `root@example.com`
- Password: `1234567890`

## Data Reset

1. Stop all services
2. Delete `server/data.json`
3. Restart services (automatically rebuilds default data)

## Current Feature Status

### Completed

- User authentication (register/login/logout)
- Message sending/receiving, replies, emoji reactions
- Agent configuration management UI
- Multi-agent concurrent execution
- Agent heartbeat tracking
- Web search tool (DuckDuckGo)
- RAG knowledge base service (ChromaDB)
- Virtualized message rendering
- Error boundary and network status monitoring

### Future Directions

- WebSocket/SSE to replace polling
- LLM streaming responses
- Multi-channel/private messaging model
- Message edit history
