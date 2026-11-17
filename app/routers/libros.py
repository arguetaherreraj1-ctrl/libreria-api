from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Libro, Editorial
from app.schemas import LibroCreate, LibroUpdate, LibroResponse, LibroSinExistenciaResponse
from app.auth import get_current_user

router = APIRouter(prefix="/libros", tags=["Libros"])

# --- CONSULTAS PERSONALIZADAS ---

@router.get("/sinexistencia", response_model=List[LibroSinExistenciaResponse], summary="6.1 VerLibrosNoExistencia")
def ver_libros_no_existencia(db: Session = Depends(get_db)):
    libros = db.query(Libro).filter(Libro.existencia == 0).all()
    return libros

@router.get("/editorial/{editorial_id}", response_model=List[LibroResponse], summary="6.2 BuscarLibrosPorEditorial")
def buscar_libros_por_editorial(editorial_id: int, db: Session = Depends(get_db)):
    libros = db.query(Libro).filter(Libro.editorial_id == editorial_id).all()
    return libros

@router.get("/anio/{anio}", response_model=List[LibroResponse], summary="6.3 BuscarLibroAnio")
def buscar_libros_por_anio(anio: int, db: Session = Depends(get_db)):
    libros = db.query(Libro).filter(Libro.anio == anio).all()
    return libros


# --- OPERACIONES CRUD ---

@router.post("", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
def crear_libro(
    libro: LibroCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Validar que exista la editorial
    editorial = db.query(Editorial).filter(Editorial.id == libro.editorial_id).first()
    if not editorial:
        raise HTTPException(status_code=404, detail="La editorial especificada no existe")

    # Validar ISBN único
    if db.query(Libro).filter(Libro.isbn == libro.isbn).first():
        raise HTTPException(status_code=400, detail="Ya existe un libro con ese ISBN")

    nuevo_libro = Libro(**libro.model_dump())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

@router.get("", response_model=List[LibroResponse])
def listar_libros(db: Session = Depends(get_db)):
    return db.query(Libro).all()

@router.get("/{id}", response_model=LibroResponse)
def obtener_libro(id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.put("/{id}", response_model=LibroResponse)
def actualizar_libro(
    id: int,
    datos: LibroUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    libro = db.query(Libro).filter(Libro.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    payload = datos.model_dump(exclude_unset=True)
    if "editorial_id" in payload:
        editorial = db.query(Editorial).filter(Editorial.id == payload["editorial_id"]).first()
        if not editorial:
            raise HTTPException(status_code=404, detail="La editorial especificada no existe")

    for key, value in payload.items():
        setattr(libro, key, value)

    db.commit()
    db.refresh(libro)
    return libro

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_libro(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    libro = db.query(Libro).filter(Libro.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro)
    db.commit()
    return {"mensaje": f"Libro '{libro.titulo}' eliminado exitosamente"}
