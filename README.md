# Event Management System

## Overview
A comprehensive web application for booking and managing event spaces, designed to prevent conflicts and ensure smooth event management.

## Features
- User Authentication (Admin and Organizer roles)
- Space Management
- Booking System with Conflict Detection
- Event Dashboard
- Notifications and Reminders
- Multi-Language Support
- Custom Themes

## Tech Stack
- Frontend: React
- Backend: Django (Python)
- Database: PostgreSQL
- Notifications: Firebase Cloud Messaging

## Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)

## Local Setup

### Backend Setup
1. Navigate to backend directory
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Docker Deployment
```bash
docker-compose up --build
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
