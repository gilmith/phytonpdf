import asyncio

from flask import jsonify, Blueprint
from injector import inject
from loguru import logger
import threading

from src.main.application.service.storage.FileApplicationService import FileApplicationService

class FileControllerImpl:
    file_blueprint = Blueprint('file_controller', __name__)

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>', methods=['GET'])
    @inject
    def list_monster_files(file_service: FileApplicationService, bucket_name):
        logger.info(f"Getting files from bucket {bucket_name}")
        try:
            files = file_service.get_all_monsters_images(bucket_name)
            return jsonify({"bucket": bucket_name, "files": files}), 200
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>/<file_name>', methods=['POST'])
    @inject
    def insert_file(file_service: FileApplicationService, bucket_name, file_name):
        logger.info(f"Inserting file {file_name} in bucket {bucket_name}")
        try:
            file_service.insert_data(bucket_name, file_name)
            return jsonify({"message": "File inserted successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>/<file_name>/split', methods=['POST'])
    @inject
    def split_file(file_service: FileApplicationService, bucket_name, file_name):
        logger.info(f"Splitting file {file_name} in bucket {bucket_name}")
        try:
            file_service.split_file(bucket_name, file_name)
            return jsonify({"message": "File inserted successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>/<file_name>/train', methods=['POST'])
    @inject
    def execute_yolo(file_service: FileApplicationService, bucket_name, file_name):
        logger.info(f"Executing yolo training on file {file_name} in bucket {bucket_name}")
        try:
            thread = threading.Thread(target=file_service.execute_yolo, args=(bucket_name, file_name))
            thread.start()
            return jsonify({"message": "YOLO training started in background"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500

    @staticmethod
    @file_blueprint.route('/files/<bucket_name>/detect', methods=['POST'])
    @inject
    def execute_detect(file_service: FileApplicationService, bucket_name):
        try:
            file_service.execute_detect(bucket_name)
            return jsonify({"message": "Detect started successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500