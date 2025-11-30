from flask import Flask, render_template, Blueprint
import os 
import json    
from datetime import datetime





app = Flask(__name__)  
main = Blueprint('main', __name__, template_folder='templates') 


# Define a route and view function
@app.route('/')
def home(): 
    
    return render_template('index.html', name = 'Home')

@app.route('/login')  
def login():
    return render_template('Login.html', name = 'Login')   

@app.context_processor
def inject_globals():
    return {'current_year': datetime.now().year}



