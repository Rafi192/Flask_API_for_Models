from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # username = request.form.get('username')
        # password = request.form.get('password')
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            return redirect(url_for('admin_dashboard'))
        else:
            return "Login Failed! Invalid credentials."
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return "Welcome to the Admin Dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
