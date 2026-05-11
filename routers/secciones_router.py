from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import Seccion, Curso
from database.connection import get_session
from schemas import seccion_schema as ss
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/secciones")
def crear_seccion(session: sessionDep, seccion_data: ss.SeccionCreate):
    if not seccion_data.turno:
        raise HTTPException(status_code=400, detail="El campo Turno no puede estar Vacío")
    if not seccion_data.aula or seccion_data.aula.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Aula no puede estar vacio")
    if seccion_data.cupo < 0:
        raise HTTPException(status_code=400, detail="El campo Cupo no puede ser negativo")
    if not seccion_data.estado:
        raise HTTPException(status_code=400, detail="El campo Estado no puede estar Vacío")
    
    curso = session.exec(select(Curso).where(Curso.id == seccion_data.curso_id, Curso.estado == True)).first()
    if not curso:
        raise HTTPException(status_code=404, detail=f"No existe el curso con id {seccion_data.curso_id}")
    
    new_seccion = Seccion(
        turno=seccion_data.turno,
        aula=seccion_data.aula,
        cupo=seccion_data.cupo,
        estado=seccion_data.estado,
        curso_id=seccion_data.curso_id
    )

    session.add(new_seccion)
    session.commit()
    session.refresh(new_seccion)
    return new_seccion

@router.get("/secciones", response_model=List[ss.SeccionRead])
def leer_secciones(session: sessionDep):
    secciones = session.exec(select(Seccion)).all()
    return secciones

@router.get("/secciones/{seccion_id}", response_model=ss.SeccionRead)
def elegir_seccion(session: sessionDep, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {seccion_id}")
    return seccion

@router.put("/secciones/{seccion_id}")
def actualizar_seccion(session: sessionDep, seccion_data: ss.SeccionUpdate, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)
    
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {seccion_id}")
    
    if not seccion_data.turno:
        raise HTTPException(status_code=400, detail="El campo Turno no puede estar Vacío")
    if not seccion_data.aula or seccion_data.aula.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Aula no puede estar vacio")
    if seccion_data.cupo < 0:
        raise HTTPException(status_code=400, detail="El campo Cupo no puede ser negativo")
    if not seccion_data.estado:
        raise HTTPException(status_code=400, detail="El campo Estado no puede estar Vacío")
    
    curso = session.exec(select(Curso).where(Curso.id == seccion_data.curso_id, Curso.estado == True)).first()
    if not curso:
        raise HTTPException(status_code=404, detail=f"No existe el curso con id {seccion_data.curso_id}")
    
    seccion.turno = seccion_data.turno
    seccion.aula = seccion_data.aula
    seccion.cupo = seccion_data.cupo
    seccion.estado = seccion_data.estado
    seccion.curso_id = seccion_data.curso_id

    session.commit()
    session.refresh(seccion)
    return seccion

@router.patch("/secciones/{seccion_id}")
def actualizar_seccion_parcial(session: sessionDep, seccion_data: ss.SeccionUpdatePartial, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)

    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {seccion_id}")

    if seccion_data.turno is not None:
        if not seccion_data.turno:
            raise HTTPException(status_code=400, detail="El campo Turno no puede estar Vacío")
        seccion.turno = seccion_data.turno
    
    if seccion_data.aula is not None:
        if seccion_data.aula.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Aula no puede estar vacio")
        seccion.aula = seccion_data.aula
    
    if seccion_data.cupo is not None:
        if seccion_data.cupo < 0:
            raise HTTPException(status_code=400, detail="El campo Cupo no puede ser negativo")
        seccion.cupo = seccion_data.cupo
    
    if seccion_data.estado is not None:
        if not seccion_data.estado:
            raise HTTPException(status_code=400, detail="El campo Estado no puede estar Vacío")
        seccion.estado = seccion_data.estado
    
    if seccion_data.curso_id is not None:
        curso = session.exec(select(Curso).where(Curso.id == seccion_data.curso_id, Curso.estado == True)).first()
        if not curso:
            raise HTTPException(status_code=404, detail=f"No existe el curso con id {seccion_data.curso_id}")
        seccion.curso_id = seccion_data.curso_id
    
    session.commit()
    session.refresh(seccion)
    return seccion

@router.delete("/secciones/{seccion_id}")
def delete_seccion(session: sessionDep, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)
    
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {seccion_id}")
    
    session.delete(seccion)
    session.commit()
    return {"message": f"Seccion con id {seccion_id} eliminada permanentemente"}