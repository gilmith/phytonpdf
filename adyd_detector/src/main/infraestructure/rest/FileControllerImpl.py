import threading

from adyd_detector_api.models.bucket_file_list_dto import BucketFileListDto
from flask import jsonify
from injector import inject
from loguru import logger

from src.main.application.service.storage.FileApplicationService import FileApplicationService


class FileControllerImpl:

    @inject
    def __init__(self, file_service: FileApplicationService):
        self.file_service = file_service

    def list_monster_files(self, bucket_name: str):

        """
        Lista los archivos de un bucket específico.
        @inject permite que 'file_service' sea inyectado automáticamente,
        similar a @Autowired en Spring.
        """
        logger.info(f"Petición API: Listando archivos del bucket {bucket_name}")

        try:
            files = self.file_service.get_all_monsters_images(bucket_name)

            response_data = BucketFileListDto(
                bucket=bucket_name,
                files_info=files
            )

            return response_data.to_dict(), 200

        except Exception as e:
            logger.error(f"Error al listar archivos: {str(e)}")
            return {"error": str(e)}, 500

    @inject
    def insert_file(self, bucket_name: str, file_name:str):
        logger.info(f"Inserting file {file_name} in bucket {bucket_name}")
        try:
            self.file_service.insert_data(bucket_name, file_name)
            return jsonify({"message": "File inserted successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500

    @inject
    def split_file(self, bucket_name: str, file_name: str):
        logger.info(f"Splitting file {file_name} in bucket {bucket_name}")
        try:
            self.file_service.split_file(bucket_name, file_name)
            return jsonify({"message": "File inserted successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500


    @inject
    def execute_yolo(self, bucket_name: str, file_name: str):
        logger.info(f"Executing yolo training on file {file_name} in bucket {bucket_name}")
        try:
            thread = threading.Thread(target=self.file_service.execute_yolo, args=(bucket_name, file_name))
            thread.start()
            return jsonify({"message": "YOLO training started in background"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500


    @inject
    def execute_detect(self, bucket_name: str):
        try:
            self.file_service.execute_detect(bucket_name)
            return jsonify({"message": "Detect started successfully"}), 201
        except Exception as e:
            logger.error(e)
            return jsonify({"error": str(e)}), 500