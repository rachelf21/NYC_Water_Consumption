from flask import render_template, request, Response
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lunch_menu')
def lunch():
    return 'lunch'