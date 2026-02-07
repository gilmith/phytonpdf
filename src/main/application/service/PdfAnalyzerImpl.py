import fitz

from src.main.domain.service.pdf.PdfAnalizerPort import PdfAnalizerPort
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
        regex_stats = r"(?:CL.*TERRENO|CLTh1A).*?[:\\]\s*(.*?)\n(?:FREC.*|FREClJE).*?[:\\]\s*(.*?)\n(?:ORG.*|ORGANIZACIÓN).*?[:\\]\s*(.*)"
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for i in range(min(len(doc), len(doc))):
                page = doc.load_page(i)
                text = page.get_text().strip()
                if len(text) > 100:
                    match = re.search(regex_stats, text, re.IGNORECASE | re.MULTILINE)
                    if match:
                        nombre = match.group(1)
                        logger.info(f"Nombre detectado en página {i + 1}: {nombre}")
                    else:
                        logger.info(f"No se encontró el patrón en página {i + 1}")
