from injector import Module, singleton, provider

from src.main.domain.service.storage.FileStoragePort import FileStoragePort
# Solo interfaces y tipos para anotaciones
from src.main.domain.service.yolo.YoloDetector import YoloDetector
from src.main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from src.main.application.service.storage.FileApplicationService import FileApplicationService


class AppModule(Module):
    def __init__(self, minio_conf):
        self.minio_conf = minio_conf

    @singleton
    @provider
    def provide_pdf_analyzer(self) -> PdfAnalizerPort:
        from src.main.application.service.pdf.PdfAnalyzerImpl import PdfAnalyzerImpl

        return PdfAnalyzerImpl()

    @singleton
    @provider
    def provide_file_storage(self, pdf_analyzer: PdfAnalizerPort) -> FileStoragePort:
        from src.main.infraestructure.storage.FileStorageImpl import FileStorageImpl

        return FileStorageImpl(
            self.minio_conf['endpoint'],
            self.minio_conf['access_key'],
            self.minio_conf['secret_key'],
            pdf_analyzer
        )

    @singleton
    @provider
    def provide_file_service(self, storage: FileStoragePort, pdf_analyzer: PdfAnalizerPort, yolo_detector: YoloDetector) -> FileApplicationService:
        from src.main.application.service.storage.FileApplicationServiceImpl import FileApplicationServiceImpl

        return FileApplicationServiceImpl(storage, pdf_analyzer, yolo_detector)

    @singleton
    @provider
    def provide_yolo_detector(self) -> YoloDetector:
        from src.main.infraestructure.yolo.YoloDetectorImpl import YoloDetectorImpl

        return YoloDetectorImpl()
