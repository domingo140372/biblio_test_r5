"""coding=utf-8."""
 
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud as crud
import models as models
import schemas as schemas
from database import SessionLocal, engine
from google_api import *
#from fastapi.responses import HTMLResponse
#from fastapi.templating import Jinja2Templates
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
    
    if not titulos:
        url = f"{configuracion['api_link']}{configuracion['params']}{titulo}{configuracion['key']}"
        titulos_google = req.get(url)
        response = titulos_google.json()
    else:
        response = titulos
    
    return response


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
async def insertar_libro(libro: schemas.CrearLibro, db: Session = Depends(get_db)):
    db_libro = crud.insertar_libro(db=db, libro=libro)
    return db_libro


@app.post("/categoria/insertar/", response_model=schemas.Categorias)
async def insertar_categoria(categoria: schemas.CrearCategoria, db: Session = Depends(get_db)):
    db_categoria = crud.insertar_categoria(db=db, categoria=categoria)
    return db_categoria


@app.delete("/libros/{id}")
async def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = crud.get_libro_id(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="el libro no existe")
    else:
        return crud.eliminar_libro(db, libro_id)



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