from pydantic import BaseModel
from models.modelos_orm import turno_seccion, estados_secciones

class SeccionCreate(BaseModel):
    turno: turno_seccion
    aula: str
    cupo: int
    estado: estados_secciones
    curso_id: int

class SeccionRead(BaseModel):
    id: int
    turno: turno_seccion
    aula: str
    cupo: int
    estado: estados_secciones
    curso_id: int

class SeccionUpdate(BaseModel):
    turno: turno_seccion
    aula: str
    cupo: int
    estado: estados_secciones
    curso_id: int

class SeccionUpdatePartial(BaseModel):
    turno: turno_seccion | None
    aula: str | None
    cupo: int | None
    estado: estados_secciones | None
    curso_id: int | None

class SeccionDelete(BaseModel):
    estado: bool