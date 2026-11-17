from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario
from app.schemas import Token, LoginRequest, UsuarioCreate, UsuarioResponse
from app.auth import verify_password, get_password_hash, create_access_token

router = APIRouter(tags=["Autenticación"])

@router.post("/login", response_model=Token, summary="Inicio de sesión para obtener Bearer Token")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.nomuser == login_data.nomuser).first()
    if not user or not verify_password(login_data.passwd, user.passwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = create_access_token(data={"sub": user.nomuser})
    return {"access_token": token, "token_type": "bearer"}

# Endpoint auxiliar para que funcione el botón verde "Authorize" en Swagger UI (/docs)
@router.post("/token", response_model=Token, include_in_schema=False)
def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.nomuser == form_data.username).first()
    if not user or not verify_password(form_data.password, user.passwd):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token(data={"sub": user.nomuser})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/usuarios/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def registrar_usuario(user: UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(Usuario.nomuser == user.nomuser).first()
    if existing:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    hashed_pwd = get_password_hash(user.passwd)
    new_user = Usuario(
        nomuser=user.nomuser,
        passwd=hashed_pwd,
        nombrecompleto=user.nombrecompleto
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user