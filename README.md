# Dashflow - Security Operations Management System

A Flask-based web application for managing security operations, including agent management, attendance tracking, payroll processing, and reporting.

## Quick Start

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

### Quick Setup (TL;DR)

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python run.py

# 4. Open browser to http://localhost:5000
# Login with: admin@security.com / admin123
```

## Features

- **Agent Management**: Manage security agents with profiles, photos, and hourly rates
- **Client & Site Management**: Organize clients and their security sites
- **Attendance Tracking**: Record and track agent attendance with proof uploads
- **Corrections System**: Request and review attendance corrections
- **Payroll Processing**: Generate payroll based on attendance records
- **Reporting**: Generate attendance and payroll reports
- **User Management**: Admin and operator role management

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite (local dev) / PostgreSQL (production)
- **Authentication**: JWT (Flask-JWT-Extended)
- **Frontend**: Vanilla JavaScript with Tailwind CSS

## Default Credentials

- **Email**: admin@security.com
- **Password**: admin123

⚠️ **Change these credentials in production!**

## Project Structure

```
dashflow/
├── app/              # Application code
│   ├── models.py    # Database models
│   ├── routes/      # API routes
│   └── utils/       # Utility functions
├── static/          # Frontend files
├── config.py        # Configuration
└── run.py          # Entry point
```

## Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)**: Complete step-by-step setup instructions
