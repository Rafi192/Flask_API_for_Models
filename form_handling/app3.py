#forms allow users to input data( login credentials, search queries, feedback, etc.) which is then sent to the server for processing.
#flask handles form submissions using post and get methods.

#get sends data via URL, visible to users, suitable for non-sensitive data.
#post sends data in the request body, not visible in URL, suitable for sensitive data.

from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    # return f"Received! Username: {username}, Password: {password}"

    #simple authentication check
    if username == 'admin' and password == '123':
        return "Login Successful!"
    else:
        return "Login Failed! Invalid credentials."

if __name__ == '__main__':
    app.run(debug=True)
