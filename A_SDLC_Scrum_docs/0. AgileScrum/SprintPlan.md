# Sprint Plan – Tech-Forge (7-Day Solo Agile Sprint)

## Overview
This sprint plan outlines the work to be done in 7 consecutive days for building the Tech-Forge platform MVP using Agile methodology.

## Goals
- Deliver a functioning web platform for tech tutorials and coding practice
- Cover core user stories including content browsing, login, coding editor, and progress tracking

## Timeline
- This sprint runs from July 16 to July 23.

## Schedule
# 📅 7-Day Development Plan – SDLC-Based

> **Project Name**: [Your Project]  
> **Type**: Web Learning Platform (C#/React)  
> **Goal**: Complete MVP in 7 days using the SDLC process

---

## 🗓️ Day 1 – Planning & Requirement Analysis

**Objectives:**
- Define project scope and goals  
- Gather and analyze user & business requirements  
- Prepare the initial sprint plan

**Deliverables:**
- `README.md` – Project overview, key features, tech stack  
- `UserStories.md` – User stories in Agile format  
- `ProductBacklog.xlsx` – Detailed product backlog with prioritization  
- `SprintPlan.md` – 7-day sprint breakdown and task plan  
- `BFD.drawio` – Business Flow Diagram (illustrates core business process)  
- `UseCaseDiagram.drawio` – Use Case diagram (UML)  
- `UseCaseDescriptions.docx` – Descriptions of each use case (actors, flows, pre/post-conditions)

---

## 🗓️ Day 2 – System Design

**Objectives:**
- Design system architecture  
- Create database, class, and process diagrams  
- Sketch out UI wireframes

**Deliverables:**
- `BRD.docx` – Business Requirement Document  
- `FRD.docx` – Functional Requirement Document  
- `NFR.docx` – Non-Functional Requirements (security, performance, scalability)  
- `ERD.drawio` – Entity Relationship Diagram (data model)  
- `ClassDiagram.drawio` – UML Class Diagram  
- `SequenceDiagram.drawio` – Sequence diagram for major flows  
- `Wireframes.pdf/png` – UI wireframes or mockups (Figma/sketches)

---

## 🗓️ Day 3 – Auth System & Project Setup

**Objectives:**
- Scaffold frontend/backend source structure  
- Implement authentication system (Register/Login/Profile)  
- Setup database and perform initial migration

**Deliverables:**
- Source scaffolding (React + .NET Core or backend of choice)  
- Auth API (JWT or session-based)  
- UI for login, register, and user profile  
- Database migration: `User`, `Role`, `Token`, etc.

---

## 🗓️ Day 4 – Tutorials Module

**Objectives:**
- Build theory-based tutorials module

**Deliverables:**
- Tutorial list/detail UI  
- Backend API for tutorial management (CRUD)  
- Database: `Tutorial`, `Topic`, `Lesson` schemas  
- Unit tests for key APIs

---

## 🗓️ Day 5 – Code Practice Module

**Objectives:**
- Integrate an in-browser code editor  
- Auto-evaluate user submissions with test cases

**Deliverables:**
- Monaco Editor (or similar) UI integration  
- Backend code runner API (via Docker or secure sandbox)  
- Database: `Exercise`, `TestCase`, `Submission`  
- Store submission results + pass/fail evaluation

---

## 🗓️ Day 6 – Progress Tracking & Testing

**Objectives:**
- Track learning progress and user submissions  
- Perform functional testing and bug reporting

**Deliverables:**
- UI for submission history and point tracking  
- `TestCases.xlsx` – List of manual/automated test cases  
- `BugList.md` – Bugs found during testing and their status  
- Unit tests and basic integration tests

---

## 🗓️ Day 7 – Deployment & Final Documentation

**Objectives:**
- Deploy system to VPS or cloud  
- Write complete technical and user documentation

**Deliverables:**
- Live deployment on VPS / Render / Vercel / Railway  
- `UserGuide.md` – How to use the system (end-user manual)  
- `InstallationGuide.md` – How to set up project (dev/prod)  
- `API_Documentation.md` – Swagger or manual API docs  
- `FinalTestReport.md` – Test summary and final QA checklist

---

## Notes
- Priority follows MoSCoW model
- Tasks estimated in story points
- Everything tracked via this plan + ProductBacklog.xlsx
