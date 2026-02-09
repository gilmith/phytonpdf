from injector import inject
from minio import Minio, S3Error
from loguru import logger
from minio.datatypes import Object

from src.main.domain.model.FileInfo.FileInfoDom import FileInfoDom
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

    def list_files(self, bucket_name: str) -> list[FileInfoDom]:
        files = self.client.list_objects(bucket_name)
        files_info = []
        for file in files:
            files_info.append(FileInfoDom(file.object_name, file.size, FileUnit.BYTES.value, file.content_type,  file.last_modified, self._analize_file(bucket_name, file)))
        return files_info

    def insertData(self, bucket_name, file_name):
        try:
            file_full = self.client.get_object(bucket_name, file_name)
            data = file_full.read()
            return self.pdf_analyzer.analyze_header(file_name, data)
        except S3Error as e:
            logger.error(e)
            raise

    def get_file(self, bucket_name, file_name):
        file_full = self.client.get_object(bucket_name, file_name)
        data = file_full.read()
        doc = fitz.open(stream=data, filetype="pdf")
        images = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # 2. Renderizar la página a una imagen (pixmap)
            # alpha=False elimina transparencias para evitar fondos negros
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)

            # 3. Convertir a formato que puedas manipular o guardar
            img_data = pix.tobytes("png")

            # Opcional: Si quieres trabajar con la imagen en memoria (Pillow)
            # img = Image.open(io.BytesIO(img_data))

            images.append({
                "page": page_num + 1,
                "bytes": img_data
            })

        doc.close()
        return images


    def _analize_file(self, bucket_name: str, file: Object) -> bool:
        try:
            file_full = self.client.get_object(bucket_name, file.object_name)
            data = file_full.read()
            return self.pdf_analyzer.has_ocr(file.object_name, data)
        except S3Error as e:
            logger.error(e)
            raise