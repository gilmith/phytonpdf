from loguru import logger
from ultralytics import YOLO

from src.main.domain.service.yolo.YoloDetector import YoloDetector
import os

class YoloDetectorImpl(YoloDetector):

    def __init__(self):
        pass

    def train(self, bucket_name: str, file_name: str):
        logger.info("Detecting monsters")
        model = YOLO("yolov8n.pt")
        path_yaml = r"C:\Users\jacobo\PycharmProjects\phytonpdf\src\main\resources\dataset\data.yaml"
        model.train(
            data=path_yaml,
            epochs=100,
            imgsz=640,
            batch=16,  #
            name="modelo_add_v1",
            device="cpu",
            workers=0
        )

    def detect(self, imagenbytes: bytes):
        logger.info("Detecting monsters")
        model = YOLO("yolov8n.pt")
        path_yaml = r"C:\Users\jacobo\PycharmProjects\phytonpdf\src\main\resources\dataset\data.yaml"
        model.train(
            data=path_yaml,
            epochs=100,
            imgsz=640,
            batch=16,  #
            name="modelo_add_v1",
            device="cpu",
            workers=0
        )