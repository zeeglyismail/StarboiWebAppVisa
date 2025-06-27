# Starboi WebApp - Visa Management System

## Overview

A Flask-based web application for managing visa records and applications. The system provides a comprehensive dashboard for tracking visa applications, managing payment status, and monitoring processing timelines. Built with Python Flask, SQLAlchemy ORM, and Bootstrap frontend, it offers a complete CRUD interface for visa record management.

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
- Personal information (name, passport_no, phone_no, country)
- Document tracking (hotel_file, ticket_file, bank_file, passport_file, pic_file, other_docs)
- Timeline management (file_given_date, file_submit_date, visa_date)
- Status tracking (visa_status, payment_status, payment_amount)
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
- **Dashboard** (`/`): Main listing with filtering and statistics
- **Create** (`/create`): New record creation
- **Edit** (`/edit/<id>`): Record modification
- **Detail** (`/detail/<id>`): Read-only record view
- **Delete** (`/delete/<id>`): Record removal with confirmation

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

## User Preferences

Preferred communication style: Simple, everyday language.