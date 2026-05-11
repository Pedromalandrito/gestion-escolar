from pydantic import BaseModel

class SeccionAsignaturaCreate(BaseModel):
    id_seccion: int
    id_asignatura: int

class SeccionAsignaturaRead(BaseModel):
    id_seccion: int
    id_asignatura: int