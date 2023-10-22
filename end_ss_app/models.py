from datetime import datetime


from end_ss_app import db



class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    admin_fname = db.Column(db.String(50), nullable=False)
    admin_lname = db.Column(db.String(50), nullable=False)
    admin_pass = db.Column(db.String(150), nullable=False)
    admin_email = db.Column(db.String(120), nullable=False) 
    admin_status = db.Column(db.Enum('1','0'), server_default='0')


class Contact(db.Model): 
    Contact_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    contact_name = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False) 
    contact_message = db.Column(db.String(255), nullable=False) 


class Payment(db.Model):
    customer_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    customer_fname = db.Column(db.String(50), nullable=False)
    customer_lname = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(120), nullable=False)
    customer_amount = db.Column(db.String(120), nullable=False)
    customer_reference_number = db.Column(db.String(120), nullable=False, unique=True)
    customer_payment_status= db.Column(db.Enum('1','0'), server_default='0')
    customer_payment_date = db.Column(db.DateTime())

class Gallery(db.Model):
    photo_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    photo_url=db.Column(db.String(120),nullable=False)