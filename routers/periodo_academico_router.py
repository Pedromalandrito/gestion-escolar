from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import PeriodoAcademico
from database.connection import get_session
from schemas import periodo_academico_schema as pas
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/periodos_academicos")
def crear_periodo_academico(session: sessionDep, periodo_data: pas.PeriodoAcademicoCreate):
    if not periodo_data.nombre or periodo_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not periodo_data.fecha_inicio:
        raise HTTPException(status_code=400, detail="El campo Fecha Inicio no puede estar vacio")
    if not periodo_data.fecha_fin:
        raise HTTPException(status_code=400, detail="El campo Fecha Fin no puede estar vacio")
    
    if periodo_data.fecha_fin <= periodo_data.fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la fecha de inicio")
    
    existe_periodo = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.nombre == periodo_data.nombre)).first()
    if existe_periodo:
        raise HTTPException(status_code=400, detail=f"El periodo academico con nombre {periodo_data.nombre} ya existe")
    
    new_periodo = PeriodoAcademico(
        nombre=periodo_data.nombre,
        fecha_inicio=periodo_data.fecha_inicio,
        fecha_fin=periodo_data.fecha_fin
    )

    session.add(new_periodo)
    session.commit()
    session.refresh(new_periodo)
    return new_periodo

@router.get("/periodos_academicos", response_model=List[pas.PeriodoAcademicoRead])
def leer_periodos_academicos(session: sessionDep):
    periodos = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.estado == True)).all()
    return periodos

@router.get("/periodos_academicos/{periodo_id}", response_model=pas.PeriodoAcademicoRead)
def elegir_periodo_academico(session: sessionDep, periodo_id: int):
    periodo = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.id == periodo_id, PeriodoAcademico.estado == True)).first()
    if not periodo:
        raise HTTPException(status_code=404, detail=f"No existe el periodo academico con id {periodo_id}")
    return periodo

@router.put("/periodos_academicos/{periodo_id}")
def actualizar_periodo_academico(session: sessionDep, periodo_data: pas.PeriodoAcademicoUpdate, periodo_id: int):
    periodo = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.id == periodo_id, PeriodoAcademico.estado == True)).first()
    
    if not periodo:
        raise HTTPException(status_code=404, detail=f"No existe el periodo academico con id {periodo_id}")
    
    if not periodo_data.nombre or periodo_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not periodo_data.fecha_inicio:
        raise HTTPException(status_code=400, detail="El campo Fecha Inicio no puede estar vacio")
    if not periodo_data.fecha_fin:
        raise HTTPException(status_code=400, detail="El campo Fecha Fin no puede estar vacio")
    
    if periodo_data.fecha_fin <= periodo_data.fecha_inicio:
        raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la fecha de inicio")
    
    if periodo_data.nombre != periodo.nombre:
        existe = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.nombre == periodo_data.nombre)).first()
        if existe:
            raise HTTPException(status_code=400, detail=f"El nombre {periodo_data.nombre} ya está en uso")
        periodo.nombre = periodo_data.nombre
    
    periodo.fecha_inicio = periodo_data.fecha_inicio
    periodo.fecha_fin = periodo_data.fecha_fin

    session.commit()
    session.refresh(periodo)
    return periodo

@router.patch("/periodos_academicos/{periodo_id}")
def actualizar_periodo_academico_parcial(session: sessionDep, periodo_data: pas.PeriodoAcademicoUpdatePartial, periodo_id: int):
    periodo = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.id == periodo_id, PeriodoAcademico.estado == True)).first()

    if not periodo:
        raise HTTPException(status_code=404, detail=f"No existe el periodo academico con id {periodo_id}")

    if periodo_data.nombre is not None:
        if periodo_data.nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
        if periodo_data.nombre != periodo.nombre:
            existe = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.nombre == periodo_data.nombre)).first()
            if existe:
                raise HTTPException(status_code=400, detail=f"El nombre {periodo_data.nombre} ya está en uso")
            periodo.nombre = periodo_data.nombre
    
    if periodo_data.fecha_inicio is not None:
        periodo.fecha_inicio = periodo_data.fecha_inicio
    
    if periodo_data.fecha_fin is not None:
        periodo.fecha_fin = periodo_data.fecha_fin
    
    if periodo_data.fecha_inicio is not None and periodo_data.fecha_fin is not None:
        if periodo.fecha_fin <= periodo.fecha_inicio:
            raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la fecha de inicio")
    elif periodo_data.fecha_fin is not None:
        if periodo_data.fecha_fin <= periodo.fecha_inicio:
            raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la fecha de inicio")
    elif periodo_data.fecha_inicio is not None:
        if periodo.fecha_fin <= periodo_data.fecha_inicio:
            raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la fecha de inicio")
    
    if periodo_data.estado is not None:
        periodo.estado = periodo_data.estado
    
    session.commit()
    session.refresh(periodo)
    return periodo

@router.delete("/periodos_academicos/{periodo_id}")
def delete_periodo_academico(session: sessionDep, periodo_id: int, eliminacion: bool = True):
    periodo = session.exec(select(PeriodoAcademico).where(PeriodoAcademico.id == periodo_id)).first()
    
    if not periodo:
        raise HTTPException(status_code=404, detail=f"No existe el periodo academico con id {periodo_id}")
    
    if eliminacion:
        session.delete(periodo)
        session.commit()
        return {"message": f"Periodo academico con id {periodo_id} eliminado permanentemente"}
    else:
        periodo.estado = False
        session.commit()
        session.refresh(periodo)
        return {"message": f"Periodo academico con id {periodo_id} eliminado de forma Logica"}