from flask import *
from pathlib import Path
from rauth import OAuth2Service
import os
import binascii

base_dir = Path(__file__).parents[1]
static_dir = base_dir / "frontend" / "static"


app = Flask(__name__,
            static_folder=static_dir)


@app.route("/")
def index():
    return render_template("html/index.html")


if __name__ == "__main__":
    app.run(debug=True)


# coding: utf-8





# Read secret keys from env vars
# See: http://12factor.net/config
GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']

app = Flask(__name__)
app.secret_key = os.environ['SESSION_SECRET_KEY']  # necessary for session

# Set up service wrapper for GitHub
# - `client_id` and `client_secret`: available in an application page of GitHub
# - `name`: name for human
# - `authorize_url` and `access_token_url`: available in the GitHub's developer guide
#    http://developer.github.com/v3/oauth/#web-application-flow
# - `base_url`: base url for calling API
github = OAuth2Service(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    base_url='https://api.github.com/')


@app.route('/')
def top():
    """
    Top page
    """

    # For authorized users, show welcome message and links
    if 'username' in session:
        return 'Welcome @{0}! <a href="/repos">Repos</a> <a href="/logout">Logout</a>'.format(
            session['username'])

    # Generte and store a state in session before calling authorize_url
    if 'oauth_state' not in session:
        session['oauth_state'] = binascii.hexlify(os.urandom(24))

    # For unauthorized users, show link to sign in
    authorize_url = github.get_authorize_url(scope='', state=session['oauth_state'])
    return '<a href="{0}">Sign in with GitHub</a>'.format(authorize_url)


@app.route('/callback/github')
def callback():
    """
    OAuth callback from GitHub
    """

    code = request.args['code']
    state = request.args['state'].encode('utf-8')

    # Validate state param to prevent CSRF
    if state != session['oauth_state']:
        abort(400)

    # Request access token
    auth_session = github.get_auth_session(data={'code': code})
    session['access_token'] = auth_session.access_token

    # Call API to retrieve username.
    # `auth_session` is a wrapper object of requests with oauth access token
    r = auth_session.get('/user')
    session['username'] = r.json()['login']

    return redirect('/')


@app.route('/logout')
def logout():
    """
    Logout
    """

    # Delete session data
    session.pop('username')
    session.pop('access_token')

    return redirect('/')


@app.route('/repos')
def repos():
    """
    List recently updated repositories
    """

    # Restore auth_session from the access_token stored in session
    auth_session = github.get_session(session['access_token'])
    r = auth_session.get('/user/repos', params={'sort': 'updated'})
    repos = r.json()

    list_items = []
    for repo in repos:
        list_items.append('<li>{0}</li>'.format(repo['full_name']))

    return '<ul>{0}</ul>'.format('\n'.join(list_items))


if __name__ == '__main__':
    app.run(debug=True)