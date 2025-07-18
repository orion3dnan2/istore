#!/usr/bin/env python3
"""
Initialize the database with sample data for istore.deals
"""

from app import app, db
from models import User, Category, Product, StoreSetting
from werkzeug.security import generate_password_hash

def initialize_sample_data():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if Category.query.first():
            print("Data already exists, skipping initialization")
            return
        
        # Create categories
        categories = [
            {
                'name_en': 'Smartphones',
                'name_ar': 'الهواتف الذكية',
                'slug': 'smartphones',
                'sort_order': 1,
                'is_active': True
            },
            {
                'name_en': 'Laptops',
                'name_ar': 'أجهزة الكمبيوتر المحمولة',
                'slug': 'laptops',
                'sort_order': 2,
                'is_active': True
            },
            {
                'name_en': 'Tablets',
                'name_ar': 'الأجهزة اللوحية',
                'slug': 'tablets',
                'sort_order': 3,
                'is_active': True
            },
            {
                'name_en': 'Gaming Consoles',
                'name_ar': 'أجهزة الألعاب',
                'slug': 'gaming-consoles',
                'sort_order': 4,
                'is_active': True
            },
            {
                'name_en': 'Audio & Headphones',
                'name_ar': 'الصوتيات وسماعات الرأس',
                'slug': 'audio-headphones',
                'sort_order': 5,
                'is_active': True
            },
            {
                'name_en': 'Smart Home',
                'name_ar': 'المنزل الذكي',
                'slug': 'smart-home',
                'sort_order': 6,
                'is_active': True
            },
            {
                'name_en': 'Cameras',
                'name_ar': 'الكاميرات',
                'slug': 'cameras',
                'sort_order': 7,
                'is_active': True
            },
            {
                'name_en': 'Wearables',
                'name_ar': 'الأجهزة القابلة للارتداء',
                'slug': 'wearables',
                'sort_order': 8,
                'is_active': True
            }
        ]
        
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        print("Categories created successfully!")
        
        # Create sample products
        products = [
            {
                'name_en': 'iPhone 15 Pro',
                'name_ar': 'آيفون 15 برو',
                'description_en': 'The latest iPhone with advanced Pro camera system and titanium design',
                'description_ar': 'أحدث آيفون مع نظام كاميرا برو متقدم وتصميم من التيتانيوم',
                'price': 999.99,
                'stock_quantity': 15,
                'category_id': 1,
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'Samsung Galaxy S24 Ultra',
                'name_ar': 'سامسونج جالاكسي S24 الترا',
                'description_en': 'Premium Android smartphone with S Pen and powerful camera',
                'description_ar': 'هاتف أندرويد راقي مع قلم S وكاميرا قوية',
                'price': 1199.99,
                'stock_quantity': 8,
                'category_id': 1,
                'image_url': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'MacBook Pro 14"',
                'name_ar': 'ماك بوك برو 14 بوصة',
                'description_en': 'Professional laptop with M3 chip and Liquid Retina XDR display',
                'description_ar': 'كمبيوتر محمول احترافي مع معالج M3 وشاشة Liquid Retina XDR',
                'price': 1999.99,
                'stock_quantity': 5,
                'category_id': 2,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'iPad Pro 12.9"',
                'name_ar': 'آيباد برو 12.9 بوصة',
                'description_en': 'Most advanced iPad with M2 chip and Apple Pencil support',
                'description_ar': 'أكثر آيباد تقدماً مع معالج M2 ودعم Apple Pencil',
                'price': 1099.99,
                'stock_quantity': 12,
                'category_id': 3,
                'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'Sony PlayStation 5',
                'name_ar': 'سوني بلايستيشن 5',
                'description_en': 'Next-gen gaming console with ultra-high-speed SSD',
                'description_ar': 'كونسول ألعاب الجيل القادم مع SSD فائق السرعة',
                'price': 499.99,
                'stock_quantity': 3,
                'category_id': 4,
                'image_url': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'Sony WH-1000XM5',
                'name_ar': 'سوني WH-1000XM5',
                'description_en': 'Premium noise-canceling wireless headphones',
                'description_ar': 'سماعات لاسلكية راقية مع إلغاء الضوضاء',
                'price': 399.99,
                'stock_quantity': 20,
                'category_id': 5,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'Canon EOS R5',
                'name_ar': 'كانون EOS R5',
                'description_en': 'Professional mirrorless camera with 8K video recording',
                'description_ar': 'كاميرا احترافية بدون مرآة مع تسجيل فيديو 8K',
                'price': 3899.99,
                'stock_quantity': 4,
                'category_id': 7,
                'image_url': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=300&fit=crop',
                'is_active': True
            },
            {
                'name_en': 'Apple Watch Series 9',
                'name_ar': 'آبل واتش السلسلة 9',
                'description_en': 'Advanced smartwatch with health monitoring and fitness tracking',
                'description_ar': 'ساعة ذكية متقدمة مع مراقبة الصحة وتتبع اللياقة',
                'price': 399.99,
                'stock_quantity': 18,
                'category_id': 8,
                'image_url': 'https://images.unsplash.com/photo-1434493907317-a46b5bbe7834?w=400&h=300&fit=crop',
                'is_active': True
            }
        ]
        
        for prod_data in products:
            product = Product(**prod_data)
            db.session.add(product)
        
        db.session.commit()
        print("Products created successfully!")
        
        # Create store settings
        store_setting = StoreSetting(
            email='info@istore.deals',
            phone='+1 (555) 123-4567',
            whatsapp='15551234567',
            address_en='123 Tech Street, Silicon Valley, CA 94025',
            address_ar='123 شارع التقنية، وادي السيليكون، كاليفورنيا 94025',
            slogan_en='Your trusted electronics store for new and used devices',
            slogan_ar='متجر الإلكترونيات الموثوق للأجهزة الجديدة والمستعملة',
            facebook='https://facebook.com/istore.deals',
            instagram='https://instagram.com/istore.deals',
            twitter='https://twitter.com/istoredeals',
            copyright_en='© 2025 istore.deals. All rights reserved.',
            copyright_ar='© ٢٠٢٥ istore.deals. جميع الحقوق محفوظة.'
        )
        
        db.session.add(store_setting)
        db.session.commit()
        print("Store settings created successfully!")
        
        # Create admin user
        admin_user = User(
            name='Admin User',
            email='admin@istore.deals',
            is_admin=True,
            language='en'
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
        
        print("\n✅ Database initialized with sample data!")
        print("Admin login: admin@istore.deals / admin123")

if __name__ == '__main__':
    initialize_sample_data()