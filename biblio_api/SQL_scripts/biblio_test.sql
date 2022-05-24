/*
Archivo para crear la base de datos de manera manual

*/

CREATE DATABASE "biblio_test";

-- public.tbl_libros definition

-- Drop table

-- DROP TABLE public.tbl_libros;

CREATE TABLE public.tbl_libros (
	id serial4 NOT NULL,
	id_categoria int4 NULL,
	titulo varchar NULL,
	subtitulo varchar NULL,
	autor varchar NULL,
	fecha_publicacion timestamp NULL,
	editor varchar NULL,
	descripcion varchar NULL,
	disponible bool NULL,
	url_imagen varchar NULL,
	CONSTRAINT tbl_libros_pkey PRIMARY KEY (id),
	CONSTRAINT tbl_libros_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.tbl_categorias(id)
);
CREATE INDEX ix_tbl_libros_id ON public.tbl_libros USING btree (id);

-- public.tbl_categorias definition

-- Drop table

-- DROP TABLE public.tbl_categorias;

CREATE TABLE public.tbl_categorias (
	id serial4 NOT NULL,
	categoria varchar NULL,
	descripcion text NULL,
	CONSTRAINT tbl_categorias_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_tbl_categorias_id ON public.tbl_categorias USING btree (id);