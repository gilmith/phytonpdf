from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime

class AnalyzedFileDocument(Document):
    # MongoEngine usa 'meta' para el nombre de la colección, no 'Settings'
    meta = {'collection': 'analyzed_files'}

    # Los campos deben ser instancias de los campos de mongoengine
    monster_name = StringField(required=True)
    url = StringField()
    analyze_date = DateTimeField(default=datetime.now)
    success = BooleanField(default=False)