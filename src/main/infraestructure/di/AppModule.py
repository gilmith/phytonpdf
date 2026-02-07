from injector import Module, singleton, provider

from src.main.application.service.PdfAnalyzerImpl import PdfAnalyzerImpl
from src.main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from src.main.infraestructure.storage.FileStorageImpl import FileStorageImpl
from src.main.application.service.FileService import FileService

class AppModule(Module):
    def __init__(self, minio_conf):
        self.minio_conf = minio_conf

    @singleton
    @provider
    def provide_pdf_analyzer(self) -> PdfAnalizerPort:
        return PdfAnalyzerImpl()

    @singleton
    @provider
    def provide_file_storage(self, pdf_analyzer: PdfAnalizerPort) -> FileStorageImpl:
        return FileStorageImpl(
            self.minio_conf['endpoint'],
            self.minio_conf['access_key'],
            self.minio_conf['secret_key'],
            pdf_analyzer
        )

    @singleton
    @provider
    def provide_file_service(self, storage: FileStorageImpl) -> FileService:
        return FileService(storage)
