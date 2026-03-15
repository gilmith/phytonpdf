import yaml
from flask_injector import FlaskInjector
from src.main.infraestructure.di.AppModule import AppModule
from src.main.infraestructure.rest.FlaskFactory import FlaskAppFactory
from src.main.infraestructure.config.logger import configure_logger, get_logger


def load_config(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config('./resources/config.yaml')
    configure_logger('./resources/config.yaml')
    logger = get_logger()
    logger.info('Configuración de logger cargada')
    minio_conf = config['minio']
    app = FlaskAppFactory().create_app(minio_conf)
    logger.info('Aplicación Flask iniciada')
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()