# Software Requirements Specification (SRS)
## CampusCopilot AI Platform
**Document Identifier:** SRS-CCAI-2026-V1  
**Standard Reference:** IEEE Std 830-1998 / ISO/IEC/IEEE 29148:2018 Compliant

---

### 1. Introduction
#### 1.1 Purpose
This document specifies the software requirements for CampusCopilot AI, an AI-powered conversational university assistant that retrieves verified university information from authorized institutional documents.

#### 1.2 Scope
The system encompasses a React/TypeScript frontend, a FastAPI asynchronous backend, a Google Gemini and Google ADK-powered Multi-Agent RAG engine, vector persistence, and an administrative document control system.

#### 1.3 Definitions and Acronyms
- **RAG:** Retrieval-Augmented Generation
- **ADK:** Agent Development Kit
- **RBAC:** Role-Based Access Control
- **JWT:** JSON Web Token
- **Faithfulness:** Proportion of claims in generated output substantiated by retrieved context.

---

### 2. Functional Requirements

#### 2.1 Authentication & Authorization
- **FR-001:** The system shall allow students and staff to register and authenticate using email and password.
- **FR-002:** The system shall enforce role-based access control with predefined roles: `STUDENT`, `STAFF`, and `ADMIN`.
- **FR-003:** JWT access tokens shall expire after 60 minutes; refresh tokens shall be cryptographically rotated.

#### 2.2 Document Management & Ingestion Pipeline
- **FR-004:** The system shall allow authorized administrators to upload documents in PDF, DOCX, TXT, and CSV formats.
- **FR-005:** The ingestion pipeline shall extract text, identify page numbers, apply recursive character chunking (chunk size 512-1024 tokens with 10% overlap), and compute embeddings.
- **FR-006:** Ingested chunks shall persist metadata including `document_id`, `university_id`, `department`, `page_number`, `version`, and `effective_date`.
- **FR-007:** The system shall support document deletion and re-indexing, invalidating orphaned vector chunks immediately.

#### 2.3 Multi-Agent Conversational Intelligence
- **FR-008:** The Intent Classifier Agent shall categorize queries into: `ACADEMIC`, `EXAMINATION`, `FEES`, `ADMISSION`, `PLACEMENT`, `EVENT`, and `GENERAL`.
- **FR-009:** The Retrieval Agent shall perform semantic vector search and filter chunks by institutional metadata, returning top-$K$ chunks ($K=4$).
- **FR-010:** The Answer Generation Agent shall synthesize concise responses strictly conditioned on the retrieved document context.
- **FR-011:** The Critic Agent shall verify all factual assertions against the retrieved chunks before returning the answer to the client.
- **FR-012:** If the similarity score of retrieved chunks is below threshold $\tau < 0.65$ or information is absent, the system shall execute deterministic abstention.

#### 2.4 Citations & User Interface
- **FR-013:** Every factual response shall render clickable citation badges specifying Document Title, Page Number, and Section.
- **FR-014:** The chat interface shall support streaming responses via Server-Sent Events (SSE).
- **FR-015:** Users shall be able to submit binary feedback (thumbs up / thumbs down) with optional textual comments on each assistant response.

#### 2.5 Administration & Monitoring
- **FR-016:** Administrators shall have access to analytics tracking query volume, latency distribution, top searched queries, and user feedback rates.
- **FR-017:** Administrators shall be able to view and manage campus notices and upcoming academic calendar events.

---

### 3. Non-Functional Requirements

#### 3.1 Security & Data Integrity
- **NFR-001:** Passwords must be hashed using Argon2 or bcrypt with a minimum work factor of 12. Plaintext passwords shall never be logged or persisted.
- **NFR-002:** All endpoints must sanitize inputs against SQL injection, XSS, and prompt injection attacks.
- **NFR-003:** Administrative endpoints must enforce role checks (`HTTP 403 Forbidden` for non-admin accounts).
- **NFR-004:** API communications must be encrypted in transit via TLS 1.3.

#### 3.2 Performance & Scalability
- **NFR-005:** Average response latency for vector retrieval and initial stream generation must remain under $2.0$ seconds at 100 concurrent user sessions.
- **NFR-006:** The backend must be containerized and scale horizontally on Google Cloud Run or Kubernetes.

#### 3.3 Reliability & Availability
- **NFR-007:** The platform must maintain 99.9% uptime during academic operating hours.
- **NFR-008:** In the event of Gemini API timeouts or network partition, the system shall degrade gracefully and return an actionable retry notice.

---

### 4. Acceptance Criteria Matrix
| Requirement ID | Acceptance Criterion | Verification Method |
| :--- | :--- | :--- |
| **FR-001 / FR-003** | User receives valid JWT pair upon valid credentials; invalid credentials yield `HTTP 401`. | Automated Integration Test |
| **FR-005 / FR-006** | Uploaded 20-page PDF yields indexed vectors with verified `page_number` tags in database. | End-to-End Pipeline Test |
| **FR-012** | Querying an unmentioned topic (e.g., "rocket propulsion syllabus") yields standard abstention message. | AI Evaluation Test Suite |
| **FR-013** | Citations accurately match the page text containing the answer. | Critic Verification Eval |
