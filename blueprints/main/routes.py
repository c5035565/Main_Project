from flask import Flask, render_template, Blueprint, current_app
import os 
import json    
from datetime import datetime





main = Flask(__name__)  
main = Blueprint('main', __name__, template_folder='templates') 


# Define a route and view function
@main.route('/')
def home(): 
    
    return render_template('index.html', name = 'Home')

@main.route('/login')  
def login():
    return render_template('Login.html', name = 'Login')    


@main.route('/staffdata')
def staffdata():
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)
    return render_template('from_json.html', staffData=staff_data)

@main.context_processor
def inject_globals():
    return {'current_year': datetime.now().year}



