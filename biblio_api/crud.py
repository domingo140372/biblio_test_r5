"""coding=utf-8."""
 
from sqlalchemy.orm import Session
from sqlalchemy import text, and_
import  models as models
import schemas as schemas

import datetime

def get_libros(db: Session,skip: int = 0, limit: int = 100):
	return db.query(models.Libros).offset(skip).limit(limit).all()


def get_libro_id(db: Session, id_libro: int):
	return db.query(models.Libros).filter(models.Libros.id == id_libro).first()


def get_libros_por_titulo(db: Session, titulo: str):
	return db.query(models.Libros).filter(models.Libros.titulo.like(f'%{titulo}%')).all()


def get_consulta(db: Session, consulta:str):
	xxx = db.execute(consulta).fetchall()
	print(xxx)
	return xxx


def get_categorias(db: Session,skip: int = 0, limit: int = 100):
	return db.query(models.Categorias).offset(skip).limit(limit).all()


def get_categoria_id(db: Session, cat_id: int):
	return db.query(models.Categorias).filter(models.Categorias.id == cat_id).first()


def get_libros_categorias(db: Session,skip: int = 0, limit: int = 100):
	return db.query(models.Categorias).join(models.Libros, models.Libros.id_categoria == models.Categorias.id).\
	offset(skip).limit(limit).all()


#inserciones

def insertar_libro(db: Session, libro: schemas.CrearLibro):
	id_categoria = libro.id_categoria
	titulo = libro.titulo
	subtitulo = libro.subtitulo
	autor = libro.autor
	fecha_publicacion= libro.fecha_publicacion 
	editor = libro.editor
	descripcion = libro.descripcion
	disponible = libro.disponible
	url_imagen = libro.url_imagen

	db_libro = models.Libros(id_categoria=id_categoria, 
								titulo=titulo,
								subtitulo=subtitulo,
								autor=autor,
								fecha_publicacion=fecha_publicacion,
								editor=editor,
								descripcion=descripcion,
								disponible=disponible,
								url_imagen=url_imagen)
	db.add(db_libro)
	db.commit()
	db.refresh(db_libro)
	return db_libro


def insertar_categoria(db: Session, categoria: schemas.CrearCategoria):
	db_categoria = models.Categorias(categoria=categoria.categoria, descripcion=categoria.descripcion)
	db.add(db_categoria)
	db.commit()
	db.refresh(db_categoria)
	return db_categoria

#eliminar

def eliminar_libro(db: Session, id_libro: int):
	db_libro = get_libro_id(db, id_libro)
	db.delete(db_libro)
	db.commit()
	return {"mensaje":f"Libro: '{db_libro.titulo}', ha sido eliminado exitosamente", "Eliminado": True}


""" 
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
 
 
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
 
 
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
    #return db.query(models.User).join(models.Payment, models.Payment.usr_id == models.User.id).\
	#offset(skip).limit(limit).all()
 
 
def create_user(db: Session, user: schemas.UserCreate):
	codepass = user.password.encode()
	hashed_password_new = hbl.new('sha256', codepass)
	hashed_password = hashed_password_new.digest()
	user_name = user.name
	usr_uuid = uuid.uuid4()
	
	db_user = models.User(email=user.email, hashed_password=hashed_password, name=user_name, usr_uuid=str(usr_uuid),register_date=datetime.datetime.now())
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def get_payments(db: Session, skip: int = 0, limit: int = 50):
	return db.query(models.Payment).offset(skip).limit(limit).all()


def get_payment(db: Session, payment_uuid: str):
	return db.query(models.Payment).filter(models.Payment.pay_uuid == payment_uuid).first()


def create_payment(db: Session, payment: schemas.PaymentCreate):
	description = payment.description
	payment_type = payment.payment_type
	amount = payment.amount
	payment_date = payment.payment_date
	pay_uuid = uuid.uuid4()

	db_payment = models.Payment(description=description, payment_type=payment_type, amount=amount, payment_date=payment_date, pay_uuid=pay_uuid)
	db.add(db_payment)
	db.commit()
	db.refresh(db_payment)
	return db_payment

# Notificaciones
def get_notifications(db: Session, skip: int = 0, limit: int = 50):
	return db.query(models.Notification).offset(skip).limit(limit).all()



def get_notification(db: Session, notification_uuid: str):
	return db.query(models.Notification).filter(models.Notification.not_uuid == notification_uuid).first()


def create_notification(db: Session, notification: schemas.NotificationCreate):
	message = notification.message
	notification_date = notification.notification_date
	effected = notification.effected

	db_notification = models.Notification(message=message, notification_date=notification_date, effected=effected)
	db.add(db_notification)
	db.commit()
	db.refresh(db_notification)
	return db_notification

def get_all_users_payments(db: Session, skip: int = 0, limit: int = 50):
	return db.query(models.User).join(models.Payment, models.Payment.usr_id == models.User.id).\
	offset(skip).limit(limit).all()









"""