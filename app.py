# -*- coding: utf-8 -*-

import pandas as pd
import stripe
import os
from random import randint

import flask
from flask import request, jsonify, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

#initialize flask app
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = os.urandom(32)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["MONGO_DBNAME"] = "test"
stripe_sk = "sk_test_291pSiDba23GGIOYuAqH4eg600q77nHQRZ"
stripe.api_key = stripe_sk
mongo = PyMongo(app)

class InfoForm(FlaskForm):
	first_name = StringField('First name',validators=[InputRequired()],render_kw={"placeholder": "First name","style":"font-size:100%;"})
	last_name = StringField('Last name',validators=[InputRequired()],render_kw={"placeholder": "Last name","style":"font-size:100%;"})
	email = StringField('Contact email',validators=[InputRequired()],render_kw={"placeholder": "E-mail","style":"font-size:100%;"})
	phone_number = StringField('Contact phone number',validators=[InputRequired()],render_kw={"placeholder": "Phone number","style":"font-size:100%;"})
	fbname = StringField('Food bank name',validators=[InputRequired()],render_kw={"placeholder": "Food bank name","style":"font-size:100%;"})
	address = StringField('Address',validators=[InputRequired()],render_kw={"placeholder": "Address","style":"font-size:100%;"})
	city = StringField('City',validators=[InputRequired()],render_kw={"placeholder": "City","style":"font-size:100%;"})
	state = StringField('State',validators=[InputRequired()],render_kw={"placeholder": "State","style":"font-size:100%;"})
	zc = StringField('Zip code',validators=[InputRequired()],render_kw={"placeholder": "Zip code","style":"font-size:100%;"})
	q1 = StringField('Over capacity',validators=[InputRequired()],render_kw={"placeholder": "Q1","style":"font-size:100%;"})
	q2 = StringField('Population',validators=[InputRequired()],render_kw={"placeholder": "Q2","style":"font-size:100%;"})

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('Breadbasket.html')

@app.route('/fb',methods=['GET','POST'])
def fb_form():

	form = InfoForm()
	banks = mongo.db.banks 

	if request.method == "POST":
		fields = ['first_name','last_name','email','phone_number','fb_name','address','city','state','zc','q1','q2']
		input_dictionary = {item:request.form[item] for item in fields}
		c = 1
		while True:
			try:
				input_dictionary[str(request.form[f'food_type{c}'])+':'+request.form[f'food_item{c}']] = float(request.form[f'quantity{c}'])
			except:
				break
			c+=1
		banks.insert(input_dictionary)

	return render_template('FoodBanks.html',form=form)

@app.route('/fp',methods=['GET','POST'])
def fp_form():

	form = InfoForm()
	suppliers = mongo.db.suppliers

	if request.method == "POST":
		fields = ['first_name','last_name','email','phone_number','fp_name','address','city','state','zc','q1','q2']
		input_dictionary = {item:request.form[item] for item in fields}
		c = 1
		while True:
			try:
				input_dictionary[str(request.form[f'food_type{c}'])+':'+request.form[f'food_item{c}']] = float(request.form[f'quantity{c}'])
			except:
				break
			c+=1
		suppliers.insert(input_dictionary)

	return render_template('FoodProcessors.html',form=form)

@app.route('/route',methods=['GET','POST'])
def get_route():
		form = InfoForm()
		routes = mongo.db.routes
		route = routes.find_one({'id':request.args.get('id')})
		print(route)
		if request.method == "POST":
			if request.form['bid'] < route['Current Fee']:
				routes.update({'id':request.args.get('id')},{"$set":{'Current Fee':request.form['bid']}})

		locations = []
		for i in range(int(route['Route length'])):
			locations.append((float(route[str(i)]['Lat']),float(route[str(i)]['Long'])))

		return render_template('Routes.html',route=route,locations=[locations],form=form,date=route['Expiration'])


@app.route('/courier',methods=['GET','POST'])
def courier_form():
	routes = mongo.db.routes
	all_routes = list(routes.find({'Courier selection':'Incomplete'}))
	locations = []
	for route in all_routes:
		stops = []
		for i in range(int(route['Route length'])):
			stops.append((float(route[str(i)]['Lat']),float(route[str(i)]['Long'])))
		locations.append(stops)
	return render_template('Courier2.html',routes=all_routes,locations=locations)

@app.route('/public',methods=['GET','POST'])
def donate_form():
	form = InfoForm()
	volunteers = mongo.db.volunteers

	if request.method == "POST":
		fields = ['first_name','last_name','email','phone_number','address','city','state','zc','route_m','route_ul']
		input_dictionary = {item:request.form[item] for item in fields}
		print(input_dictionary)
		volunteers.insert(input_dictionary)

	return render_template('Public.html',form=form,pub_key="pk_test_DCb7o35M61huNlchdbxiSiIU00UQ8s17Ax")

@app.route('/pay', methods=['POST'])
def pay():
    
    print(request.form)
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=19900,
        currency='usd',
        description='The Product'
    )

    return redirect(url_for('thanks'),pub_key="pk_test_DCb7o35M61huNlchdbxiSiIU00UQ8s17Ax")

#> python app.py
if __name__ == "__main__":
	app.run(debug=True)#host='0.0.0.0',debug=True,port=5000)