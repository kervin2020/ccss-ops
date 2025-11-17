# Dashflow Local Setup Guide

This guide will walk you through setting up and running the Dashflow application on your local machine step by step.

## Prerequisites

Before you begin, make sure you have:
- **Python 3.8 or higher** installed on your system
- **pip** (Python package installer) - usually comes with Python
- A terminal/command line interface

## Step-by-Step Setup Instructions

### Step 1: Verify Python Installation

First, let's check if Python is installed and what version you have:

```bash
python3 --version
```

You should see something like `Python 3.8.x` or higher. If you get an error, you need to install Python first.

**What this does:** This command checks if Python 3 is installed on your system.

---

### Step 2: Navigate to the Project Directory

Open your terminal and navigate to the project folder:

```bash
cd /Users/kervinrobergeau/Code/dashflow
```

**What this does:** Changes your current directory to the project folder so all commands run in the right location.

---

### Step 3: Create a Virtual Environment

A virtual environment isolates your project's dependencies from other Python projects on your system:

```bash
python3 -m venv venv
```

**What this does:** Creates a new folder called `venv` that will contain a separate Python environment for this project.

**Why we do this:** This keeps the packages for this project separate from other Python projects, preventing conflicts.

---

### Step 4: Activate the Virtual Environment

Activate the virtual environment you just created:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

**What this does:** Activates the virtual environment. You should see `(venv)` appear at the beginning of your terminal prompt.

**How to know it worked:** Your terminal prompt should now show `(venv)` at the start, like this:
```
(venv) kervinrobergeau@MacBook dashflow %
```

---

### Step 5: Upgrade pip (Optional but Recommended)

Upgrade pip to the latest version:

```bash
pip install --upgrade pip
```

**What this does:** Updates pip (the Python package installer) to the latest version to ensure smooth package installation.

---

### Step 6: Install Project Dependencies

Install all the required Python packages for the project:

```bash
pip install -r requirements.txt
```

**What this does:** Reads the `requirements.txt` file and installs all the packages listed there (Flask, SQLAlchemy, JWT, etc.).

**What to expect:** This will take a few minutes as it downloads and installs packages. You'll see a lot of output showing what's being installed.

**Common issues:**
- If you get an error about a package version, the `requirements.txt` has been updated to use compatible versions
- If installation fails, make sure your virtual environment is activated (you should see `(venv)` in your prompt)

---

### Step 7: Set Up Environment Variables (Optional)

The application can work without a `.env` file for local development, but you can create one if you want to customize settings.

Create a file named `.env` in the project root:

```bash
touch .env
```

Then open it in a text editor and add:

```
SESSION_SECRET=dev-secret-key-change-in-production

# Cloud Storage Configuration (Optional)
# Set to 's3' to use AWS S3, or 'local' for local storage (default)
STORAGE_TYPE=local

# AWS S3 Configuration (only needed if STORAGE_TYPE=s3)
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# S3_BUCKET_NAME=your-bucket-name
# S3_REGION=us-east-1
```

**What this does:** 
- Sets a secret key for session management
- Configures file storage (local by default, or AWS S3 for production)

**Note:** 
- The application is configured to use SQLite (a file-based database) by default for local development
- Files are stored locally by default, but can be configured to use AWS S3 for cloud storage
- Even with cloud storage enabled, files are also saved locally for redundancy

---

### Step 8: Run the Application

Start the Flask development server:

```bash
python run.py
```

**What this does:** Starts the Flask web server on your local machine.

**What to expect:** You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Important:** Keep this terminal window open while the application is running. The server will stop if you close the terminal or press `Ctrl+C`.

---

### Step 9: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

**What this does:** Opens the Dashflow application in your browser.

**What you should see:** A login page with the Security Operations Management System interface.

---

### Step 10: Log In with Default Credentials

The application automatically creates a default admin user on first run. Use these credentials:

- **Email:** `admin@security.com`
- **Password:** `admin123`

**What this does:** Logs you into the application with administrator privileges.

**Security Note:** Change this password immediately in a production environment!

---

## Verifying Everything Works

### Check the Database

The application automatically creates a SQLite database file (`dashflow.db`) in the project directory on first run. You can verify it exists:

```bash
ls -la dashflow.db
```

**What this does:** Lists the database file if it exists, confirming the database was created successfully.

---

## Common Commands Reference

### Start the Application
```bash
source venv/bin/activate  # Activate virtual environment (if not already active)
python run.py             # Start the server
```

### Stop the Application
Press `Ctrl+C` in the terminal where the server is running.

### Deactivate Virtual Environment
When you're done working, you can deactivate the virtual environment:
```bash
deactivate
```

### Reinstall Dependencies
If you need to reinstall all packages:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Troubleshooting

### Issue: "python3: command not found"
**Solution:** Python might not be in your PATH. Try `python` instead of `python3`, or install Python from python.org.

### Issue: "ModuleNotFoundError" when running the app
**Solution:** Make sure your virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Address already in use" error
**Solution:** Port 5000 is already in use. Either:
- Stop the other application using port 5000
- Or change the port in `run.py` (line 11) to a different number like `5001`

### Issue: Database errors
**Solution:** Delete the database file and let it recreate:
```bash
rm dashflow.db
python run.py  # This will recreate the database
```

### Issue: Can't access http://localhost:5000
**Solution:** 
- Make sure the server is running (check the terminal for errors)
- Try `http://127.0.0.1:5000` instead
- Check your firewall settings

---

## Project Structure Overview

Understanding the project structure helps you navigate the codebase:

```
dashflow/
├── app/                    # Main application code
│   ├── __init__.py        # Flask app initialization
│   ├── models.py         # Database models (User, Agent, etc.)
│   ├── routes/           # API route handlers
│   │   ├── auth_routes.py
│   │   ├── agent_routes.py
│   │   └── ...
│   └── utils/            # Utility functions
├── static/               # Frontend files
│   ├── index.html       # Main HTML page
│   └── js/
│       └── app.js       # Frontend JavaScript
├── config.py            # Configuration settings
├── run.py              # Application entry point
├── requirements.txt    # Python dependencies
└── dashflow.db        # SQLite database (created on first run)
```

---

## New Features

### Excel Export Functionality

The application now includes comprehensive Excel export capabilities:

1. **Export Agents:** Export all agent data to Excel
2. **Export Attendance:** Export attendance records with date filters
3. **Export Payroll:** Export payroll information
4. **Export Clients & Sites:** Export client and site data
5. **Export Users:** Admin-only feature to export user data
6. **Export All Data:** Admin-only feature to export all data in a single Excel file with multiple sheets

**How to use:**
- Navigate to the "Reports" section in the dashboard
- Click on any export button to download the data as an Excel file
- All exports include formatted headers and proper column widths

**Why this is important:** This allows you to create backups of your data before making changes or in case of data loss.

### Cloud Storage for Photos

The application supports cloud storage for photos and files:

- **Local Storage (Default):** Files are stored locally in the `uploads/` folder
- **AWS S3 (Optional):** Configure AWS S3 for cloud storage in production
- **Hybrid Approach:** Even with cloud storage enabled, files are also saved locally for redundancy

**Benefits:**
- Prevents server storage from filling up
- Scalable file storage
- Redundancy with local backup
- Better performance with CDN integration (when using S3)

## Next Steps

Once you have the application running:

1. **Explore the Interface:** Log in and explore the different sections (Agents, Clients, Attendance, etc.)

2. **Try Export Features:** Go to the Reports section and try exporting data to Excel

3. **Read the Code:** Start with `run.py` to see how the app starts, then look at `app/__init__.py` to see how routes are registered.

4. **Make Changes:** The application is set up for development, so changes you make will automatically reload (thanks to Flask's debug mode).

5. **Check the API:** The application has a REST API. You can test it using tools like Postman or curl.

---

## Development Tips

- **Debug Mode:** The app runs in debug mode by default, which means:
  - Changes to code automatically reload the server
  - Detailed error messages are shown
  - This is only for development, not production!

- **Database Changes:** If you modify models in `app/models.py`, you may need to delete `dashflow.db` and let it recreate, or use Flask-Migrate for proper database migrations.

- **Logs:** Check the terminal where the server is running for any error messages or logs.

---

## Summary

You've successfully set up the Dashflow application! Here's what you did:

1. ✅ Verified Python installation
2. ✅ Created a virtual environment
3. ✅ Activated the virtual environment
4. ✅ Installed all dependencies
5. ✅ Started the Flask server
6. ✅ Accessed the application in your browser
7. ✅ Logged in with default credentials

The application is now running locally and ready for development!

---

## Need Help?

If you encounter issues not covered in this guide:
1. Check the terminal output for error messages
2. Verify all steps were completed correctly
3. Make sure your virtual environment is activated
4. Ensure all dependencies are installed

Happy coding! 🚀

