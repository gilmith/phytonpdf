from loguru import logger

from src.main.domain.model.FileInfo.AnalyzedFileDom import AnalyzedFileDom
from src.main.domain.service.dao.FileRepository import FileRepository
from src.main.infraestructure.mongodb.document.AnalyzedFileDocument import AnalyzedFileDocument

class FileRepositoryImpl(FileRepository):

    def insertOne(self, analyzed_file: AnalyzedFileDom):
        logger.info("Saving info to MongoDB...")

        # 1. Extraemos los datos del objeto de Dominio (Pydantic)
        data = analyzed_file.model_dump(exclude={'id'})

        # 2. Creamos el documento de infraestructura
        # Asegúrate de que AnalyzedFileDocument tenga los mismos nombres de campos
        file_analyzed = AnalyzedFileDocument(**data)

        # 3. Guardado síncrono (Sin await)
        file_analyzed.save()
        logger.info("Info saved successfully")