
from mongoengine import connect

class MongoConfig:

    @staticmethod
    def init_db():
        # Configuramos el Pool al conectar
        connect(
            db="adyd",
            host="mongodb://localhost:27017",
            username="root",
            password="pass4root",
            authentication_source="admin",
            # CONFIGURACIÓN DEL POOL:
            maxPoolSize=50,       # Máximo de conexiones simultáneas
            minPoolSize=10,       # Mantener siempre 10 conexiones abiertas
            waitQueueTimeoutMS=5000 # Tiempo máximo de espera por una conexión libre
        )