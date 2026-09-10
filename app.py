import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_, func

# Local imports
from models import db, User, Studio, Portfolio, Booking, Review
from utils.notifications import (
    send_booking_requested_notification,
    send_booking_status_notification
)

try:
    from utils.ai_tags import analyze_image
    from utils.chat_bot import get_chat_response
except ImportError:
    analyze_image = None
    get_chat_response = None

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-booking-key")

# Database configuration: PostgreSQL via DATABASE_URL or SQLite fallback
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    db_path = os.path.abspath("database.db")
    DATABASE_URL = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Production Connection Pooling for PostgreSQL concurrency
if DATABASE_URL.startswith("postgresql"):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

db.init_app(app)

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- AUTH DECORATORS ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def studio_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'studio':
            flash("Studio host access required.", "error")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route("/")
def index():
    return render_template("front_page.html")

@app.route("/home")
def home():
    trending_studios = Studio.query.order_by(Studio.id.desc()).limit(6).all()
    return render_template("main_hub.html", studios=trending_studios)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        flash(f"Thank you {name}! Your inquiry has been received. Our studio concierge will contact you shortly.", "success")
        return redirect(url_for('contact'))
    return render_template("contact.html")

# --- AUTHENTICATION ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        role = request.form.get("role")  # 'customer' or 'studio'
        
        if role not in ['customer', 'studio']:
            role = 'customer'
            
        # Check existing user
        if User.query.filter(or_(User.email == email, User.phone == phone)).first():
            flash("Email or phone number already registered.", "error")
            return render_template("register.html")
            
        hashed_pw = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=hashed_pw,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        
        # If studio, automatically provision their profile
        if role == 'studio':
            new_studio = Studio(
                user_id=new_user.id,
                name=f"{name}'s Studio",
                description="Welcome to our creative photography and film production space.",
                location="Mumbai, Maharashtra",
                city="Mumbai",
                category="Fashion",
                price_per_hour=2500.0,
                cover_image="/static/image/studio_stage_cinema.jpg"
            )
            db.session.add(new_studio)
            db.session.commit()
            
        flash("Registration successful! Please sign in.", "success")
        return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("login_id") # email or phone
        password = request.form.get("password")
        
        user = User.query.filter(or_(User.email == login_id, User.phone == login_id)).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['name'] = user.name
            session['role'] = user.role
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "error")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

# --- DASHBOARDS ---

@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session['user_id']
    role = session['role']
    
    if role == 'studio':
        studio = Studio.query.filter_by(user_id=user_id).first()
        if not studio:
            flash("Studio profile not found.", "error")
            return redirect(url_for('home'))
            
        portfolios = Portfolio.query.filter_by(studio_id=studio.id).all()
        bookings = Booking.query.filter_by(studio_id=studio.id).order_by(Booking.id.desc()).all()
        reviews = Review.query.filter_by(studio_id=studio.id).order_by(Review.id.desc()).all()
        
        return render_template(
            "dashboard_studio.html", 
            studio=studio, 
            portfolios=portfolios, 
            bookings=bookings,
            reviews=reviews
        )
    else:
        # Customer Dashboard
        bookings = Booking.query.filter_by(customer_id=user_id).order_by(Booking.id.desc()).all()
        return render_template("dashboard_customer.html", bookings=bookings)

# --- STUDIO DISCOVERY & LIVE SQL SEARCH / FILTERING ---

@app.route("/studios")
def list_studios():
    q = request.args.get('q', '').strip()
    city = request.args.get('city', '').strip()
    category = request.args.get('category', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    sort = request.args.get('sort', 'newest')

    query = Studio.query

    # 1. Text Search (name, description, amenities, location)
    if q:
        search_fmt = f"%{q}%"
        query = query.filter(
            or_(
                Studio.name.ilike(search_fmt),
                Studio.description.ilike(search_fmt),
                Studio.location.ilike(search_fmt),
                Studio.amenities.ilike(search_fmt)
            )
        )

    # 2. City Filter
    if city and city.lower() != 'all':
        query = query.filter(Studio.city.ilike(f"%{city}%"))

    # 3. Category Filter
    if category and category.lower() != 'all':
        query = query.filter(Studio.category.ilike(f"%{category}%"))

    # 4. Price Range (in ₹ INR)
    if min_price is not None:
        query = query.filter(Studio.price_per_hour >= min_price)
    if max_price is not None and max_price > 0:
        query = query.filter(Studio.price_per_hour <= max_price)

    # 5. Sorting
    if sort == 'price_asc':
        query = query.order_by(Studio.price_per_hour.asc())
    elif sort == 'price_desc':
        query = query.order_by(Studio.price_per_hour.desc())
    else:
        query = query.order_by(Studio.id.desc())

    studios = query.all()

    # Filter by minimum rating if specified (computed property)
    if min_rating:
        studios = [s for s in studios if s.average_rating >= min_rating]

    # Available cities and categories for filter dropdowns
    available_cities = ["Bareilly", "Mumbai", "Bengaluru", "Delhi NCR", "Hyderabad", "Goa", "Pune"]
    available_categories = ["Fashion", "Wedding & Fashion", "Portrait", "Cinema", "Product", "Cyclorama", "Daylight Loft"]

    return render_template(
        "studios.html", 
        studios=studios,
        q=q,
        city=city,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        available_cities=available_cities,
        available_categories=available_categories
    )

@app.route("/api/studios/search")
def api_search_studios():
    """Live async search JSON endpoint for instant AJAX filtering"""
    q = request.args.get('q', '').strip()
    city = request.args.get('city', '').strip()
    category = request.args.get('category', '').strip()
    max_price = request.args.get('max_price', type=float)

    query = Studio.query
    if q:
        search_fmt = f"%{q}%"
        query = query.filter(or_(Studio.name.ilike(search_fmt), Studio.description.ilike(search_fmt)))
    if city and city.lower() != 'all':
        query = query.filter(Studio.city.ilike(f"%{city}%"))
    if category and category.lower() != 'all':
        query = query.filter(Studio.category.ilike(f"%{category}%"))
    if max_price:
        query = query.filter(Studio.price_per_hour <= max_price)

    studios = query.order_by(Studio.id.desc()).all()
    results = []
    for s in studios:
        results.append({
            "id": s.id,
            "name": s.name,
            "city": s.city,
            "category": s.category,
            "price_per_hour": s.price_per_hour,
            "cover_image": s.cover_image or url_for('static', filename='image/studio_stage_cinema.jpg'),
            "rating": s.average_rating,
            "reviews": s.review_count,
            "url": url_for('studio_detail', studio_id=s.id)
        })
    return jsonify({"count": len(results), "studios": results})

# --- STUDIO DETAIL, REVIEWS & BOOKINGS ---

@app.route("/studio/<int:studio_id>")
def studio_detail(studio_id):
    studio = Studio.query.get_or_404(studio_id)
    portfolios = Portfolio.query.filter_by(studio_id=studio_id).all()
    reviews = Review.query.filter_by(studio_id=studio_id).order_by(Review.id.desc()).all()
    return render_template(
        "studio_detail.html", 
        studio=studio, 
        portfolios=portfolios, 
        reviews=reviews
    )

@app.route("/studio/<int:studio_id>/review", methods=["POST"])
@login_required
def add_review(studio_id):
    studio = Studio.query.get_or_404(studio_id)
    rating = request.form.get("rating", type=int, default=5)
    review_text = request.form.get("review_text", "").strip()

    if not review_text:
        flash("Please write a short review before submitting.", "error")
        return redirect(url_for('studio_detail', studio_id=studio_id))

    rating = max(1, min(5, rating))
    new_review = Review(
        studio_id=studio_id,
        customer_id=session['user_id'],
        rating=rating,
        review_text=review_text
    )
    db.session.add(new_review)
    db.session.commit()

    flash(f"Thank you for rating {studio.name} {rating}★! Your review is live.", "success")
    return redirect(url_for('studio_detail', studio_id=studio_id))

@app.route("/book/<int:studio_id>", methods=["POST"])
@login_required
def book_studio(studio_id):
    if session.get('role') == 'studio':
        flash("Studio hosts cannot book other studios.", "error")
        return redirect(url_for('studio_detail', studio_id=studio_id))
        
    studio = Studio.query.get_or_404(studio_id)
    booking_date = request.form.get("booking_date")
    hours = request.form.get("hours", type=int, default=4)
    notes = request.form.get("notes", "")
    customer_id = session['user_id']
    customer = User.query.get(customer_id)

    total_amount = float(hours * studio.price_per_hour)
    
    booking = Booking(
        studio_id=studio_id,
        customer_id=customer_id,
        booking_date=booking_date,
        hours=hours,
        total_amount=total_amount,
        status="pending",
        payment_status="unpaid",
        notes=notes
    )
    db.session.add(booking)
    db.session.commit()

    # Trigger Email / SMS Notification to Studio Host
    host = studio.owner
    if host:
        send_booking_requested_notification(
            studio_owner_email=host.email,
            studio_owner_phone=host.phone,
            studio_name=studio.name,
            customer_name=customer.name,
            booking_date=booking_date,
            total_inr=total_amount
        )

    flash(f"Booking request for {studio.name} sent successfully! The studio host has been notified.", "success")
    return redirect(url_for('dashboard'))

@app.route("/update_booking/<int:booking_id>", methods=["POST"])
@studio_required
def update_booking(booking_id):
    status = request.form.get("status")
    if status in ['confirmed', 'rejected', 'completed']:
        booking = Booking.query.get_or_404(booking_id)
        booking.status = status
        db.session.commit()

        # Alert Customer
        customer = booking.customer
        if customer:
            send_booking_status_notification(
                customer_email=customer.email,
                customer_phone=customer.phone,
                studio_name=booking.studio.name,
                status=status,
                booking_date=booking.booking_date,
                total_inr=booking.total_amount
            )

        flash(f"Booking status updated to {status.capitalize()}.", "success")
    return redirect(url_for('dashboard'))

# --- PORTFOLIO UPLOADS & AI ---

@app.route("/upload_portfolio", methods=["POST"])
@studio_required
def upload_portfolio():
    file = request.files.get("photo")
    if not file or file.filename == "":
        flash("No photo file selected.", "error")
        return redirect(url_for('dashboard'))
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Run AI Analysis
    ai_data = {"category": "", "hashtags": "", "details": "", "improvement_tips": ""}
    if analyze_image:
        try:
            ai_data = analyze_image(filepath)
        except Exception as e:
            print(f"AI image analysis error: {e}")
        
    studio = Studio.query.filter_by(user_id=session['user_id']).first()
    
    new_portfolio = Portfolio(
        studio_id=studio.id,
        image_url=url_for('static', filename='uploads/' + filename),
        caption=(ai_data.get('details', '')[:60] + '...') if ai_data.get('details') else "Studio production shot",
        category=ai_data.get('category', 'Production'),
        hashtags=ai_data.get('hashtags', '#Studioza #Photography'),
        details=ai_data.get('details', ''),
        improvement_tips=ai_data.get('improvement_tips', '')
    )
    db.session.add(new_portfolio)
    db.session.commit()
    
    flash("Photo successfully uploaded and analyzed by AI!", "success")
    return redirect(url_for('dashboard'))

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"response": "I didn't receive a message."})
        
    if get_chat_response:
        ai_response = get_chat_response(messages)
    else:
        ai_response = "The AI concierge is currently standing by. Please explore our verified studios in ₹ INR."
        
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, port=port)