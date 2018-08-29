from flask import render_template, redirect
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/home')
def home():
    return render_template('home_page.html')


@app.route('/entry')
def entry():
    return render_template('entry.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/docs')
def docs():
    return redirect('https://baronsmydiary.docs.apiary.io/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404