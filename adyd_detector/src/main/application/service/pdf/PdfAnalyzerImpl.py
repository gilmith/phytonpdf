import os
from pathlib import Path

import fitz

from main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
from loguru import logger
import re


class PdfAnalyzerImpl(PdfAnalizerPort):

    def has_ocr(self, file_name: str, file_bytes: bytes) -> bool:
        logger.info(f"Analyzing file {file_name}")
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for i in range(min(len(doc), 10)):
                page = doc.load_page(i)
                text = page.get_text().strip()
                if len(text) > 50:
                    logger.info(f"Text detected {i + 1}")
                    return True
            logger.warning("no text detected.")
            return False

    def analyze_header(self, file_name: str, file_bytes: bytes) -> None:
        logger.info(f"Analyzing header of file {file_name}")
        regex_first_paragraph = r"^([^\n]+)"
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for i in range(5, len(doc)):
                page = doc.load_page(i)
                text = page.get_text().strip()
                if len(text) > 100:
                    match = re.search(regex_first_paragraph, text, re.MULTILINE)
                    if match:
                        nombre = match.group(1)
                        logger.info(f"Primer párrafo detectado en página {i + 1}: {nombre}")
                    else:
                        logger.info(f"No se encontró un párrafo en página {i + 1}")

    def split_in_jpg(self, file_data: bytes, bucket_name: str, file_name: str, zoom: int = 3) -> Path:
        home = Path.home()
        path = home / "pdf_split" / bucket_name / file_name.split(".")[0]
        os.makedirs(path, exist_ok=True)
        with fitz.open(stream=file_data, filetype="pdf") as doc:
            matrix = fitz.Matrix(zoom, zoom)
            for i in range(len(doc)):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=matrix)
                pix.save(f"{path}/page-{i}.jpg", "jpeg", 100)
        return path
