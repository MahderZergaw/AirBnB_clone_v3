from flask import Blueprint, jsonify

# Create a Blueprint named app_views
app_views = Blueprint('app_views', __name__)

# Define a route /status on the app_views Blueprint


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
