from adyd_detector_api.models import DetectDto
from loguru import logger as log

from main.application.service.yolo.YoloApplicationService import YoloApplicationService
from main.domain.model.yolo.DetectDom import DetectDom
from main.domain.service.storage.FileStoragePort import FileStoragePort
from main.domain.service.yolo.YoloDetector import YoloDetector


class YoloApplicationServiceImpl(YoloApplicationService):

    def __init__(self, yolo_detector: YoloDetector, storage: FileStoragePort):
        self.yolo_detector = yolo_detector
        self.storage = storage


def execute_yolo(self, bucket_name, file_name):
    self.yolo_detector.train(bucket_name, file_name)


def execute_detect(self, detect_dom: DetectDom):
    log.info("Detecting labels in image {} in bucket {}", detect_dom.file_name, detect_dom.bucket_name)
    files_in_bucket = self.storage.list_files(detect_dom.bucket_name)
    for file in files_in_bucket:
        if file.file_name == detect_dom.file_name:
            log.info("Initializing detect")
            file_data = self.storage.get_file(detect_dom.bucket_name, file.file_name)
            data = self.yolo_detector.detect(file_data, detect_dom)
            self.yolo_detector.analyze_resultset(data, file.file_name)
