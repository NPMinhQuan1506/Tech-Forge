# ⚙️ Tech-Forge

**Tech-Forge** is a programming learning platform that combines theory and practice. Learners can explore technical topics such as C#, JavaScript, algorithms, design patterns, system design, and practice directly in the browser.

This project was built in 7 days following Agile/Scrum methodology—as a hands-on "tech forge" for learning, coding, and designing a professional software development process.

---

## ✨ Main Features

- View tutorials with sample code and illustrations
- Run code directly in the browser (similar to a mini LeetCode)
- Solve exercises with test cases, get instant feedback, and save results
- Track learning progress and submission history
- Admins can create new lessons and manage content
- Clean interface optimized for learner experience

---

## 🧱 Technology Stack

- Frontend: ReactJS, Tailwind CSS, Monaco Editor (VSCode-like)
- Backend: ASP.NET Core API
- Database:
  - MongoDB (stores tutorials & exercises)
  - PostgreSQL / SQL Server (stores users, submissions)
- Authentication: JWT, ASP.NET Identity
- CI/CD: Docker, GitHub Actions (optional for future expansion)

---

## 📂 Folder Structure

Tech-Forge/
├── frontend/        # React UI
├── backend/         # .NET Core API
├── docs/
│   └── 0_AgileScrum/
│       ├── SprintPlan.md
│       ├── UserStories.md
│       ├── ProductBacklog.xlsx
│       └── MoSCoW_Priorities.xlsx
├── docker-compose.yml
└── README.md

---

## 🛠️ How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/your-username/tech-forge.git
cd tech-forge
```
