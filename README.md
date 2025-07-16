# 🧠 Tech-Forge – Computer Science Learning Platform

Tech-Forge is a modern web-based platform for learning and practicing topics in computer science.  
It offers tutorials, coding exercises, and interactive challenges across a wide range of subjects such as:

- Programming Languages (C#, Python, JavaScript, etc.)
- Software Engineering (Design Patterns, System Design)
- AI & Machine Learning (Coming soon)
- Libraries & Frameworks
- Business Analysis & Product Thinking
- UX/UI and Visual Design (Planned)

## Key Features

### For Learners
- Browse structured tutorials with code, visuals, and explanations
- Practice with coding exercises and instant test case validation (like LeetCode)
- Earn points, climb ranks, and track topic-wise progress
- Personalized user account with profile and history

### For Admins
- Add/edit tutorials with Markdown + images
- Manage exercises (code templates, test cases, tags)
- Control visibility and categorize content

## Tech Stack

- **Frontend**: ReactJS + TailwindCSS
- **Backend**: .NET Core 6 (RESTful API)
- **Database**: SQL Server
- **Deployment**: VPS with CI/CD

## Project Structure (simplified)
```
Tech-Forge/
├── frontend/       # React app
├── backend/        # .NET Core API
├── docs/           # Documentation
├── scripts/        # Deployment scripts
└── README.md
```

## 🚀 Deployment
The platform will be deployed to a self-managed VPS and configured with environment-specific settings using `.env` files and Docker if needed.
