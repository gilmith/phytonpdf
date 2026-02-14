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
            imgsz=1280,
            batch=16,
            name="modelo_add_v1",
            device="cpu",
            workers=8,  # 0 para evitar problemas de multiprocessing en Windows
            val=True,  # Habilitar validación
            fraction=0.8  # 80% para entrenamiento, 20% para validación
        )

    def detect(self, imagen_bytes: bytes):
        logger.info("Detecting monsters")
        model = YOLO(r"C:\Users\jacobo\PycharmProjects\phytonpdf\runs\detect\modelo_add_v112\weights\best.pt")
        temp_image_path = "temp_detect_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(imagen_bytes)
        results = model.predict(temp_image_path, device="cpu", conf=0.25)
        for r in results:
            logger.info(r.boxes.xyxy)
            logger.info(r.names)
            for box in r.boxes:
                logger.info(box)
                logger.info(box.cls)
                logger.info(box.conf)
        os.remove(temp_image_path)
        return results
