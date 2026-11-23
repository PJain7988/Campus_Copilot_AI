# UI/UX Screen Inventory & Design Specifications
## CampusCopilot AI Platform

---

### 1. Design System Foundation
- **Visual Identity:** Clean, calm academic aesthetic with deep navy slate primary tones (`#0F172A`), indigo accent (`#4F46E5`), emerald confirmation (`#10B981`), and high-contrast accessible typography (Inter / SF Pro).
- **Themes:** Light & Dark theme responsive styling with Tailwind CSS.
- **Card Styling:** Elevated cards with subtle borders (`border-slate-200 dark:border-slate-800`), rounded-xl geometry, and zero jarring visual clutter.

---

### 2. Complete Screen Inventory

#### A. Public Portals
1. **Landing Page (`/`):** Hero section with interactive query demonstration, institutional value proposition, features overview, security disclosures, and login CTA.
2. **Login Page (`/login`):** Institutional email login with role detection, password reset, and session persistence.
3. **Registration Page (`/register`):** Student and staff account creation with university affiliation selector.
4. **Forgot Password (`/forgot-password`):** Secure token-based password reset workflow.

#### B. Student Workspace
1. **Student Dashboard (`/app`):** Overview card showing quick links, pinned university announcements, search shortcuts, and recent conversations.
2. **Interactive AI Chat (`/app/chat` / `/app/chat/:id`):** 
   - Left sidebar with conversation history, pinned chats, and "New Chat" button.
   - Message timeline with user questions, assistant streaming tokens, interactive citation cards, and copy/feedback buttons.
   - Grounded Citation Slide-Over preview displaying document title, verified page number, and highlighted excerpt.
   - Query prompt bar with dynamic suggestions ("Attendance regulations", "Exam schedule", "Fee deadlines").
3. **University Knowledge Search (`/app/search`):** Semantic search engine allowing direct keyword & concept discovery across indexed university circulars.
4. **Notices & Events Board (`/app/events`):** Chronological feed of official announcements, exam circulars, and campus events.
5. **Student Profile & Settings (`/app/settings`):** University ID preferences, dark mode toggle, and notification thresholds.

#### C. Administration & Operations Center
1. **Admin Overview (`/admin`):** High-level KPI widgets (Active users, 24h query volume, average latency, groundedness score, user CSAT).
2. **Document Control Manager (`/admin/documents`):** 
   - List of all uploaded institution documents with indexing badges (`READY`, `INDEXING`, `FAILED`).
   - Drag-and-drop file uploader supporting PDF, DOCX, TXT, CSV.
   - Re-index and purge actions with deletion of associated vector chunks.
3. **Agent & Query Observability (`/admin/agents`):** Real-time trace logs detailing agent routing paths, critic confidence scores, and token usage metrics.
4. **User & Access Management (`/admin/users`):** Directory of enrolled students/staff with role provisioning.
5. **Audit Logs (`/admin/audit`):** Immutable chronological log of document ingestion, administrative changes, and security events.
