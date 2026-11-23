# System Architecture & Technical Design
## CampusCopilot AI Platform

---

### 1. High-Level Architecture
CampusCopilot AI follows a modern, decoupled cloud architecture designed for high availability, low latency, and deterministic factual accuracy.

```mermaid
flowchart TD
    subgraph ClientLayer ["Client Layer (Web Application)"]
        UI["React 18 + Vite + Tailwind CSS + TypeScript"]
        Router["React Router v6"]
        State["Zustand Store + TanStack Query"]
        UI --> Router --> State
    end

    subgraph APILayer ["API & Gateway Layer"]
        Gateway["FastAPI Gateway (Uvicorn / ASGI)"]
        AuthMid["JWT Authentication & RBAC Middleware"]
        RateLimit["Rate Limiting & CORS"]
        Gateway --> AuthMid --> RateLimit
    end

    subgraph AgentLayer ["Multi-Agent Orchestration Layer (Google ADK / Gemini)"]
        Orchestrator["Orchestrator Agent"]
        IntentClassifier["Intent Classification Agent"]
        Guardrails["Safety & Guardrails Agent"]
        RetrievalAgent["Knowledge Retrieval Agent"]
        SpecializedAgents["Domain Agents (Academic, Placement, Fees)"]
        AnswerGen["Answer Generation Agent (Gemini 1.5 / 2.0)"]
        CriticAgent["Critic & Citation Verifier Agent"]

        Orchestrator --> Guardrails
        Orchestrator --> IntentClassifier
        IntentClassifier --> RetrievalAgent
        RetrievalAgent --> SpecializedAgents
        SpecializedAgents --> AnswerGen
        AnswerGen --> CriticAgent
        CriticAgent --> Orchestrator
    end

    subgraph DataLayer ["Data & Storage Layer"]
        PG["PostgreSQL (Relational Metadata & Audit Logs)"]
        VectorDB["Vector Store (pgvector / ChromaDB)"]
        RedisCache["Redis (Sessions, Cache, Rate Limits)"]
        DocStore["Object Storage (Documents & PDFs)"]
    end

    ClientLayer <-->|HTTPS / REST & SSE Stream| APILayer
    APILayer <--> AgentLayer
    AgentLayer <--> DataLayer
    APILayer <--> DataLayer
```

---

### 2. End-to-End Query Execution Flow
The diagram below details how a student's prompt is processed from input to streaming cited response:

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student
    participant FE as React Frontend
    participant API as FastAPI Backend
    participant Agent as Agent Orchestrator
    participant Guard as Guardrails Agent
    participant Vec as Vector Store (pgvector)
    participant LLM as Google Gemini API
    participant Critic as Critic Agent

    Student->>FE: Types "What is the minimum attendance required for exams?"
    FE->>API: POST /api/v1/chat/message (Bearer JWT)
    API->>Agent: Dispatch query context + user session
    Agent->>Guard: Validate prompt against injection / toxicity
    Guard-->>Agent: Passed
    Agent->>Agent: Intent Classifier identifies [ACADEMIC_REGULATIONS]
    Agent->>Vec: Query dense embeddings (Top-K=4, filter: university_id='GU')
    Vec-->>Agent: Return candidate chunks with page numbers and text
    alt Sufficient Context Found (Score >= 0.65)
        Agent->>LLM: Generate response conditioned strictly on retrieved chunks
        LLM-->>Agent: Draft answer with potential citations
        Agent->>Critic: Verify claims against retrieved chunk text
        Critic-->>Agent: Grounding verified (Score 0.98)
        Agent-->>API: Stream answer chunks + citation payload
        API-->>FE: SSE Stream tokens + citation badges
        FE-->>Student: Renders stream with interactive citation cards
    else Context Insufficient (Score < 0.65)
        Agent-->>API: Deliver deterministic abstention response
        API-->>FE: "I couldn't find verified information... Please contact registrar."
        FE-->>Student: Displays guided contact card
    end
```

---

### 3. Document Ingestion Pipeline Flow

```mermaid
flowchart LR
    Upload["Admin Upload (PDF/DOCX)"] --> Validation["File Type & Size Validation"]
    Validation --> Parser["Document Parser (PyMuPDF / docx)"]
    Parser --> Chunker["Semantic/Recursive Chunker (512-1024 tokens)"]
    Chunker --> Embedder["Embedding Generation (Gemini Embeddings)"]
    Embedder --> VectorStore["pgvector / ChromaDB"]
    Chunker --> MetaStore["PostgreSQL Document Metadata"]
    VectorStore & MetaStore --> Status["Index Status: READY"]
```
