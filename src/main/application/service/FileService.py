from src.main.domain.service.storage.FileStoragePort import FileStoragePort


class FileService:
    def __init__(self, storage_port: FileStoragePort):
        self.storage = storage_port

    def get_all_monsters_images(self, bucket):
        return self.storage.list_files(bucket)

    def insert_data(self, bucket_name, file_name):
        return self.storage.insertData(bucket_name, file_name)