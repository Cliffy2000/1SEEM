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

        return render_template('/pages/login.html', show_login_box=False)
        
    return render_template('/pages/login.html', show_login_box=False)


@app.route('/reports')
def reports():
    query = -1
    if 'user_type' not in session:
        return render_template('/pages/reports.html', user_type='')

    query = 0
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
    
    if request.method == 'POST':
        receiver_name = request.form.get('receiver_name')
        report_content = request.form.get('report_content')
        user_id = session.get('user_id')
        receiver_id = users.get_user_id(receiver_name)
        
        report.submit_report(user_id, receiver_id, report_content)
        return redirect(url_for('reports'))

    return render_template('submit_report.html')
        


@app.route('/search')
def search():
    return render_template('/pages/search.html')


if __name__ == "__main__":
    db.connect_to_db()
    app.run()
