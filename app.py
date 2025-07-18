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
    admin_user = models.User.query.filter_by(email='admin@electronics.com').first()
    if not admin_user:
        admin_user = models.User(
            username='admin',
            email='admin@electronics.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Admin user created")
    
    # Create sample categories if they don't exist
    if models.Category.query.count() == 0:
        categories = [
            models.Category(name='Smartphones', name_ar='الهواتف الذكية', description='Latest smartphones and accessories'),
            models.Category(name='Laptops', name_ar='أجهزة الكمبيوتر المحمولة', description='Laptops and notebooks'),
            models.Category(name='Tablets', name_ar='الأجهزة اللوحية', description='Tablets and e-readers'),
            models.Category(name='Accessories', name_ar='الإكسسوارات', description='Electronic accessories and peripherals'),
            models.Category(name='Audio', name_ar='الصوتيات', description='Headphones, speakers, and audio devices'),
            models.Category(name='Gaming', name_ar='الألعاب', description='Gaming consoles and accessories')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        logging.info("Sample categories created")
