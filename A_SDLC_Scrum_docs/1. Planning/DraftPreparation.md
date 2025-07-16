## 1. System Architecture

- Web Browser
  - User: Learner / Admin
- Frontend App (ReactJS)
  - Communicates with Backend API via HTTPS
- Backend API Server (.NET Core 6 REST API)
  - Handles business logic and data access
  - Connects to:
    - SQL Server Database (stores users, data)
    - Code Runner API (e.g., Judge0 or Sandbox) for code execution and grading

Optional features:
- Auth via JWT
- File upload (e.g., tutorial images)
- Deployment via Docker on VPS (nginx reverse proxy)

---

## 2. Functional Overview

- User Roles
  - Learner
  - Admin
  - Guest

- Main Features
  - Home / Dashboard View
    - Explore Topics
      - View Tutorials (Markdown + Tags)
      - View Learning Roadmap (per topic or track)
    - Practice Challenges
      - Submit Code + Get Score
      - Auto evaluate with tests
    - Account Management
      - Edit Profile
      - Track Submissions

---

## 3. Draft ERD

### Entity List

- User
- Tutorial
- Exercise
- Submission
- Progress
- Roadmap (optional)
- Topic
- Tag