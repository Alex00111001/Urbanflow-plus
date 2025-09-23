# Arquitectura técnica

## Visión general
UrbanFlow+ adopta una arquitectura modular compuesta por aplicaciones móviles nativas (Android/iOS), servicios backend basados en microservicios y un motor de rutas híbrido con capacidades on-device y en la nube. La plataforma prioriza resiliencia, baja latencia y cumplimiento normativo.

```
Usuarios → Apps móviles → API Gateway → Servicios backend → Motores IA / Bases de datos → Integraciones externas
```

## Componentes principales

### Aplicaciones móviles
- **Android (Kotlin + Jetpack Compose)** y **iOS (Swift + SwiftUI)** con capas compartidas de lógica mediante Kotlin Multiplatform o módulos Dart (si se evalúa Flutter). 
- **Módulos clave**: Onboarding, Inicio (búsqueda conversacional, favoritos), Planificador de rutas, Viaje en curso, Premium Hub, Perfil.
- **Sincronización en tiempo real**: WebSockets/SSE para actualizaciones de llegada, alertas de incidencias y replanificación.
- **Modo offline**: almacenamiento cifrado con Room/Core Data, tiles vectoriales (MapLibre), rutas y líneas frecuentes cacheadas.

### API Gateway y Backend
- **API principal** con FastAPI o NestJS, operando en contenedores sobre Kubernetes.
- **Autenticación**: OAuth 2.0 + OpenID Connect, soporte para inicio social y credenciales corporativas.
- **Servicios especializados**:
  - `routing-service`: orquesta peticiones al motor de rutas, aplica filtros (más rápido, menos caminata, accesible).
  - `realtime-service`: ingesta GTFS-RT, crowdsourcing y eventos externos; publica actualizaciones vía Redis Streams.
  - `user-profile-service`: gestiona preferencias, idioma, favoritos, hábitos y métricas de mapa de calor.
  - `premium-service`: IA de cronograma inteligente, bitácora, widgets y exportación a calendarios.
  - `analytics-service`: pipeline ClickHouse + OpenTelemetry para métricas, experimentos y auditoría.

### Motor de rutas híbrido
- Implementado en Python (NetworkX/OR-Tools) con módulos ML ligeros (LightGBM/NN) empaquetados vía ONNX.
- **Planificación on-device** para rutas recurrentes o ajustes rápidos; sincronización con el motor central cuando hay conectividad.
- **Explicabilidad**: cada recomendación incluye atributos (tiempo, costo, CO₂, caminata, accesibilidad) y razones ponderadas.
- **Replanificación proactiva** mediante colas Redis + worker de eventos que recalcula rutas frente a retrasos/incidencias.

### Almacenamiento y datos
- **Postgres + PostGIS** para datos estáticos (mapas, estaciones, rutas base).
- **Redis** para caché de sesiones, colas de eventos y almacenamiento de estado en tiempo real.
- **ClickHouse** para analítica de grandes volúmenes y telemetría.
- **S3/MinIO** para tiles vectoriales y paquetes offline.

### Integraciones externas
- **GTFS/GTFS-RT**: ingesta periódica y en streaming con validadores automáticos.
- **Ride-hailing (Uber/Bolt/99/DiDi)**: APIs oficiales según región, con estimaciones de tarifa y tiempo de llegada.
- **Clima y eventos**: APIs meteorológicas y calendarios municipales para ajustar cronogramas IA.
- **Servicios push**: Firebase Cloud Messaging (Android) y APNs (iOS) para alertas y notificaciones proactivas.

## Infraestructura y DevOps
- **Despliegue**: Docker + Kubernetes (EKS/GKE) con Terraform y GitOps (ArgoCD/Flux).
- **Entrega continua**: pipelines CI/CD (GitHub Actions) con pruebas unitarias, integración y tests end-to-end con dispositivos reales.
- **Observabilidad**: OpenTelemetry → Grafana, Loki, Prometheus; Sentry para rastreo de errores.
- **Seguridad**: escaneo de contenedores, secretos gestionados con Vault/Secret Manager, cumplimiento LGPD/GDPR.

## Estrategia de baja latencia
- CDNs (Cloudflare) para distribución de tiles y assets.
- Caches regionales de rutas populares y datos en Redis + replicación multi-región.
- Compresión de payloads (gRPC/HTTP2, Brotli) y throttling adaptativo de sockets.

## Escalabilidad y resiliencia
- Feature flags por ciudad y AB testing para desplegar nuevas funciones.
- Sharding de datos por región para cumplir regulaciones (ej. datos de la UE en centros EU).
- Estrategias de autoscaling basadas en colas de eventos y métricas de CPU/memoria.
- Modo degradado: fallback a horarios estáticos y rutas históricas ante pérdida de datos en tiempo real.

## Seguridad y privacidad
- Cifrado TLS 1.3 en tránsito, AES-256 en reposo.
- Consentimiento granular (ubicación, analítica, comunicaciones) con registros auditables.
- Differential privacy en agregaciones para mapa de calor y analítica B2B.
- Modo privado en apps: no se guarda historial ni preferencias en la nube.

## Roadmap técnico
1. Configurar pipelines de datos GTFS/GTFS-RT y normalización en PostGIS.
2. Desarrollar MVP del motor de rutas con heurísticas básicas + UI móvil.
3. Añadir modelos ML para priorización de rutas y cronograma inteligente.
4. Optimizar modo offline (paquetes descargables, delta updates).
5. Fortalecer gobernanza de datos, certificaciones de seguridad y auditorías.
