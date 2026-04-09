import connexion
from importlib import resources

from connexion import Resolver
from flask_injector import FlaskInjector
from injector import Injector
from loguru import logger

from src.main.infraestructure.config.MongoConfig import MongoConfig
from src.main.infraestructure.config.YoloInit import yolo
from src.main.infraestructure.di.AppModule import AppModule

# Singleton global accesible desde cualquier puente
injector: Injector = None

class FlaskAppFactory:
    def __init__(self):
        self.package_name = 'adyd_detector_api'
        self.yaml_name = 'openapi.yaml'

    def create_app(self, minio_conf):
        global injector

        # 1. Localizamos la ruta del YAML
        try:
            pkg_path = resources.files(self.package_name).joinpath("openapi").joinpath(self.yaml_name)
            try:
                with resources.as_file(pkg_path) as yaml_path:
                    if yaml_path.is_file():
                        spec_dir = str(yaml_path.parent)
                        logger.info(f"spec_dir: ", spec_dir)
                    else:
                        raise FileNotFoundError()
            except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
                pkg_path = resources.files(self.package_name).joinpath(self.yaml_name)
                with resources.as_file(pkg_path) as yaml_path:
                    spec_dir = str(yaml_path.parent)

        except Exception as e:
            raise FileNotFoundError(f"No se pudo localizar {self.yaml_name} en el paquete {self.package_name}: {e}")

        # 2. Creamos la instancia de Connexion
        connexion_app = connexion.App('', specification_dir=spec_dir)
        connexion_app.add_api(
            self.yaml_name,
            arguments={'title': 'Detector API'},
            pythonic_params=True
        )

        # 3. Configuración Flask
        flask_app = connexion_app.app
        MongoConfig.init_db()
        yolo.init_app(flask_app)

        # 4. Inyección de dependencias — exponemos el injector como singleton
        flask_injector = FlaskInjector(app=flask_app, modules=[AppModule(minio_conf)])
        injector = flask_injector.injector

        return connexion_app