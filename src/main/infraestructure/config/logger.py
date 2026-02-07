from loguru import logger
import yaml
import sys

# Carga configuración desde YAML

def configure_logger(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    log_conf = config.get('logging', {})
    logger.remove()  # Elimina el handler por defecto
    # Configuración básica
    log_level = log_conf.get('level', 'INFO')
    log_format = log_conf.get('format', "<green>{time}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    log_file = log_conf.get('file')
    rotation = log_conf.get('rotation', '10 MB')
    retention = log_conf.get('retention', '7 days')
    # Añade handler para archivo
    if log_file:
        logger.add(log_file, level=log_level, format=log_format, rotation=rotation, retention=retention)
    # Añade handler para consola
    logger.add(sys.stdout, level=log_level, format=log_format)

# Exporta logger para uso global
def get_logger():
    return logger
