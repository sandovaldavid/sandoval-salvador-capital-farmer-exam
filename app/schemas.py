from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum


class TipoServicio(str, Enum):
    CONSTITUCION = "constitucion"
    DEFENSA_LABORAL = "defensa_laboral"
    CONSULTORIA_TRIBUTARIA = "consultoria_tributaria"


class CotizacionBase(BaseModel):
    nombre: str
    email: str
    tipo_servicio: TipoServicio
    descripcion: str


class CotizacionCreate(CotizacionBase):
    pass


class CotizacionResponse(CotizacionBase):
    id: int
    num_cotizacion: str
    precio: float
    fecha: datetime

    class Config:
        from_attributes = True


class AnalisisIA(BaseModel):
    complejidad: str
    ajuste: float
    servicios_adicionales: list
    texto_profesional: str
