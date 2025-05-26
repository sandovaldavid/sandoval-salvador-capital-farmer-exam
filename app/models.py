from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)
    num_cotizacion = Column(String(50), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    tipo_servicio = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=False)
    precio = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Cotizacion(num_cotizacion='{self.num_cotizacion}', nombre='{self.nombre}')>"
