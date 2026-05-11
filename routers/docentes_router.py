from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.modelos_orm import Docente
from database.connection import get_session
from schemas import docente_schema as ds
from typing import Annotated, List

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/docentes")
def crear_docente(session: sessionDep, docente_data: ds.DocenteCreate):
    if not docente_data.nombre or docente_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not docente_data.documento or docente_data.documento.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Documento no puede estar vacio")
    if not docente_data.especialidad:
        raise HTTPException(status_code=400, detail="El campo Especialidad no puede estar Vacío")
    if not docente_data.correo or docente_data.correo.strip() == "":
        raise HTTPException(status_code=400, detail="El campo correo no puede estar vacio")
    if not docente_data.telefono or docente_data.telefono.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
    
    existe_docente = session.exec(select(Docente).where(Docente.documento == docente_data.documento)).first()
    if existe_docente:
        raise HTTPException(status_code=400, detail=f"El Docente con el documento {docente_data.documento} ya existe")
    
    existe_correo = session.exec(select(Docente).where(Docente.correo == docente_data.correo)).first()
    if existe_correo:
        raise HTTPException(status_code=400, detail=f"El correo {docente_data.correo} ya está registrado")
    
    new_docente = Docente(
        nombre=docente_data.nombre,
        documento=docente_data.documento,
        especialidad=docente_data.especialidad,
        correo=docente_data.correo,
        telefono=docente_data.telefono
    )

    session.add(new_docente)
    session.commit()
    session.refresh(new_docente)
    return new_docente

@router.get("/docentes", response_model=List[ds.DocenteRead])
def leer_docentes(session: sessionDep):
    docentes = session.exec(select(Docente).where(Docente.is_active == True)).all()
    return docentes

@router.get("/docentes/{documento}", response_model=ds.DocenteRead)
def elegir_docente(session: sessionDep, documento: str):
    docente = session.exec(select(Docente).where(Docente.documento == documento, Docente.is_active == True)).first()
    if not docente:
        raise HTTPException(status_code=404, detail=f"No existe el docente con documento {documento}")
    return docente

@router.put("/docentes/{documento}")
def actualizar_docente(session: sessionDep, docente_data: ds.DocenteUpdate, documento: str):
    docente = session.exec(select(Docente).where(Docente.documento == documento, Docente.is_active == True)).first()
    
    if not docente:
        raise HTTPException(status_code=404, detail=f"No existe el docente con documento {documento}")
    
    if not docente_data.nombre or docente_data.nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
    if not docente_data.documento or docente_data.documento.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Documento no puede estar vacio")
    if not docente_data.especialidad:
        raise HTTPException(status_code=400, detail="El campo Especialidad no puede estar Vacío")
    if not docente_data.correo or docente_data.correo.strip() == "":
        raise HTTPException(status_code=400, detail="El campo correo no puede estar vacio")
    if not docente_data.telefono or docente_data.telefono.strip() == "":
        raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
    
    if docente_data.documento != documento:
        existe = session.exec(select(Docente).where(Docente.documento == docente_data.documento)).first()
        if existe:
            raise HTTPException(status_code=400, detail=f"El documento {docente_data.documento} ya está en uso")
        docente.documento = docente_data.documento
    
    if docente_data.correo != docente.correo:
        existe_correo = session.exec(select(Docente).where(Docente.correo == docente_data.correo)).first()
        if existe_correo:
            raise HTTPException(status_code=400, detail=f"El correo {docente_data.correo} ya está registrado")
        docente.correo = docente_data.correo
    
    docente.nombre = docente_data.nombre
    docente.especialidad = docente_data.especialidad
    docente.telefono = docente_data.telefono

    session.commit()
    session.refresh(docente)
    return docente

@router.patch("/docentes/{documento}")
def actualizar_docente_parcial(session: sessionDep, docente_data: ds.DocenteUpdatePartial, documento: str):
    docente = session.exec(select(Docente).where(Docente.documento == documento, Docente.is_active == True)).first()

    if not docente:
        raise HTTPException(status_code=404, detail=f"No existe el docente con documento {documento}")

    if docente_data.nombre is not None:
        if docente_data.nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Nombre no puede estar Vacío")
        docente.nombre = docente_data.nombre

    if docente_data.documento is not None:
        if docente_data.documento.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Documento no puede estar vacio")
        if docente_data.documento != documento:
            existe = session.exec(select(Docente).where(Docente.documento == docente_data.documento)).first()
            if existe:
                raise HTTPException(status_code=400, detail=f"El documento {docente_data.documento} ya está en uso")
            docente.documento = docente_data.documento
    
    if docente_data.especialidad is not None:
        if not docente_data.especialidad:
            raise HTTPException(status_code=400, detail="El campo Especialidad no puede estar Vacío")
        docente.especialidad = docente_data.especialidad

    if docente_data.correo is not None:
        if docente_data.correo.strip() == "":
            raise HTTPException(status_code=400, detail="El campo correo no puede estar vacio")
        if docente_data.correo != docente.correo:
            existe_correo = session.exec(select(Docente).where(Docente.correo == docente_data.correo)).first()
            if existe_correo:
                raise HTTPException(status_code=400, detail=f"El correo {docente_data.correo} ya está registrado")
            docente.correo = docente_data.correo
    
    if docente_data.telefono is not None:
        if docente_data.telefono.strip() == "":
            raise HTTPException(status_code=400, detail="El campo Telefono no puede estar Vacío")
        docente.telefono = docente_data.telefono
    
    if docente_data.condicion_laboral is not None:
        docente.condicion_laboral = docente_data.condicion_laboral
    
    session.commit()
    session.refresh(docente)
    return docente

@router.delete("/docentes/{documento}")
def delete_docente(session: sessionDep, documento: str, eliminacion: bool = True):
    docente = session.exec(select(Docente).where(Docente.documento == documento)).first()
    
    if not docente:
        raise HTTPException(status_code=404, detail=f"No existe el docente con documento {documento}")
    
    if eliminacion:
        session.delete(docente)
        session.commit()
        return {"message": f"Docente con documento {documento} eliminado permanentemente"}
    else:
        docente.is_active = False
        session.commit()
        session.refresh(docente)
        return {"message": f"Docente con documento {documento} eliminado de forma Logica"}