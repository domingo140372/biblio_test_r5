"""coding=utf-8."""
 

from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime as dtm
from google_api import *
import crud as crud
import models as models
import json 
import schemas as schemas
import requests as req

###### hasta aqui se escriben los import #######
 
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="BIBLIO API")
 
 
###### Hasta aqui va la declaracion de variables globales ######
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/libros/", response_model=List[schemas.Libros])
async def get_libros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    libros = crud.get_libros(db, skip=skip, limit=limit)
    return libros 


@app.get("/libros/titulo/{titulo}")
async def get_libros_por_titulo(titulo: str, db:Session = Depends(get_db)):
    titulos = crud.get_libros_por_titulo(db, titulo=titulo)
    parametro_valor = list(configuracion['params'].values())
    parametro_titulo = parametro_valor[0]
    if not titulos:
        url = f"{configuracion['api_link']}{parametro_titulo}{titulo}{configuracion['access_key']}"
        titulos_google = req.get(url)
        response = titulos_google.json()
    else:
        response = titulos
    
    return response


@app.get("/libros/parametros/q={parametros}")
async def get_libros_por_parametros(parametros: str, db:Session = Depends(get_db)):
    if parametros ==" ":
        raise HTTPException(status_code=404, detail="no hay parametros para la consulta")
    else:
        condicion = crearCondiciones(parametros=parametros)

        consulta = f"""
                SELECT * FROM tbl_libros WHERE {condicion};
                """
        respuesta = crud.get_consulta(db,consulta)

        if not respuesta:
            url = crearUrl(configuracion['api_link'], parametros, configuracion['access_key'])
            titulos_google = req.get(url)
            response_json=titulos_google.json()
            libro = jsonGoogleInsert(response_json=response_json, db=db)
            if not libro:
                response = {"mensaje":"Error al insertar el libro en la Bse de datos", "status":"400"}
            else:
                response = libro
        else:
            response = respuesta
    
    return response


def jsonGoogleInsert(response_json, db: Session = Depends(get_db)):
    item = 0
    for i in response_json:
        titulo = response_json['items'][item]['volumeInfo']['title']
        autor = response_json['items'][item]['volumeInfo']['authors']
        lista_autores = ", ".join(autor)
        
        try:
            editor = response_json['items'][item]['volumeInfo']['publisher']
            descripcion = response_json['items'][item]['volumeInfo']['description']
            subtitulo = response_json['items'][item]['volumeInfo']['description']
            url_imagen = response_json['items'][item]['volumeInfo']['imageLinks']['thumbnail']
        
        except KeyError:
            editor = "no tiene editor"
            descripcion = "no tiene descripcion"
            subtitulo = "no posee subtitulo"
            url_imagen = "no tiene imagenes asociadas"
        
        try:
            fecha = str(dtm.fromisoformat(response_json['items'][item]['volumeInfo']['publishedDate']))
            
        except ValueError as error:
                fecha = str(dtm.now())
        
        libro = {
                "id_categoria":1,
                "titulo":titulo,
                "subtitulo":subtitulo,
                "autor":lista_autores,
                "fecha_publicacion": fecha,
                "editor":editor,
                "descripcion":descripcion,
                "disponible":True,
                "url_imagen":url_imagen,
            }
        #libro_json = json.loads(libro)
        item +=1
        
        libro_nuevo = crud.insertar_libro(db=db, libro=libro, tipo=True)
        
        return libro_nuevo
        

@app.get("/categorias/", response_model=List[schemas.Categorias])
async def get_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    libros = crud.get_categorias(db, skip=skip, limit=limit)
    return libros 


@app.get("/categorias/id/{cat_id}", response_model=schemas.Categorias)
async def get_categoria_id(cat_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria_id(db, cat_id=cat_id)
    return categoria


@app.get("/libros/categorias/", response_model=List[schemas.LibrosCategorias])
async def get_libros_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    listado = crud.get_libros_categorias(db, skip=skip, limit=limit)
    return listado


@app.post("/libro/insertar/", response_model=schemas.CrearLibro)
async def insertar_libro(libro: schemas.CrearLibro, db: Session = Depends(get_db), tipo=False):
    db_libro = crud.insertar_libro(db=db, libro=libro)
    return db_libro


@app.post("/categoria/insertar/", response_model=schemas.Categorias)
async def insertar_categoria(categoria: schemas.CrearCategoria, db: Session = Depends(get_db)):
    db_categoria = crud.insertar_categoria(db=db, categoria=categoria)
    return db_categoria


@app.delete("/libros/eliminar/{id}")
async def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = crud.get_libro_id(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="el libro no existe")
    else:
        return crud.eliminar_libro(db, libro_id)



def crearUrl(link: str, parametros: str, acces_key: str):
    cadena = ""
    posicion = 0
    if "&" in parametros:
        lista_parametros = parametros.split("&")
        for i in lista_parametros:
            lista_valor = i.split("=")
            dicc = configuracion['params']
            for key, value in dicc.items():
                if lista_valor[0] == value:
                    cadena = f"{key}:{lista_valor[1]}&"
            cadena += cadena

    else:
        lista_valor = parametros.split("=")
        dicc = configuracion['params']
        for key, value in dicc.items():
            if lista_valor[0] == value:
                cadena = f"{key}:{lista_valor[1]}"
    
    url =f"{link}{cadena}{acces_key}"
    print(url)
    return url


def crearCondiciones(parametros:str):
    resultado =""
    posicion = 0
    if parametros is None:
        resultado = None
    else:
        if "&" in parametros:
            lista = parametros.split("&")
            largo = len(lista)
            for i in lista:
                condiciones= i.split("=")
                if posicion == largo-1:
                    condicion = f"lower({condiciones[0]}) Like(lower('%{condiciones[1]}%')) \n"
                else:
                    condicion = f"lower({condiciones[0]}) Like(lower('%{condiciones[1]}%')) AND \n"
                resultado += condicion
                posicion +=1
        else:
            condiciones= parametros.split("=")
            condicion = f"lower({condiciones[0]}) Like(lower('%{condiciones[1]}%')) "
            resultado += condicion

    return resultado



'''
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
 
 
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
 
 
@app.get("/users/{user_id}", response_model=schemas.User)
async def consulta_usuario(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found");
    return db_user


# nodos para obtener e insertar payments
@app.get("/payments/",response_model=List[schemas.payment])
async def consulta_payments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    payments = crud.get_payments(db, skip=skip, limit=limit)
    return payments


@app.get("/payments/{payment_uuid}", response_model=schemas.payment)
async def consulta_payment(payment_uuid: str, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_uuid=payment_uuid)
    
    if db_payment is None:
        raise HTTPException(status_code=404, detail="The payment not found");
    return db_payment 

@app.post("/payments/", response_model=schemas.payment)
async def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db=db, payment=payment)


# Nodos para insertar y obtener las noticicaciones
@app.get("/notifications/",response_model=List[schemas.Notification])
async def consulta_notifications(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db, skip=skip, limit=limit)
    return notifications

@app.get("/notifications/{notification_uuid}", response_model=schemas.Notification)
async def consulta_notification(notification_uuid: str, db: Session = Depends(get_db)):
    notification = crud.get_notification(db, notification_uuid=notification_uuid)

    if notification is None:
        raise HTTPException(status_code=404, detail="The notification not found");
    return notification

@app.post("/notifications/", response_model=schemas.Notification)
async def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.create_notification(db=db, notification=notification)

@app.put("/notifications/", response_model=schemas.Notification)
async def update_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.create_notification(db=db, notification=notification)
'''