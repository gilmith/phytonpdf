from typing import Self

from adyd_detector_api.models import DetectDto
from pydantic import BaseModel, Field, ConfigDict

class DetectDom(BaseModel):
    # Configuramos Pydantic v2 para que sea estricto y permita tipos arbitrarios si fuera necesario
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)
    file_name: str = Field(default=None)
    bucket_name: str = Field(default=None)
    show: bool = Field(default=False, description="Muestra la ventana de feedback visual")
    save: bool = Field(default=False, description="Guarda los resultados en disco")
    show_labels: bool = Field(default=False) # Ejemplo de alias si el dominio interno difiere
    show_boxes: bool = Field(default=False)

    # Aquí puedes añadir métodos de lógica de negocio (Lo que no tiene el DTO)
    def should_render(self) -> bool:
        """Lógica de negocio: decide si se debe procesar visualmente"""
        return self.show or self.save

    @classmethod
    def from_dto(cls, dto: DetectDto, file_name: str, bucket_name :str) -> Self:
        """
        Constructor alternativo que mapea el DTO plano al DOM.
        """
        # Extraemos los datos del DTO (que usa propiedades con guion bajo internamente)
        # Usamos los getters públicos del DTO que ya tienes definidos
        return cls(
            file_name=file_name,
            bucket_name=bucket_name,
            show=dto.show,
            save=dto.save,
            show_boxes=dto.show_boxes,
            show_labels=dto.show_labels
        )