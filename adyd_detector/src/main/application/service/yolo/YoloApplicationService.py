from abc import ABC
from main.domain.model.yolo.DetectDom import DetectDom


class YoloApplicationService(ABC):

    def execute_yolo(self, bucket_name, file_name):
        pass

    def execute_detect(self, detect_dom: DetectDom):
        pass



