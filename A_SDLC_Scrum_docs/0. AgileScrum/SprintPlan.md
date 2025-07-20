# 🚀 Sprint Plan – Tech-Forge (7-Day Solo Agile Sprint)

## 🧭 Overview
This sprint plan defines a focused solo Agile development sprint to build the MVP for **Tech-Forge**, a gamified learning platform for computer science. It follows full SDLC phases and includes essential deliverables for each stage.

### 🗓 Sprint Duration
**July 16 – July 23**

### 🎯 Sprint Goals
- Build an MVP of the Tech-Forge platform  
- Cover Tutorial Library, Roadmap tracking, code practice, and basic gamification  
- Deliver core user experience: learning, progression, submission, and tracking

---

## 📅 7-Day SDLC-Based Development Plan

### 🟩 Day 1 – Planning & Requirement Analysis

**Objectives:**
- Clarify product vision and user value
- Define user journeys and system boundaries
- Draft Agile backlog and use cases

**Deliverables:**
- `README.md` – Product vision, features, tech stack  
- `SprintPlan.md` – This sprint document  
- `UserStories.md` – Core user stories (Agile format)  
- `ProductBacklog.xlsx` – Backlog with MoSCoW prioritization  
- `BFD.drawio` – Business Function Diagram  
- `UseCaseDiagram.drawio` – Use Case UML  
- `UseCaseDescriptions.docx` – Use case narratives (actors, flow, pre/post-conditions)

---

### 🟦 Day 2 – System Design

**Objectives:**
- Design overall architecture (Clean + Monolith-first)
- Model domain entities, flows, and UI
- Prepare system for future modularization

**Deliverables:**
- `ArchitectureDiagram.drawio` – High-level system architecture  
- `BRD.docx` – Business Requirements Document  
- `FRD.docx` – Functional Requirements  
- `NFR.docx` – Non-functional requirements (performance, security...)  
- `ERD.drawio` – Entity Relationship Diagram  
- `ClassDiagram.drawio`, `SequenceDiagram.drawio` – UML interactions  
- `Wireframes.pdf` – UI wireframes or sketches  
- `API_Spec.yaml` – OpenAPI/Swagger contract  

---

### 🟧 Day 3 – Project Setup & Auth System

**Objectives:**
- Scaffold project structure (Frontend + Backend)
- Setup database and CI/CD skeleton
- Build user authentication system

**Deliverables:**
- React + .NET source folder structure  
- Auth module: register/login/profile (JWT)  
- User schema, roles, tokens  
- `.env.sample`, `docker-compose.yml`  
- Initial migration scripts  

---

### 🟨 Day 4 – Tutorials Module (Phase 1)

**Objectives:**
- Implement public browsing of tutorials and lessons
- Enable reading + discovery point earning

**Deliverables:**
- UI for browsing topics and lessons  
- Backend CRUD APIs: Tutorial, Topic, Lesson  
- DiscoveryPoint system  
- Unit tests for lesson APIs  
- Integrated DB schemas  

---

### 🟨 Day 5 – Code Practice Module

**Objectives:**
- Add coding editor for exercises
- Implement code evaluation and submission logic

**Deliverables:**
- Monaco/CodeMirror in-browser editor  
- `Exercise`, `TestCase`, `Submission` entities  
- CodeRunner service (Dockerized or sandboxed)  
- Store pass/fail result + user feedback  

---

### 🟪 Day 6 – Roadmap Module + Testing

**Objectives:**
- Enable Roadmap exploration and progress tracking  
- Validate key features via testing

**Deliverables:**
- Join roadmap flow  
- Unlock lessons and EXP gain  
- UI for user roadmap progress  
- `TestCases.xlsx` – Manual/automated tests  
- `BugList.md` – Defects and resolutions  

---

### 🟥 Day 7 – Deployment & Final Documentation

**Objectives:**
- Deploy to production (VPS/Render/Vercel)  
- Finalize all user-facing and developer docs

**Deliverables:**
- Live deployment  
- `InstallationGuide.md` – Setup instructions  
- `UserGuide.md` – Platform usage guide  
- `API_Documentation.md` – Swagger/Markdown API docs  
- `FinalTestReport.md` – QA report  

---

## 🔖 Notes
- **Sprint Model**: Solo Agile with SDLC  
- **Architecture**: Clean Architecture + Monolith-first  
- **Tracking**: All tasks managed via `ProductBacklog.xlsx`  
- **Prioritization**: MoSCoW (Must, Should, Could, Won’t)
