from pydantic import BaseModel
from models.modelos_orm import EstadoAcademico
from datetime import datetime

class EstudianteCreate(BaseModel):
    nombre: str
    apellido: str
    documento: str
    correo: str
    telefono: str
    fecha_nacimiento: datetime | None = None
    estado_academico: EstadoAcademico
    seccion_id: int
    periodo_academico_id: int | None = None

class EstudianteRead(BaseModel):
    numero_control: int
    nombre: str
    apellido: str
    documento: str
    correo: str
    telefono: str
    fecha_nacimiento: datetime | None
    fecha_ingreso: datetime
    estado_academico: EstadoAcademico
    seccion_id: int
    is_active: bool

class EstudianteUpdate(BaseModel):
    nombre: str
    apellido: str
    documento: str
    correo: str
    telefono: str
    fecha_nacimiento: datetime | None = None
    estado_academico: EstadoAcademico
    seccion_id: int
    periodo_academico_id: int | None = None

class EstudianteUpdatePartial(BaseModel):
    nombre: str | None
    apellido: str | None
    documento: str | None
    correo: str | None
    telefono: str | None
    fecha_nacimiento: datetime | None = None
    estado_academico: EstadoAcademico | None
    seccion_id: int | None
    periodo_academico_id: int | None = None

class EstudianteDelete(BaseModel):
    is_active: bool