from flask import render_template, redirect
from app import app


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/home_page.html')
def home():
    return render_template('home_page.html')


@app.route('/entry.html')
def entry():
    return render_template('entry.html')


@app.route('/account.html')
def account():
    return render_template('account.html')


@app.route('/docs')
def docs():
    return redirect('https://baronsmydiary.docs.apiary.io/')