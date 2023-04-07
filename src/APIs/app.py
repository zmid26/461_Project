from flask import Flask, request, jsonify, make_response, request, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c43a444c6857419e969677cc155210ab'

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'logged in currently'

# Just to show you that a public route is available for everyone

@app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !  '

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == 'Cocorello2002!':
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.form['username'],
            # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

@app.route('/logout', methods=['POST'])
def logout():
    pass
# your code goes here

if __name__ == "__main__":
    app.run(host='localhost', port=8080)
