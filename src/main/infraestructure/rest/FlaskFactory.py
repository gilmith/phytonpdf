from flask import Flask

from src.main.infraestructure.config.MongoConfig import MongoConfig
from src.main.infraestructure.config.YoloInit import yolo


class FlaskAppFactory:
    def __init__(self):
        pass

    def create_app(self):
        from src.main.infraestructure.rest.FileControllerImpl import FileControllerImpl
        app = Flask(__name__)
        MongoConfig.init_db()
        yolo.init_app(app)
        app.register_blueprint(FileControllerImpl.file_blueprint)
        return app