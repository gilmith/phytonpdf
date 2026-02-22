from pydantic import BaseModel


class image_dto(BaseModel):
    bucket_name : str
    file_name : str
    crop_name: str

