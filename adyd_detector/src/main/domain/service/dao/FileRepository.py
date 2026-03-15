from abc import ABC, abstractmethod

from src.main.domain.model.FileInfo.AnalyzedFileDom import AnalyzedFileDom


class FileRepository(ABC):

    @abstractmethod
    async def insertOne(self, file_info_dom: AnalyzedFileDom):
        pass
