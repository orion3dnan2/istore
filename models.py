from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Full name instead of username
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Renamed from password_hash
    role = db.Column(db.String(20), default='customer')  # admin, customer, merchant
    language = db.Column(db.String(2), default='en')  # en or ar
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    repair_requests = db.relationship('RepairRequest', backref='user', lazy=True)
    sell_requests = db.relationship('SellRequest', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.name}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)  # English name
    name_ar = db.Column(db.String(100), nullable=False)  # Arabic name
    slug = db.Column(db.String(100), unique=True, nullable=False)  # For URL use
    is_active = db.Column(db.Boolean, default=True)  # Shown or hidden
    sort_order = db.Column(db.Integer, default=0)  # Order in lists
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    sell_requests = db.relationship('SellRequest', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name_en}>'

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(200), nullable=False)  # English name
    name_ar = db.Column(db.String(200), nullable=False)  # Arabic name
    description_en = db.Column(db.Text)  # English description
    description_ar = db.Column(db.Text)  # Arabic description
    brand = db.Column(db.String(100))  # e.g., Apple, Samsung
    condition = db.Column(db.String(20), default='new')  # new, used
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Final price
    stock_quantity = db.Column(db.Integer, default=0)  # How many in stock
    image_url = db.Column(db.String(500), default='https://via.placeholder.com/300x200?text=No+Image')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name_en}>'

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def get_total_price(self):
        return self.quantity * self.product.price
    
    def __repr__(self):
        return f'<CartItem {self.product.name_en} x{self.quantity}>'

class RepairRequest(db.Model):
    __tablename__ = 'repair_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # nullable
    device_type = db.Column(db.String(100), nullable=False)  # e.g., Laptop, Phone
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    issue_description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(500))  # Optional image
    contact_info = db.Column(db.String(200), nullable=False)  # Email or phone
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, done
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RepairRequest {self.device_type} - {self.status}>'

class SellRequest(db.Model):
    __tablename__ = 'sell_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # nullable
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    condition = db.Column(db.String(20), nullable=False)  # new, like-new, used
    expected_price = db.Column(db.Numeric(10, 2))
    photos_url = db.Column(db.Text)  # JSON array or comma-separated URLs
    contact_info = db.Column(db.String(200), nullable=False)  # Email/phone
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SellRequest {self.brand} {self.model}>'

class StoreSetting(db.Model):
    __tablename__ = 'store_settings'
    
    id = db.Column(db.Integer, primary_key=True, default=1)  # Always 1 row
    email = db.Column(db.String(120))  # Contact email
    phone = db.Column(db.String(20))  # Customer service phone
    whatsapp = db.Column(db.String(20))  # Optional WhatsApp
    address_en = db.Column(db.String(500))  # Address (English)
    address_ar = db.Column(db.String(500))  # Address (Arabic)
    slogan_en = db.Column(db.String(200))  # Short store tagline
    slogan_ar = db.Column(db.String(200))
    facebook = db.Column(db.String(200))  # URL
    instagram = db.Column(db.String(200))  # URL
    twitter = db.Column(db.String(200))  # URL
    tiktok = db.Column(db.String(200))  # URL
    linkedin = db.Column(db.String(200))  # URL
    copyright_en = db.Column(db.String(200))  # e.g., "© 2025 istore.deals"
    copyright_ar = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<StoreSetting {self.email}>'
