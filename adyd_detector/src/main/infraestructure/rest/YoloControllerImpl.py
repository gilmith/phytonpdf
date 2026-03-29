import threading

from adyd_detector_api.models import DetectDto
from flask import jsonify
from injector import inject
from loguru import logger as log

from src.main.application.service.yolo.YoloApplicationService import YoloApplicationService
from src.main.domain.model.yolo.DetectDom import DetectDom


class YoloControllerImpl:

    @inject
    def __init__(self, yolo_application: YoloApplicationService):
        self.yolo_application = yolo_application


    def execute_yolo(self, bucket_name: str, file_name: str):
        pass


    def execute_detect(self, bucket_name: str, file_name: str, detect_dto: DetectDto):
        pass

    def execute_detect_all(self, bucket_name: str, body: DetectDto):
        log.info("Detect yolo for all pages in the bucket {}", bucket_name)
        detect_dom = DetectDom.from_dto(file_name="", bucket_name=bucket_name, dto=body)
        self.yolo_application.execute_detect_all(detect_dom)
        return jsonify({"message": "Detect started successfully for all files in the bucket"}), 201