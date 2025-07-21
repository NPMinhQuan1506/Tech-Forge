# ⚙️ Non-Functional Requirements Document (NFR)

## Project Name: Tech-Forge Platform – Computer Science Learning System

---

## 1. Introduction

This document specifies the non-functional requirements (NFRs) for the Tech-Forge Platform MVP. These NFRs define the system's quality attributes, ensuring it meets standards for performance, security, and usability within the project's constraints.

---

## 2. Non-Functional Requirements

| ID        | Category          | Requirement Description                                                                                      |
| :-------- | :---------------- | :----------------------------------------------------------------------------------------------------------- |
| NFR-PE-01 | **Performance**   | **Page Load:** Core user-facing pages (tutorials, roadmap view) should load in under 3 seconds on a standard internet connection. |
| NFR-PE-02 | **Performance**   | **API Response:** 95% of API requests should complete in under 500ms.                                        |
| NFR-PE-03 | **Performance**   | **Code Execution:** Execution of a solution for a simple algorithm exercise should return a result within 10 seconds. |
| NFR-SE-01 | **Security**      | **Authentication:** User authentication must be handled securely using industry-standard tokens (e.g., JWT). All passwords must be hashed. |
| NFR-SE-02 | **Security**      | **Transport Security:** All data transmitted between the client and server must be encrypted via HTTPS.      |
| NFR-SE-03 | **Security**      | **Code Sandboxing:** User-submitted code **must** be executed in a securely isolated and containerized environment (Docker) to prevent any access to the host system or other users' data. |
| NFR-SE-04 | **Security**      | **Authorization:** The admin interface must be protected and accessible only to users with the 'Admin' role. |
| NFR-US-01 | **Usability**     | **Responsiveness:** The user-facing platform must have a responsive design that is functional and readable on modern desktop and mobile web browsers. |
| NFR-CO-01 | **Compatibility** | **Browser Support:** The platform must be fully functional on the latest versions of Google Chrome, Mozilla Firefox, and Microsoft Edge. |
| NFR-AR-01 | **Architecture**  | **Maintainability:** The backend shall be built as a Modular Monolith following Clean Architecture principles to simplify future maintenance and potential migration to microservices. |
| NFR-CO-02 | **Constraints**   | **Development:** The MVP must be achievable by a solo developer within the 7-day schedule. This may require prioritizing core features over extensive optimization. |
| NFR-CO-03 | **Deployment**    | **Infrastructure:** The entire system must be deployable to a single VPS using Docker and Nginx. |

---

*Document version: v1.0 – July 2025*