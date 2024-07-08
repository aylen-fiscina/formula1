from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Piloto(db.Model):
    __tablename__ = 'piloto'
    id_piloto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(255), nullable=False)
    podios = db.Column(db.Integer, nullable=False)
    id_escuderia = db.Column(db.Integer, db.ForeignKey('escuderia.id_escuderia'))
    campeonatos_mundiales = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255), nullable=False)

class Escuderia(db.Model):
    __tablename__ = 'escuderia'
    id_escuderia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    campeonatos_mundiales = db.Column(db.Integer, nullable=False)
    lider = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)


class Circuito(db.Model):
    __tablename__ = 'circuito'
    id_circuito = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(255), nullable=False)
    distancia = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255), nullable=False)

class Carrera(db.Model):
    __tablename__ = 'carrera'
    id_piloto = db.Column(db.Integer, db.ForeignKey('piloto.id_piloto'), primary_key=True)
    id_circuito = db.Column(db.Integer, db.ForeignKey('circuito.id_circuito'), primary_key=True)
    fecha = db.Column(db.Integer, primary_key=True)
    pos = db.Column(db.Integer, nullable=False)
    puntos = db.Column(db.Integer, nullable=False)