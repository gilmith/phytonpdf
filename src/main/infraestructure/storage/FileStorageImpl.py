from pathlib import Path

from injector import inject
from minio import Minio, S3Error
from loguru import logger
from minio.datatypes import Object

from src.main.domain.model.FileInfo.FileInfoStorageDom import FileInfoStorageDom
from src.main.domain.model.enum.FileUnit import FileUnit
from src.main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from src.main.domain.service.storage.FileStoragePort import FileStoragePort

class FileStorageImpl(FileStoragePort):

    @inject
    def __init__(self, endpoint, access_key, secret_key, pdf_analyzer: PdfAnalizerPort):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        self.pdf_analyzer = pdf_analyzer

    def list_files(self, bucket_name: str) -> list[FileInfoStorageDom]:
        files = self.client.list_objects(bucket_name)
        files_info = []
        for file in files:
            files_info.append(FileInfoStorageDom(file.object_name, file.size, FileUnit.BYTES.value, file.content_type, file.last_modified))
        return files_info

    def insertData(self, bucket_name, file_name):
        try:
            file_full = self.client.get_object(bucket_name, file_name)
            data = file_full.read()
            return self.pdf_analyzer.analyze_header(file_name, data)
        except S3Error as e:
            logger.error(e)
            raise

    def get_file(self, bucket_name, file_name) -> bytes:
        try:
            file_full = self.client.get_object(bucket_name, file_name)
            return file_full.read()
        except S3Error as e:
            logger.error(e)
            raise


    def _analyze_file(self, bucket_name: str, file: Object) -> bool:
        try:
            file_full = self.client.get_object(bucket_name, file.object_name)
            data = file_full.read()
            return self.pdf_analyzer.has_ocr(file.object_name, data)
        except S3Error as e:
            logger.error(e)
            raise

    def upload_jpg(self, bucket_name, jpg_path: Path):
        logger.info(f"Starting upload process. Bucket: {bucket_name}, Path: {jpg_path}")
        if self._existsBucketName(bucket_name):
            logger.info(f"Bucket {bucket_name} already exists")
        else:
            logger.info(f"Creating bucket {bucket_name}")
            self._createBucket(bucket_name)

        uploaded_count = 0
        for jpg in jpg_path.iterdir():
            if jpg.is_file() and jpg.suffix.lower() in ['.jpg', '.jpeg']:
                logger.info(f"Uploading {jpg.name} from {jpg} to bucket {bucket_name}")
                self.client.fput_object(bucket_name, jpg.name, str(jpg))
                uploaded_count += 1

        logger.info(f"Upload completed. Total files uploaded: {uploaded_count}")


    def _existsBucketName(self, bucket_name: str)-> bool:
        return self.client.bucket_exists(bucket_name)

    def _createBucket(self, bucket_name: str):
        self.client.make_bucket(bucket_name)