Tech-Forge System - Use Case Descriptions

Author: NP Minh Quan  
Date: July 21, 2025

# Package: 1. Tutorial Library – UC-1.1: Explore Free Content

Actors: Guest, Learner

Description: Allows users to browse, search, and view tutorials and lessons in a free library without committing to a learning path.

Related User Stories: US-01, US-02, US-03, US-04, US-05

Main Flow:

- \- User accesses the "Tutorial Library" section.
- \- The system displays categorized topics.
- \- User selects a topic to see its list of lessons.
- \- User selects a lesson to view its details and any sample exercises.

# Package: 2. Roadmaps – UC-2.1: Manage Roadmap Enrollment

Actors: Learner

Description: Allows learners to explore available learning roadmaps, view details, and join one to start tracking progress.

Related User Stories: US-06, US-07

Main Flow:

- \- Learner accesses the "Roadmaps" section.
- \- The system displays all available roadmaps.
- \- Learner selects a roadmap to view its description and milestones.
- \- Learner clicks "Join Roadmap".
- \- The system confirms and adds the roadmap to the learner profile.

# Package: 2. Roadmaps – UC-2.2: Follow Guided Roadmap

Actors: Learner

Description: Learner follows a structured roadmap with lessons and challenges. Completing steps unlocks content and rewards.

Related User Stories: US-08, US-09, US-11, US-12

Relations: Includes: UC-4.2: Submit Exercise, Extends: UC-2.3: Face Boss Quiz

Main Flow:

- \- Learner selects an active roadmap.
- \- The system shows the progression interface with unlocked lessons.
- \- Learner completes lessons and exercises (&lt;<include&gt;> UC-4.2).
- \- System tracks progress, awards EXP, and unlocks next content.
- \- At milestones, learner may face a Boss Quiz (&lt;<extend&gt;> UC-2.3).

# Package: 3. Courses – UC-3.1: Enroll in Premium Course

Actors: Learner

Description: Allows learners to browse premium courses and enroll using earned points.

Related User Stories: US-13, US-14, US-15

Main Flow:

- \- Learner browses the premium courses list.
- \- Learner selects a course to view details and cost (in points).
- \- Learner may need to complete an entry quiz.
- \- Learner confirms point deduction to enroll.
- \- System deducts points and grants access to course.

# Package: 3. Courses – UC-3.2: Follow Premium Course

Actors: Learner

Description: Learner progresses through exclusive course content, possibly personalized based on performance.

Related User Stories: US-16, US-17, US-18, US-19

Relations: Includes: UC-4.2: Submit Exercise, Extends: UC-3.3: Access Special Events

Main Flow:

- \- Learner accesses an enrolled course.
- \- System displays exclusive lessons and exercises.
- \- Learner completes exercises (&lt;<include&gt;> UC-4.2).
- \- System evaluates performance and may adjust content or grant rewards.
- \- High performers may access special events (&lt;<extend&gt;> UC-3.3).

# Package: 4. Core Platform & Community – UC-4.1: Register Account

Actors: Guest

Description: Allows a guest to register a new learner account for personalized access.

Related User Stories: (Precondition for US-07, US-11, US-23, US-25)

Preconditions: User is a Guest.

Postconditions: A new learner account is created and logged in.

Main Flow:

- \- Guest clicks "Register" or "Sign Up".
- \- System displays the registration form.
- \- Guest fills in required info (e.g., username, email, password).
- \- Guest confirms password and accepts Terms of Service.
- \- Guest clicks "Create Account".
- \- System validates input.
- \- System creates learner record and saves data.
- \- User is logged in and redirected to dashboard.

Alternative Flows:

- \- Invalid input: System shows validation errors and prompts corrections.
- \- Duplicate email/username: System prompts to choose another.

# Package: 4. Core Platform & Community – UC-4.2: Submit Exercise

Actors: Learner

Description: Describes the process of submitting an exercise solution and receiving automatic feedback.

Related User Stories: US-21, US-22

Main Flow:

- \- Learner navigates to assigned exercise.
- \- Learner submits solution (code/answer).
- \- System evaluates automatically and gives feedback (pass/fail, score, comments).

# Package: 4. Core Platform & Community – UC-4.3: View Profile & Rankings

Actors: Learner

Description: Allows learners to view personal profile including EXP, ranks, badges, and leaderboard position.

Related User Stories: US-23, US-27

Main Flow:

- \- Learner accesses profile dashboard.
- \- System shows experience points, badges, inventory.
- \- System shows global and roadmap-specific rankings.

# Package: 4. Core Platform & Community – UC-4.4: Manage Custom Roadmaps

Actors: Learner

Description: Allows learners to create, share, and manage custom roadmaps; also explore and reuse others'.

Related User Stories: US-25, US-26

Main Flow:

- \- Learner accesses 'My Roadmaps'.
- \- Learner creates/edit a custom roadmap (title, topics, lessons).
- \- Learner publishes roadmap to community.
- \- Learner browses community roadmaps and can import or rate.

# Package: 5. System Administration – UC-5.1: Manage Learning Content

Actors: Admin

Description: Provides admin with interface to manage lessons, exercises, roadmaps, courses, and events.

Related User Stories: US-29, US-30, US-31, US-34

Main Flow:

- \- Admin logs in to backend panel.
- \- Admin creates/edits/deletes any content item (lesson, roadmap, course).
- \- Changes are saved and reflected immediately.

# Package: 5. System Administration – UC-5.2: Manage Users & Rules

Actors: Admin

Description: Allows admin to monitor user activities, adjust scores, and enforce platform policies.

Related User Stories: US-24, US-32

Main Flow:

- \- Admin views user list and profiles.
- \- Admin modifies user EXP/rank if needed.
- \- Admin applies penalties for violations or locks accounts.

# Package: 5. System Administration – UC-5.3: View System Analytics

Actors: Admin

Description: Provides admin with dashboards and metrics on platform usage, learning trends, and user performance.

Related User Stories: US-33

Main Flow:

- \- Admin accesses analytics dashboard.
- \- System shows reports on user progress, top roadmaps, course popularity, and other KPIs.