import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///electronics_store.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Create admin user if it doesn't exist
    from werkzeug.security import generate_password_hash
    admin_user = models.User.query.filter_by(email='admin@istore.deals').first()
    if not admin_user:
        admin_user = models.User(
            name='Administrator',
            email='admin@istore.deals',
            role='admin',
            language='en'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Admin user created")
    
    # Create sample categories if they don't exist
    if models.Category.query.count() == 0:
        categories = [
            models.Category(name_en='Smartphones', name_ar='الهواتف الذكية', slug='smartphones', sort_order=1),
            models.Category(name_en='Laptops', name_ar='أجهزة اللابتوب', slug='laptops', sort_order=2),
            models.Category(name_en='Tablets', name_ar='الأجهزة اللوحية', slug='tablets', sort_order=3),
            models.Category(name_en='Accessories', name_ar='الإكسسوارات', slug='accessories', sort_order=4),
            models.Category(name_en='Gaming & Consoles', name_ar='الألعاب وأجهزة اللعب', slug='gaming-consoles', sort_order=5),
            models.Category(name_en='Audio & Headphones', name_ar='الصوتيات والسماعات', slug='audio-headphones', sort_order=6),
            models.Category(name_en='Smart Home', name_ar='المنزل الذكي', slug='smart-home', sort_order=7)
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        logging.info("Sample categories created")
    
    # Create default store settings if they don't exist
    store_settings = models.StoreSetting.query.first()
    if not store_settings:
        store_settings = models.StoreSetting(
            email='info@istore.deals',
            phone='+1234567890',
            whatsapp='+1234567890',
            address_en='123 Electronics Street, Tech City, TC 12345',
            address_ar='١٢٣ شارع الإلكترونيات، مدينة التقنية، تك ١٢٣٤٥',
            slogan_en='Your trusted electronics store',
            slogan_ar='متجر الإلكترونيات الموثوق',
            facebook='https://facebook.com/istore.deals',
            instagram='https://instagram.com/istore.deals',
            twitter='https://twitter.com/istore.deals',
            copyright_en='© 2025 istore.deals',
            copyright_ar='© ٢٠٢٥ istore.deals'
        )
        db.session.add(store_settings)
        db.session.commit()
        logging.info("Default store settings created")
