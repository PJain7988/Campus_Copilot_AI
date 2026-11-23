# CampusCopilot AI
> **Production-Ready AI University Information Assistant**  
> Built for **Geeta University, Panipat** (Multi-tenant extensible architecture)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18_%2B_Vite-61DAFB?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini_%2B_ADK-8E75C2?logo=google)](https://ai.google.dev/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_pgvector-4169E1?logo=postgresql)](https://www.postgresql.org/)

---

### Overview
**CampusCopilot AI** is a production-grade, multi-agent conversational AI platform engineered to answer student queries regarding academic ordinances, examination schedules, fee structures, admissions, and placements with zero hallucinations and verified page-level document citations.

---

### Core Highlights
- 🧠 **Multi-Agent Orchestration:** Specialized agents (Orchestrator, Intent Classifier, Academic, Placement, Fees, Critic, Guardrails) built using Google Gemini and Google ADK design principles.
- 📄 **Rigorous RAG Pipeline:** PDF & document ingestion with chunking, pgvector semantic search, and top-$K$ relevance ranking.
- 🔍 **Verifiable Citations:** Exact document title, page number, and snippet previews for every factual statement.
- 🛡️ **Zero-Hallucination Policy:** Automated critic verification and deterministic abstention whenever facts are unavailable.
- 📊 **Administrative Control & Observability:** Ingestion monitoring, real-time query analytics, latency tracking, and feedback metrics.

---

### Project Structure
```text
CampusCopilot-AI/
├── docs/                      # Enterprise documentation & specifications
│   ├── 01-Product-Documentation/ (PRD, User Personas, etc.)
│   ├── 02-Requirements/          (SRS, Functional & Non-Functional Specs)
│   ├── 03-Architecture/          (System, High-Level, DB, Agent Design)
│   ├── 04-AI-Documentation/      (Multi-Agent, RAG, Guardrails, Prompts)
│   ├── 05-UI-UX/                 (Design System, Screen Inventory)
│   ├── 06-Development/           (Roadmap, Standards)
│   ├── 07-Testing/               (Strategy, AI Evaluation)
│   ├── 08-Deployment/            (Docker, Cloud Run, CI/CD)
│   └── 09-Project-Management/    (Risk Register, Milestones)
├── frontend/                  # React + TypeScript + Vite + Tailwind CSS
├── backend/                   # FastAPI + SQLAlchemy + pgvector + Gemini ADK
├── infrastructure/            # Docker, NGINX, deployment scripts
├── tests/                     # Deterministic & AI Evaluation test suites
├── docker-compose.yml         # Containerized local environment
└── README.md
```

---

### Documentation Links
- [Product Requirements Document (PRD)](file:///d:/Project/CharactAI/docs/01-Product-Documentation/PRD.md)
- [Software Requirements Specification (SRS)](file:///d:/Project/CharactAI/docs/02-Requirements/SRS.md)
- [High-Level System Architecture](file:///d:/Project/CharactAI/docs/03-Architecture/High-Level-Design.md)
- [Database & ERD Design](file:///d:/Project/CharactAI/docs/03-Architecture/Database-Design.md)
- [Multi-Agent Architecture & Guardrails](file:///d:/Project/CharactAI/docs/04-AI-Documentation/Multi-Agent-Architecture.md)
- [Screen Inventory & UI/UX](file:///d:/Project/CharactAI/docs/05-UI-UX/Screen-Inventory.md)
- [Testing & Evaluation Strategy](file:///d:/Project/CharactAI/docs/07-Testing/Test-Strategy.md)
- [Development Roadmap](file:///d:/Project/CharactAI/docs/06-Development/Development-Roadmap.md)
