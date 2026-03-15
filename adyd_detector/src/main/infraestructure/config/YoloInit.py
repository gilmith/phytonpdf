from ultralytics import YOLO


class YoloInit:

    def __init__(self, app=None):
        self.model = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.model = YOLO(r"../runs/detect/modelo_add_v1/weights/best.pt")

yolo = YoloInit()
