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
        self.pdf_analyzer.split_in_jpg(file_data, bucket_name, file_name)

    def execute_yolo(self, bucket_name, file_name):
        self.yolo_detector.train(bucket_name, file_name)
