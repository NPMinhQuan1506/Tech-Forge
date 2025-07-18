# 📄 Business Requirements Document (BRD)

## Project Name: Tech-Forge Platform – Computer Science Learning System

---

## 1. Executive Summary

Tech-Forge is a web-based educational platform that helps users learn and practice computer science topics through structured tutorials, interactive exercises, and AI-powered feedback. It is designed for self-learners, students, and professionals aiming to strengthen their knowledge in areas such as programming languages, algorithms, system design, and AI.

---

## 2. Business Objectives

* Democratize computer science education by providing curated, multi-topic learning tracks.
* Enable hands-on learning via in-browser code execution and testing.
* Motivate learners with progress tracking, ranking, and gamification.
* Empower content creators/admins with full control over curriculum, exercises, and roadmap management.

---

## 3. Scope of Work

### In Scope:

* User-facing platform with tutorials, coding exercises, and progress tracking.
* Admin interface to manage content and roadmaps.
* Support for multiple programming languages and topics.
* User authentication and profile management.
* Roadmap-based learning and ranking.
* Backend API (.NET 6), frontend (React), database (SQL Server), deployable to VPS.

### Out of Scope (initial release):

* Real-time chat or forums
* Payment or subscription systems
* Mobile apps

---

## 4. Stakeholders

* **Project Owner:** \[Your Name]
* **Primary Users:** Self-learners, developers, CS students
* **Secondary Users:** Admins/content creators

---

## 5. Functional Requirements (High-Level)

* Browse learning tracks and topics
* View and complete structured tutorials
* Write and run code in-browser
* Submit exercises with test cases
* Track learning progress and history
* Register, log in, and edit profile
* Admins manage tutorials, exercises, and roadmaps
* View ranking and achievements

---

## 6. Non-Functional Requirements

* Responsive design for web
* Secure authentication using JWT or Identity
* Code runner isolated and containerized
* Scalable backend API design
* Admin interface access restricted by role

---

## 7. Assumptions

* User will access via desktop or modern browsers.
* Code execution will be sandboxed for security.
* Admin roles will be assigned manually via database in early versions.

---

## 8. Constraints

* One developer team (solo dev)
* Limited to 7-day MVP schedule
* Hosting on VPS only, no commercial cloud services initially

---

## 9. Success Criteria

* MVP deployed and functional within 7 days
* Learners can complete at least 1 full roadmap
* Admin can add content without database access
* All critical user stories labeled "Must" are completed in Sprint 1 and 2

---

## 10. Appendices

* User Stories (see UserStories.md)
* Product Backlog (ProductBacklog.xlsx)
* ERD (tech\_forge\_erd.drawio)
* Architecture (ArchitectureDiagram.drawio)

---

*Document version: v1.0 – July 2025*
