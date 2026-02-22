from loguru import logger
from ultralytics import YOLO

from src.main.infraestructure.config.YoloInit import yolo
from src.main.domain.service.yolo.YoloDetector import YoloDetector
import os


class YoloDetectorImpl(YoloDetector):

    def __init__(self):
        pass

    def train(self, bucket_name: str, file_name: str):
        logger.info("Detecting monsters")
        path_yaml = r"C:\Users\jacobo\PycharmProjects\phytonpdf\src\main\resources\dataset\data.yaml"
        results_dir = r"C:\Users\jacobo\PycharmProjects\phytonpdf\runs\detect\modelo_add_v1\weights"
        last_ckpt = os.path.join(results_dir, "last.pt")
        total_epochs = 40
        # Si existe last.pt, continuar desde ahí
        if os.path.exists(last_ckpt):
            logger.info(f"Cargando checkpoint: {last_ckpt}")
            model = YOLO(last_ckpt)
            resume = True
        else:
            logger.info("Entrenando desde cero (yolov8n.pt)")
            model = YOLO("yolov8n.pt")
            resume = False
        logger.info(f"Entrenando por {total_epochs} épocas (resume={resume})")
        model.train(
            data=path_yaml,
            epochs=total_epochs,
            imgsz=1280,
            batch=10,
            name="modelo_add_v1",
            device="cpu",
            workers=0,
            val=True,
            fraction=0.8,
            resume=resume
        )

    def detect(self, imagen_bytes: bytes):
        logger.info("Detecting monsters")
        temp_image_path = "temp_detect_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(imagen_bytes)

        if yolo.model is None:
             raise Exception("YOLO model not initialized in ServiceRegistry")

        results = yolo.model.predict(temp_image_path, device="cpu", conf=0.50, show=False)
        os.remove(temp_image_path)
        return results
