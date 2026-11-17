from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Editorial(Base):
    __tablename__ = "editoriales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    pais = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)

    libros = relationship("Libro", back_populates="editorial", cascade="all, delete-orphan")


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    isbn = Column(String(50), nullable=False, unique=True)
    anio = Column(Integer, nullable=False)
    existencia = Column(Integer, nullable=False, default=0)
    editorial_id = Column(Integer, ForeignKey("editoriales.id", ondelete="CASCADE"), nullable=False)

    editorial = relationship("Editorial", back_populates="libros")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nomuser = Column(String(50), unique=True, index=True, nullable=False)
    passwd = Column(String(255), nullable=False)
    nombrecompleto = Column(String(150), nullable=False)