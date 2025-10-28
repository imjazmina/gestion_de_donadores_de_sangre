from app import db
from datetime import datetime

class SolicitudDonante(db.Model):
    __tablename__ = 'solicitud_donacion'

    id_solicitud = db.Column(db.Integer, primary_key=True)
    id_doctor = db.Column(db.Integer, nullable=False)
    tipo_sangre = db.Column(db.String(5), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')
    comentarios = db.Column(db.Text)
