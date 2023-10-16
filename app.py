from flask import Flask
from src import get_config
from blueprints import home,api

app = Flask(__name__, static_folder='assets', static_url_path="/")
app.secret_key = get_config("secret_key")

app.register_blueprint(home.bp)
app.register_blueprint(api.bp)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=7000, debug=True)
