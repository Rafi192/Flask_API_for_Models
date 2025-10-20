from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')

def show_user_profile(username):
    return f"User Profile Page of {username}"

@app.route('/post/<int:post_id>')

def show_post(post_id):
    return f"Post Page with ID: {post_id}"

if __name__ == '__main__':
    app.run(debug=True)
    