# src/main/infraestructure/rest/file_controller.py
from src.main.infraestructure.rest.FileControllerImpl import FileControllerImpl


def _get_controller() -> FileControllerImpl:
    from src.main.infraestructure.rest.FlaskFactory import injector
    return injector.get(FileControllerImpl)


def list_monster_files(bucket_name: str):
    return _get_controller().list_monster_files(bucket_name)


def insert_file(bucket_name: str, file_name:str):
    return _get_controller().insert_file(bucket_name, file_name)

def split_file(bucket_name: str, file_name: str):
    return _get_controller().split_file(bucket_name, file_name)

def execute_yolo(bucket_name: str, file_name: str):
    return _get_controller().execute_yolo(bucket_name, file_name)

def execute_detect(bucket_name: str):
    return _get_controller().execute_detect(bucket_name)