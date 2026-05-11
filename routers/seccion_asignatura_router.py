from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import intermediariaAsignaturas, Seccion, Asignatura
from database.connection import get_session
from schemas import seccion_asignatura_schema as sas
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/secciones_asignaturas")
def crear_relacion_seccion_asignatura(session: sessionDep, relacion_data: sas.SeccionAsignaturaCreate):
    seccion = session.get(Seccion, relacion_data.id_seccion)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {relacion_data.id_seccion}")
    
    asignatura = session.get(Asignatura, relacion_data.id_asignatura)
    if not asignatura:
        raise HTTPException(status_code=404, detail=f"No existe la asignatura con id {relacion_data.id_asignatura}")
    
    existe_relacion = session.exec(select(intermediariaAsignaturas).where(
        intermediariaAsignaturas.id_seccion == relacion_data.id_seccion,
        intermediariaAsignaturas.id_asignatura == relacion_data.id_asignatura
    )).first()
    
    if existe_relacion:
        raise HTTPException(status_code=400, detail="La relacion entre esta seccion y asignatura ya existe")
    
    new_relacion = intermediariaAsignaturas(
        id_seccion=relacion_data.id_seccion,
        id_asignatura=relacion_data.id_asignatura
    )

    session.add(new_relacion)
    session.commit()
    return {"message": "Relacion creada exitosamente", "id_seccion": relacion_data.id_seccion, "id_asignatura": relacion_data.id_asignatura}

@router.get("/secciones_asignaturas")
def leer_relaciones(session: sessionDep):
    relaciones = session.exec(select(intermediariaAsignaturas)).all()
    return relaciones

@router.get("/secciones_asignaturas/seccion/{seccion_id}")
def obtener_asignaturas_por_seccion(session: sessionDep, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {seccion_id}")
    
    asignaturas = session.exec(select(Asignatura).join(intermediariaAsignaturas).where(intermediariaAsignaturas.id_seccion == seccion_id)).all()
    return asignaturas

@router.get("/secciones_asignaturas/asignatura/{asignatura_id}")
def obtener_secciones_por_asignatura(session: sessionDep, asignatura_id: int):
    asignatura = session.get(Asignatura, asignatura_id)
    if not asignatura:
        raise HTTPException(status_code=404, detail=f"No existe la asignatura con id {asignatura_id}")
    
    secciones = session.exec(select(Seccion).join(intermediariaAsignaturas).where(intermediariaAsignaturas.id_asignatura == asignatura_id)).all()
    return secciones

@router.delete("/secciones_asignaturas")
def eliminar_relacion(session: sessionDep, id_seccion: int, id_asignatura: int):
    relacion = session.exec(select(intermediariaAsignaturas).where(
        intermediariaAsignaturas.id_seccion == id_seccion,
        intermediariaAsignaturas.id_asignatura == id_asignatura
    )).first()
    
    if not relacion:
        raise HTTPException(status_code=404, detail="No existe la relacion entre esta seccion y asignatura")
    
    session.delete(relacion)
    session.commit()
    return {"message": f"Relacion entre seccion {id_seccion} y asignatura {id_asignatura} eliminada permanentemente"}