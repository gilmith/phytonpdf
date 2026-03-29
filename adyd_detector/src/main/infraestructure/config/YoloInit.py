import cv2
from ultralytics import YOLO


class YoloInit:

    def __init__(self, app=None):
        self.model = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Deshabilitar el pool de hilos interno de OpenCV para evitar
        # conflictos con el pool de hilos de uvicorn/a2wsgi en Windows
        cv2.setNumThreads(1)
        self.model = YOLO(r"../runs/detect/modelo_add_v1/weights/best.pt")

yolo = YoloInit()
