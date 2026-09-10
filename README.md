---
title: SAP Website
emoji: 🐠
colorFrom: red
colorTo: green
sdk: docker
pinned: false
---

# SAP-Website: Photography & Studio Booking Platform

SAP-Website is a comprehensive, full-stack photography gallery and studio booking web application. It is designed to connect photographers/customers with professional studios. The platform enables users to discover studios, view portfolios, make bookings, and leave reviews. It also provides studio owners with a dedicated dashboard to manage their portfolios and booking requests.

## 🚀 Features

- **Role-Based Authentication:** 
  - **Customers:** Can browse studios, book sessions, and leave reviews.
  - **Studios (Hosts):** Have a dedicated dashboard to manage their studio profile, upload portfolios, and approve/manage bookings.
- **Studio Discovery & Filtering:** Live search and filtering of studios based on categories (e.g., Fashion, Cinema, Cyclorama, Loft, Product, Portrait) and locations.
- **Booking Management:** Integrated booking system allowing customers to request hours and studios to confirm or reject them.
- **Portfolio & Gallery:** Studios can upload portfolio images. 
- **AI & Utility Integrations:**
  - `ai_tags.py`: AI-powered image analysis and auto-tagging.
  - `chat_bot.py`: Integrated chatbot for user assistance.
  - `exif_reader.py`: Extracts EXIF metadata from uploaded photography.
  - `notifications.py`: Handles booking request and status update notifications.
- **Reviews & Ratings:** Customers can rate and review studios they've booked, contributing to an aggregated average rating for each studio.

## 🛠️ Technology Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite (default for local development) with SQLAlchemy ORM. Configurable to use PostgreSQL via `DATABASE_URL` for production.
- **Frontend:** HTML5, CSS3, Jinja2 Templates (`templates/`)
- **Authentication:** Werkzeug security (password hashing) and Flask Sessions.

## 📂 Project Structure

```text
├── app.py                 # Main Flask application and route definitions
├── models.py              # SQLAlchemy Database Models (User, Studio, Portfolio, Booking, Review)
├── init_db.py             # Script to initialize the database
├── update_db.py           # Script for database migrations/updates
├── database.db            # SQLite database (generated locally)
├── static/
│   ├── image/             # Static assets and default images
│   └── uploads/           # User-uploaded portfolio images
├── templates/             # Jinja2 HTML Templates (Dashboards, Auth, Hub, etc.)
└── utils/                 # Helper scripts and AI integrations
    ├── ai_tags.py         # AI image analysis logic
    ├── chat_bot.py        # Chatbot integration
    ├── exif_reader.py     # EXIF metadata extraction
    └── notifications.py   # Booking and status notifications
```

## 🗄️ Database Schema

- **Users:** Stores authentication credentials, roles (`customer` or `studio`), and basic info.
- **Studios:** Linked to a User. Contains studio details, pricing, location, category, and amenities.
- **Portfolios:** Linked to a Studio. Stores image URLs, captions, categories, hashtags, and AI-generated improvement tips.
- **Bookings:** Tracks booking requests between Users (Customers) and Studios, including dates, hours, amounts, and statuses (pending, confirmed, etc.).
- **Reviews:** Stores ratings and text reviews left by customers for studios.

## 💻 Local Setup & Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AryanPatel-AI/SAP-Website.git
   cd SAP-Website
   ```

2. **Activate Virtual Environment:**
   *(A `venv/` is provided, but you can create your own)*
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   Ensure you have Flask, Flask-SQLAlchemy, and Werkzeug installed. 
   *(Note: You may need to create a `requirements.txt` if not present)*
   ```bash
   pip install Flask Flask-SQLAlchemy Werkzeug
   ```

4. **Initialize Database:**
   ```bash
   python init_db.py
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```
   The app will run by default on `http://localhost:5002` (or the port specified in your environment variables).

## 🤖 AI Agent & LLM Context (ChatGPT / Claude / Gemini)

If an AI is reading this to assist with development:
- **Backend changes:** Primarily involve `app.py` and `models.py`.
- **Database changes:** If `models.py` is modified, you may need to update the SQLite schema manually or use `update_db.py`, as Flask-Migrate is not strictly configured.
- **Frontend changes:** Use standard Jinja2 templating syntax within the `templates/` directory. Be aware of existing styling patterns in `base.html`.
- **Do not use Node.js commands** (e.g., `npm run dev`) as this is purely a Python/Flask application.

---
*Check out the Hugging Face configuration reference at https://huggingface.co/docs/hub/spaces-config-reference*
