from app import db
from datetime import datetime, date
from sqlalchemy import func

class VisaRecord(db.Model):
    __tablename__ = 'visa_records'
    
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    passport_no = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    

    
    file_given_date = db.Column(db.Date, nullable=False, default=date.today)
    file_submit_date = db.Column(db.Date, nullable=False, default=date.today)
    visa_date = db.Column(db.Date)
    visa_status = db.Column(db.String(20), nullable=False, default='Pending')  # Approved, Pending, Rejected
    payment_status = db.Column(db.String(20), nullable=False, default='Not Paid')  # Paid, Not Paid

    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<VisaRecord {self.id}: {self.name} - {self.country}>'
    
    @property
    def visa_days(self):
        """Calculate visa days = visa_date - file_submit_date"""
        if self.visa_date and self.file_submit_date:
            return (self.visa_date - self.file_submit_date).days
        return None
    
    @classmethod
    def get_statistics(cls):
        """Get statistics for the dashboard"""
        today = date.today()
        current_month_start = date(today.year, today.month, 1)
        current_year_start = date(today.year, 1, 1)
        
        # Total files this month
        total_this_month = cls.query.filter(
            cls.created_at >= current_month_start
        ).count()
        
        # Total files this year
        total_this_year = cls.query.filter(
            cls.created_at >= current_year_start
        ).count()
        
        # Total files lifetime
        total_lifetime = cls.query.count()
        
        # Payment status counters
        paid_count = cls.query.filter(cls.payment_status == 'Paid').count()
        not_paid_count = cls.query.filter(cls.payment_status == 'Not Paid').count()
        
        return {
            'total_this_month': total_this_month,
            'total_this_year': total_this_year,
            'total_lifetime': total_lifetime,
            'paid_count': paid_count,
            'not_paid_count': not_paid_count
        }
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'country': self.country,
            'passport_no': self.passport_no,
            'name': self.name,
            'phone_no': self.phone_no,
            'email': self.email,
            'file_given_date': self.file_given_date.isoformat() if self.file_given_date else None,
            'file_submit_date': self.file_submit_date.isoformat() if self.file_submit_date else None,
            'visa_date': self.visa_date.isoformat() if self.visa_date else None,
            'visa_status': self.visa_status,
            'payment_status': self.payment_status,

            'visa_days': self.visa_days,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
