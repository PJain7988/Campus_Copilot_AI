# Product Requirements Document (PRD)
## CampusCopilot AI: Production-Ready AI University Information Assistant

- **Document Version:** 1.0.0
- **Status:** Approved / Base Architecture
- **Target Institution:** Geeta University, Panipat (with multi-tenant extensibility)
- **Author:** Product Engineering & AI Architecture Team

---

### 1. Executive Summary
University students navigate hundreds of pages of disjointed PDFs, unstructured notices, examination ordinances, fee schedules, and placement notifications each semester. High administrative query volumes strain staff during admissions, examinations, and placements. **CampusCopilot AI** is a production-grade, enterprise-scale AI SaaS platform built to provide grounded, citation-backed answers to student inquiries using a Multi-Agent Retrieval-Augmented Generation (RAG) architecture powered by Google Gemini and Google ADK. Answers are strictly bounded by official university publications to eliminate hallucinations.

---

### 2. Product Vision
To empower university ecosystems with an autonomous, trusted conversational intelligence platform that eliminates information asymmetry for students while reducing administrative ticket overhead by >75%.

---

### 3. Problem Statement
1. **Scattered Information:** Regulations, circulars, and notifications are fragmented across university portals, physical boards, and multi-page PDFs.
2. **Administrative Backlog:** Repetitive questions regarding attendance cutoffs, backlogs, fee due dates, and registration procedures swamp registrar and department desks.
3. **Hallucination & Misinformation Risk:** Generic chatbots invent university deadlines and grading rules. A campus assistant must guarantee 100% verifiability with pinpoint document and page-level citations.

---

### 4. Proposed Solution
A specialized multi-agent application integrating:
- **Intelligent Intent Classifier & Router** categorizing queries across Academics, Examinations, Placements, Fees, and Admissions.
- **Strict RAG Pipeline** operating over verified university artifacts (PyMuPDF chunking, dense embeddings, vector database, and source re-ranking).
- **Critic & Safety Guardrails** enforcing ground truth validation and preventing prompt injection or unverified assertions.
- **Enterprise Web Interface** featuring student conversational workspace with inline citation previews, search, notifications, and an administrative control center.

---

### 5. Business Objectives
- Decrease support inquiries handled manually by administrative staff by 70% within 90 days of deployment.
- Attain >90% verified student query satisfaction (CSAT) across examination and admission windows.
- Deliver average end-to-end response latency under 1.8 seconds with streaming generation.

---

### 6. Target Audience & Stakeholders
1. **Undergraduate & Postgraduate Students:** Inquiring about attendance thresholds, examination timetables, fee installments, scholarships, and placement eligibility.
2. **Faculty & Academic Mentors:** Clarifying ordinance provisions, prerequisite criteria, and academic calendar dates.
3. **Administrative & Department Staff:** Ingestion of notices, management of ordinances, and supervision of query analytics.
4. **University Leadership & Deans:** Tracking institutional query trends, identifying operational friction, and auditing compliance.

---

### 7. User Personas
- **Persona 1: Riya Sharma (2nd Year B.Tech CSE Student, Geeta University)**
  - *Goal:* Determine minimum attendance percentage required to sit for end-semester exams and verify the medical leave waiver procedure.
  - *Pain Point:* Searching 60-page PDF academic regulations on a smartphone is tedious and confusing.
- **Persona 2: Kunal Verma (Final Year Student)**
  - *Goal:* Verify placement drive eligibility criteria and clearance requirements.
  - *Pain Point:* Placement cell circulars are posted on disparate notice boards with conflicting addenda.
- **Persona 3: Dr. Ramesh Kumar (Academic Registrar / Admin)**
  - *Goal:* Upload revised examination schedule or fee deadlines and verify that the AI immediately answers students accurately without manual notice distribution.
  - *Pain Point:* Inundated with repetitive student telephone calls and emails every exam season.

---

### 8. Product Scope
#### In-Scope:
- Multi-format document ingestion (PDF, DOCX, TXT, CSV) with OCR support.
- Multi-agent orchestration (Orchestrator, Intent Classifier, Retrieval, Academic, Placement, Student Services, Critic, Guardrails).
- Citation generation citing verified source document, version, and page number.
- Natural abstention when data is missing: *"I couldn't find verified information about this in the available university documents. Please contact the relevant university department."*
- Full RBAC (Student, Department Coordinator, Super Admin).
- Real-time analytics (latency, query categories, retrieval hit rate, token costs).

#### Out-of-Scope:
- Direct financial transactions for tuition payment inside chat (redirection to official payment gateway provided).
- Tampering with student academic records or official grade generation.
- Unauthenticated public scraping of non-verified 3rd-party blogs.

---

### 9. Feature Prioritization (MoSCoW)
- **Must Have (MVP):**
  - Secure JWT authentication & RBAC.
  - RAG ingestion pipeline (PDF/DOCX) with pgvector/ChromaDB.
  - Streaming conversational UI with conversation memory.
  - Precise page-level citation cards.
  - Deterministic abstention guardrail.
  - Admin document upload and ingestion status panel.
- **Should Have (Release 2):**
  - Full Google ADK multi-agent routing.
  - Event and notification calendar with notice board feeds.
  - Document version comparison and deprecation management.
  - Detailed analytics dashboard (latency, DAU, feedback breakdown).
- **Could Have (Release 3):**
  - Multi-university tenant isolation.
  - Proactive deadline WhatsApp/Email alert integrations.
  - Audio/Voice query interface.
- **Won't Have (Immediate Scope):**
  - Automated grading of student assignments.

---

### 10. Success Metrics (KPIs)
| Metric | Target | Measurement Method |
| :--- | :--- | :--- |
| **Groundedness / Faithfulness** | $\ge 98\%$ | Evaluated via synthetic test suite & Critic Agent |
| **Hallucination Rate** | $< 1\%$ | Automated citation verification against source text |
| **Abstention Accuracy** | $\ge 99\%$ | Test cases with unanswerable questions |
| **Response Latency (p95)** | $< 2.0\text{ s}$ | Backend APM & Query logs |
| **User Satisfaction** | $\ge 92\%$ | Explicit thumbs up/down user feedback |
