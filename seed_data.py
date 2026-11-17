from app.database import SessionLocal, engine, Base
from app.models import Usuario, Editorial, Libro
from app.auth import get_password_hash

def sembrar_datos():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Usuario inicial
        if not db.query(Usuario).filter(Usuario.nomuser == "admin").first():
            admin = Usuario(
                nomuser="admin",
                passwd=get_password_hash("admin123"),
                nombrecompleto="Administrador Chiapas"
            )
            db.add(admin)

        # 2. Editoriales iniciales
        if db.query(Editorial).count() == 0:
            ed1 = Editorial(nombre="Editorial Sudamericana", pais="Argentina", email="contacto@sudamericana.com")
            ed2 = Editorial(nombre="Alfaguara", pais="España", email="info@alfaguara.es")
            ed3 = Editorial(nombre="Fondo de Cultura Económica", pais="México", email="atencion@fce.com.mx")
            db.add_all([ed1, ed2, ed3])
            db.commit()

            # 3. Libros iniciales
            lib1 = Libro(titulo="Cien años de soledad", autor="Gabriel García Márquez", isbn="978-0307474728", anio=1967, existencia=0, editorial_id=ed1.id)
            lib2 = Libro(titulo="El amor en los tiempos del cólera", autor="Gabriel García Márquez", isbn="978-0307389732", anio=1985, existencia=15, editorial_id=ed1.id)
            lib3 = Libro(titulo="Rayuela", autor="Julio Cortázar", isbn="978-8420491172", anio=1963, existencia=5, editorial_id=ed2.id)
            lib4 = Libro(titulo="Pedro Páramo", autor="Juan Rulfo", isbn="978-9681601614", anio=1955, existencia=0, editorial_id=ed3.id)
            lib5 = Libro(titulo="Ensayo Moderno 2020", autor="Autor Chiapas", isbn="978-1234567890", anio=2020, existencia=8, editorial_id=ed3.id)
            db.add_all([lib1, lib2, lib3, lib4, lib5])

        db.commit()
        print("¡Datos de prueba insertados con éxito!")
    finally:
        db.close()

if __name__ == "__main__":
    sembrar_datos()