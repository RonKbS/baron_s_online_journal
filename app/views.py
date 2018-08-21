from flask import render_template, redirect
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/docs')
def docs():
    return redirect('https://baronsmydiary.docs.apiary.io/')