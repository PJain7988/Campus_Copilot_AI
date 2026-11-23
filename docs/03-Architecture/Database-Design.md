# Database Design & Entity Relationship Specifications
## CampusCopilot AI Platform

---

### 1. Architectural Strategy
CampusCopilot AI utilizes a PostgreSQL relational database with `pgvector` extension for dense embedding storage, maintaining strict referential integrity, tenant isolation, and auditability.

---

### 2. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    UNIVERSITIES ||--o{ DEPARTMENTS : contains
    UNIVERSITIES ||--o{ USERS : enrolls
    UNIVERSITIES ||--o{ DOCUMENTS : owns
    DEPARTMENTS ||--o{ DOCUMENTS : issues
    USERS ||--o{ CONVERSATIONS : initiates
    CONVERSATIONS ||--o{ MESSAGES : contains
    MESSAGES ||--o{ CITATIONS : references
    MESSAGES ||--o{ FEEDBACK : receives
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : splits_into
    DOCUMENT_CHUNKS ||--o{ CITATIONS : cites
    USERS ||--o{ AUDIT_LOGS : triggers

    UNIVERSITIES {
        uuid id PK
        varchar code UK "e.g., GU"
        varchar name "Geeta University"
        varchar domain
        jsonb settings
        timestamp created_at
    }

    USERS {
        uuid id PK
        uuid university_id FK
        varchar email UK
        varchar hashed_password
        varchar full_name
        varchar role "STUDENT | STAFF | ADMIN"
        boolean is_active
        timestamp created_at
    }

    DOCUMENTS {
        uuid id PK
        uuid university_id FK
        uuid department_id FK
        varchar title
        varchar file_path
        varchar file_type "PDF | DOCX | CSV"
        varchar category "ACADEMIC | EXAM | FEES | PLACEMENT"
        varchar version
        varchar index_status "PENDING | INDEXING | READY | FAILED"
        int total_pages
        timestamp published_at
        timestamp created_at
    }

    DOCUMENT_CHUNKS {
        uuid id PK
        uuid document_id FK
        int chunk_index
        int page_number
        text content
        vector_768 embedding "pgvector column"
        jsonb metadata_json
        timestamp created_at
    }

    CONVERSATIONS {
        uuid id PK
        uuid user_id FK
        varchar title
        timestamp created_at
        timestamp updated_at
    }

    MESSAGES {
        uuid id PK
        uuid conversation_id FK
        varchar sender "USER | ASSISTANT | SYSTEM"
        text content
        jsonb agent_routing_metadata
        int latency_ms
        timestamp created_at
    }

    CITATIONS {
        uuid id PK
        uuid message_id FK
        uuid chunk_id FK
        varchar document_title
        int page_number
        text snippet
    }

    FEEDBACK {
        uuid id PK
        uuid message_id FK
        uuid user_id FK
        int rating "1 for positive, -1 for negative"
        text comment
        timestamp created_at
    }

    AUDIT_LOGS {
        uuid id PK
        uuid user_id FK
        varchar action
        varchar resource_type
        varchar ip_address
        jsonb details
        timestamp created_at
    }
```

---

### 3. Key Schema Design Decisions
1. **Unified Storage (`pgvector`):** Collocating tabular metadata with vector embeddings inside PostgreSQL eliminates dual-write consistency issues and reduces infrastructure overhead.
2. **Deterministic Chunks & Page Numbers:** Chunks explicitly preserve `page_number` and `document_id` foreign keys to ensure citations link to actual physical pages in official PDFs.
3. **Auditability & Observability:** Every interaction records `latency_ms`, agent classification paths, and user feedback to compute real-time product metrics.
