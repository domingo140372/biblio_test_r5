"""coding=utf-8."""
 
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator
from sqlalchemy.orm import Query

class OrmBase(BaseModel):
    # Common properties across orm models
    id: int

    # Pre-processing validator that evaluates lazy relationships before any other validation
    # NOTE: If high throughput/performance is a concern, you can/should probably apply
    #       this validator in a more targeted fashion instead of a wildcard in a base class.
    #       This approach is by no means slow, but adds a minor amount of overhead for every field
    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True


class CategoriasBase(OrmBase):
	id: int


class Categorias(CategoriasBase):	
	categoria: str
	descripcion: str

	class Config:
		orm_mode = True


class CrearCategoria(Categorias):
	categoria: str
	descripcion: str


class LibrosBase(OrmBase):
	id: int


class Libros(LibrosBase):
	id_categoria: int  
	titulo: str
	subtitulo: str
	autor: str
	fecha_publicacion: datetime 
	editor: str
	descripcion: str  
	disponible: bool
	url_imagen: Optional[str]  

	class Config:
		orm_mode = True


class CrearLibro(LibrosBase):
	id_categoria: int  
	titulo: str
	subtitulo: str
	autor: str
	fecha_publicacion: datetime 
	editor: str
	descripcion: str  
	disponible: bool
	url_imagen: Optional[str]
	
	
class LibrosCategorias(Categorias):
	libros: List[Libros]