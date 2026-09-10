---

title: SAP Website
emoji: 🐠
colorFrom: red
colorTo: green
sdk: docker
pinned: false
-------------

# SAP-Website: Photography & Studio Booking Platform

**SAP-Website** is a full-stack photography gallery and studio booking platform designed to connect customers with professional photography studios.

The platform allows users to discover studios, explore portfolios, check studio information, request bookings, and leave reviews. Studio owners have their own dashboard where they can manage their studio profile, portfolio, and booking requests.

> 🚧 **Project Status: Active Development**
>
> SAP-Website is currently being actively developed and improved. Features, UI, database structure, and integrations may continue to change as the project evolves.

---

## 🚀 Features

### 👤 Role-Based Authentication

The platform supports different types of users.

#### Customers

Customers can:

* Create an account
* Browse photography studios
* Search and filter studios
* View studio portfolios
* Request studio bookings
* Track booking status
* Leave reviews and ratings

#### Studios / Hosts

Studio owners can:

* Create and manage their studio profile
* Add studio information
* Set pricing
* Upload portfolio images
* Manage portfolio content
* View booking requests
* Approve or reject bookings
* Manage their studio presence

---

## 🔎 Studio Discovery & Filtering

Users can discover studios using:

* Search
* Location
* Studio category
* Pricing
* Amenities
* Photography type

Supported studio categories include:

* Fashion
* Cinema
* Cyclorama
* Loft
* Product
* Portrait
* And more

---

## 📅 Booking Management

The platform provides an integrated booking system between customers and studios.

### Booking Flow

```text
Customer
   ↓
Select Studio
   ↓
Choose Date & Hours
   ↓
Submit Booking Request
   ↓
Studio Receives Request
   ↓
Approve / Reject
   ↓
Booking Status Updated
```

Booking records include:

* Customer
* Studio
* Booking date
* Number of hours
* Amount
* Booking status
* Request information

Possible booking statuses include:

```text
Pending
Confirmed
Rejected
Cancelled
Completed
```

---

## 📸 Portfolio & Gallery

Studio owners can showcase their photography work through their portfolio.

Portfolio features include:

* Image uploads
* Captions
* Categories
* Hashtags
* Studio-specific galleries
* AI-generated image insights
* Portfolio management

---

## 🤖 AI & Utility Integrations

SAP-Website includes several AI and utility features.

### AI Image Tagging

`utils/ai_tags.py`

Provides AI-powered image analysis and automatic tagging for uploaded photography.

### AI Chatbot

`utils/chat_bot.py`

Provides an integrated chatbot to assist users with questions and platform-related interactions.

### EXIF Metadata

`utils/exif_reader.py`

Extracts metadata from uploaded photography files, such as available camera and image information.

### Notifications

`utils/notifications.py`

Handles notifications related to:

* Booking requests
* Booking approvals
* Booking rejections
* Booking status updates

---

## ⭐ Reviews & Ratings

Customers can review studios they have booked.

Reviews include:

* Rating
* Review text
* Customer information
* Studio association

Studio ratings are aggregated to provide an overall rating for each studio.

---

# 🛠️ Technology Stack

| Layer          | Technology                   |
| -------------- | ---------------------------- |
| Backend        | Python 3, Flask              |
| Database       | SQLite / PostgreSQL          |
| ORM            | SQLAlchemy                   |
| Frontend       | HTML5, CSS3, Jinja2          |
| Authentication | Flask Sessions + Werkzeug    |
| AI             | Python-based AI integrations |
| Deployment     | Docker / Hugging Face Spaces |

### Database

SQLite is used by default for local development.

For production, the application can be configured to use PostgreSQL through:

```text
DATABASE_URL
```

---

# 📂 Project Structure

```text
SAP-Website/
│
├── app.py                    # Main Flask application
├── models.py                 # SQLAlchemy database models
├── init_db.py                # Database initialization
├── update_db.py              # Database updates / migrations
├── database.db               # Local SQLite database
│
├── static/
│   ├── image/                # Static images and assets
│   └── uploads/              # Uploaded portfolio images
│
├── templates/                # Jinja2 templates
│   ├── base.html
│   ├── auth/
│   ├── dashboards/
│   └── ...
│
├── utils/
│   ├── ai_tags.py            # AI image analysis and tagging
│   ├── chat_bot.py           # AI chatbot
│   ├── exif_reader.py        # EXIF metadata extraction
│   └── notifications.py     # Notification utilities
│
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
└── README.md
```

---

# 🗄️ Database Schema

The application uses SQLAlchemy ORM for database management.

### Users

Stores:

* Authentication credentials
* User role
* Basic user information

Supported roles:

```text
customer
studio
```

### Studios

Stores:

* Studio information
* Owner
* Pricing
* Location
* Category
* Amenities
* Description

### Portfolios

Stores:

* Studio association
* Image URLs
* Captions
* Categories
* Hashtags
* AI-generated information

### Bookings

Stores:

* Customer
* Studio
* Date
* Hours
* Amount
* Status
* Booking information

### Reviews

Stores:

* Customer
* Studio
* Rating
* Review text
* Review information

---

# 💻 Local Setup & Development

## 1. Clone the Repository

```bash
git clone https://github.com/AryanPatel-AI/SAP-Website.git

cd SAP-Website
```

## 2. Create a Virtual Environment

You can create your own Python virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```powershell
venv\Scripts\activate
```

## 3. Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Otherwise:

```bash
pip install Flask Flask-SQLAlchemy Werkzeug
```

Additional dependencies may be required for AI, image processing, EXIF extraction, and other integrations.

## 4. Configure Environment Variables

Create a `.env` file if required by the application.

Example:

```env
DATABASE_URL=sqlite:///database.db
SECRET_KEY=your-secret-key
```

For production PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@host:port/database
```

> Do not commit real secrets, API keys, passwords, or production credentials to GitHub.

## 5. Initialize the Database

```bash
python init_db.py
```

If database updates are required:

```bash
python update_db.py
```

## 6. Run the Application

```bash
python app.py
```

The application will normally be available at:

```text
http://localhost:5002
```

The port can be changed through the application's configuration/environment variables.

---

# 🐳 Docker

SAP-Website also includes Docker support.

Build the Docker image:

```bash
docker build -t sap-website .
```

Run the container:

```bash
docker run -p 5002:5002 sap-website
```

For production deployment, configure the required environment variables and database connection appropriately.

---

# 🤖 AI Agent / LLM Development Context

If an AI coding assistant such as ChatGPT, Claude, or Gemini is helping develop this project, the following conventions should be followed.

### Backend

The primary backend logic is located in:

```text
app.py
models.py
```

Before modifying routes or database functionality, inspect the existing implementation and follow the established patterns.

### Database

Database models are defined in:

```text
models.py
```

When modifying models, check whether the existing database requires an update or migration.

Relevant scripts:

```text
init_db.py
update_db.py
```

### Frontend

Frontend templates are located in:

```text
templates/
```

The project uses **Jinja2** templates.

Before creating new pages, inspect:

```text
templates/base.html
```

and follow the existing layout and styling conventions.

### Static Files

Static assets are located in:

```text
static/
```

Uploaded portfolio images are stored under:

```text
static/uploads/
```

### Important

This application is a **Python/Flask application**.

Do not use Node.js development commands such as:

```bash
npm run dev
```

unless a future part of the project explicitly introduces a Node.js frontend/build system.

---

# 🚧 Roadmap

### Core Platform

* [x] Flask application
* [x] User authentication
* [x] Customer accounts
* [x] Studio accounts
* [x] Studio discovery
* [x] Studio filtering
* [x] Portfolio management
* [x] Booking system
* [x] Reviews & ratings
* [x] AI utilities
* [x] Chatbot integration
* [x] EXIF extraction
* [x] Notifications

### In Development

* [ ] Improved studio discovery
* [ ] Advanced booking management
* [ ] Better portfolio management
* [ ] Improved AI image analysis
* [ ] AI-powered recommendations
* [ ] Advanced studio dashboard
* [ ] Customer dashboard improvements
* [ ] PostgreSQL production configuration
* [ ] Improved notification system
* [ ] Production optimization

### Future

* [ ] Online payments
* [ ] Advanced availability calendar
* [ ] Private client galleries
* [ ] High-resolution photo delivery
* [ ] Photographer profiles
* [ ] Advanced analytics
* [ ] Mobile application
* [ ] Advanced AI photography tools

---

# 🔐 Security

For production deployment, make sure to:

* Use strong secret keys
* Store secrets in environment variables
* Never commit API keys
* Never commit database credentials
* Use HTTPS
* Configure secure sessions
* Validate uploaded files
* Restrict upload sizes
* Use PostgreSQL for production
* Keep dependencies updated

---

# 📌 Project Status

**🟢 Active Development**

SAP-Website is currently a working project and is actively being developed.

The core platform is functional, while additional features, improvements, integrations, and production optimizations are being added continuously.

The architecture and APIs may change during development.

---

# 👨‍💻 Developer

**Aryan Patel**

Designed, developed, and maintained by **Aryan Patel**.

---

# 📄 License

This project is currently under active development.

License information will be added upon public release.

Until an official license is provided, all rights are reserved by the author.

**Copyright © 2026 Aryan Patel.**

---

## 🌐 Project

**GitHub:** `AryanPatel-AI/SAP-Website`

**Status:** 🟢 Active Development

> Building a modern photography and studio booking experience with Flask, AI, and a focus on scalable studio management.
