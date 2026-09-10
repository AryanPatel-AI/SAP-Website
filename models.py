import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(30), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer') # 'customer' or 'studio'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    studios = db.relationship('Studio', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

class Studio(db.Model):
    __tablename__ = 'studios'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(80), nullable=True, default='Mumbai')
    category = db.Column(db.String(80), nullable=True, default='Fashion') # Fashion, Cinema, Cyclorama, Loft, Product, Portrait
    price_per_hour = db.Column(db.Float, nullable=False, default=2000.0) # In Indian Rupees (INR)
    cover_image = db.Column(db.String(255), nullable=True)
    amenities = db.Column(db.String(255), nullable=True) # e.g. "Air Conditioned, Makeup Station, 4K Monitors"
    contact_phone = db.Column(db.String(30), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolios = db.relationship('Portfolio', backref='studio', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='studio', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='studio', lazy=True, cascade='all, delete-orphan')

    @property
    def display_phone(self):
        return self.contact_phone or (self.owner.phone if self.owner else "+91 94120 00000")

    @property
    def display_email(self):
        return self.contact_email or (self.owner.email if self.owner else "host@studioza.in")

    @property
    def average_rating(self):
        if not self.reviews:
            return 4.9 # Default showcase rating
        total = sum(r.rating for r in self.reviews)
        return round(total / len(self.reviews), 1)

    @property
    def review_count(self):
        return len(self.reviews)

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(80), nullable=True)
    hashtags = db.Column(db.String(255), nullable=True)
    details = db.Column(db.Text, nullable=True)
    improvement_tips = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.String(50), nullable=False)
    hours = db.Column(db.Integer, nullable=False, default=4)
    total_amount = db.Column(db.Float, nullable=False, default=8000.0) # In INR (₹)
    status = db.Column(db.String(30), nullable=False, default='pending') # pending, confirmed, rejected, completed
    payment_status = db.Column(db.String(30), nullable=False, default='unpaid') # unpaid, deposit_paid, paid
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5) # 1 to 5
    review_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
