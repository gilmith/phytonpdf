from pymongo import MongoClient
class MongoDB:
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.client = MongoClient("mongodb://localhost:27017/adyd",
            maxPoolSize=20,
            minPoolSize=5,
            serverSelectionTimeoutMS=5000
        )

mongo = MongoDB() # Instancia global vacía