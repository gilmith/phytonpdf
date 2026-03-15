from loguru import logger
from main.domain.service.dao.FileRepository import FileRepository
from main.application.service.storage.FileApplicationService import FileApplicationService
from main.domain.service.yolo.YoloDetector import YoloDetector
from main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from main.domain.service.storage.FileStoragePort import FileStoragePort


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
            self.yolo_detector.analyze_resultset(self.yolo_detector.detect(file_data), file.file_name)



