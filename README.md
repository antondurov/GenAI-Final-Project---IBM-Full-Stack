# 📚 CodeCraftHub API

A beginner-friendly REST API built with Python and Flask that lets you manage a list of learning courses. This project is a great starting point for anyone learning how REST APIs work — it covers the four core operations every API needs: **Create, Read, Update, and Delete** (CRUD).

---

## 📖 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

CodeCraftHub API is a course-tracking tool. You can use it to keep track of courses you're learning, their descriptions, and their progress status (`Not Started`, `In Progress`, or `Completed`).

Instead of a traditional database, it stores all data in a local JSON file (`courses.json`). This keeps the setup simple — no database installation required — while still teaching the core concepts of REST API design.

**What you'll learn from this project:**

- How REST APIs are structured
- How HTTP methods (GET, POST, PUT, DELETE) map to actions
- How to send and receive JSON data
- How to handle errors and return proper HTTP status codes

---

## Features

- **Get all courses** — retrieve your full course list in one request
- **Get a single course** — look up any course by its ID
- **Create a course** — add a new course with a name, description, and status
- **Update a course** — edit any field of an existing course
- **Delete a course** — remove a course permanently
- **Input validation** — the API checks for required fields and valid status values
- **Auto-incrementing IDs** — each new course gets a unique numeric ID automatically
- **JSON file storage** — all data is saved to `courses.json` (no database needed)
- **Human-readable storage** — the JSON file is formatted and easy to read/inspect

---

## Project Structure

```
codecrafthub/
│
├── app.py            ← Main application file (all routes and logic live here)
├── courses.json      ← Auto-created on first run; stores all your course data
└── README.md         ← This file
```

**What each file does:**

`app.py` contains everything: the Flask app setup, helper functions for reading/writing the JSON file, and all the API route handlers. It's intentionally kept in one file to make it easier to follow as a beginner.

`courses.json` is created automatically the first time you run the app. You don't need to create it yourself. It will look something like this after you add a course:

```json
{
    "courses": [
        {
            "id": 1,
            "name": "Python Basics",
            "description": "Learn Python from scratch",
            "status": "In Progress",
            "created_at": "2024-01-15T10:30:00"
        }
    ],
    "next_id": 2
}
```

---

## Installation

Follow these steps carefully. Each one builds on the last.

### Step 1 — Make sure Python is installed

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
python --version
```

You should see something like `Python 3.8.0` or higher. If you get an error, download Python from [python.org](https://www.python.org/downloads/).

### Step 2 — Download the project

If you have Git installed:

```bash
git clone https://github.com/your-username/codecrafthub.git
cd codecrafthub
```

Or download the ZIP file from GitHub and unzip it, then open your terminal inside that folder.

### Step 3 — Create a virtual environment

A virtual environment keeps this project's dependencies separate from other Python projects on your computer. Think of it as a clean, isolated workspace.

**On Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

When the virtual environment is active, you'll see `(venv)` at the start of your terminal prompt. That means you're in the right place.

### Step 4 — Install dependencies

```bash
pip install flask
```

That's it! Flask is the only dependency this project needs.

### Step 5 — Verify the installation

```bash
python -c "import flask; print('Flask version:', flask.__version__)"
```

If you see a version number printed, you're all set.

---

## Running the Application

Make sure your virtual environment is active (you should see `(venv)` in your prompt), then run:

```bash
python app.py
```

You should see output like this:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

The API is now running on your computer at `http://127.0.0.1:5000`. This address only works on your machine — it's not accessible from the internet.

To stop the server at any time, press `Ctrl + C` in your terminal.

> **What is `127.0.0.1:5000`?**
> `127.0.0.1` is your computer's "loopback" address — it means "this machine". `5000` is the port number the server is listening on. Together, they form the base URL for all your API requests.

---

## API Endpoints

An **endpoint** is a URL that your API responds to. Each endpoint handles a specific action.

### Quick Reference

| Method | URL | Action |
|--------|-----|--------|
| GET | `/` | Welcome message & endpoint list |
| GET | `/api/courses` | Get all courses |
| POST | `/api/courses` | Create a new course |
| GET | `/api/courses/<id>` | Get one course by ID |
| PUT | `/api/courses/<id>` | Update a course by ID |
| DELETE | `/api/courses/<id>` | Delete a course by ID |

Replace `<id>` with an actual number, like `/api/courses/1`.

---

### GET `/`

Returns a welcome message and a list of all available endpoints. Good for checking that the server is running.

**Request:**
```
GET http://127.0.0.1:5000/
```

**Response (200 OK):**
```json
{
    "message": "Welcome to CodeCraftHub API",
    "version": "1.0",
    "endpoints": {
        "GET /": "This welcome message",
        "GET /api/courses": "Get all courses",
        ...
    }
}
```

---

### GET `/api/courses`

Returns a list of all courses currently stored.

**Request:**
```
GET http://127.0.0.1:5000/api/courses
```

**Response (200 OK):**
```json
{
    "total": 2,
    "courses": [
        {
            "id": 1,
            "name": "Python Basics",
            "description": "Learn Python from scratch",
            "status": "In Progress",
            "created_at": "2024-01-15T10:30:00"
        },
        {
            "id": 2,
            "name": "Flask Web Development",
            "description": "Build APIs with Flask",
            "status": "Not Started",
            "created_at": "2024-01-16T09:00:00"
        }
    ]
}
```

---

### POST `/api/courses`

Creates a new course. You must send JSON data in the request body.

**Required field:** `name`

**Optional fields:** `description` (defaults to `""`), `status` (defaults to `"Not Started"`)

**Valid status values:** `Not Started`, `In Progress`, `Completed`

**Request:**
```
POST http://127.0.0.1:5000/api/courses
Content-Type: application/json

{
    "name": "JavaScript Fundamentals",
    "description": "Learn the basics of JS",
    "status": "Not Started"
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "name": "JavaScript Fundamentals",
    "description": "Learn the basics of JS",
    "status": "Not Started",
    "created_at": "2024-01-17T14:22:00"
}
```

**Error — missing name (400 Bad Request):**
```json
{
    "error": "Course name is required"
}
```

**Error — invalid status (400 Bad Request):**
```json
{
    "error": "Status must be one of: ['Not Started', 'In Progress', 'Completed']"
}
```

---

### GET `/api/courses/<id>`

Returns a single course by its numeric ID.

**Request:**
```
GET http://127.0.0.1:5000/api/courses/1
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python from scratch",
    "status": "In Progress",
    "created_at": "2024-01-15T10:30:00"
}
```

**Error — not found (404 Not Found):**
```json
{
    "error": "Course not found"
}
```

---

### PUT `/api/courses/<id>`

Updates one or more fields of an existing course. You only need to include the fields you want to change.

**Request:**
```
PUT http://127.0.0.1:5000/api/courses/1
Content-Type: application/json

{
    "status": "Completed"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python from scratch",
    "status": "Completed",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-20T16:45:00"
}
```

---

### DELETE `/api/courses/<id>`

Permanently deletes a course by its ID.

**Request:**
```
DELETE http://127.0.0.1:5000/api/courses/1
```

**Response (200 OK):**
```json
{
    "message": "Course deleted",
    "course": {
        "id": 1,
        "name": "Python Basics",
        ...
    }
}
```

---

## Testing the API

You need a way to send HTTP requests to your API. Here are three options, from easiest to most flexible.

### Option 1 — Postman (Recommended for beginners)

Postman is a free desktop app with a visual interface — no coding required to send requests.

1. Download Postman from [postman.com](https://www.postman.com/downloads/)
2. Open it and click **New Request**
3. Select the HTTP method (GET, POST, etc.) from the dropdown
4. Enter the URL, e.g. `http://127.0.0.1:5000/api/courses`
5. For POST/PUT requests: click the **Body** tab → select **raw** → choose **JSON** from the dropdown → paste your JSON
6. Click **Send**

### Option 2 — curl (Terminal)

`curl` is a command-line tool that comes pre-installed on Mac and Linux. On Windows, it's available in PowerShell.

**Get all courses:**
```bash
curl http://127.0.0.1:5000/api/courses
```

**Create a course:**
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Docker for Beginners", "status": "Not Started"}'
```

**Update a course:**
```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

**Delete a course:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

### Option 3 — Browser (GET requests only)

Your browser can only send GET requests, but that's enough to read data. While the server is running, just visit:

```
http://127.0.0.1:5000/
http://127.0.0.1:5000/api/courses
http://127.0.0.1:5000/api/courses/1
```

---

## Troubleshooting

### "Address already in use" error

This means port 5000 is already being used by another process (maybe a previous run of the app that didn't shut down cleanly).

**Fix:** Find and stop the process using port 5000.

On Mac/Linux:
```bash
lsof -i :5000
kill -9 <PID>   # Replace <PID> with the number shown
```

On Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Or simply change the port in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 instead
```

---

### "ModuleNotFoundError: No module named 'flask'"

Flask isn't installed in your current environment.

**Fix:** Make sure your virtual environment is active, then install Flask:
```bash
# Activate virtual environment first:
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# Then install:
pip install flask
```

---

### "Connection refused" when making requests

The server isn't running, or you're using the wrong URL.

**Fix checklist:**
- Make sure `python app.py` is running in your terminal
- Check the URL starts with `http://` not `https://`
- Make sure you're using port `5000` (or whichever port you configured)
- Confirm the terminal shows `Running on http://127.0.0.1:5000`

---

### JSON file looks broken or contains invalid data

If `courses.json` gets corrupted (e.g. from a crash mid-write), the app will return an empty course list.

**Fix:** Delete the file and let the app recreate it:
```bash
rm courses.json     # Mac/Linux
del courses.json    # Windows
```

> ⚠️ This will erase all your saved courses.

---

### "405 Method Not Allowed"

You're using the wrong HTTP method for that endpoint. For example, sending a GET request to a POST-only endpoint.

**Fix:** Check the [Quick Reference table](#quick-reference) above to confirm which methods each endpoint supports.

---

### Changes not saving after update/delete

This usually means the app doesn't have permission to write to the folder.

**Fix:** Make sure you're running the app from inside the project folder, and that your user account has write permissions to that folder.

---

## Next Steps

Once you're comfortable with this project, here are some ideas to extend it:

- Add a `category` field to courses (e.g. "Programming", "Design")
- Add filtering — e.g. `GET /api/courses?status=In Progress`
- Replace the JSON file with a real database using SQLite and SQLAlchemy
- Add user authentication so each user has their own course list
- Build a simple frontend with HTML/JavaScript that calls this API

---

*Built for learning. Happy coding! 🚀*