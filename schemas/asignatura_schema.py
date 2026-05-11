from pydantic import BaseModel

class AsignaturaCreate(BaseModel):
    nombre: str
    descripcion: str
    carga_horaria: int
    docente_id: int

class AsignaturaRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    carga_horaria: int
    estado: bool
    docente_id: int

class AsignaturaUpdate(BaseModel):
    nombre: str
    descripcion: str
    carga_horaria: int
    docente_id: int

class AsignaturaUpdatePartial(BaseModel):
    nombre: str | None
    descripcion: str | None
    carga_horaria: int | None
    estado: bool | None
    docente_id: int | None

class AsignaturaDelete(BaseModel):
    estado: bool