# 📋 Functional Requirements Document (FRD)

## Project Name: Tech-Forge Platform – Computer Science Learning System

---

## 1. Introduction

This document details the specific functional requirements for the Tech-Forge Platform MVP. It breaks down the high-level features outlined in the BRD into actionable requirements for development, categorized by user role.

---

## 2. Guest Requirements (Unauthenticated User)

| ID       | Requirement Description                                       | Related User Story | Priority |
| :------- | :------------------------------------------------------------ | :----------------- | :------- |
| FR-G-01  | The system shall allow guests to browse all public tutorials and topics. | US-01, US-03       | Must     |
| FR-G-02  | The system shall provide a registration form for guests to create a new Learner account. | (Implicit)         | Must     |

---

## 3. Learner Requirements (Authenticated User)

| ID       | Requirement Description                                       | Related User Story | Priority |
| :------- | :------------------------------------------------------------ | :----------------- | :------- |
| FR-L-01  | The system shall allow learners to log in and log out securely. | (Implicit)         | Must     |
| FR-L-02  | Learners shall be able to view and edit their own profile information (e.g., name, avatar). | US-23              | Should   |
| FR-L-03  | Learners shall be able to enroll in a learning Roadmap and have their progress saved. | US-06, US-07       | Must     |
| FR-L-04  | The system shall display the learner's progress within a Roadmap (e.g., completed lessons). | US-08, US-11       | Must     |
| FR-L-05  | Learners shall be able to write code in an in-browser editor for an exercise. | US-21              | Must     |
| FR-L-06  | Upon submission, the system shall run the code against predefined test cases and show the result (Pass/Fail). | US-21              | Must     |
| FR-L-07  | Learners shall be able to view their submission history for each exercise. | US-22              | Should   |
| FR-L-08  | The system shall display a leaderboard or ranking based on learner progress or points. | US-27              | Could    |

---

## 4. Admin Requirements (Content Creator)

| ID       | Requirement Description                                       | Related User Story | Priority |
| :------- | :------------------------------------------------------------ | :----------------- | :------- |
| FR-A-01  | Admins shall be able to log into a dedicated admin interface.   | (Implicit)         | Must     |
| FR-A-02  | Admins shall be able to Create, Read, Update, and Delete (CRUD) learning tutorials/lessons. | US-29              | Must     |
| FR-A-03  | Admins shall be able to CRUD coding exercises, including their descriptions and test cases. | US-30              | Must     |
| FR-A-04  | Admins shall be able to CRUD learning Roadmaps by assembling existing lessons and exercises. | US-31              | Must     |

---

*Document version: v1.0 – July 2025*