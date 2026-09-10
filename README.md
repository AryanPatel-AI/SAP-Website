---
title: SAP Website
emoji: "🐠"
colorFrom: red
colorTo: green
sdk: docker
pinned: false
---

# 📸 SAP Website — Photography & Studio Booking Platform

A full-stack photography gallery and professional studio booking platform that connects **photographers, creators, customers, and studio owners** in one place.

Users can discover studios, explore photography portfolios, request bookings, leave reviews, and interact with an AI-powered assistant. Studio owners can manage their studio profiles, portfolios, and booking requests through the platform.

> 🚧 **Status:** Active Development

---

## ✨ Features

### 🔐 Role-Based Authentication

The platform supports different user roles with dedicated functionality.

#### 👤 Customers

* Create an account and log in securely
* Browse available studios
* Search and filter studios
* View studio details and portfolios
* Submit booking requests
* Track booking status
* Leave ratings and reviews
* Interact with the AI chatbot

#### 🏢 Studio Owners / Hosts

* Create and manage studio profiles
* Upload studio portfolio images
* Manage studio information
* View incoming booking requests
* Approve or reject booking requests
* Manage existing bookings
* Maintain their studio presence on the platform

---

## 🏢 Studio Discovery

Users can discover studios based on different categories and locations.

### Studio Categories

* 👗 Fashion
* 🎬 Cinema
* 🔵 Cyclorama
* 🏠 Loft
* 📦 Product
* 👤 Portrait

Users can browse studio information including:

* Studio name
* Location
* Description
* Pricing
* Category
* Portfolio images
* Ratings and reviews
* Availability

---

## 📅 Studio Booking System

The platform provides a booking-request workflow between customers and studio owners.

### Booking Flow

```text
Customer
   │
   ▼
Browse Studios
   │
   ▼
Select Studio
   │
   ▼
Choose Date & Hours
   │
   ▼
Submit Booking Request
   │
   ▼
Studio Owner
   │
   ├── Approve
   │
   └── Reject
   │
   ▼
Booking Status Updated
```

### Booking Features

* Hour-based booking requests
* Date selection
* Booking duration
* Booking status tracking
* Studio approval/rejection
* Booking notifications
* Customer booking history

---

## 🖼️ Photography Portfolio

Studio owners can showcase their work through image portfolios.

Portfolio functionality includes:

* Image uploads
* Studio-specific galleries
* Photography showcases
* Portfolio management
* Image metadata processing

Uploaded images can also be processed by the application's utility tools.

---

# 🤖 AI & Utility Features

The project includes several AI and utility components.

### 🏷️ AI Image Tagging

Located at:

```text
utils/ai_tags.py
```

This module analyzes uploaded images and generates relevant tags.

Possible use cases include:

* Automatic image categorization
* Photography style detection
* Search optimization
* Portfolio organization

---

### 💬 AI Chatbot

Located at:

```text
utils/chat_bot.py
```

The chatbot provides an interactive assistant for users.

It can be used for:

* Studio discovery assistance
* General platform questions
* Booking-related guidance
* User assistance

---

### 📷 EXIF Metadata Reader

Located at:

```text
utils/exif_reader.py
```

The EXIF utility extracts metadata from uploaded photographs.

Depending on the image, metadata can include:

* Camera information
* Lens information
* Image dimensions
* Capture date
* Photography metadata

---

### 🔔 Notifications

Located at:

```text
utils/notifications.py
```

The notification system can be used for events such as:

* New booking requests
* Booking approvals
* Booking rejections
* Booking status updates
* Other platform notifications

---

# ⭐ Reviews & Ratings

Customers can leave reviews after using a studio.

The review system supports:

* ⭐ Star ratings
* Written reviews
* Studio-specific reviews
* Review display
* Average studio ratings

This helps customers evaluate studios before making a booking.

---

# 🛠️ Tech Stack

## Backend

* 🐍 Python 3
* 🌐 Flask
* 🗄️ Flask-SQLAlchemy
* 🔐 Werkzeug
* 🔑 Flask Sessions

## Frontend

* HTML5
* CSS3
* Jinja2 Templates
* JavaScript

## Database

### Development

```text
SQLite
```

### Production

```text
PostgreSQL
```

The production database can be configured using:

```text
DATABASE_URL
```

## AI / Utilities

* AI image analysis
* Automatic image tagging
* Chatbot
* EXIF metadata extraction
* Notification utilities

## Deployment

* Docker
* Flask
* PostgreSQL

---

# 📁 Project Structure

```text
SAP-Website/
│
├── app.py
├── models.py
├── init_db.py
├── update_db.py
├── database.db
│
├── static/
│   ├── image/
│   └── uploads/
│
├── templates/
│
├── utils/
│   ├── ai_tags.py
│   ├── chat_bot.py
│   ├── exif_reader.py
│   └── notifications.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 🗄️ Database Schema

The application uses SQLAlchemy ORM for database management.

## Users

Stores registered platform users.

```text
Users
├── id
├── name
├── email
├── password
└── role
```

Roles may include:

```text
customer
studio
```

---

## Studios

Stores professional studio information.

```text
Studios
├── id
├── owner_id
├── name
├── location
├── category
├── description
├── price
└── availability
```

---

## Portfolios

Stores studio photography portfolio content.

```text
Portfolios
├── id
├── studio_id
├── image
├── title
└── description
```

---

## Bookings

Stores customer booking requests.

```text
Bookings
├── id
├── user_id
├── studio_id
├── date
├── start_time
├── end_time
└── status
```

Booking statuses may include:

```text
pending
approved
rejected
completed
cancelled
```

---

## Reviews

Stores customer feedback.

```text
Reviews
├── id
├── user_id
├── studio_id
├── rating
├── comment
└── created_at
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/AryanPatel-AI/SAP-Website.git
```

```bash
cd SAP-Website
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

Or install the main dependencies manually:

```bash
pip install Flask Flask-SQLAlchemy Werkzeug
```

---

# 🗄️ Database Setup

Initialize the database:

```bash
python init_db.py
```

If database updates are required:

```bash
python update_db.py
```

The default development database is:

```text
database.db
```

---

# ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5002
```

or:

```text
http://localhost:5002
```

---

# 🐳 Docker

The project can also be deployed using Docker.

Build the image:

```bash
docker build -t sap-website .
```

Run the container:

```bash
docker run -p 5002:5002 sap-website
```

The application can then be accessed at:

```text
http://localhost:5002
```

---

# 🔑 Environment Variables

For production deployments, configure environment variables as required.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/sap_website
SECRET_KEY=your-secret-key
```

Additional AI or external-service credentials can be configured through environment variables when required by the corresponding utility modules.

> ⚠️ Never commit API keys, passwords, secret keys, or production database credentials to Git.

---

# 🤖 AI Agent Development Context

This project is a **Python + Flask application**.

When making backend changes:

```text
app.py
models.py
utils/
```

When changing database models:

```text
models.py
update_db.py
init_db.py
```

When changing the frontend:

```text
templates/
static/
```

### Important

This project does **not** use Node.js as its primary backend runtime.

Do not use commands such as:

```bash
npm install
npm run dev
pnpm install
```

unless a future frontend/build system explicitly introduces Node.js dependencies.

The main application is started with:

```bash
python app.py
```

---

# 🔒 Security

The project uses Flask and Werkzeug security features for authentication and password handling.

Recommended production practices include:

* Use strong secret keys
* Hash passwords securely
* Validate uploaded files
* Restrict upload file types
* Protect authenticated routes
* Use environment variables for secrets
* Enable HTTPS in production
* Use PostgreSQL for production deployments
* Implement appropriate authorization checks
* Avoid exposing sensitive EXIF metadata
* Never commit credentials to Git

---

# 🧪 Development

For local development:

```bash
python app.py
```

After modifying database models, update the database using the appropriate database initialization or migration workflow.

Keep uploaded media inside the configured upload directory:

```text
static/uploads/
```

---

# 🗺️ Roadmap

Future improvements may include:

* [ ] Advanced studio search
* [ ] Availability calendar
* [ ] Real-time booking availability
* [ ] Online payments
* [ ] Photographer profiles
* [ ] Advanced AI image tagging
* [ ] AI-powered studio recommendations
* [ ] Improved chatbot
* [ ] Email notifications
* [ ] SMS notifications
* [ ] Real-time notifications
* [ ] Studio analytics dashboard
* [ ] Admin dashboard
* [ ] PostgreSQL production optimization
* [ ] Cloud image storage
* [ ] Image moderation
* [ ] Mobile application
* [ ] Advanced review moderation

---

# 📊 Project Status

🟢 **Active Development**

The project is continuously being improved with new booking, photography, AI, and studio-management features.

---

# 👨‍💻 Developer

**Aryan Patel**

SAP Website is designed, developed, and maintained by **Aryan Patel**.

---

# 📄 License

This project is currently under active development.

License information will be added upon public release.

Until an official license is provided, all rights are reserved by the author.

Copyright © 2026 **Aryan Patel**.

---

# ⭐ Contributing

The project is currently under active development.

Contribution guidelines will be added as the project approaches a public release.

---

# 📞 Contact

For questions, suggestions, or collaboration related to the project, please open an issue in the repository.

---

## 🚀 Built for Photographers & Creators

**SAP Website** aims to make it easier for photographers, creators, customers, and studio owners to discover, showcase, and book professional photography spaces.
