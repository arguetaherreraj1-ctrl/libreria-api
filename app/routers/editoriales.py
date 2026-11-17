from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Editorial
from app.schemas import EditorialCreate, EditorialUpdate, EditorialResponse
from app.auth import get_current_user

router = APIRouter(prefix="/editoriales", tags=["Editoriales"])

@router.post("", response_model=EditorialResponse, status_code=status.HTTP_201_CREATED)
def crear_editorial(
    editorial: EditorialCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    nueva_editorial = Editorial(**editorial.model_dump())
    db.add(nueva_editorial)
    db.commit()
    db.refresh(nueva_editorial)
    return nueva_editorial

@router.get("", response_model=List[EditorialResponse])
def listar_editoriales(db: Session = Depends(get_db)):
    return db.query(Editorial).all()

@router.get("/{id}", response_model=EditorialResponse)
def obtener_editorial(id: int, db: Session = Depends(get_db)):
    editorial = db.query(Editorial).filter(Editorial.id == id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    return editorial

@router.put("/{id}", response_model=EditorialResponse)
def actualizar_editorial(
    id: int,
    datos: EditorialUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    editorial = db.query(Editorial).filter(Editorial.id == id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(editorial, key, value)

    db.commit()
    db.refresh(editorial)
    return editorial

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_editorial(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    editorial = db.query(Editorial).filter(Editorial.id == id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")
    
    db.delete(editorial)
    db.commit()
    return {"mensaje": f"Editorial con ID {id} eliminada exitosamente"}
