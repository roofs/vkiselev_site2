from uuid import uuid4

from google.appengine.api import mail

from flask import Flask, render_template, request, session, make_response
from flask import redirect
from yaml import load
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
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

# app.jinja_env = jinja2.Environment(
# loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
# extensions=['jinja2.ext.autoescape'],
# autoescape=True)

# if __name__ == '__main__':
#     app.run()

@app.route('/')
def hello():
    return render_template('index.html')


def get_yaml(block, id):
    full_path = os.path.join(templates_dir, block, id, 'desc.yaml')
    document = open(full_path).read().decode('utf8')
    return load(document)


def get_desc(block, id):
    full_path = os.path.join(templates_dir, block, id, 'big_text.html')
    document = open(full_path).read().decode('utf8')
    return document


@app.route('/animated')
def animated():
    path = os.path.join(templates_dir, 'cartoons')
    items = []
    for item_id in os.listdir(path):
        yaml = get_yaml('cartoons', item_id)

        item = {'url': '/cartoons/' + yaml['url'],
                'img': '/cartoons/' + item_id + '/small_pic.jpg',
                'desc': yaml['hover_text']}
        items.append(item)

    return render_template('animated.html', cartoons=items)

@app.route("/cartoons/<path:path>")
def cartoon_page(path):
    full_path = os.path.join(templates_dir, 'cartoons')
    for item_id in os.listdir(full_path):
        yaml = get_yaml('cartoons', item_id)

        if yaml['url'] == path:
            item = {'name': yaml['hover_text'],
                    'desc': get_desc('cartoons', item_id),
                    'youtube': yaml['youtube']
                    }
            return render_template('cartoon.html', item=item)
    return 'Sorry, cartoon not found'


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")
    # return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
