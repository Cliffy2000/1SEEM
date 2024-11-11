import os
from flask import Flask, session, render_template, request, redirect, url_for

from scripts import db, users


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


users = {
    'admin': {'password': 'admin', 'type': 'admin'},
    'user': {'password': 'user', 'type': 'user'}
}


@app.route('/')
def index():
    return render_template('/pages/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.get(username)
        # if user and user['password'] == password:
        user_check = users.authenticate_user(username, password)
        if user_check:
            session['username'] = username
            session['user_type'] = user['type']
            return redirect(url_for(('index')))   

        return render_template('/pages/login.html', show_login_box=False)
        
    return render_template('/pages/login.html', show_login_box=False)


@app.route('/mail')
def mail():
    return render_template('/pages/mail.html')


@app.route('/search')
def search():
    return render_template('/pages/search.html')


if __name__ == "__main__":
    db.connect_to_db()
    app.run()
