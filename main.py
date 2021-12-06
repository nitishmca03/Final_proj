from flask import Flask, render_template, request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
import random
import json
from flask import redirect, url_for
import sys


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server']
app = Flask(__name__)
app.secret_key = "new"

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)
    option4 = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.String(50), nullable=False)


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=False)


@app.route("/",methods=['POST'])
def login():
    return render_template('index.html')

@app.route("/info" ,methods=['POST','GET'])
def info():
    return render_template('info.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        session['name'] = name
        session['email'] = email

    questions = Questions.query.from_statement(text("""SELECT * from questions ORDER BY RAND()""")).all()
    last = 10
    option = request.args.get('option')
    

    session['marks'] = 0
    i=0
    
    if str(questions[0].answer) ==str(option):
        session['marks'] += 1
        print("marks is "+str(session['marks']),file=sys.stderr)
    i
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    questions = questions[(page - 1): page]
    if page == 1:
        next = "/home?page=" + str(page + 1)
        print("i is"+str(i),file=sys.stderr)
    elif page == last:
        next = "#"
    else:
        next = "/home?page=" + str(page + 1)
        print("i is"+str(i),file=sys.stderr)
    print('correct answer  is :'+str(questions[0].answer), file=sys.stderr)


    return render_template('question.html', questions=questions, next=next, page=page, last=last)


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    name = session['name']
    email = session['email']
    marks = session['marks']
    entry = Users(name=name, email=email, marks=marks, date=datetime.now())
    db.session.add(entry)
    db.session.commit()
    return render_template('marks.html', marks=marks, name=name)


app.run(debug=True)