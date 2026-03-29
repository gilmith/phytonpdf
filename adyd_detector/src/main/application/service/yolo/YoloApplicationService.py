from abc import ABC, abstractmethod
from src.main.domain.model.yolo.DetectDom import DetectDom


class YoloApplicationService(ABC):

    @abstractmethod
    def execute_detect_all(self, detect_dom: DetectDom):
        pass



