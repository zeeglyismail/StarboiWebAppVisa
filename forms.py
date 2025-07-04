from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from datetime import date

class VisaRecordForm(FlaskForm):
    # Define country choices
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('Malaysia', 'Malaysia'),
        ('Thailand', 'Thailand'),
        ('China', 'China'),
        ('Singapore', 'Singapore')
    ]
    
    VISA_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Not Paid', 'Not Paid'),
        ('Paid', 'Paid')
    ]
    
    # Basic Information
    country = SelectField('Country', choices=COUNTRY_CHOICES, validators=[DataRequired()])
    passport_no = StringField('Passport No', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    phone_no = StringField('Phone No', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(min=1, max=120)])
    

    
    # Dates
    file_given_date = DateField('File Given Date', validators=[DataRequired()], default=date.today)
    file_submit_date = DateField('File Submit Date', validators=[DataRequired()], default=date.today)
    visa_date = DateField('Visa Date', validators=[Optional()])
    
    # Status and Payment
    visa_status = SelectField('Visa Status', choices=VISA_STATUS_CHOICES, validators=[DataRequired()])
    payment_status = SelectField('Payment Status', choices=PAYMENT_STATUS_CHOICES, validators=[DataRequired()])

class FilterForm(FlaskForm):
    passport_no = StringField('Passport No', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    country = SelectField('Country', choices=[('', 'All Countries')] + VisaRecordForm.COUNTRY_CHOICES[1:], validators=[Optional()])
    visa_status = SelectField('Visa Status', choices=[('', 'All Statuses')] + VisaRecordForm.VISA_STATUS_CHOICES, validators=[Optional()])
    payment_status = SelectField('Payment Status', choices=[('', 'All Payment Statuses')] + VisaRecordForm.PAYMENT_STATUS_CHOICES, validators=[Optional()])
