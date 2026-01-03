# DevTools Playground - Backend

Backend API desarrollado con FastAPI siguiendo principios SOLID y Clean Code.

## Arquitectura

El proyecto sigue una arquitectura en capas con separación clara de responsabilidades:

```
backend/
├── app/
│   ├── core/           # Configuración y utilidades centrales
│   │   ├── config.py   # Configuración de la aplicación
│   │   ├── database.py # Configuración de base de datos
│   │   ├── exceptions.py # Excepciones personalizadas
│   │   └── startup.py  # Lógica de inicio
│   ├── dictionary/     # Módulo de diccionario
│   │   ├── db_models.py    # Modelos SQLAlchemy
│   │   ├── schemas.py      # Esquemas Pydantic
│   │   ├── repository.py   # Capa de acceso a datos
│   │   ├── service.py      # Lógica de negocio
│   │   └── router.py       # Endpoints API
│   ├── shopping/       # Módulo de calculadora de compras
│   └── words/          # Módulo de concatenación de palabras
├── tests/              # Tests unitarios e integración
├── alembic/           # Migraciones de base de datos
└── requirements.txt    # Dependencias Python
```

## Principios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada módulo tiene una responsabilidad única
- Repository: Solo acceso a datos
- Service: Solo lógica de negocio
- Router: Solo manejo de HTTP

### Open/Closed Principle (OCP)
- Interfaces abstractas permiten extensión sin modificación
- `IDictionaryRepository` permite diferentes implementaciones

### Liskov Substitution Principle (LSP)
- Implementaciones de interfaces son intercambiables
- `DictionaryRepository` puede ser reemplazado por cualquier implementación de `IDictionaryRepository`

### Interface Segregation Principle (ISP)
- Interfaces específicas y pequeñas
- `IDictionaryRepository` solo expone métodos necesarios

### Dependency Inversion Principle (DIP)
- Dependencias de abstracciones, no de implementaciones concretas
- Services dependen de interfaces, no de implementaciones

## Clean Code

- **Nombres descriptivos**: Variables y funciones con nombres claros
- **Funciones pequeñas**: Cada función hace una sola cosa
- **Documentación**: Docstrings completos en todas las funciones
- **Type hints**: Tipado completo para mejor IDE support
- **Validación**: Validación de inputs en múltiples capas
- **Manejo de errores**: Excepciones personalizadas y manejo robusto

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para acceso a datos
- **PostgreSQL**: Base de datos relacional
- **Pydantic**: Validación de datos y configuración
- **Alembic**: Migraciones de base de datos
- **Pytest**: Framework de testing

## Desarrollo Local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html
```

## Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Description"

# Aplicar migraciones
alembic upgrade head
```

## Docker

```bash
# Construir imagen
docker build -t devtools-backend .

# Ejecutar contenedor
docker run -p 8000:8000 devtools-backend
```

