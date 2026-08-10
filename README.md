\# FlowPilot 🚀



AI-powered project management platform built with Python, Streamlit, SQLite, and Google Gemma.



\## Overview



FlowPilot transforms unstructured meeting notes into structured project information and actionable tasks.



The platform connects AI-powered meeting analysis with project and task management.



\## Features



\- AI meeting summarization

\- Action item extraction

\- Risk identification

\- Next-step generation

\- Automatic task generation

\- Task owner extraction

\- Task priority extraction

\- Deadline extraction

\- Duplicate task detection

\- Project management

\- Task CRUD operations

\- Task status tracking

\- Task filtering

\- Project progress tracking

\- Dashboard analytics



\## Workflow



Meeting Notes

↓

Google Gemma

↓

Structured JSON

↓

Action Items

↓

Tasks

↓

SQLite Database

↓

Projects / Tasks / Dashboard



\## Tech Stack



\- Python

\- Streamlit

\- SQLite

\- REST API

\- Google Gemma

\- OpenRouter



\## Project Structure



flowpilot/

├── app.py

├── database.py

├── llm.py

├── requirements.txt

├── README.md

├── .gitignore

└── pages/

&#x20;   ├── Projects.py

&#x20;   ├── meetings.py

&#x20;   └── tasks.py



\## Setup



Install dependencies:



pip install -r requirements.txt



Create a .env file in the project root:



OPENROUTER\_API\_KEY=your\_api\_key\_here



Run the application:



streamlit run app.py



\## Architecture



Meeting Notes

↓

Google Gemma

↓

Structured JSON

↓

Task Extraction

↓

SQLite

↓

Task Management

↓

Dashboard

