from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Category, Product, CartItem, RepairRequest, SellRequest, StoreSetting
from utils import get_current_language, set_language, get_text, get_localized_field, load_translations
import logging

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Language context processor
@app.context_processor
def inject_language():
    current_lang = get_current_language()
    translations = load_translations(current_lang)
    store_settings = StoreSetting.query.first()
    
    return dict(
        current_lang=current_lang,
        translations=translations,
        get_text=get_text,
        get_localized_field=get_localized_field,
        store_settings=store_settings
    )

# Helper function to check if user is admin
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need administrator privileges to access this page.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Language Routes
@app.route('/set_language/<lang>')
def set_language_route(lang):
    if set_language(lang):
        flash(get_text('common.success'), 'success')
    return redirect(request.referrer or url_for('index'))

# Main Routes
@app.route('/')
def index():
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    return render_template('index.html', categories=categories, featured_products=featured_products)

@app.route('/products')
def products():
    category_id = request.args.get('category')
    search_query = request.args.get('search', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search_query:
        current_lang = get_current_language()
        if current_lang == 'ar':
            query = query.filter(Product.name_ar.contains(search_query))
        else:
            query = query.filter(Product.name_en.contains(search_query))
    
    products = query.all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    selected_category = Category.query.get(category_id) if category_id else None
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories, 
                         selected_category=selected_category,
                         search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter_by(category_id=product.category_id, is_active=True).limit(4).all()
    return render_template('product_detail.html', product=product, related_products=related_products)

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(get_text('auth.login_success'), 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Repair Service Routes
@app.route('/repair', methods=['GET', 'POST'])
def repair_service():
    if request.method == 'POST':
        device_type = request.form['device_type']
        brand = request.form['brand']
        model = request.form['model']
        issue_description = request.form['issue_description']
        contact_info = request.form['contact_info']
        
        repair_request = RepairRequest(
            user_id=current_user.id if current_user.is_authenticated else None,
            device_type=device_type,
            brand=brand,
            model=model,
            issue_description=issue_description,
            contact_info=contact_info
        )
        
        db.session.add(repair_request)
        db.session.commit()
        
        flash(get_text('repair.request_submitted'), 'success')
        return redirect(url_for('repair_service'))
    
    return render_template('repair_service.html')

# Sell Device Routes
@app.route('/sell', methods=['GET', 'POST'])
def sell_device():
    if request.method == 'POST':
        category_id = int(request.form['category_id'])
        brand = request.form['brand']
        model = request.form['model']
        condition = request.form['condition']
        expected_price = float(request.form['expected_price'])
        contact_info = request.form['contact_info']
        
        sell_request = SellRequest(
            user_id=current_user.id if current_user.is_authenticated else None,
            category_id=category_id,
            brand=brand,
            model=model,
            condition=condition,
            expected_price=expected_price,
            contact_info=contact_info
        )
        
        db.session.add(sell_request)
        db.session.commit()
        
        flash(get_text('sell.request_submitted'), 'success')
        return redirect(url_for('sell_device'))
    
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return render_template('sell_device.html', categories=categories)

# Cart Routes
@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.get_total_price() for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('cart'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'info')
    return redirect(url_for('cart'))

# Admin Routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()
    
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_categories=total_categories,
                         total_users=total_users,
                         recent_products=recent_products)

@app.route('/admin/products')
@login_required
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/categories')
@login_required
@admin_required
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form['name']
        name_ar = request.form.get('name_ar', '')
        description = request.form['description']
        price = float(request.form['price'])
        stock_quantity = int(request.form['stock_quantity'])
        category_id = int(request.form['category_id'])
        image_url = request.form.get('image_url', 'https://via.placeholder.com/300x200?text=No+Image')
        
        product = Product(
            name=name,
            name_ar=name_ar,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category_id=category_id,
            image_url=image_url
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.name_ar = request.form.get('name_ar', '')
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock_quantity = int(request.form['stock_quantity'])
        product.category_id = int(request.form['category_id'])
        product.image_url = request.form.get('image_url', product.image_url)
        product.is_active = 'is_active' in request.form
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/delete_product/<int:product_id>')
@login_required
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'info')
    return redirect(url_for('admin_products'))

@app.route('/admin/add_category', methods=['POST'])
@login_required
@admin_required
def admin_add_category():
    name = request.form['name']
    name_ar = request.form.get('name_ar', '')
    description = request.form.get('description', '')
    
    category = Category(
        name=name,
        name_ar=name_ar,
        description=description
    )
    
    db.session.add(category)
    db.session.commit()
    
    flash('Category added successfully!', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/delete_category/<int:category_id>')
@login_required
@admin_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    # Check if category has products
    if category.products:
        flash('Cannot delete category with existing products!', 'error')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'info')
    
    return redirect(url_for('admin_categories'))

# New Service Routes for istore.deals
@app.route('/repair-service', methods=['GET', 'POST'])
def repair_service():
    if request.method == 'POST':
        # Handle repair service form submission
        device_type = request.form.get('device_type')
        brand = request.form.get('brand')
        model = request.form.get('model')
        issue_description = request.form.get('issue_description')
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        
        # Here you would typically save to database or send email
        flash('Repair request submitted successfully! We will contact you within 24 hours.', 'success')
        return redirect(url_for('repair_service'))
    
    return render_template('repair_service.html')

@app.route('/sell-device', methods=['GET', 'POST'])
def sell_device():
    if request.method == 'POST':
        # Handle sell device form submission
        device_type = request.form.get('device_type')
        brand = request.form.get('brand')
        model = request.form.get('model')
        condition = request.form.get('condition')
        description = request.form.get('description')
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        
        # Here you would typically calculate price and save to database
        flash('Device submission received! We will evaluate your device and contact you with a quote.', 'success')
        return redirect(url_for('sell_device'))
    
    return render_template('sell_device.html')

@app.route('/dashboard')
@login_required
def user_dashboard():
    user_orders = []  # You would fetch user's orders from database
    repair_requests = []  # You would fetch user's repair requests from database
    sold_devices = []  # You would fetch user's sold devices from database
    
    return render_template('user_dashboard.html', 
                         user_orders=user_orders,
                         repair_requests=repair_requests,
                         sold_devices=sold_devices)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
