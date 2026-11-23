# Risk Register & Mitigation Strategy
## CampusCopilot AI Platform

---

| Risk ID | Category | Description | Likelihood | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-001** | AI Quality | LLM hallucinates an exam date or fee cutoff, leading to student distress. | Medium | Critical | Zero-shot Critic Agent verification against retrieved chunks; deterministic abstention if similarity $< 0.65$. |
| **RSK-002** | Security | Malicious student attempts prompt injection to reveal system prompts or tamper with chat. | Medium | High | Multi-stage Guardrails Agent sanitizing prompts; strict system prompt isolation; no administrative functions accessible via conversational queries. |
| **RSK-003** | Data Freshness | Outdated document version is cited after a regulation amendment. | Medium | High | Version control tags on documents; superseding notifications automatically flag older document versions as archived. |
| **RSK-004** | Performance | Heavy traffic spike during university results announcement causes API throttling. | High | Medium | Redis response caching for high-frequency queries; horizontal scaling on containerized runners; streaming SSE for perceptual speed. |
| **RSK-005** | Document Quality | Scanned PDF notices with poor quality yield corrupted OCR text. | Low | Medium | OCR fallback with preprocessing (contrast normalization) via Tesseract / PyMuPDF text filters. |
