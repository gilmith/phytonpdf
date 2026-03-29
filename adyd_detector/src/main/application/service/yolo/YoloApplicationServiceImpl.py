from injector import inject
from loguru import logger as log

from src.main.application.service.yolo.YoloApplicationService import YoloApplicationService
from src.main.domain.model.yolo.DetectDom import DetectDom
from src.main.domain.service.storage.FileStoragePort import FileStoragePort
from src.main.domain.service.yolo.YoloDetector import YoloDetector


class YoloApplicationServiceImpl(YoloApplicationService):

 @inject
 def __init__(self, yolo_detector: YoloDetector, storage: FileStoragePort):
   self.yolo_detector = yolo_detector
   self.storage = storage

 def execute_detect_all(self, detect_dom: DetectDom):
    log.info("Detecting labels in image {} in bucket {}", detect_dom.file_name, detect_dom.bucket_name)
    files_in_bucket = self.storage.list_files(detect_dom.bucket_name)
    for file in files_in_bucket:
        log.info("Initializing detect")
        file_data = self.storage.get_file(detect_dom.bucket_name, file.file_name)
        data = self.yolo_detector.detect(file_data, detect_dom)
        self.yolo_detector.analyze_resultset(data, file.file_name)
