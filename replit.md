# Starboi WebApp - Visa Management System

## Overview

A Flask-based web application for managing visa records and applications with authentication system. The system provides a comprehensive dashboard for tracking visa applications, managing payment status, and monitoring processing timelines. Built with Python Flask, SQLAlchemy ORM, and Bootstrap frontend, it offers role-based access control where authenticated users can perform full CRUD operations while anonymous users can only view and filter records.

## System Architecture

### Backend Architecture
- **Framework**: Flask 3.1.1 with Python 3.11
- **ORM**: SQLAlchemy 2.0.41 with Flask-SQLAlchemy integration
- **Database**: SQLite (development) with PostgreSQL support (production)
- **Forms**: Flask-WTF with WTForms for form handling and validation
- **Deployment**: Gunicorn WSGI server with autoscale deployment target

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with Replit dark theme
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JavaScript with Bootstrap components
- **Templating**: Jinja2 templates with inheritance-based layout

### Database Schema
The application uses a single primary entity:

**VisaRecord Model**:
- Personal information (name, passport_no, phone_no, email, country)
- Timeline management (file_given_date, file_submit_date, visa_date)
- Status tracking (visa_status, payment_status)
- Audit fields (created_at, updated_at)

## Key Components

### Models (`models.py`)
- **VisaRecord**: Core entity with full visa application lifecycle tracking
- Includes calculated properties (visa_days) and class methods for statistics
- Supports audit trail with created_at/updated_at timestamps

### Forms (`forms.py`)
- **VisaRecordForm**: Comprehensive form with validation for all visa record fields
- Predefined choices for countries, visa status, and payment status
- Date validation and field-specific constraints

### Routes (`routes.py`)
- **Dashboard** (`/`): Main listing with filtering and statistics (public access)
- **Login** (`/login`): Authentication page with demo credentials
- **Logout** (`/logout`): Session termination
- **Create** (`/create`): New record creation (requires authentication)
- **Edit** (`/edit/<id>`): Record modification (requires authentication)
- **Detail** (`/detail/<id>`): Read-only record view (public access)
- **Delete** (`/delete/<id>`): Record removal with confirmation (requires authentication)

### Templates
- **Base template**: Bootstrap-based layout with navigation and flash messages
- **Index**: Dashboard with statistics cards and filterable record listing
- **Create/Edit**: Form-based record management
- **Detail**: Comprehensive record view with action buttons

## Data Flow

1. **Record Creation**: Form submission → validation → database insert → redirect to listing
2. **Record Viewing**: Database query → template rendering with filtered results
3. **Record Updates**: Form pre-population → validation → database update → redirect
4. **Statistics**: Real-time calculation of monthly, yearly, and lifetime metrics
5. **Filtering**: URL parameter-based filtering with form state preservation

## External Dependencies

### Python Packages
- **Flask ecosystem**: Flask, Flask-SQLAlchemy, Flask-WTF
- **Database**: SQLAlchemy, psycopg2-binary (PostgreSQL adapter)
- **Validation**: WTForms, email-validator
- **Production**: Gunicorn WSGI server
- **Utilities**: Werkzeug for middleware and utilities

### Frontend Dependencies
- **Bootstrap**: Replit dark theme variant via CDN
- **Font Awesome**: Icon library via CDN
- **JavaScript**: Bootstrap components for interactivity

### System Dependencies
- **OpenSSL**: For secure connections
- **PostgreSQL**: Database server for production deployment

## Deployment Strategy

### Development Environment
- **Runtime**: Python 3.11 with Nix package management
- **Database**: SQLite for local development
- **Server**: Flask development server with debug mode

### Production Environment
- **Deployment Target**: Replit autoscale infrastructure
- **WSGI Server**: Gunicorn with multiple worker processes
- **Database**: PostgreSQL with connection pooling
- **Configuration**: Environment variable-based configuration
- **Security**: ProxyFix middleware for proper header handling

### Configuration Management
- **Session Secret**: Environment variable with fallback
- **Database URL**: Environment variable with SQLite fallback
- **Connection Pooling**: 300-second recycle with pre-ping health checks

## Changelog
- June 27, 2025. Initial setup
- June 27, 2025. Added email field to CRUD operations and filtering
- June 27, 2025. Enhanced dashboard with payment status counters (paid/not paid)
- June 27, 2025. Removed file details section as requested by user
- June 27, 2025. Removed auto-submit functionality from forms
- June 27, 2025. Removed payment revenue section and all dollar signs from dashboard and CRUD operations
- June 28, 2025. Added login system with demo credentials (admin/admin123)
- June 28, 2025. Implemented role-based access: authenticated users get full CRUD, anonymous users view-only

## User Preferences

Preferred communication style: Simple, everyday language.
Dashboard layout: Organized sections (file statistics, payment status) to fit window properly - no payment revenue or dollar amounts needed.
Authentication: Demo login system with hardcoded credentials that can be changed in code. No registration needed.