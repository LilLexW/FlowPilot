# 🚀 FlowPilot

AI-powered project management platform that transforms meeting notes into structured insights and actionable tasks.

[🚀 Live Demo](https://flowpilot.streamlit.app/)

---

## Overview

FlowPilot is an AI-powered project management platform that turns unstructured meeting notes into actionable project tasks.

The system uses an AI Meeting Assistant to analyze meeting notes, extract action items, identify project risks, and generate next steps. Users can then convert these action items into project tasks and manage them through projects, task status, deadlines, and progress tracking.

---

## Key Features

### AI Meeting Assistant

- Generate meeting summaries from meeting notes
- Extract actionable tasks
- Identify task owners
- Assign task priorities and deadlines
- Identify project risks
- Generate next steps
- Return structured JSON for downstream processing

### Automatic Task Generation

- Convert AI-generated action items into project tasks
- Assign owners and priorities
- Store deadlines
- Prevent duplicate task creation
- Track task status

### Project Management

- Create projects
- View project progress
- View project-specific tasks
- Track completed tasks
- Delete projects and associated tasks

### Dashboard

- Total projects
- Total tasks
- Tasks in progress
- Completed tasks
- Overall completion progress

---

## Workflow

Meeting Notes

↓

AI Meeting Assistant

↓

Summary + Action Items + Risks + Next Steps

↓

Task Generation

↓

Duplicate Detection

↓

SQLite Database

↓

Projects + Tasks

↓

Dashboard

---

## Screenshots

### Dashboard

![FlowPilot Dashboard](screenshots/Dashboard.png)

### AI Meeting Assistant

![AI Meeting Assistant](screenshots/AI-Meeting-Assistant.png)

### Task Management

![Task Management](screenshots/Tasks.png)

### Project Management

![Project Management](screenshots/Projects.png)

### Duplicate Task Detection

![Duplicate Task Detection](screenshots/Duplicate.png)

---

## Tech Stack

Python  
Streamlit  
SQLite  
OpenRouter API  
Google Gemma  
python-dotenv

---

## Architecture

The application follows a simple modular architecture:

- `app.py` — Main Streamlit dashboard
- `pages/meetings.py` — AI Meeting Assistant and task generation
- `pages/tasks.py` — Task management
- `pages/Projects.py` — Project management
- `llm.py` — LLM API integration and structured response processing
- `database.py` — SQLite database operations

---

## Project Structure

FlowPilot/
├── app.py
├── database.py
├── llm.py
├── requirements.txt
├── README.md
├── .gitignore
├── pages/
│   ├── Projects.py
│   ├── meetings.py
│   └── tasks.py
└── screenshots/
    ├── AI-Meeting-Assistant.png
    ├── Dashboard.png
    ├── Duplicate.png
    ├── Projects.png
    └── Tasks.png

---

## Local Setup

### 1. Clone the repository

git clone https://github.com/LilLexW/FlowPilot

cd FlowPilot

### 2. Install dependencies

pip install -r requirements.txt

### 3. Configure the API key

Create a `.env` file in the project root.

OPENROUTER_API_KEY=your_api_key

### 4. Run the application

streamlit run app.py

---

## Security

API keys are stored using environment variables and are not included in the repository.

For the deployed application, API credentials are managed through Streamlit Secrets.

---

## Future Improvements

- User authentication
- Multi-user project workspaces
- Cloud database integration
- Calendar integration
- Advanced project analytics
- More AI-powered project insights
