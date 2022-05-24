# Proyecto BIBLIOTECA test para R5

# Requisitos
0. python3.6 o superior
1. postgresql server (en este caso se usara una bd en postgres)
2. tener el modulo psycopg2 para acceder a la BD
3. tener instalado pip
4. instalar fastapi
    `pip install fastapi`
5. instalar uvicorn (es un server para python)
    `pip install uvicorn[standard]`
6. instalar sqlalchemy (modulo ORM para python)
    `pip install sqlalchemy`
7. instalar alembic (control de versiones de la BD para python, para realizar las migraciones)
    `pip install alembic`

# Consideraciones

1. Para crear la BD se debe correr el script que se encuentra en la carpeta SQL/biblio_test.sql.

2. Modificar el archivo database.py y el archivo alembic.init con los parametros de conexion 
    `` DATABASE_URL = "postgresql://user:password@127.0.0.1:5432/biblio_test" ``

3. para iniciar el servidor:
    `uvicorn main:app --reload`
    Nota: con esta instruccion se deben generar automaticamente las tablas en la BD
          de no ser asi hay que ejecutar;
          `alembic upgrade head` en la linea de comandos
          y `alembic revision --autogenerate -m"cualquier comentario"`
          ya con esto deben estar las tablas en la BD.
    volver a ejecutar `uvicorn main:app --reload`

4. abrir un navegador en la url: `localhost:8000/docs` para ver el swagger y la documentación de los noodos.

# Enlaces de interes

    https://fastapi.tiangolo.com/
    https://github.com/tiangolo/full-stack-fastapi-postgresql
    https://www.postgresql.org/
    https://swagger.io/
    https://www.json.org/json-es.html
    https://www.python.org/
    https://git-scm.com/
    https://developers.google.com/books/docs/v1/using
    https://www.linux.org/
    https://ubuntu.com/

    
