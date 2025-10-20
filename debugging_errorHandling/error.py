#404 = not found --> url not found
# 500 --> internal server error --> server side error . Any logical error in the code.

from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))   

#method 1
app.route('/')

def home():
    return "welcome to home page"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

#method 2-> try - catch block
 

if __name__ == '__main__':
    app.run(debug=False)
