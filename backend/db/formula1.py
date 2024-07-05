from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drivers(db.Model):
    __tablename__ = 'pilotos'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(255), nullable=False)
    podiums= db.Column(db.Integer, nullable=False)
    world_champions= db.Column(db.Integer, nullable=False)
    