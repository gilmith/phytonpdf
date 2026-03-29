import io
import threading
from typing import List

import cv2
import numpy as np
from loguru import logger
from PIL import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results

from src.main.domain.model.FileInfo.AnalyzedFileDom import AnalyzedFileDom
from src.main.domain.model.FileInfo.FileInfoDom import FileInfoDom
from src.main.domain.model.yolo.DetectDom import DetectDom
from src.main.domain.service.dao.FileRepository import FileRepository
from src.main.domain.service.ocr.OcrService import OcrService
from src.main.infraestructure.config.YoloInit import yolo
from src.main.domain.service.yolo.YoloDetector import YoloDetector
import os

_yolo_lock = threading.Lock()  # ← lock global a nivel de módulo


class YoloDetectorImpl(YoloDetector):

    def __init__(self, file_repository: FileRepository, ocr: OcrService):
        self.file_repository =  file_repository
        self.ocr = ocr

    def train(self, bucket_name: str, file_name: str):
        logger.info("Detecting monsters")
        path_yaml = r"/main/resources/dataset/data.yaml"
        results_dir = r"/runs/detect/modelo_add_v12/weights"
        last_ckpt = os.path.join(results_dir, "last.pt")
        total_epochs = 100
        # Si existe last.pt, continuar desde ahí
        if os.path.exists(last_ckpt):
            logger.info(f"Cargando checkpoint: {last_ckpt}")
            model = YOLO(last_ckpt,)
            resume = True
        else:
            logger.info("Entrenando desde cero (yolov26n.pt)")
            model = YOLO("yolo26n.pt")
            resume = False
        logger.info(f"Entrenando por {total_epochs} épocas (resume={resume})")
        model.train(
            data=path_yaml,
            epochs=total_epochs,
            imgsz=1280,
            batch=5,
            name="modelo_add_v1",
            device="cpu",
            workers=0,
            val=True,
            fraction=0.8,
            resume=resume
        )

    def detect(self, imagen_bytes: bytes, detect_dom: DetectDom) -> List[Results]:
        logger.info("Detecting monsters")

        if yolo.model is None:
            raise Exception("YOLO model not initialized in ServiceRegistry")

        pil_img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        img = np.ascontiguousarray(cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))

        with _yolo_lock:
            results = yolo.model.predict(img, device="cpu", conf=0.75, show=False)

        return results

    def analyze_resultset(self, list_result, file_name: str):
        home_dir = os.path.expanduser("~")
        results_dir = os.path.join(home_dir, "yolo_results")
        os.makedirs(results_dir, exist_ok=True)
        list_file_analyzed = []
        for i, r in enumerate(list_result):
            im_orig = r.orig_img
            for j, box in enumerate(r.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                type_file = r.names[cls]
                crop = np.ascontiguousarray(im_orig[y1:y2, x1:x2])
                _, crop_bytes = cv2.imencode('.jpg', crop)
                logger.debug(f"Detección [{i},{j}] → clase='{type_file}' | bbox=({x1},{y1},{x2},{y2})")
                list_file_analyzed.append(FileInfoDom(file_name=file_name, type_file=type_file, content=crop_bytes.tobytes()))
        # Una vez recorridos todos los resultados, analiza la lista completa
        self._analyze_list_result(list_file_analyzed)

    def _analyze_list_result(self, list_file_analyzed: list[FileInfoDom]):
        logger.info("Analyzing...")
        success = False
        index = 0
        while not success and index < len(list_file_analyzed) and len(list_file_analyzed) > 0:
            if list_file_analyzed[index].type_file == "nombre":
                logger.info("Successful detection!!")
                success = True
                nombre = self.ocr.analyze_nombre(list_file_analyzed[index].content)
                self.file_repository.insertOne(AnalyzedFileDom(monster_name=nombre, success=True))
            index += 1
        pass
