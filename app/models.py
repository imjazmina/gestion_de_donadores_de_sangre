from app import db
from datetime import datetime

class SolicitudDonante(db.Model):
    __tablename__ = 'solicitud_donacion'

    id_solicitud = db.Column(db.Integer, primary_key=True)
    id_donante = db.Column(db.Integer, db.ForeignKey('donante.id_donante'), nullable=False)
    tipo_sangre = db.Column(db.String(5), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')
    comentarios = db.Column(db.Text)
    motivo = db.Column(db.Text)

    # Relación inversa hacia el donante
    donante = db.relationship('Donante', back_populates='solicitudes')

    #Convierte el modelo a un diccionario para JSON
    def to_dict(self):
        return {
            "id_solicitud": self.id_solicitud,
            "id_donante": self.id_donante,
            "tipo_sangre": self.tipo_sangre,
            "cantidad": self.cantidad,
            "fecha_solicitud": self.fecha_solicitud.isoformat(),
            "estado": self.estado,
            "comentarios": self.comentarios, 
            "motivo": self.motivo
        }

# -------------------------------
# MODELO USUARIO
# -------------------------------
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    rol = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    donante = db.relationship('Donante', back_populates='usuario', uselist=False)
    doctor = db.relationship('Doctor', back_populates='usuario', uselist=False)
    admin = db.relationship('Admin', back_populates='usuario', uselist=False)

    def __repr__(self):
        return f"<Usuario {self.nombre} {self.apellido}>"
    
    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "rol": self.rol,
            "activo": self.activo,
            "fecha_registro": self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_registro else None
        }

# -------------------------------
# MODELO DONANTE
# -------------------------------
class Donante(db.Model):
    __tablename__ = 'donante'

    id_donante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    tipo_sangre = db.Column(db.String(5), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(150))
    ultima_donacion = db.Column(db.Date)#cambiar a null
    disponible_para_donar = db.Column(db.Boolean, default=True)

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='donante')
    # Turnos creados por este donante como voluntario
    agendamientos = db.relationship(
        "Agendamiento",
        foreign_keys="Agendamiento.id_donante",
        back_populates="donante"
    )

    # Turnos donde este donante es receptor de ayuda
    turnos_recibidos = db.relationship(
        "Agendamiento",
        foreign_keys="Agendamiento.id_receptor",
        back_populates="receptor"
    )
    solicitudes = db.relationship('SolicitudDonante', back_populates='donante', lazy=True)


    def __repr__(self):
        return f"<Donante {self.id_donante} - Tipo: {self.tipo_sangre}>"


# -------------------------------
# MODELO DOCTOR
# -------------------------------
class Doctor(db.Model):
    __tablename__ = 'doctor'

    id_doctor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    especialidad = db.Column(db.String(100))
    matricula = db.Column(db.String(50))

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='doctor')
    agendamientos = db.relationship('Agendamiento', back_populates='doctor', lazy=True)

    def __repr__(self):
        return f"<Doctor {self.id_doctor} - Matricula: {self.matricula}>"#??
    
# -------------------------------
# MODELO ADMIN
# -------------------------------
class Admin(db.Model):
    __tablename__ = 'admin'

    id_admin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    cargo = db.Column(db.String(100))

    # Relación con Usuario
    usuario = db.relationship('Usuario', back_populates='admin')

    def __repr__(self):
        return f"<Admin {self.id_admin} - Cargo: {self.cargo}>"




# -------------------------------
# MODELO AGENDAMIENTO
# -------------------------------
class Agendamiento(db.Model):
    __tablename__ = 'agendamiento'

    id_agendamiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_donante = db.Column(db.Integer, db.ForeignKey('donante.id_donante'), nullable=False)
    id_receptor = db.Column(db.Integer, db.ForeignKey('donante.id_donante'), nullable=True)
    id_doctor = db.Column(db.Integer, db.ForeignKey('doctor.id_doctor'), nullable=True)

    fecha_turno = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    observaciones = db.Column(db.Text, nullable=True)

    peso = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    temperatura = db.Column(db.Numeric(precision=4, scale=1), nullable=True)
    hemoglobina = db.Column(db.Numeric(precision=4, scale=2), nullable=True)
    presion_arterial = db.Column(db.String(10), nullable=True)

    #  Donante que agenda
    donante = db.relationship(
        'Donante',
        foreign_keys=[id_donante],
        back_populates='agendamientos'
    )

    #  Donante que recibe la ayuda
    receptor = db.relationship(
        'Donante',
        foreign_keys=[id_receptor],
        back_populates='turnos_recibidos'
    )
    doctor = db.relationship('Doctor', back_populates='agendamientos')