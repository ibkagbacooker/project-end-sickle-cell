from flask import render_template, request, jsonify, flash,redirect, url_for
from flask_wtf.csrf import generate_csrf
import requests,json
from end_ss_app import app 
from end_ss_app import db, csrf
from .models import Payment, Contact
from datetime import datetime
api_key = app.config['API_KEY']


@app.route("/", methods=['GET'])

def user_home():
    
   
    return render_template('user/index.html')


@app.route("/index2", methods=['GET'])

def user_home2():
    
   
    return render_template('user/index2.html')



# time converter

def convert_api_timestamp(api_timestamp):
    formatted_timestamp = datetime.fromisoformat(api_timestamp)
    return formatted_timestamp


@csrf.exempt
@app.route("/transaction", methods=['POST'])

def confirm_transaction():
    fname = request.get_json().get('firstName')
    lname = request.get_json().get('lastName')
    email = request.get_json().get('email')
    phone = request.get_json().get('phone')
    amount = request.get_json().get('amount')
    ref = request.get_json().get('reference')
    csrf = request.get_json().get('csrf')
    
    try:
        headers={"Content-Type":"application.json","Authorization":api_key}

        url_verification ="https://api.paystack.co/transaction/verify/"+str(ref)
        response = requests.get(url_verification, headers=headers)
        res_json=  json.loads(response.text)
        date= res_json['data']['paid_at']
        date_formatted = convert_api_timestamp(date)
        if res_json['status'] == True:
            if (res_json['data']['status']=='success') and (res_json['data']['amount'] == int(amount)*100):
                
                #insert payment object to dm
                payment_obj = Payment(customer_fname=fname, customer_lname=lname, customer_email=email, customer_phone=phone, customer_amount=amount,  customer_reference_number=ref, customer_payment_status='1',customer_payment_date  =date_formatted )
                                    

                db.session.add(payment_obj)
                db.session.commit()

                sendback={'status':'success', 'message':'Payment confirmed'}
                return json.dumps(sendback)
            else:
                sendback={'status':'Failed', 'message':'Transaction failed, please try again'}
                return json.dumps(sendback)
        else:
            sendback={'status':'Failed', 'message':'Transaction failed false'}
            return json.dumps(sendback)

    except requests.exceptions.HTTPError as http_err:
        error_message = f'HTTP error occurred: {http_err}'
        return json.dumps({'status': 'Failed', 'message': error_message}), 500 
    
    except Exception as err:
        # Handle other types of exceptions
        error_message = f'An error occurred: {err}'
        # Log the error or provide feedback to the user
        return json.dumps({'status': 'Failed', 'message': error_message}), 500
    
@csrf.exempt
@app.route('/contact', methods=['POST'])

def contact():
    name= request.form.get('fullname')
    add= request.form.get('emailadd')
    msg=  request.form.get('text')

    contact_obj = Contact( contact_name= name, contact_email=add, contact_message=msg)
    db.session.add(contact_obj)
    db.session.commit()
    flash('Message Received! we will be in touch.','success')
    return redirect(url_for("user_home"))

@app.route('/thankyou', methods=['GET'])

def thank_you():
    name=request.args.get('name')
    return render_template('user/Thankyou.html', name=name)


@app.route('/gallery',methods=['GET'])
def gallery():
    return render_template('user/gallery.html')


@app.route('/oops', methods=['GET'])

def oops():
    
    return render_template('user/oops.html')
