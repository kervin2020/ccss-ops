# Starting the Servers

## Current Status

### Frontend (frontendfinal)
- ✅ Dependencies installed
- ⚠️ Node processes detected but server status unclear

### Backend (backendfinal)
- ⚠️ Python not found in system PATH
- ⚠️ Virtual environment appears to be from Linux/Mac (has `bin` instead of `Scripts`)

## Setup Instructions

### Option 1: Install Python (Recommended)

1. **Install Python 3.8+ from python.org:**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Create a new virtual environment:**
   ```powershell
   cd C:\Users\aa\Downloads\ccss-ops\backendfinal
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Start the backend:**
   ```powershell
   python run.py
   ```

### Option 2: Use Existing Setup (if Python is installed elsewhere)

If Python is installed but not in PATH:

1. Find your Python installation path
2. Use the full path to Python:
   ```powershell
   C:\Path\To\Python\python.exe -m venv venv
   ```

### Frontend Setup

The frontend dependencies are already installed. To start:

```powershell
cd C:\Users\aa\Downloads\ccss-ops\frontendfinal
npm run dev
```

## Expected URLs

- **Backend API:** http://localhost:5000
- **Frontend:** http://localhost:5173 (Vite default)

## Troubleshooting

### If ports are already in use:
- Backend: Set `PORT` environment variable: `$env:PORT=5001; python run.py`
- Frontend: Vite will automatically use the next available port

### If Python is not found:
- Make sure Python is installed and added to PATH
- Or use the full path to Python executable

### If virtual environment issues:
- Delete the existing `venv` folder
- Create a new one using `python -m venv venv` (Windows will create `Scripts` folder)

