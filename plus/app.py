"""
Simple Python app to sign in to Google plus
"""
import os
import logging
import traceback

from flask import Flask
from flask import request
from flask import json
from flask import render_template
from flask import make_response
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import session

from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

import httplib2
from apiclient.discovery import build

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenRefreshError

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Load settings
settings = json.load(
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings.json'), 'r')
)
# Get the client id from the client secrets file
settings['client_id'] = json.load(
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../client_secrets.json'), 'r')
).get('web').get('client_id')

# Flask config
app = Flask(__name__, static_folder='../static', static_url_path='', template_folder='../templates')
app.secret_key = settings['flask']['secret_key']

# This will replace the app's session handling with an in-memory key/value store
KVSessionExtension(DictStore(), app)


def create_service(service_name='plus', version='v1'):
    """
    Creates a Google service
    """
    credentials = session.get('credentials', None)
    http = httplib2.Http()
    return build(service_name, version, http=credentials.authorize(http))


class ErrorWithResponse(Exception):
    """
    Custom exception handler for responses; the error creates its own
    response object for use when the exception is caught
    """
    def __init__(self, message, response):
        super(ErrorWithResponse, self).__init__(message)
        self.response = response


def call_plus(uri, as_json=True):
    """
    Makes a call to Google Plus with the specified path and
    OAuth credentials; returns the results as a Python dictionary unless
    as_json is set to False.

    e.g.:

        try:
            result = call_plus('https://www.googleapis.com/plus/v1/people/me/people/visible')
        except ErrorWithResponse as e:
            return e.response
        return jsonify(result)
    """
    credentials = session.get('credentials', None)
    if credentials is None:
        raise ErrorWithResponse('User not logged in', make_response('User not logger in', 401))
    try:
        # Create a new authorized API client.
        http = httplib2.Http()
        http = credentials.authorize(http)
        resp, result = http.request(uri, 'GET')
    except AccessTokenRefreshError:
        raise ErrorWithResponse('Failed to refresh access token', make_response('Failed to refresh access token', 500))
    return json.loads(result) if as_json else result


@app.route('/')
def index():
    return render_template('index.html',
        app_name='Google Plus Sign-in App',
        client_id = settings['client_id']
    )


def _exchange_code_for_credentials(code):
    """
    Exchanges an auth code for credentials. These credentials can them
    be used to access a user's Google Plus data
    """
    logging.info('Exchanging code for auth token')
    try:
        # Trade the authorization code for a credentials object
        oauth_flow = flow_from_clientsecrets(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '../client_secrets.json'),
            scope=''
        )
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        logging.error('Problem with exchanging code for credentials')
    except Exception:
        logging.error('Unable to get credentials from Google Plus')
        logging.error(traceback.format_exc())

    session['credentials'] = credentials


@app.route('/login', methods=['POST'])
def login():
    try:
        code = request.data
    except ValueError as e:
        logging.error('Malformed data provided:')
        logging.error(data)
        response = make_response(json.dumps({'error' : 'Malformed data'}), 500)
    else:
        # The authorisation code used to claim credentials
        _exchange_code_for_credentials(code)
        response = make_response(json.dumps({'msg' : 'ok'}), 200)

    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/logout', methods=['GET'])
def logout():
    """
    Deauthorises the app to access the user's Google Plus account
    """
    credentials = session.get('credentials', None)
    try:
        result = call_plus('https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials.access_token, as_json=False)
    except ErrorWithResponse as e:
        return e.response
    return redirect(url_for('index'))


@app.route('/people', methods=['GET'])
def people():
    """
    GET https://www.googleapis.com/plus/v1/people/me/people/visible
    
    Returns: JSON list of people
    """
    return jsonify(create_service().people().list(userId='me', collection='visible').execute())


@app.route('/me', methods=['GET'])
def me():
    """
    GET https://www.googleapis.com/plus/v1/people/me

    Returns: JSON
    """
    return jsonify(create_service().people().get(userId='me').execute())


@app.route('/email', methods=['GET'])
def email():
    """
    GET https://www.googleapis.com/oauth2/v2/userinfo
    
    Returns:

    {
        "email": "x@y.com",
        "id": "XXXXX",
        "verified_email": true
    }
    """
    return make_response(create_service('oauth2', 'v2').userinfo().get().execute()['email'])


@app.route('/activity', methods=['GET'])
def activity():
    """
    GET https://www.googleapis.com/plus/v1/people/me/activities/public

    Returns: JSON list of user's activities
    """
    return jsonify(create_service().activities().list(userId='me', collection='public').execute())


@app.route('/moment', methods=['GET'])
def moment():
    """
    GET https://www.googleapis.com/plus/v1/people/me/moments/vault
    
    Returns JSON
    """
    return jsonify(create_service().moments().list(userId='me', collection='vault').execute())


@app.route('/moment/add', methods=['GET'])
def moment_add():
    """
    Create a moment for a user
    """
    uri = 'https://www.googleapis.com/plus/v1/people/me/moments/vault'

    moment = {
        "type": "http://schemas.google.com/AddActivity",
          "target": {
            "id": "target-id-1",
            "type":"http://schemas.google.com/AddActivity",
            "name": "This is a test moment",
            "description": "A test moment to test out posting the moments stuff!",
            "image": "http://www.artsalliancemedia.com/sites/default/files/styles/person_image/public/people/Matt-Sullivan_resized.jpg"
          }
    }
    result = create_service().moments().insert(userId='me', collection='vault', body=moment).execute()
    return str(result)


def main():
    app.debug = True
    logging.info('Starting web server')
    app.run(host='0.0.0.0', port=4567)


if __name__ == '__main__':
    main()