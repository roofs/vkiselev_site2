from uuid import uuid4
import os
import re

from bs4 import BeautifulSoup
from flask import Flask, render_template, session
from flask import redirect
from yaml import load


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


def prepare_animated_section(section_name, reverse=True):
    def to_int(x):
        return int(x)

    path = os.path.join(templates_dir, section_name)
    items = []
    listdir = sorted(map(to_int, filter(str.isdigit, os.listdir(path))), reverse=reverse)
    for item_id in listdir:
        item_id = str(item_id)
        yaml = get_yaml(section_name, item_id)

        item_url = get_subpage_url(yaml, section_name, item_id)
        item = {'url': item_url,
                'img': '/' + section_name + '/' + item_id + '/small_pic.jpg',
                'desc': yaml['hover_text']}
        items.append(item)

    return items


def prepare_flat_section(section_name):
    return prepare_animated_section(section_name)


def get_subpage_url(yaml, section_name, item_id):
    item_url = yaml['url']
    if not item_url:
        item_url = str(item_id)
    return '/' + section_name + '/' + item_url


@app.route('/animated')
def animated():
    citems = prepare_animated_section('cartoons')
    mitems = prepare_animated_section('misc')
    psitems = prepare_animated_section('princess_seasons', reverse=False)
    pitems = prepare_animated_section('princess', reverse=False)

    return render_template('animated.html', cartoons=citems, misc=mitems, princess_seasons=psitems, princess=pitems)


@app.route('/still')
def still():
    fitems = prepare_flat_section('flat')
    pitems = prepare_flat_section('projects')
    citems = prepare_flat_section('comics')
    return render_template('still.html', flat=fitems, projects=pitems, comics=citems)


@app.route('/memories')
def memories():
    return render_template('memories.html')


@app.route('/vasili')
def vasili():
    return render_template('vasili.html')


def process_video_url(url):
    if "youtube.com" in url:
        if "playlist" not in url:
            return url + "?rel=0&showinfo=0&autohide=1&cc_load_policy=1&disablekb=1"
    return url


def render_animated_subpage(section_name, path, reverse=True):
    full_path = os.path.join(templates_dir, section_name)
    for item_id in os.listdir(full_path):
        if not item_id.isdigit():
            continue
        yaml = get_yaml(section_name, item_id)

        item_url = yaml['url']
        if not item_url:
            item_url = str(item_id)
        if item_url == path:
            prev, next = get_next_prev(section_name, item_id, reverse)

            desc = get_desc(section_name, item_id)
            soup = BeautifulSoup(desc)
            og_desc = soup.findAll('div', class_='desc')[0].text
            item = {'name': yaml['hover_text'],
                    'desc': desc,
                    'og_desc': og_desc,
                    'youtube': process_video_url(yaml['youtube']),
                    'img': '/' + section_name + '/' + item_id + '/small_pic.jpg'}
            if 'width' in yaml:
                item['width'] = yaml['width']
            return render_template('cartoon.html', item=item, prev=prev, next=next)
    return 'Sorry, cartoon not found'


def get_next_prev(section_name, item_id, reverse=True):
    prev = None
    next = None

    prev_id = int(item_id) - 1
    if prev_id != 0:
        prev_yaml = get_yaml(section_name, str(prev_id))
        prev = {'url': get_subpage_url(prev_yaml, section_name, str(prev_id)),
                'name': prev_yaml['hover_text']}

    next_id = int(item_id) + 1
    if os.path.isfile(os.path.join(templates_dir, section_name, str(next_id), 'desc.yaml')):
        next_yaml = get_yaml(section_name, str(next_id))
        next = {'url': get_subpage_url(next_yaml, section_name, str(next_id)),
                'name': next_yaml['hover_text']}

    if reverse:
        return next, prev
    else:
        return prev, next


def render_flat_subpage(section_name, path, reverse=True):
    full_path = os.path.join(templates_dir, section_name)
    for item_id in os.listdir(full_path):
        if not item_id.isdigit():
            continue
        yaml = get_yaml(section_name, item_id)

        item_url = yaml['url']
        if not item_url:
            item_url = str(item_id)
        if item_url == path:
            prev, next = get_next_prev(section_name, item_id, reverse)

            desc = get_desc(section_name, item_id)
            og_desc = yaml['hover_text']
            item = {'name': yaml['hover_text'],
                    'desc': desc,
                    'og_desc': og_desc,
                    'img': '/' + section_name + '/' + item_id + '/big_pic.jpg'}
            return render_template('flat.html', item=item, prev=prev, next=next)
    return 'Sorry, cartoon not found'


def render_comics_subpage(section_name, path, reverse=True):
    full_path = os.path.join(templates_dir, section_name)
    for item_id in os.listdir(full_path):
        if not item_id.isdigit():
            continue
        yaml = get_yaml(section_name, item_id)

        item_url = yaml['url']
        if not item_url:
            item_url = str(item_id)
        if item_url == path:
            prev, next = get_next_prev(section_name, item_id, reverse)

            desc = get_desc(section_name, item_id)
            og_desc = yaml['hover_text']

            pages = []
            for i in range(1, yaml['pages'] + 1):
                pages.append('/' + section_name + '/' + item_id + '/p' + str(i) + '.jpg')

            item = {'name': yaml['hover_text'],
                    'desc': desc,
                    'og_desc': og_desc,
                    'cover': '/' + section_name + '/' + item_id + '/cover.jpg'}
            return render_template('comics.html', item=item, prev=prev, next=next, pages=pages)
    return 'Sorry, cartoon not found'


@app.route("/cartoons/<path:path>")
def cartoon_page(path):
    return render_animated_subpage('cartoons', path, reverse=False)


@app.route("/misc/<path:path>")
def misc_page(path):
    return render_animated_subpage('misc', path)


@app.route("/princess/<path:path>")
def princess_page(path):
    return render_animated_subpage('princess', path)


@app.route("/princess_seasons/<path:path>")
def princess_season_page(path):
    return render_animated_subpage('princess_seasons', path)


@app.route("/flat/<path:path>")
def flat_page(path):
    return render_flat_subpage('flat', path)


@app.route("/projects/<path:path>")
def projects_page(path):
    return render_flat_subpage('projects', path)


@app.route("/comics/<path:path>")
def comics_page(path):
    return render_comics_subpage('comics', path)


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")
    # return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
