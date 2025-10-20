from flask import Flask
app = Flask(__name__)


@app.route('/')

def home():
    return "Welcome to the Static Routing Home Page!"



@app.route('/about')

def about():
    return "This is the About Page of the Static Routing Application."


if __name__ == '__main__':
    app.run(debug=True)