from pydantic import BaseModel

class CursoCreate(BaseModel):
    nombre: str
    descripcion: str

class CursoRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: bool

class CursoUpdate(BaseModel):
    nombre: str
    descripcion: str

class CursoUpdatePartial(BaseModel):
    nombre: str | None
    descripcion: str | None
    estado: bool | None

class CursoDelete(BaseModel):
    estado: bool