from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import Curso
from database.connection import get_session
from schemas import curso_schema as cs
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/cursos")
def crear_curso(session: sessionDep, curso_data: cs.CursoCreate):
    if not curso_data.nombre or curso_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not curso_data.descripcion or curso_data.descripcion.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Descripcion no puede estar vacio")
    
    existe_curso = session.exec(select(Curso).where(Curso.nombre == curso_data.nombre)).first()
    if existe_curso:
        raise HTTPException(status_code=400, detail=f"El curso con nombre {curso_data.nombre} ya existe")
    
    new_curso = Curso(
        nombre=curso_data.nombre,
        descripcion=curso_data.descripcion
    )

    session.add(new_curso)
    session.commit()
    session.refresh(new_curso)
    return new_curso

@router.get("/cursos", response_model=List[cs.CursoRead])
def leer_cursos(session: sessionDep):
    cursos = session.exec(select(Curso).where(Curso.estado == True)).all()
    return cursos

@router.get("/cursos/{curso_id}", response_model=cs.CursoRead)
def elegir_curso(session: sessionDep, curso_id: int):
    curso = session.exec(select(Curso).where(Curso.id == curso_id, Curso.estado == True)).first()
    if not curso:
        raise HTTPException(status_code=404, detail=f"No existe el curso con id {curso_id}")
    return curso

@router.put("/cursos/{curso_id}")
def actualizar_curso(session: sessionDep, curso_data: cs.CursoUpdate, curso_id: int):
    curso = session.exec(select(Curso).where(Curso.id == curso_id, Curso.estado == True)).first()
    
    if not curso:
        raise HTTPException(status_code=404, detail=f"No existe el curso con id {curso_id}")
    
    if not curso_data.nombre or curso_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not curso_data.descripcion or curso_data.descripcion.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Descripcion no puede estar vacio")
    
    if curso_data.nombre != curso.nombre:
        existe = session.exec(select(Curso).where(Curso.nombre == curso_data.nombre)).first()
        if existe:
            raise HTTPException(status_code=400, detail=f"El nombre {curso_data.nombre} ya está en uso")
        curso.nombre = curso_data.nombre
    
    curso.descripcion = curso_data.descripcion

    session.commit()
    session.refresh(curso)
    return curso

@router.patch("/cursos/{curso_id}")
def actualizar_curso_parcial(session: sessionDep, curso_data: cs.CursoUpdatePartial, curso_id: int):
    curso = session.exec(select(Curso).where(Curso.id == curso_id, Curso.estado == True)).first()

    if not curso:
        raise HTTPException(status_code=404, detail=f"No existe el curso con id {curso_id}")

    if curso_data.nombre is not None:
        if curso_data.nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
        if curso_data.nombre != curso.nombre:
            existe = session.exec(select(Curso).where(Curso.nombre == curso_data.nombre)).first()
            if existe:
                raise HTTPException(status_code=400, detail=f"El nombre {curso_data.nombre} ya está en uso")
            curso.nombre = curso_data.nombre
    
    if curso_data.descripcion is not None:
        if curso_data.descripcion.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Descripcion no puede estar vacio")
        curso.descripcion = curso_data.descripcion
    
    if curso_data.estado is not None:
        curso.estado = curso_data.estado
    
    session.commit()
    session.refresh(curso)
    return curso

@router.delete("/cursos/{curso_id}")
def delete_curso(session: sessionDep, curso_id: int, eliminacion: bool = True):
    curso = session.exec(select(Curso).where(Curso.id == curso_id)).first()
    
    if not curso:
        raise HTTPException(status_code=404, detail=f"No existe el curso con id {curso_id}")
    
    if eliminacion:
        session.delete(curso)
        session.commit()
        return {"message": f"Curso con id {curso_id} eliminado permanentemente"}
    else:
        curso.estado = False
        session.commit()
        session.refresh(curso)
        return {"message": f"Curso con id {curso_id} eliminado de forma Logica"}