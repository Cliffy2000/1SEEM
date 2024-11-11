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
    if 'user_type' not in session:
        return render_template('/pages/reports.html', user_type='')

    user_type = session['user_type']
    if user_type == 'user':
        query = report.get_report_by_sender(session['username'])
    elif user_type == 'admin':
        query = report.get_report_by_receiver(session['username'])
    
    return render_template('/pages/reports.html', query=query, user_type=user_type)


@app.route('/search')
def search():
    return render_template('/pages/search.html')


if __name__ == "__main__":
    db.connect_to_db()
    app.run()
