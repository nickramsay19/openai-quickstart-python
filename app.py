import os
from urllib.request import urlopen
import secrets
import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)

# for session storage flask needs a key
app.secret_key = secrets.token_bytes(64)
#app.config['SESSION_TYPE'] = ''#'memcached'

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=('GET', 'POST'))
def index():
    if not session.permanent:
        session.permanent = True
    if session.new or 'messages' not in session.keys():
        session['messages'] = []
        session["temperature"] = 1.0
    
    if request.method == 'POST':
        #session['response-type'] = request.form['response-type']
        session['model'] = request.form['model']
        
        #print(session['temperature'], float(request.form['temperature']))
        session['temperature'] = float(request.form['temperature'])
        
        session['messages'] += [{
            'role': 'user',
            'content': request.form['prompt'],
        }]
        
        response = openai.ChatCompletion.create(
            model=session["model"],
            temperature=session['temperature'],
            messages=session["messages"],
            max_tokens=500
        )
        
        response_content = response['choices'][0]['message']['content']
        
        session['messages'] += [{
            'role': 'assistant',
            'content': response_content
        }]
        
    return render_template('index.html', session=session)

@app.route('/image', methods=('GET', 'POST'))
def image():
    return ''
