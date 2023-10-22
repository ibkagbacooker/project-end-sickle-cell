from flask import render_template, session, request, jsonify, flash,redirect, url_for
from end_ss_app import app 
from end_ss_app import db
from .models import Payment, Contact,Admin
from end_ss_app import csrf
from werkzeug.security import check_password_hash, generate_password_hash
import re
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
   if request.method=="GET":
      return render_template('admin/signup.html')
   else:
      fname=request.form.get('fname')   
      lname=request.form.get('lname')   
      email=request.form.get('email')   
      password=request.form.get('pass')  
      cpassword = request.form.get('pass2')
      regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      regex_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
      hashed_pass = generate_password_hash(password)  
      details= db.session.query(Admin).filter(Admin.admin_email==email).first()

      if details:
          flash('Email already exists, error')
      else:
         if fname==''or lname=='' or email==''or password=='':
            flash('Fill in all fields','error')
            return redirect(url_for('admin_signup'))
            
         elif not(re.match(regex_email,email)):
            flash('Please input a valid email','error')
            return redirect(url_for('admin_signup'))
            
         elif password!=cpassword:
            flash('passwords do not match','error')
            return redirect(url_for('admin_signup'))
         elif email == 'ibukunogunfowokan@gmail.com' or email == 'akpounique@gmail.com': 
            A=Admin(admin_fname=fname, admin_lname=lname, admin_email=email, admin_pass=hashed_pass, admin_status='1')
            db.session.add(A)
            db.session.commit()
            flash('registration sucessful, login here','success')
            return redirect(url_for('admin_login'))
         else:
            A=Admin(admin_fname=fname, admin_lname=lname, admin_email=email, admin_pass=hashed_pass)
            db.session.add(A)
            db.session.commit()
            flash('registration sucessful, login here','success')
            return redirect(url_for('admin_login'))
          
    

@app.route('/admin/login', methods=['GET', 'POST'] )
def admin_login():
   if request.method=="GET":
      return render_template('admin/login.html') 
   else:
      email= request.form.get('email')
      password = request.form.get('password')
      print(email)
      print(password)
      

      if email!='' and password!='':
         details= db.session.query(Admin).filter(Admin.admin_email==email).first() 
         if details:
            pass_db_hash = details.admin_pass 
            check= check_password_hash(pass_db_hash,password)
            if details.admin_status =='0':
               flash('Unauthorized access','error')
               return redirect('/admin/login') 
            elif check:
               id=details.admin_id
               session['current_admin']= id
               return redirect(url_for('payments'))
            else:
               flash('Incorrect username or password', 'error')
               return redirect(url_for('admin_login'))
         else:
            flash('Looks like you are not registered', 'error')
            return redirect(url_for('admin_signup'))
      else:   
         flash('please fill all fields','error')
         return redirect(url_for('admin_login'))  


# @app.route('/admin/navbar', methods = ['GET', 'POST'])
# def navbar():
#     if request.method=="GET":
#         return render_template('admin/navbar.html') 
    


@app.route('/admin/payments', methods = ['GET', 'POST'])
def payments():
   id = session.get('current_admin')
   if id:
      
      if request.method=="GET":
        admin_deets=db.session.query(Admin).get(id) 
        payment_tag='p'
        payment_deets= db.session.query(Payment).all()
        total_amount = db.session.query(db.func.sum(Payment.customer_amount)).scalar()

        return render_template('admin/payments.html',admin_deets=admin_deets, payment_deets=payment_deets, total_amount=total_amount, payment_tag=payment_tag) 
   else:
      return redirect(url_for('admin_login'))

@app.route('/admin/search', methods = [ 'POST'])
def search():
   id = session.get('current_admin')
   if id: 
      payment_tag='p'
      admin_deets=db.session.query(Admin).get(id)
      customer_query=request.form.get('search')

      if customer_query!='':

         searched_customer= Payment.query.filter(Payment.customer_fname.like(f'%{customer_query}%')).all()
         return render_template('/admin/search.html', searched_customer=searched_customer, admin_deets=admin_deets,payment_tag=payment_tag)
      else:
         flash("Sorry, no Donors found",'error')
         return redirect(url_for('search', admin_deets=admin_deets))
 
   else:
      return redirect(url_for('admin_login')) 
   



@app.route('/admin/activate',methods=['GET'])

def activate():
   id = session.get('current_admin')
   if id: 
      
      admin_deets=db.session.query(Admin).get(id)
      unactive_admins= db.session.query(Admin).filter(Admin.admin_status=='0').all() 
      return render_template('/admin/activate_admins.html', admin_deets=admin_deets, unactive_admins=unactive_admins) 
   else:
      return redirect(url_for('admin_login')) 


@app.route('/admin/messages',methods=['GET'])

def messages():
   id = session.get('current_admin')
   if id: 
      
      admin_deets=db.session.query(Admin).get(id)
      messages= db.session.query(Contact).all() 
      return render_template('/admin/messages.html', admin_deets=admin_deets, messages=messages) 
   else:
      return redirect(url_for('admin_login')) 


@app.route('/delete/<admin_id>', methods=['GET'])

def delete(admin_id): 
    id=session.get('current_admin')
    if id:
        admin=Admin.query.get(admin_id)
        db.session.delete(admin)
        db.session.commit()
        flash('Admin deleted!','success')
        return redirect(url_for('activate'))
    else:
        return redirect('/admin/login')
    

@app.route('/admin/activate/<admin_id>', methods=['GET'])

def activate_admin(admin_id): 
    id=session.get('current_admin')
    if id:
        admin=Admin.query.get(admin_id)
        admin.admin_status='1'
        db.session.commit()
        flash('Admin activated!','success')  
        return redirect(url_for('activate'))
    else:
        return redirect('/admin/login')


@app.route('/admin/signout', methods=['GET'])

def signout():
   if session.get('current_admin') != None:
        session.pop('current_admin',None)
   return redirect(url_for('admin_login'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('admin/404.html'), 404