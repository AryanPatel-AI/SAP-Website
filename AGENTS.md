# SAP Website Project Context

## Overview
This is a photo gallery / photo sharing web application built using Python and Flask. It uses a SQLite database (`database.db`) to store photo metadata (title, path, likes, category).

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite (`database.db`)
- **Frontend:** HTML templates (in `templates/`) and static assets (in `static/`)
- **Authentication:** Simple session-based admin login.
- **Environment:** There is a virtual environment available in the `venv/` directory.

## Project Structure
- `app.py`: The main Flask application containing all routes (home, upload, admin, login, like, view_photo, etc.).
- `database.db`: The SQLite database.
- `static/image/`: Directory where uploaded photos are stored.
- `templates/`: HTML templates for the UI.
- `utils/`: Contains utility scripts (`exif_reader.py` for reading image metadata, and `ai_tags.py` for optional AI caption generation).

## How to Run the App
**Important Note:** This is a Python project, not a Node.js project. Do NOT use `npm start`. 

To run the application locally:
1. Activate the virtual environment (if needed).
2. Run the Python script:
   ```bash
   python app.py
   ```
   *Note: If you need to use the provided virtual environment directly, run `./venv/bin/python app.py`.*
3. The application will start and listen on port `5002` by default (configurable via the `PORT` environment variable).

## Common Tasks for Agents
- When making backend changes, look at `app.py`.
- Database schema changes might require updating SQLite queries in `app.py`.
- If the user attempts Node.js commands (like `npm install` or `npm start`), gently remind them that this is a Flask application.
