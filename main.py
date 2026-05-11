from fastapi import FastAPI, APIRouter
from sqlmodel import SQLModel
from database.connection import engine

from routers.estudiantes_router import router as er
from routers.docentes_router import router as dr
from routers.cursos_router import router as cr
from routers.asignaturas_router import router as ar
from routers.secciones_router import router as sr
from routers.periodo_academico_router import router as par
from routers.seccion_asignatura_router import router as sar

app = FastAPI(title="API escolar")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

routers: dict[str, APIRouter] = {
    "Endpoints Estudiantes": er,
    "Endpoints Docentes": dr,
    "Endpoints Cursos": cr,
    "Endpoints Asignaturas": ar,
    "Endpoints Secciones": sr,
    "Endpoints Periodos Académicos": par,
    "Endpoints Seccion-Asignatura": sar
}

for etiqueta, router in routers.items():
    app.include_router(router, tags=[etiqueta])