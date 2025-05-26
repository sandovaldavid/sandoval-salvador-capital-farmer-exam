# Sistema de Cotizaciones - Capital & Farmer

## Instalación

1. Clonar el repositorio
2. Crear archivo `.env` con tu API key de OpenAI:
    ```
    OPENAI_API_KEY=tu_api_key_aquí
    ```
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`

## Uso

-   Ir a `http://localhost:8000`
-   Llenar formulario y generar cotización

## APIs utilizadas

-   OpenAI Chat API

## Funcionalidades bonus

-   Validación de formulario
-   IA para propuesta legal automática
-   Interfaz moderna y responsiva
-   Manejo de errores de API

---

## Parte 3 - Arquitectura

### 1. Modularización

Para escalar el sistema, implementaría:

-   **Separación por dominios**: Crear módulos independientes para cotizaciones, clientes, pagos, etc.
-   **Arquitectura hexagonal**: Separar lógica de negocio de infraestructura
-   **APIs bien definidas**: Usar interfaces claras entre módulos
-   **Microservicios**: Para alta escala, dividir en servicios independientes comunicándose vía REST/GraphQL

### 2. Escalabilidad de Base de Datos

Para manejar mayor volumen:

-   **Migración a PostgreSQL**: Mayor robustez y escalabilidad que SQLite
-   **Índices estratégicos**: En campos de búsqueda frecuente (email, num_cotización, fecha)
-   **Normalización**: Separar tablas para clientes, servicios, precios
-   **Connection pooling**: Para manejo eficiente de conexiones
-   **Read replicas**: Para distribuir carga de lectura

### 3. Integraciones Externas

Para integrar con servicios externos:

-   **SDKs oficiales**: Usar Google Drive API SDK, Dropbox API SDK
-   **Tareas asíncronas**: Implementar con Celery + Redis para procesos largos
-   **Circuit breaker pattern**: Para manejar fallos de servicios externos
-   **Retry policies**: Con backoff exponencial para reintentos
-   **Webhooks**: Para notificaciones en tiempo real

### 4. Deployment y Infraestructura

Para producción recomiendo:

-   **Containerización**: Docker para portabilidad y consistencia
-   **Cloud platforms**: Railway, Render, o AWS para escalabilidad
-   **HTTPS obligatorio**: SSL/TLS para seguridad
-   **CDN**: Para archivos estáticos
-   **Monitoring**: Logs centralizados y métricas de performance
-   **CI/CD**: Pipeline automatizado para deploys seguros

### 5. Seguridad

Medidas de seguridad implementadas/recomendadas:

-   **Validación de entrada**: Sanitización de datos con Pydantic
-   **Escape de HTML**: Prevención de XSS en templates
-   **Rate limiting**: Prevenir abuso de APIs
-   **Autenticación/Autorización**: JWT tokens para usuarios autenticados
-   **Variables de entorno**: Para secrets como API keys
-   **Logs de seguridad**: Auditoría de accesos y operaciones
