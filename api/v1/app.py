#!/usr/bin/python3
'''
Create Flask app; and register the blueprint app_views to Flask instance app.
'''
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    '''
    function to tear down app context so that the storage is closed
    '''
    storage.close()

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.register_blueprint(app_views, url_prefix="/api/v1")
    app.run(host=host, port=port, threaded=True)
