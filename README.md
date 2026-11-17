# API REST - Librería Chiapas

## Descripción del proyecto
API REST desarrollada con Python y FastAPI para la administración de libros y editoriales de la Tienda de Libros "Librería Chiapas", con autenticación mediante Bearer Token y persistencia en PostgreSQL[cite: 5].

## Tecnologías utilizadas
- Python 3[cite: 1, 8]
- FastAPI[cite: 8]
- PostgreSQL[cite: 8]
- SQLAlchemy[cite: 8]
- Pydantic[cite: 8]
- Uvicorn[cite: 8]
- JWT (python-jose & passlib)
- Render (Despliegue en la nube)[cite: 8]

## Estructura del proyecto
\`\`\`
libreria-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── editoriales.py
│       └── libros.py
├── requirements.txt
├── seed_data.py
├── .gitignore
└── README.md
\`\`\`

## Instalación y ejecución local
1. Clonar el repositorio y entrar a la carpeta `libreria-api`.
2. Crear y activar el entorno virtual:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   \`\`\`
3. Instalar dependencias:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
4. Crear un archivo `.env` en la raíz con las variables:
   \`\`\`env
   DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
   SECRET_KEY=clave_secreta_para_produccion
   \`\`\`
5. Cargar datos iniciales de prueba:
   \`\`\`bash
   python seed_data.py
   \`\`\`
6. Iniciar el servidor local:
   \`\`\`bash
   uvicorn app.main:app --reload
   \`\`\`

## Configuración de PostgreSQL
La conexión se gestiona mediante SQLAlchemy en `app/database.py` leyendo la variable de entorno `DATABASE_URL`. Las tablas (`usuarios`, `editoriales`, `libros`) se crean automáticamente al arrancar la aplicación[cite: 6].

## Mecanismo de autenticación
Se utiliza autenticación basada en **Bearer Token (JWT)**[cite: 7, 8].
1. Enviar credenciales a `POST /login` (`{"nomuser": "admin", "passwd": "admin123"}`).
2. Copiar el `access_token` devuelto[cite: 2, 7].
3. Incluir en las peticiones protegidas (POST, PUT, DELETE) el encabezado:
   `Authorization: Bearer <access_token>`[cite: 2, 7]

## Endpoints disponibles
- **Autenticación:** `POST /login`, `POST /usuarios/registro`[cite: 7]
- **Editoriales:** `GET /editoriales`, `GET /editoriales/{id}`, `POST /editoriales`, `PUT /editoriales/{id}`, `DELETE /editoriales/{id}`[cite: 6]
- **Libros:** `GET /libros`, `GET /libros/{id}`, `POST /libros`, `PUT /libros/{id}`, `DELETE /libros/{id}`[cite: 6]
- **Consultas personalizadas:** `GET /libros/sinexistencia`, `GET /libros/editorial/{editorial_id}`, `GET /libros/anio/{anio}`[cite: 7]

## Ejemplos de solicitudes
- **Login:** `POST /login` -> Body JSON: `{"nomuser": "admin", "passwd": "admin123"}`
- **Crear libro:** `POST /libros` -> Header: `Authorization: Bearer <token>` -> Body JSON: `{"titulo": "Nuevo Libro", "autor": "Autor", "isbn": "978-0000000001", "anio": 2024, "existencia": 10, "editorial_id": 1}`[cite: 2, 6]

## URL de producción
- **API Base:** `https://tu-proyecto.onrender.com`[cite: 8, 9]
- **Documentación Swagger:** `https://tu-proyecto.onrender.com/docs`[cite: 2, 8, 9]
