from pydantic import BaseModel
from datetime import datetime

class PeriodoAcademicoCreate(BaseModel):
    nombre: str
    fecha_inicio: datetime
    fecha_fin: datetime

class PeriodoAcademicoRead(BaseModel):
    id: int
    nombre: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: bool

class PeriodoAcademicoUpdate(BaseModel):
    nombre: str
    fecha_inicio: datetime
    fecha_fin: datetime

class PeriodoAcademicoUpdatePartial(BaseModel):
    nombre: str | None
    fecha_inicio: datetime | None
    fecha_fin: datetime | None
    estado: bool | None

class PeriodoAcademicoDelete(BaseModel):
    estado: bool