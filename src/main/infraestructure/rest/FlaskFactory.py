from flask import Flask
from src.main.infraestructure.rest.FileControllerImpl import FileControllerImpl

class FlaskAppFactory:
    def __init__(self):
        pass

    def create_app(self):
        app = Flask(__name__)
        app.register_blueprint(FileControllerImpl.file_blueprint)
        return app