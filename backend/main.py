import os

from flask import Flask

from backend.core_api import api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # доступ ко всем эндпоинтам??
    CORS(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    @app.route('/')
    def hello():
        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/api/report/" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

    app.register_blueprint(api, url_prefix='/api/')

    return app
