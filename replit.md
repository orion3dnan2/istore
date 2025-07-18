# Electronics Store Application

## Overview

This is a professional bilingual (English + Arabic) e-commerce web application called **istore.deals** for an electronics store that sells, buys, displays, and repairs electronic devices. The application is built with Flask and includes complete functionality for product catalog management, user authentication, shopping cart, repair services, device selling, and administrative features.

**Migration Status**: Currently migrating from Replit Agent to Replit environment with enhanced database schema and bilingual support.

## Recent Changes

**July 18, 2025**
- ✓ Migrated database schema to include proper bilingual support (name_en/name_ar fields)
- ✓ Added new models: RepairRequest, SellRequest, StoreSetting
- ✓ Created bilingual translation system with JSON files (English/Arabic)
- ✓ Implemented RTL support and Arabic fonts in CSS
- ✓ Enhanced User model with role-based access (admin/customer/merchant)
- ✓ Added language switching functionality
- ✓ Created repair service and sell device features
- ✓ Updated routing system to eliminate conflicts
- ✓ **COMPLETED**: Modern electronics-themed homepage with animated background
- ✓ **COMPLETED**: Professional glass morphism hero section with floating icons
- ✓ **COMPLETED**: Added 8 sample products across 8 categories with real data
- ✓ **COMPLETED**: Modern clean navigation with blue color scheme
- ✓ **COMPLETED**: Professional product cards with stock indicators and pricing

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: HTML templates with Jinja2 templating engine
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Font Awesome 6.0.0 for UI icons
- **JavaScript**: Vanilla JavaScript with Bootstrap components for interactivity
- **Layout**: Template inheritance using a base template for consistent UI

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for user session management
- **Password Security**: Werkzeug security utilities for password hashing
- **Session Management**: Flask sessions with configurable secret key

### Database Architecture
- **ORM**: SQLAlchemy with DeclarativeBase
- **Default Database**: SQLite (configurable via DATABASE_URL environment variable)
- **Connection Pooling**: Configured with pool_recycle and pool_pre_ping for reliability
- **Models**: User, Category, Product, and CartItem with proper relationships

## Key Components

### Models and Data Structure
- **User Model**: Handles user authentication, admin privileges, and cart relationships
- **Category Model**: Product categorization with bilingual support (English/Arabic)
- **Product Model**: Product catalog with pricing, inventory, and multilingual names
- **CartItem Model**: Shopping cart functionality linking users to products

### Authentication System
- **User Registration**: Username, email, and password validation
- **Login System**: Username/password authentication with session management
- **Admin System**: Role-based access control with admin decorators
- **Password Security**: Hashed passwords using Werkzeug

### Product Management
- **Catalog Display**: Product listings with category filtering and search
- **Product Details**: Individual product pages with full information
- **Admin CRUD**: Complete product management interface for administrators
- **Inventory Tracking**: Stock quantity management with availability checks

### Shopping Cart
- **Cart Management**: Add, update, and remove items from cart
- **User-specific Carts**: Each user has their own persistent cart
- **Quantity Controls**: Adjustable quantities with stock validation
- **Price Calculation**: Automatic total calculation for cart items

## Data Flow

### User Journey
1. **Browse Products**: Users can view products by category or search
2. **User Registration/Login**: Account creation or authentication
3. **Add to Cart**: Products added to user-specific shopping cart
4. **Cart Management**: Users can modify quantities or remove items
5. **Admin Functions**: Administrators can manage products and categories

### Data Processing
1. **Product Queries**: Dynamic filtering by category and search terms
2. **Cart Operations**: Real-time cart updates with stock validation
3. **User Authentication**: Session-based authentication with Flask-Login
4. **Admin Operations**: CRUD operations for products and categories

## External Dependencies

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework via CDN
- **Font Awesome 6.0.0**: Icon library via CDN
- **Custom CSS**: Additional styling in static/css/style.css

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Werkzeug**: WSGI utilities and security helpers

### Database
- **SQLite**: Default development database
- **PostgreSQL**: Production-ready option via DATABASE_URL configuration

## Deployment Strategy

### Configuration
- **Environment Variables**: 
  - `DATABASE_URL`: Database connection string
  - `SESSION_SECRET`: Flask session secret key
- **WSGI Configuration**: ProxyFix middleware for proper header handling
- **Database Initialization**: Automatic table creation and admin user setup

### Development Setup
- **Debug Mode**: Enabled for development with hot reloading
- **Host Configuration**: Configured to run on 0.0.0.0:5000 for accessibility
- **Logging**: Debug-level logging enabled for development

### Production Considerations
- **Secret Key**: Environment-based session secret configuration
- **Database**: Configurable database URL for production deployment
- **Static Files**: Organized static assets for CSS and JavaScript
- **Error Handling**: Flash messages for user feedback

### Admin Features
- **Dashboard**: Statistics overview with product, category, and user counts
- **Product Management**: Complete CRUD interface for product catalog
- **Category Management**: Category creation and management
- **User Management**: Admin user privileges and access control

The application follows Flask best practices with proper separation of concerns, secure authentication, and a modular template structure that supports future expansion and maintenance.