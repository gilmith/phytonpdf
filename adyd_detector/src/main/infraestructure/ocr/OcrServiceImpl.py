import numpy as np
import easyocr
import cv2
from loguru import logger

from main.domain.service.ocr.OcrService import OcrService


class OcrServiceImpl(OcrService):
    def __init__(self):
        self._reader = easyocr.Reader(['es', 'en'], gpu=False)

    def analyze_nombre(self, image_bytes: bytes) -> str:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            image = np.ascontiguousarray(image)
            results = self._reader.readtext(image, detail=0)
            text = " ".join(results).strip()
            logger.debug(f"OCR detectado: {text}")
            return text
        except Exception as e:
            logger.error(f"Error en OCR: {e}")
            return ""
