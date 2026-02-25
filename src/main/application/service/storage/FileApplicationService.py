from abc import ABC


class FileApplicationService(ABC):


    def get_all_monsters_images(self, bucket):
        pass

    def insert_data(self, bucket_name, file_name):
        pass

    def split_file(self, bucket_name, file_name):
        pass

    def execute_yolo(self, bucket_name, file_name):
        pass

    async def execute_detect(self, bucket_name):
        pass