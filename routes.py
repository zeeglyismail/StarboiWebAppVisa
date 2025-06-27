from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import VisaRecord
from forms import VisaRecordForm, FilterForm
from datetime import datetime, date

@app.route('/')
def index():
    """Main page with list of visa records and filtering"""
    filter_form = FilterForm()
    
    # Start with all records
    query = VisaRecord.query
    
    # Apply filters if provided
    if request.args.get('passport_no'):
        query = query.filter(VisaRecord.passport_no.ilike(f"%{request.args.get('passport_no')}%"))
        filter_form.passport_no.data = request.args.get('passport_no')
    
    if request.args.get('email'):
        query = query.filter(VisaRecord.email.ilike(f"%{request.args.get('email')}%"))
        filter_form.email.data = request.args.get('email')
    
    if request.args.get('country'):
        query = query.filter(VisaRecord.country == request.args.get('country'))
        filter_form.country.data = request.args.get('country')
    
    if request.args.get('visa_status'):
        query = query.filter(VisaRecord.visa_status == request.args.get('visa_status'))
        filter_form.visa_status.data = request.args.get('visa_status')
    
    if request.args.get('payment_status'):
        query = query.filter(VisaRecord.payment_status == request.args.get('payment_status'))
        filter_form.payment_status.data = request.args.get('payment_status')
    
    # Order by most recent first
    records = query.order_by(VisaRecord.created_at.desc()).all()
    
    # Get statistics
    statistics = VisaRecord.get_statistics()
    
    return render_template('index.html', 
                         records=records, 
                         filter_form=filter_form, 
                         statistics=statistics)

@app.route('/create', methods=['GET', 'POST'])
def create_record():
    """Create a new visa record"""
    form = VisaRecordForm()
    
    if form.validate_on_submit():
        try:
            record = VisaRecord()
            record.country = form.country.data
            record.passport_no = form.passport_no.data
            record.name = form.name.data
            record.phone_no = form.phone_no.data
            record.email = form.email.data
            record.file_given_date = form.file_given_date.data
            record.file_submit_date = form.file_submit_date.data
            record.visa_date = form.visa_date.data
            record.visa_status = form.visa_status.data
            record.payment_status = form.payment_status.data
            
            db.session.add(record)
            db.session.commit()
            
            flash('Visa record created successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating record: {str(e)}', 'danger')
            app.logger.error(f'Error creating record: {str(e)}')
    
    return render_template('create.html', form=form)

@app.route('/detail/<int:record_id>')
def detail_record(record_id):
    """View detailed information of a visa record"""
    record = VisaRecord.query.get_or_404(record_id)
    return render_template('detail.html', record=record)

@app.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    """Edit an existing visa record"""
    record = VisaRecord.query.get_or_404(record_id)
    form = VisaRecordForm(obj=record)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(record)
            record.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Visa record updated successfully!', 'success')
            return redirect(url_for('detail_record', record_id=record.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating record: {str(e)}', 'danger')
            app.logger.error(f'Error updating record: {str(e)}')
    
    return render_template('edit.html', form=form, record=record)

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    """Delete a visa record"""
    record = VisaRecord.query.get_or_404(record_id)
    
    try:
        db.session.delete(record)
        db.session.commit()
        flash('Visa record deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
        app.logger.error(f'Error deleting record: {str(e)}')
    
    return redirect(url_for('index'))

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for statistics (for dynamic updates)"""
    statistics = VisaRecord.get_statistics()
    return jsonify(statistics)

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('base.html', 
                         title='Page Not Found',
                         content='<div class="text-center"><h2>Page Not Found</h2><p>The page you are looking for does not exist.</p></div>'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('base.html',
                         title='Internal Server Error', 
                         content='<div class="text-center"><h2>Internal Server Error</h2><p>Something went wrong. Please try again later.</p></div>'), 500
