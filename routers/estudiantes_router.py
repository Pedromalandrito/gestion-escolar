from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import Estudiante, Seccion, PeriodoAcademico
from database.connection import get_session
from schemas import estudiante_schema as es
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/estudiantes")
def crear_estudiante(session: sessionDep, estudiante_data: es.EstudianteCreate):
    if not estudiante_data.correo or estudiante_data.correo.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Correo no puede estar vacio")
    if not estudiante_data.telefono or estudiante_data.telefono.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
    if not estudiante_data.estado_academico:
        raise HTTPException(status_code=400, detail="El campo Estado Academico no puede estar Vacío")
    
    existe_correo = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_data.correo)).first()
    if existe_correo:
        raise HTTPException(status_code=400, detail=f"El correo {estudiante_data.correo} ya está registrado")
    
    seccion = session.get(Seccion, estudiante_data.seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {estudiante_data.seccion_id}")
    
    new_estudiante = Estudiante(
        correo=estudiante_data.correo,
        telefono=estudiante_data.telefono,
        estado_academico=estudiante_data.estado_academico,
        seccion_id=estudiante_data.seccion_id,
        periodo_academico_id=estudiante_data.periodo_academico_id
    )

    session.add(new_estudiante)
    session.commit()
    session.refresh(new_estudiante)
    return new_estudiante

@router.get("/estudiantes", response_model=List[es.EstudianteRead])
def leer_estudiantes(session: sessionDep):
    estudiantes = session.exec(select(Estudiante).where(Estudiante.is_active == True)).all()
    return estudiantes

@router.get("/estudiantes/{numero_control}", response_model=es.EstudianteRead)
def elegir_estudiante(session: sessionDep, numero_control: int):
    estudiante = session.exec(select(Estudiante).where(Estudiante.numero_control == numero_control, Estudiante.is_active == True)).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail=f"No existe el estudiante con numero de control {numero_control}")
    return estudiante

@router.put("/estudiantes/{numero_control}")
def actualizar_estudiante(session: sessionDep, estudiante_data: es.EstudianteUpdate, numero_control: int):
    estudiante = session.exec(select(Estudiante).where(Estudiante.numero_control == numero_control, Estudiante.is_active == True)).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail=f"No existe el estudiante con numero de control {numero_control}")
    
    if not estudiante_data.correo or estudiante_data.correo.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Correo no puede estar vacio")
    if not estudiante_data.telefono or estudiante_data.telefono.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
    if not estudiante_data.estado_academico:
        raise HTTPException(status_code=400, detail="El campo Estado Academico no puede estar Vacío")
    
    seccion = session.get(Seccion, estudiante_data.seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {estudiante_data.seccion_id}")
    
    if estudiante_data.correo != estudiante.correo:
        existe_correo = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_data.correo)).first()
        if existe_correo:
            raise HTTPException(status_code=400, detail=f"El correo {estudiante_data.correo} ya está registrado")
        estudiante.correo = estudiante_data.correo
    
    estudiante.telefono = estudiante_data.telefono
    estudiante.estado_academico = estudiante_data.estado_academico
    estudiante.seccion_id = estudiante_data.seccion_id

    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.patch("/estudiantes/{numero_control}")
def actualizar_estudiante_parcial(session: sessionDep, estudiante_data: es.EstudianteUpdatePartial, numero_control: int):
    estudiante = session.exec(select(Estudiante).where(Estudiante.numero_control == numero_control, Estudiante.is_active == True)).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail=f"No existe el estudiante con numero de control {numero_control}")

    if estudiante_data.correo is not None:
        if estudiante_data.correo.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Correo no puede estar vacio")
        if estudiante_data.correo != estudiante.correo:
            existe_correo = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_data.correo)).first()
            if existe_correo:
                raise HTTPException(status_code=400, detail=f"El correo {estudiante_data.correo} ya está registrado")
            estudiante.correo = estudiante_data.correo
    
    if estudiante_data.telefono is not None:
        if estudiante_data.telefono.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
        estudiante.telefono = estudiante_data.telefono
    
    if estudiante_data.estado_academico is not None:
        estudiante.estado_academico = estudiante_data.estado_academico
    
    if estudiante_data.periodo_academico_id is not None:
        estudiante.periodo_academico_id = estudiante_data.periodo_academico_id
    
    if estudiante_data.seccion_id is not None:
        seccion = session.get(Seccion, estudiante_data.seccion_id)
        if not seccion:
            raise HTTPException(status_code=404, detail=f"No existe la seccion con id {estudiante_data.seccion_id}")
        estudiante.seccion_id = estudiante_data.seccion_id
    
    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.delete("/estudiantes/{numero_control}")
def delete_estudiante(session: sessionDep, numero_control: int, eliminacion: bool = True):
    estudiante = session.exec(select(Estudiante).where(Estudiante.numero_control == numero_control)).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail=f"No existe el estudiante con numero de control {numero_control}")
    
    if eliminacion:
        session.delete(estudiante)
        session.commit()
        return {"message": f"Estudiante con numero de control {numero_control} eliminado permanentemente"}
    else:
        estudiante.is_active = False
        session.commit()
        session.refresh(estudiante)
        return {"message": f"Estudiante con numero de control {numero_control} eliminado de forma Logica"}