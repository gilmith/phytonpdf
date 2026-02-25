import asyncio
import os

from loguru import logger

from src.main.domain.model.FileInfo.AnalyzedFileDom import AnalyzedFileDom
from src.main.domain.model.FileInfo.FileInfoDom import FileInfoDom
from src.main.domain.service.dao.FileRepository import FileRepository
from src.main.application.service.storage.FileApplicationService import FileApplicationService
from src.main.domain.service.yolo.YoloDetector import YoloDetector
from src.main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from src.main.domain.service.storage.FileStoragePort import FileStoragePort


class FileApplicationServiceImpl(FileApplicationService):
    def __init__(self, storage_port: FileStoragePort, pdf_analyzer: PdfAnalizerPort, yolo_detector: YoloDetector
                 , file_repository : FileRepository):
        self.storage = storage_port
        self.pdf_analyzer = pdf_analyzer
        self.yolo_detector = yolo_detector
        self.file_repository = file_repository

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
            list_file_analyzed = []
            for i, r in enumerate(list_result):
                im_orig = r.orig_img
                for j, box in enumerate(r.boxes):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    type_file = r.names[cls]
                    crop = im_orig[y1:y2, x1:x2]
                    list_file_analyzed.append(FileInfoDom(file_name=file.file_name, type_file=type_file, content=crop))
                    #file_name = f"{results_dir}/{type}_{i}_{j}.jpg"
                    #cv2.imwrite(file_name, crop)
                    self._analyze_list_result(list_file_analyzed)

    def _analyze_list_result(self, list_file_analyzed: list[FileInfoDom]):
        logger.info("Analyzing...")
        success = False
        index = 0
        while not success and index < len(list_file_analyzed) and len(list_file_analyzed) > 0:
            if list_file_analyzed[index].type_file == "nombre":
                logger.info("Successful detection!!")
                success = True
                file_analyzed = AnalyzedFileDom(monster_name=list_file_analyzed[index].type_file,success=True)
                self.file_repository.insertOne(file_analyzed)
            index += 1


