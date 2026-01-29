# Social Engineering Detector

> **Una capa de defensa inteligente contra ataques de Ingeniería Social.**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)](tests/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción General

**Social Engineering Detector** es una API de ciberseguridad avanzada diseñada para operar como una **capa de defensa proactiva** ante amenazas de Ingeniería Social.

Su objetivo principal es **proteger al usuario final** analizando artefactos digitales (como URLs, correos electrónicos o mensajes SMS) en tiempo real para identificar intentos de manipulación, fraude o Phishing antes de que ocurra una interacción peligrosa.

Este proyecto ha sido construido bajo los principios de **Arquitectura Limpia (Clean Architecture)** y el **Ciclo de Desarrollo de Software Seguro (SSDLC)**, lo que garantiza no solo una detección eficaz, sino también un sistema mantenible, escalable y auditable.

### ¿Para qué sirve?

- **Detección Temprana:** Identifica enlaces sospechosos o maliciosos basándose en heurísticas avanzadas y patrones de ataque conocidos.
- **Análisis Automatizado:** Procesa grandes volúmenes de solicitudes sin intervención humana gracias a su arquitectura asíncrona.
- **Integración de Seguridad:** Sirve como backend de análisis para clientes de correo, navegadores o sistemas SIEM corporativos.

---

## 🚀 Características Clave (Novedades)

- **Arquitectura Limpia:** Estricta separación de responsabilidades que facilita la evolución del software sin deuda técnica.
- **Rendimiento Asíncrono:** Migración completa a `httpx` y `async/await` para evitar bloqueos bajo alta concurrencia.
- **Observabilidad Completa:** Sistema de **Logging Estructurado** (vía `loguru`) que permite auditoría forense y depuración en producción.
- **Alta Calidad (Testing):** Suite de pruebas automatizadas (Unitarias e Integración) con `pytest` para garantizar la estabilidad del código.
- **Seguridad por Diseño:** Middleware de seguridad configurado y manejo responsable de secretos.
- **Patrón Strategy:** Motor de análisis extensible. Agregar soporte para nuevos tipos de amenazas es tan simple como implementar una nueva "Estrategia".
- **Docker Ready:** Listo para despliegue contenerizado seguro.

### 🛡️ Mejoras Recientes (Security & Architecture Hardening)

- **Gestión de Secretos:** Implementación de `SecretStr` para manejo seguro de credenciales. Las API Keys ya no están hardcoded.
- **CORS Estricto:** Configuración robusta de CORS validando orígenes permitidos mediante `BACKEND_CORS_ORIGINS`.
- **Inyección de Dependencias:** Refactorización del Orquestador para un acoplamiento débil, facilitando pruebas y mantenibilidad.
- **Dependencias Pinneadas:** `requirements.txt` con versiones fijas para garantizar construcciones reproducibles y seguras.
- **Validación Estricta:** Schemas de Pydantic reforzados para sanitización de entradas.

---

## 🏗️ Arquitectura del Sistema

El sistema actúa como un **orquestador inteligente** que recibe artefactos y delega el análisis al motor más apropiado.

Graph TD:
`Cliente -> API (FastAPI) -> Orquestador -> Motores de Análisis -> Resultado`

### Capas del Proyecto

1.  **Domain (`src/domain`):** Modelos de datos y reglas de negocio puras.
2.  **Services (`src/services`):** Lógica aplicativa, Orquestador y Motores de Análisis (Heurísticos, ML, etc.).
3.  **API (`src/api`):** Controladores REST, inyección de dependencias y validación de esquemas.
4.  **Core (`src/core`):** Configuración transversal, Logging y Utilidades.

---

## 🛠️ Estructura del Proyecto

```text
social_eng_detector/
├── src/
│   ├── api/                 # Endpoints y Rutas
│   ├── core/                # Configuración y Logging
│   ├── domain/              # Modelos (Schemas)
│   ├── services/            # Lógica de Negocio (Orquestador y Motores)
│   └── main.py              # Punto de entrada de la aplicación
├── tests/                   # Suite de Pruebas Automatizadas
├── Dockerfile               # Configuración de Contenedor
├── requirements.txt         # Dependencias Modernas (httpx, loguru, fastapi)
└── README.md                # Documentación del Proyecto
```

---

## 💻 Instalación y Uso

### Prerrequisitos

- Python 3.11+
- Docker (Opcional)

### Ejecución Local

1.  **Clonar e instalar dependencias:**

2.  **Configuración de Entorno (IMPORTANTE):**
    Crear un archivo `.env` en la raíz basado en el siguiente ejemplo:

    ```ini
    VIRUSTOTAL_API_KEY=tu_api_key_real
    OPENAI_API_KEY=tu_api_key_real
    # Lista JSON de orígenes permitidos para CORS
    BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
    ```

3.  **Instalar dependencias:**

    ```bash
    git clone <repo-url>
    cd social_eng_detector
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Iniciar el servidor:**

    ```bash
    python src/main.py
    ```

    El servidor iniciará en `http://localhost:8000`.

5.  **Ejecutar Pruebas (Nuevo):**
    Para verificar que todo funciona correctamente:
    ```bash
    pytest
    ```

### Docker (Recomendado)

```bash
docker build -t social-eng-detector .
docker run -p 8000:8000 social-eng-detector
```

---

## 📡 Uso de la API

**POST** `/api/v1/scan/analyze`

**Request:**

```json
{
  "artifact_type": "URL",
  "content": "http://paypal-secure-update.com.login.php"
}
```

**Response:**

```json
{
  "risk_score": 85,
  "risk_level": "MALICIOUS",
  "findings": [
    "Longitud de URL sospechosa",
    "Palabras clave sensibles detectadas"
  ]
}
```

---

## 💻 Comandos de Prueba

Puedes probar la API directamente desde tu terminal.

**Opción 1: cURL (Linux/Mac/Git Bash)**

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/scan/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "artifact_type": "URL",
  "content": "http://paypal-secure-update.com.login.php"
}'
```

**Opción 2: PowerShell (Windows)**

```powershell
$body = @{
    artifact_type = "URL"
    content = "http://paypal-secure-update.com.login.php"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/scan/analyze" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

---

## 🔮 Roadmap

- [x] **Fase 1:** Análisis Heurístico de URLs y Arquitectura Base.
- [x] **Fase 1.5:** Hardening (Testing, Logging, Async performance).
- [ ] **Fase 2:** Análisis de Texto Natural (NLP) para detección de Smishing.
- [ ] **Fase 3:** Integración con Threat Intelligence (VirusTotal).

---

## ⚠️ Aviso Legal

**Social Engineering Detector** es una herramienta educativa y defensiva.  
Su uso para atacar sistemas sin consentimiento es ilegal. Los desarrolladores no se hacen responsables del mal uso de este software.

---

## 👨‍💻 Autor

Desarrollado con ❤️ para una internet más segura.
