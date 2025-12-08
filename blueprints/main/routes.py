from flask import Flask, render_template, Blueprint, current_app, request
import os 
import json    
from datetime import datetime 
from config import db_config
import mysql.connector






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

@main.route('/login')  
def login():
    return render_template('Login.html', name = 'Login')    


@main.route('/staffdata')
def staffdata():
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
    return render_template('about_us.html')

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



