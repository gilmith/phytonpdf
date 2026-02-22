import os

import cv2
from loguru import logger

from src.main.application.service.storage.FileApplicationService import FileApplicationService
from src.main.domain.service.yolo.YoloDetector import YoloDetector
from src.main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from src.main.domain.service.storage.FileStoragePort import FileStoragePort


class FileApplicationServiceImpl(FileApplicationService):
    def __init__(self, storage_port: FileStoragePort, pdf_analyzer: PdfAnalizerPort, yolo_detector: YoloDetector):
        self.storage = storage_port
        self.pdf_analyzer = pdf_analyzer
        self.yolo_detector = yolo_detector

    def get_all_monsters_images(self, bucket):
        return self.storage.list_files(bucket)

    def insert_data(self, bucket_name, file_name):
        return self.storage.insertData(bucket_name, file_name)

    def split_file(self, bucket_name, file_name):
        file_data = self.storage.get_file(bucket_name, file_name)
        jpg_path = self.pdf_analyzer.split_in_jpg(file_data, bucket_name, file_name)
        self.storage.upload_jpg(bucket_name + "jpg", jpg_path)

    def execute_yolo(self, bucket_name, file_name):
        self.yolo_detector.train(bucket_name, file_name)

    def execute_detect(self, bucket_name):
        logger.info("Detecting...")
        files_in_bucket = self.storage.list_files(bucket_name)
        for file in files_in_bucket:
            file_data = self.storage.get_file(bucket_name, file.file_name)
            list_result = self.yolo_detector.detect(file_data)
            home_dir = os.path.expanduser("~")
            results_dir = os.path.join(home_dir, "yolo_results")
            os.makedirs(results_dir, exist_ok=True)
            for i, r in enumerate(list_result):
                im_orig = r.orig_img
                for j, box in enumerate(r.boxes):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    name = r.names[cls]
                    crop = im_orig[y1:y2, x1:x2]
                    file_name = f"{results_dir}/{name}_{i}_{j}.jpg"
                    cv2.imwrite(file_name, crop)
                    logger.info(f"Guardado: {file_name}")