from flask import Flask, render_template, Blueprint, current_app, request,redirect,session,flash
import os  
import re
import json    
from datetime import datetime 
from config import db_config
import mysql.connector 
from dotenv import load_dotenv 
from werkzeug.security import generate_password_hash, check_password_hash






main = Blueprint('main', __name__, template_folder='templates')  

staff_data = [
    {"id": 101, "name": "Dr. Eleanor Vance", "role": "Head of Computing Department", "department": "Computing & Engineering", "phone": "0114 555 1001", "email": "e.vance@cantor.edu", "profile_image": "Images/staff/eleanor_vance.jpg"},
    {"id": 102, "name": "Prof. Marcus Chen", "role": "Senior Lecturer in Cyber Security", "department": "Computing & Engineering", "phone": "0114 555 1002", "email": "m.chen@cantor.edu", "profile_image": "Images/staff/marcus_chen.jpg"},
    {"id": 103, "name": "Ms. Sarah Davies", "role": "Admissions Officer", "department": "Student Services", "phone": "0114 555 2005", "email": "s.davies@cantor.edu", "profile_image": "Images/staff/sarah_davies.jpg"},
    {"id": 104, "name": "Dr. Amir Khan", "role": "Course Leader - Design & Media", "department": "Creative Arts", "phone": "0114 555 1004", "email": "a.khan@cantor.edu", "profile_image": "Images/staff/amir_khan.jpg"},
    {"id": 105, "name": "Prof. Olivia Reed", "role": "Head of Faculty", "department": "Administration", "phone": "0114 555 0001", "email": "o.reed@cantor.edu", "profile_image": "Images/staff/olivia_reed.jpg"},
    {"id": 106, "name": "Mr. Ben Carter", "role": "Network Administrator", "department": "Computing & Engineering", "phone": "0114 555 1006", "email": "b.carter@cantor.edu", "profile_image": "Images/staff/ben_carter.jpg"},
    {"id": 107, "name": "Ms. Chloe Miller", "role": "Student Support Advisor", "department": "Student Services", "phone": "0114 555 2007", "email": "c.miller@cantor.edu", "profile_image": "Images/staff/chloe_miller.jpg"},
    {"id": 108, "name": "Dr. David Jones", "role": "Lecturer in Digital Media", "department": "Creative Arts", "phone": "0114 555 1008", "email": "d.jones@cantor.edu", "profile_image": "Images/staff/david_jones.jpg"}
]



@main.route('/')
def home(): 
    
    return render_template('index.html', name = 'Home')   


@main.route('/policies') 
def policies(): 
    return render_template('policies.html', name = 'Policies')






@main.route ('/register', methods = ['GET', 'POST']) 
def register():   
    if request.method == 'POST':
        first_name = request.form.get('first_name') 
        last_name = request.form.get('last_name') 
        username = request.form.get('username') 
        email = request.form.get('email') 
        password = request.form.get('password')  
        confirm_password = request.form.get('password_confirmation')  

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return render_template('register.html', error="Please enter a valid email address.", name='Register')
        

        if password != confirm_password: 
            return render_template('register.html', error ="Password must do not match!", name = 'Register')  
        
        if len(password)< 8: 
            return render_template('register.html', error="Password must be at least 8 characters long.", name='Register')  
        
        if not any(char.isdigit() for char in password):
            return render_template('register.html', error="Password must include at least one number.", name='Register')

        
        if not any(char.isupper() for char in password):
            return render_template('register.html', error="Password must include at least one uppercase letter.", name='Register') 
        
        hashed_password = generate_password_hash(password)  


    
        try:
            db = mysql.connector.connect( 
            host = os.getenv("MYSQL_HOST"), 
            user = os.getenv("MYSQL_USER"), 
            password = os.getenv("MYSQL_PASSWORD"),  
            database = os.getenv("MYSQL_DB") 

    ) 
            cursor = db.cursor()  
            sql = "INSERT INTO users (Username, Email, password_hash, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
            values = (username, email, hashed_password, first_name, last_name) 

            cursor.execute(sql,values) 
            db.commit() 
            db.close()   
            return render_template('register.html', success="Account created successfully!", name='Register') 
            
        
        except mysql.connector.Error as err: 
           
            if err.errno == 1062:
                return render_template('register.html', error="That email or username is already registered.")
            else:
                return render_template('register.html', error="A database error occurred.")

    return render_template('register.html', name = 'Register')

@main.route('/login', methods=['GET', 'POST'])  
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 

        db = mysql.connector.connect( 
            host = os.getenv("MYSQL_HOST"), 
            user = os.getenv("MYSQL_USER"), 
            password = os.getenv("MYSQL_PASSWORD"),  
            database = os.getenv("MYSQL_DB") 
        ) 
        cursor = db.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM users WHERE Username = %s", (username,)) 
        user = cursor.fetchone() 
        db.close() 

        if user and check_password_hash(user['password_hash'], password):   
            session['user_name'] = user['first_name']
            return redirect(('/'))
        else:
           return render_template('Login.html', error="Invalid username or password.")

    return render_template('Login.html', name = 'Login')    

@main.route('/logout') 
def logout(): 
    session.clear() 
    return redirect(('/')) 


@main.route('/staffdata')
def staffdata(): 
    if 'user_name' not in session: 
        return redirect(('/login'))   
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)
    return render_template('from_json.html', staffData=staff_data)

@main.route('/json_filtered', methods=['GET'])
def json_filtered():
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)

    # Add this (you forgot it)
    departments = sorted({s['department'] for s in staff_data})

    department_filter = request.args.get('department', '').strip().lower()

    if department_filter:
        filtered_data = [
            s for s in staff_data if s['department'].strip().lower() == department_filter
        ]
    else:
        filtered_data = staff_data

    return render_template(
        'filtered_staff.html',
        staffData=filtered_data,
        departments=departments,   # FIXED
        selected=department_filter
    )

@main.route('/findUs.html') 
def findUs(): 
    return render_template('findUs.html') 




@main.route('/json_dropdown', methods=['GET'])
def json_dropdown():
    json_path = os.path.join(current_app.static_folder, 'data/staff.json')
    with open(json_path) as f:
        staff_data = json.load(f)

    departments = sorted({s['department'] for s in staff_data})

    department_filter = request.args.get('department', '').strip().lower()

    # Filter if a department is selected
    if department_filter:
        filtered_data = [
            s for s in staff_data if s['department'].strip().lower() == department_filter
        ]
    else:
        filtered_data = staff_data  

    return render_template(
        'filtered_staff.html',
        staffData=filtered_data,
        departments=departments,
        selected=department_filter
    )  
@main.route('/aboutUs') 
def aboutUs():  
    api_key = os.getenv("API_KEY")
    return render_template('about_us.html', api_key=api_key)

@main.route('/courses')
def db_data():
    # Establish database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    cursor.close()
    conn.close() 


    
    
    return render_template('db_data.html', data=data)




@main.context_processor
def inject_globals():
    return {'current_year': datetime.now().year}



