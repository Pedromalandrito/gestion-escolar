from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import Asignatura, Docente
from database.connection import get_session
from schemas import asignatura_schema as asis
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/asignaturas")
def crear_asignatura(session: sessionDep, asignatura_data: asis.AsignaturaCreate):
    if not asignatura_data.nombre or asignatura_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not asignatura_data.descripcion or asignatura_data.descripcion.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Descripcion no puede estar vacio")
    if not asignatura_data.carga_horaria or asignatura_data.carga_horaria <= 0:
        raise HTTPException(status_code=400, detail="El campo Carga Horaria debe ser mayor a 0")
    
    existe_asignatura = session.exec(select(Asignatura).where(Asignatura.nombre == asignatura_data.nombre)).first()
    if existe_asignatura:
        raise HTTPException(status_code=400, detail=f"La asignatura con nombre {asignatura_data.nombre} ya existe")
    
    docente = session.exec(select(Docente).where(Docente.id == asignatura_data.docente_id, Docente.is_active == True)).first()
    if not docente:
        raise HTTPException(status_code=404, detail=f"No existe el docente con id {asignatura_data.docente_id}")
    
    new_asignatura = Asignatura(
        nombre=asignatura_data.nombre,
        descripcion=asignatura_data.descripcion,
        carga_horaria=asignatura_data.carga_horaria,
        docente_id=asignatura_data.docente_id
    )

    session.add(new_asignatura)
    session.commit()
    session.refresh(new_asignatura)
    return new_asignatura

@router.get("/asignaturas", response_model=List[asis.AsignaturaRead])
def leer_asignaturas(session: sessionDep):
    asignaturas = session.exec(select(Asignatura).where(Asignatura.estado == True)).all()
    return asignaturas

@router.get("/asignaturas/{asignatura_id}", response_model=asis.AsignaturaRead)
def elegir_asignatura(session: sessionDep, asignatura_id: int):
    asignatura = session.exec(select(Asignatura).where(Asignatura.id == asignatura_id, Asignatura.estado == True)).first()
    if not asignatura:
        raise HTTPException(status_code=404, detail=f"No existe la asignatura con id {asignatura_id}")
    return asignatura

@router.put("/asignaturas/{asignatura_id}")
def actualizar_asignatura(session: sessionDep, asignatura_data: asis.AsignaturaUpdate, asignatura_id: int):
    asignatura = session.exec(select(Asignatura).where(Asignatura.id == asignatura_id, Asignatura.estado == True)).first()
    
    if not asignatura:
        raise HTTPException(status_code=404, detail=f"No existe la asignatura con id {asignatura_id}")
    
    if not asignatura_data.nombre or asignatura_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not asignatura_data.descripcion or asignatura_data.descripcion.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Descripcion no puede estar vacio")
    if not asignatura_data.carga_horaria or asignatura_data.carga_horaria <= 0:
        raise HTTPException(status_code=400, detail="El campo Carga Horaria debe ser mayor a 0")
    
    docente = session.exec(select(Docente).where(Docente.id == asignatura_data.docente_id, Docente.is_active == True)).first()
    if not docente:
        raise HTTPException(status_code=404, detail=f"No existe el docente con id {asignatura_data.docente_id}")
    
    if asignatura_data.nombre != asignatura.nombre:
        existe = session.exec(select(Asignatura).where(Asignatura.nombre == asignatura_data.nombre)).first()
        if existe:
            raise HTTPException(status_code=400, detail=f"El nombre {asignatura_data.nombre} ya está en uso")
        asignatura.nombre = asignatura_data.nombre
    
    asignatura.descripcion = asignatura_data.descripcion
    asignatura.carga_horaria = asignatura_data.carga_horaria
    asignatura.docente_id = asignatura_data.docente_id

    session.commit()
    session.refresh(asignatura)
    return asignatura

@router.patch("/asignaturas/{asignatura_id}")
def actualizar_asignatura_parcial(session: sessionDep, asignatura_data: asis.AsignaturaUpdatePartial, asignatura_id: int):
    asignatura = session.exec(select(Asignatura).where(Asignatura.id == asignatura_id, Asignatura.estado == True)).first()

    if not asignatura:
        raise HTTPException(status_code=404, detail=f"No existe la asignatura con id {asignatura_id}")

    if asignatura_data.nombre is not None:
        if asignatura_data.nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
        if asignatura_data.nombre != asignatura.nombre:
            existe = session.exec(select(Asignatura).where(Asignatura.nombre == asignatura_data.nombre)).first()
            if existe:
                raise HTTPException(status_code=400, detail=f"El nombre {asignatura_data.nombre} ya está en uso")
            asignatura.nombre = asignatura_data.nombre
    
    if asignatura_data.descripcion is not None:
        if asignatura_data.descripcion.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Descripcion no puede estar vacio")
        asignatura.descripcion = asignatura_data.descripcion
    
    if asignatura_data.carga_horaria is not None:
        if asignatura_data.carga_horaria <= 0:
            raise HTTPException(status_code=400, detail="El campo Carga Horaria debe ser mayor a 0")
        asignatura.carga_horaria = asignatura_data.carga_horaria
    
    if asignatura_data.estado is not None:
        asignatura.estado = asignatura_data.estado
    
    if asignatura_data.docente_id is not None:
        docente = session.exec(select(Docente).where(Docente.id == asignatura_data.docente_id, Docente.is_active == True)).first()
        if not docente:
            raise HTTPException(status_code=404, detail=f"No existe el docente con id {asignatura_data.docente_id}")
        asignatura.docente_id = asignatura_data.docente_id
    
    session.commit()
    session.refresh(asignatura)
    return asignatura

@router.delete("/asignaturas/{asignatura_id}")
def delete_asignatura(session: sessionDep, asignatura_id: int, eliminacion: bool = True):
    asignatura = session.exec(select(Asignatura).where(Asignatura.id == asignatura_id)).first()
    
    if not asignatura:
        raise HTTPException(status_code=404, detail=f"No existe la asignatura con id {asignatura_id}")
    
    if eliminacion:
        session.delete(asignatura)
        session.commit()
        return {"message": f"Asignatura con id {asignatura_id} eliminada permanentemente"}
    else:
        asignatura.estado = False
        session.commit()
        session.refresh(asignatura)
        return {"message": f"Asignatura con id {asignatura_id} eliminada de forma Logica"}