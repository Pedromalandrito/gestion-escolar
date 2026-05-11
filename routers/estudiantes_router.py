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
    if not estudiante_data.nombre or estudiante_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not estudiante_data.apellido or estudiante_data.apellido.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Apellido no puede estar Vacío")
    if not estudiante_data.documento or estudiante_data.documento.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Documento no puede estar vacio")
    if not estudiante_data.correo or estudiante_data.correo.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Correo no puede estar vacio")
    if not estudiante_data.telefono or estudiante_data.telefono.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
    if not estudiante_data.estado_academico:
        raise HTTPException(status_code=400, detail="El campo Estado Academico no puede estar Vacío")
    
    existe_documento = session.exec(select(Estudiante).where(Estudiante.documento == estudiante_data.documento)).first()
    if existe_documento:
        raise HTTPException(status_code=400, detail=f"El documento {estudiante_data.documento} ya está registrado")
    
    existe_correo = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_data.correo)).first()
    if existe_correo:
        raise HTTPException(status_code=400, detail=f"El correo {estudiante_data.correo} ya está registrado")
    
    seccion = session.get(Seccion, estudiante_data.seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {estudiante_data.seccion_id}")
    
    new_estudiante = Estudiante(
        nombre=estudiante_data.nombre,
        apellido=estudiante_data.apellido,
        documento=estudiante_data.documento,
        correo=estudiante_data.correo,
        telefono=estudiante_data.telefono,
        fecha_nacimiento=estudiante_data.fecha_nacimiento,
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
    
    if not estudiante_data.nombre or estudiante_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not estudiante_data.apellido or estudiante_data.apellido.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Apellido no puede estar Vacío")
    if not estudiante_data.documento or estudiante_data.documento.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Documento no puede estar vacio")
    if not estudiante_data.correo or estudiante_data.correo.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Correo no puede estar vacio")
    if not estudiante_data.telefono or estudiante_data.telefono.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
    if not estudiante_data.estado_academico:
        raise HTTPException(status_code=400, detail="El campo Estado Academico no puede estar Vacío")
    
    seccion = session.get(Seccion, estudiante_data.seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail=f"No existe la seccion con id {estudiante_data.seccion_id}")
    
    if estudiante_data.documento != estudiante.documento:
        existe_documento = session.exec(select(Estudiante).where(Estudiante.documento == estudiante_data.documento)).first()
        if existe_documento:
            raise HTTPException(status_code=400, detail=f"El documento {estudiante_data.documento} ya está registrado")
        estudiante.documento = estudiante_data.documento
    
    if estudiante_data.correo != estudiante.correo:
        existe_correo = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_data.correo)).first()
        if existe_correo:
            raise HTTPException(status_code=400, detail=f"El correo {estudiante_data.correo} ya está registrado")
        estudiante.correo = estudiante_data.correo
    
    estudiante.nombre = estudiante_data.nombre
    estudiante.apellido = estudiante_data.apellido
    estudiante.telefono = estudiante_data.telefono
    estudiante.fecha_nacimiento = estudiante_data.fecha_nacimiento
    estudiante.estado_academico = estudiante_data.estado_academico
    estudiante.seccion_id = estudiante_data.seccion_id
    estudiante.periodo_academico_id = estudiante_data.periodo_academico_id

    session.commit()
    session.refresh(estudiante)
    return estudiante

@router.patch("/estudiantes/{numero_control}")
def actualizar_estudiante_parcial(session: sessionDep, estudiante_data: es.EstudianteUpdatePartial, numero_control: int):
    estudiante = session.exec(select(Estudiante).where(Estudiante.numero_control == numero_control, Estudiante.is_active == True)).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail=f"No existe el estudiante con numero de control {numero_control}")

    if estudiante_data.nombre is not None:
        if estudiante_data.nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
        estudiante.nombre = estudiante_data.nombre
    
    if estudiante_data.apellido is not None:
        if estudiante_data.apellido.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Apellido no puede estar Vacío")
        estudiante.apellido = estudiante_data.apellido

    if estudiante_data.documento is not None:
        if estudiante_data.documento.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Documento no puede estar vacio")
        if estudiante_data.documento != estudiante.documento:
            existe_documento = session.exec(select(Estudiante).where(Estudiante.documento == estudiante_data.documento)).first()
            if existe_documento:
                raise HTTPException(status_code=400, detail=f"El documento {estudiante_data.documento} ya está registrado")
            estudiante.documento = estudiante_data.documento

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
    
    if estudiante_data.fecha_nacimiento is not None:
        estudiante.fecha_nacimiento = estudiante_data.fecha_nacimiento
    
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