from typing import Optional, List
from pydantic import BaseModel, EmailStr

# --- USUARIOS & AUTH ---
class UsuarioBase(BaseModel):
    nomuser: str
    nombrecompleto: str

class UsuarioCreate(UsuarioBase):
    passwd: str

class UsuarioResponse(UsuarioBase):
    id: int
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    nomuser: str
    passwd: str

class Token(BaseModel):
    access_token: str
    token_type: str


# --- EDITORIALES ---
class EditorialBase(BaseModel):
    nombre: str
    pais: str
    email: EmailStr

class EditorialCreate(EditorialBase):
    pass

class EditorialUpdate(BaseModel):
    nombre: Optional[str] = None
    pais: Optional[str] = None
    email: Optional[EmailStr] = None

class EditorialResponse(EditorialBase):
    id: int
    class Config:
        from_attributes = True


# --- LIBROS ---
class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    anio: int
    existencia: int
    editorial_id: int

class LibroCreate(LibroBase):
    pass

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    anio: Optional[int] = None
    existencia: Optional[int] = None
    editorial_id: Optional[int] = None

class LibroResponse(LibroBase):
    id: int
    class Config:
        from_attributes = True

class LibroSinExistenciaResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    anio: int
    existencia: int
    class Config:
        from_attributes = True
        