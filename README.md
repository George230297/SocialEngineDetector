# Social Engineering Detector

## Descripción

**Social Engineering Detector** es una API de ciberseguridad avanzada diseñada para detectar y mitigar amenazas de Ingeniería Social. Construida sobre **Python** y **FastAPI**, esta herramienta analiza diversos artefactos digitales (actualmente URLs, con capacidad extensible para texto, imágenes y audio) para identificar indicadores de riesgo asociados con ataques de phishing, smishing y otras técnicas de manipulación.

El proyecto sigue estrictamente los principios de **Clean Architecture** (Arquitectura Limpia) y utiliza patrones de diseño como **Strategy** para permitir una escalabilidad modular y mantenible.

## Objetivo

El objetivo principal de esta herramienta es proporcionar una capa de defensa automatizada e inteligente que pueda evaluar en tiempo real la peligrosidad de elementos sospechosos antes de que un usuario interactúe con ellos. Busca reducir la superficie de ataque humana alertando sobre posibles vectores de ingeniería social.

## Características Clave

- **Arquitectura Limpia:** Separación clara de responsabilidades en capas (Dominio, Casos de Uso/Servicios, Infraestructura/API).
- **Orquestación de Motores de Análisis:** Sistema flexible que selecciona dinámicamente el motor de análisis adecuado según el tipo de artefacto (URL, TEXTO, etc.).
- **Análisis Heurístico de URLs:** Detección basada en reglas como longitud excesiva, uso de IPs directas y palabras clave sospechosas.
- **API RESTful:** Endpoints documentados automáticamente con OpenAPI (Swagger UI).
- **Docker Ready:** Configuración lista para despliegue en contenedores optimizados para producción.

## Estructura del Proyecto

```text
src/
├── api/             # Capa de presentación (Endpoints)
├── core/            # Configuración global y utilidades
├── domain/          # Modelos de datos y reglas de negocio (Schemas, Enums)
├── services/        # Lógica de negocio y orquestación
│   ├── analysis_engines/  # Motores de análisis (Strategy Pattern)
│   └── orchestrator.py    # Orquestador de servicios
└── main.py          # Punto de entrada de la aplicación
```

## Tecnologías

- **Python 3.11**
- **FastAPI**
- **Pydantic V2**
- **Uvicorn**
- **Docker**

## Cómo Ejecutar

### Localmente

1.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ejecuta el servidor:
    ```bash
    python src/main.py
    ```
3.  Accede a la documentación en: `http://localhost:8000/docs`

### Con Docker

1.  Construye la imagen:
    ```bash
    docker build -t social-eng-detector .
    ```
2.  Ejecuta el contenedor:
    ```bash
    docker run -p 8000:8000 social-eng-detector
    ```
