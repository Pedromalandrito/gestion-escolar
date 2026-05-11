from pydantic import BaseModel
from models.modelos_orm import EstadoAcademico
from datetime import datetime

class EstudianteCreate(BaseModel):
    correo: str
    telefono: str
    estado_academico: EstadoAcademico
    seccion_id: int
    periodo_academico_id: int | None = None

class EstudianteRead(BaseModel):
    numero_control: int
    correo: str
    telefono: str
    fecha_ingreso: datetime
    estado_academico: EstadoAcademico
    seccion_id: int
    is_active: bool

class EstudianteUpdate(BaseModel):
    correo: str
    telefono: str
    estado_academico: EstadoAcademico
    seccion_id: int
    periodo_academico_id: int

class EstudianteUpdatePartial(BaseModel):
    correo: str | None
    telefono: str | None
    estado_academico: EstadoAcademico | None
    seccion_id: int | None
    periodo_academico_id: int | None

class EstudianteDelete(BaseModel):
    is_active: bool