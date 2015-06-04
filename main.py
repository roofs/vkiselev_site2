from uuid import uuid4

from google.appengine.api import mail

from flask import Flask, render_template, request, session
from flask import redirect
import os


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid4())
    return session['_csrf_token']

app = Flask(__name__)
app.secret_key = '3FvdD7dFsdgfn=AF923Rdfad4%nsdfmLsweAo9='
app.jinja_env.globals['csrf_token'] = generate_csrf_token

if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    DEBUG = True
else:
    DEBUG = False

app.jinja_env.globals['debug'] = DEBUG

# app.jinja_env = jinja2.Environment(
# loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
# extensions=['jinja2.ext.autoescape'],
# autoescape=True)

# if __name__ == '__main__':
#     app.run()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/animated')
def animated():
    return render_template('animated.html')

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")
    # return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500