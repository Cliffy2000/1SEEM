import os
from flask import Flask, session, render_template, request, redirect, url_for

from scripts import db, users, report


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('/pages/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_check = users.authenticate_user(username, password)
        if user_check:
            session['username'] = username
            session['user_type'] = users.get_user_type(username)
            return redirect(url_for(('index')))   

        return render_template('/pages/login.html')
        
    return render_template('/pages/login.html')


@app.route('/logout')
def logout():
    session.pop('user_type', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/reports')
def reports():
    query = -1
    if 'user_type' not in session:
        return render_template('/pages/reports.html', query=query, user_type='')

    user_type = session['user_type']
    if user_type == 'user':
        query = report.get_report_by_sender(users.get_user_id(session['username']))
    elif user_type == 'admin':
        query = report.get_report_by_receiver(users.get_user_id(session['username']))
    
    return render_template('/pages/reports.html', query=query, user_type=user_type)


@app.route('/submit_report', methods=['GET', 'POST'])
def submit_report():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['user_type'] == 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        receiver_name = request.form.get('receiver_name')
        report_content = request.form.get('report_content')
        user_id = users.get_user_id(session.get('username'))
        receiver_id = users.get_user_id(receiver_name)
        
        report.submit_report(user_id, receiver_id, report_content)
        return redirect(url_for('reports'))

    return render_template('/pages/submit_report.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    formatted_query = -1
    if request.method == "POST":
        query = db.select_school_info(filter={
            'school': request.form.get('search_school_name').upper() or None,
            'district': request.form.get('search_distrct').upper() or None,
            'type': request.form.get('search_type').upper() or None,
            'level': request.form.get('search_level').upper() or None,
            'bus_no': request.form.get('search_bus_no') or None,
            'mrt': request.form.get('search_mrt').upper() or None 
        })
               
        formatted_query = [{
            'name': item['name'],
            'level': item['main_level'],
            'address': item['address'],
            'tel_no': item['tel_no'],
            'email': item['email']
        } for item in query]
        
        print(query)
        
        if len(formatted_query) == 0:
            return render_template('/pages/search.html', query=formatted_query, text="No results found")
        
        return render_template('/pages/search.html', query=formatted_query)
    
    return render_template('/pages/search.html', query=formatted_query, text="please enter a search condition")


if __name__ == "__main__":
    db.connect_to_db()
    app.run()
