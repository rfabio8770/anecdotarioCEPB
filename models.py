from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Curso(db.Model):
    __tablename__ = 'curso'
    id_curso = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(100), nullable=False)
    alumnos = db.relationship('Alumno', backref='curso_rel', lazy=True)

class Alumno(db.Model):
    __tablename__ = 'alumno'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nro_lista = db.Column(db.Integer)
    curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'))

class Anecdotario(db.Model):
    __tablename__ = 'anecdotario'
    id_anecdota = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200))

class Anotacion(db.Model):
    __tablename__ = 'anotacion'
    id = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    id_anecdota = db.Column(db.Integer, db.ForeignKey('anecdotario.id_acnedota'))
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)