from pydantic import BaseModel
from models.modelos_orm import Especialidades, condiciones_laborales

class DocenteCreate(BaseModel):
    nombre: str
    documento: str
    especialidad: Especialidades
    correo: str
    telefono: str

class DocenteRead(BaseModel):
    id: int
    nombre: str
    documento: str
    especialidad: Especialidades
    correo: str
    telefono: str
    condicion_laboral: condiciones_laborales

class DocenteUpdate(BaseModel):
    nombre: str
    documento: str
    especialidad: Especialidades
    correo: str
    telefono: str
    condicion_laboral: condiciones_laborales

class DocenteUpdatePartial(BaseModel):
    nombre: str | None
    documento: str | None
    especialidad: Especialidades | None
    correo: str | None
    telefono: str | None
    condicion_laboral: condiciones_laborales | None

class DocenteDelete(BaseModel):
    is_active: bool