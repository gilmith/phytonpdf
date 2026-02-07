from flask import jsonify, Blueprint
from injector import inject
from loguru import logger

from src.main.application.service.FileService import FileService

class FileControllerImpl:
    file_blueprint = Blueprint('file_controller', __name__)

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>', methods=['GET'])
    @inject
    def list_monster_files(file_service: FileService, bucket_name):
        logger.info(f"Getting files from bucket {bucket_name}")
        try:
            files = file_service.get_all_monsters_images(bucket_name)
            return jsonify({"bucket": bucket_name, "files": files}), 200
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>/<file_name>', methods=['POST'])
    def insert_file(file_service: FileService, bucket_name, file_name):
        logger.info(f"Inserting file {file_name} in bucket {bucket_name}")
        try:
            file_service.insert_data(bucket_name, file_name)
            return jsonify({"message": "File inserted successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500