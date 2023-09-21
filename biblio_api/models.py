"""coding=utf-8."""
 
from ast import Str
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from biblio_api.database import Base
#from database import Base


class Libros(Base):

	__tablename__ = "tbl_libros"

	id = Column(Integer, primary_key=True, index=True)
	id_categoria = Column(Integer, ForeignKey('tbl_categorias.id'))
	titulo = Column(String)
	subtitulo = Column(String)
	autor = Column(String)	
	fecha_publicacion = Column(DateTime)
	editor = Column(String)
	descripcion = Column(String)
	disponible = Column(Boolean, default= True)
	url_imagen = Column(String)
	categorias = relationship("Categorias", backref="tbl_libros")


class Categorias(Base):

	__tablename__ = "tbl_categorias"

	id = Column(Integer, primary_key=True, index=True)
	categoria = Column(String)
	descripcion = Column(Text())
	libros = relationship("Libros", back_populates="categorias")

class Usuarios(Base):

	__tablename__ = "tbl_usuarios"

	id = Column(Integer, primary_key=True, index=True)
	nombre = Column(String)
	email = Column(String)
	clave = Column(String)
	fecha_ingreso = Column(DateTime)













