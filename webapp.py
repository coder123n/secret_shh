Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@coder123n 
coder123n
/
DSW-OAuth-Example-Student
forked from sky-adams/DSW-OAuth-Example-Student
0
046
 Code Pull requests 0 Actions Projects 0 Wiki Security Insights Settings
DSW-OAuth-Example-Student/webapp.py / 
@coder123n coder123n Update webapp.py
d3986ea 15 minutes ago
@coder123n@sky-adams
93 lines (75 sloc)  3.31 KB
  
You're using code navigation to jump to definitions or references.
Learn more or give us feedback
from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from flask import render_template

import pprint
import os


app = Flask(__name__)

app.debug = True #Change this to False for production

app.secret_key = os.environ['SECRET_KEY'] 
oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], 
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',  
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)


@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():   
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https'))

@app.route('/logout')
def logout():
    session.clear()
    return render_template('message.html', message='You were logged out')

@app.route('/login/authorized')#the route should match the callback URL registered with the OAuth provider
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)      
    else:
        try:
            #save user data and set log in message
            session['github_token'] = (resp['access_token'],'')
            session['user_data'] = github.get('user').data
            message = 'You were successfully logged in as ' + session['user_data']['login'] + '.'
        except Exception as inst:
            #clear the session and give error message
            session.clear()
            print(inst)
            message = 'Unable to log in. Please try again.'
    return render_template('message.html', message=message)


@app.route('/page1')
def renderPage1():
    if 'user_data' in session:
        user_data_pprint = pprint.pformat(session['user_data'])#format the user data nicely
    else:
        user_data_pprint = '';
    return render_template('page1.html',dump_user_data=user_data_pprint)

@github.tokengetter
def get_github_oauth_token():
    return session['github_token']


if __name__ == '__main__':
    app.run()
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About