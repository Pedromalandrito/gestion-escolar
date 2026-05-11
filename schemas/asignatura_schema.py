from pydantic import BaseModel

class AsignaturaCreate(BaseModel):
    codigo: str
    nombre: str
    descripcion: str
    carga_horaria: int
    docente_id: int

class AsignaturaRead(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: str
    carga_horaria: int
    estado: bool
    docente_id: int

class AsignaturaUpdate(BaseModel):
    codigo: str
    nombre: str
    descripcion: str
    carga_horaria: int
    docente_id: int

class AsignaturaUpdatePartial(BaseModel):
    codigo: str | None
    nombre: str | None
    descripcion: str | None
    carga_horaria: int | None
    estado: bool | None
    docente_id: int | None

class AsignaturaDelete(BaseModel):
    estado: bool