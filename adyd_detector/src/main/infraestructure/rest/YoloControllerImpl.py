import threading

from adyd_detector_api.models import DetectDto
from flask import jsonify
from injector import inject
from loguru import logger as log

from main.application.service.yolo.YoloApplicationService import YoloApplicationService
from main.domain.model.yolo.DetectDom import DetectDom


class YoloControllerImpl:

    def __init__(self, yolo_application: YoloApplicationService):
        self.yolo_application = yolo_application

    @inject
    def execute_yolo(self, bucket_name: str, file_name: str):
        pass


    @inject
    def execute_detect(self, bucket_name: str, file_name: str, detect_dto: DetectDto):
        try:
            self.yolo_application.execute_detect(DetectDom.from_dto(file_name=file_name, bucket_name=bucket_name, dto=detect_dto))
            return jsonify({"message": "Detect started successfully"}), 201
        except Exception as e:
            log.error(e)
            return jsonify({"error": str(e)}), 500