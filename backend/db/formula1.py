from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Pilotos(db.Model):
    __tablename__ = 'pilotos'
    id_piloto = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(255), nullable=False)
    podiums = db.Column(db.Integer, nullable=False)
    world_championships_piloto = db.Column(db.Integer, nullable=False)
    number_piloto = db.Column(db.Integer, nullable=False)
    image_url_piloto = db.Column(db.String(255))

class Escuderias(db.Model):
    __tablename__ = 'escuderias'
    id_team = db.Column(db.Integer, primary_key=True)
    full_team_name = db.Column(db.String(255), nullable=False)
    world_championships_team = db.Column(db.Integer, nullable=False)
    team_chief = db.Column(db.String(255), nullable=False)
    image_url_escuderia = db.Column(db.String(255))

class Circuitos(db.Model):
    __tablename__ = 'circuitos'
    id_circuito = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    date =  db.Column(db.Date, nullable=False) 