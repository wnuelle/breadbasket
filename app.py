# -*- coding: utf-8 -*-

import sqlite3 as sql
import pandas as pd
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
app.config["MONGO_URI"] = "mongodb+srv://wnuelle:SquibbyDibby###!!!@cluster0-5suiy.mongodb.net/test?retryWrites=true&w=majority"
app.config["MONGO_DBNAME"] = "test"
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

class Bank(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	email = db.Column(db.String)
	phone_number = db.Column(db.String)
	fbname = db.Column(db.String)
	address = db.Column(db.String)
	city = db.Column(db.String)
	state = db.Column(db.String)
	zc = db.Column(db.String)
	q1 = db.Column(db.String)
	q2 = db.Column(db.String)

class Route(db.Model):
	id = db.Column(db.String,primary_key=True)
	pick_up = db.Column(db.String)
	drop_off = db.Column(db.String)


@app.route('/',methods=['GET','POST'])
def index():
	return render_template('Breadbasket.html')

@app.route('/fb',methods=['GET','POST'])
def fb_form():

	form = InfoForm()
	banks = mongo.db.banks 

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


	### print all database 
	#suppliers = mongo.db.suppliers
	#df = pd.DataFrame(list(suppliers.find()))
	#print(df)
	
	return render_template('FoodProcessors.html',form=form)

#> python app.py
if __name__ == "__main__":
	app.run(debug=True)#host='0.0.0.0',debug=True,port=5000)