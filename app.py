import sys
sys.path.append('/home/jawa/Desktop/SNA/rfid')

from flask import Flask,send_from_directory
from flask import Flask, redirect, url_for, request, render_template, session
from src import get_config

from blueprints import home,api

application = app = Flask(__name__, static_folder='assets', static_url_path="/")
app.secret_key = get_config("secret_key")
# app.register_blueprint()

#TODO: Automate importing blueprints from blueprints folder

app.register_blueprint(home.bp)
app.register_blueprint(api.bp)

# @app.after_request
# def add_cache_control(response):
#     response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache the response for 1 hour
#     return response

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=7000, debug=True)
