# Coaching Center Management System – Backend

Backend API for the Coaching Center Management System.  
Provides role-based authentication and APIs for Admin, Teacher, and Student dashboards.

## Features
- Role-based authentication (Admin, Teacher, Student)
- Admin APIs for managing students, teachers, batches, and fees
- Teacher APIs for attendance management
- Student APIs to view batches, fees and attendance
- Secure authentication and authorization
- Email sending for onboarding

## Tech Stack
- Python
- FastAPI
- PostgreSQL

## Environment Variables

1. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

2. Add your env values


## How to run locally

```bash
git clone https://github.com/Nandini0409/crms-backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```