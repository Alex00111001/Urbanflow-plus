# Fase 1: Fundaciones backend y datos

Esta fase cubre el primer trimestre del roadmap (T1) para llevar UrbanFlow+ de la visión y prototipo documental a un backend operativo con datos reales y cimientos de experiencia móvil. Se estructura en seis sprints de dos semanas con objetivos claros, responsables y criterios de salida.

## Objetivos generales
- Ingerir y normalizar feeds GTFS/GTFS-Realtime de las ciudades piloto.
- Desplegar un backend FastAPI endurecido con autenticación, cache y observabilidad básica.
- Sentar bases de las apps nativas (Android/iOS) con onboarding, home y planificador.
- Preparar infraestructura reproducible (Docker → Terraform → Kubernetes) con pipelines CI/CD mínimos.

## Sprints propuestos (2 semanas c/u)

### Sprint 1: Base de datos y ingesta inicial
- **Backend/Data**
  - Provisionar Postgres + PostGIS en entorno local y nube (Docker Compose).
  - Construir ETL incremental GTFS → PostGIS (agencias, rutas, paradas, calendarios, trips).
  - Implementar validadores de calidad (paradas huérfanas, calendarios inconsistentes).
- **DevOps**
  - Configurar repos de IaC (Terraform) para base de datos y redes.
  - Pipeline CI para lint + pruebas backend.
- **Criterio de salida**: ETL ejecuta en <30 min por feed y datos accesibles vía SQL.

### Sprint 2: Motor de rutas conectando PostGIS
- **Backend**
  - Abstraer `TransitGraph` para cargar datos desde PostGIS.
  - Implementar heurísticas A* con pesos configurables (duración, costo, CO₂, accesibilidad).
  - Endpoint `/routes/plan` protegido con throttling y validaciones.
- **Data Science**
  - Definir dataset de entrenamiento ETA (features base).
- **Mobile**
  - Estructura de proyecto (Kotlin/Swift), onboarding con idiomas e iconografía.
- **Criterio de salida**: rutas generadas desde datos reales, aceptando preferencias.

### Sprint 3: Tiempo real y sincronización
- **Backend**
  - Consumir GTFS-RT (VehiclePositions/TripUpdates) y almacenar en Redis.
  - Endpoint `/realtime/arrivals` con fallback crowdsourcing.
  - WebSocket/SSE para actualizaciones de viaje.
- **Mobile**
  - Pantalla Home con accesos rápidos (Casa/Trabajo/Favoritos) + búsqueda natural conectada al backend.
- **DevOps**
  - Instrumentar OpenTelemetry → Grafana (métricas básicas) + Sentry.
- **Criterio de salida**: llegadas en tiempo real visibles en apps dummy.

### Sprint 4: Seguridad y modo offline
- **Backend**
  - Autenticación OAuth2 (Keycloak/Auth0) + roles básicos.
  - API de favoritos/historial con cifrado en reposo.
- **Mobile**
  - Cache Room/CoreData para favoritos + historial.
  - Descarga de tiles vectoriales iniciales por zona.
- **Privacy/Legal**
  - Políticas de consentimiento granular y data retention.
- **Criterio de salida**: usuario puede planificar y guardar rutas sin conexión limitada.

### Sprint 5: Accesibilidad y experiencia en viaje
- **Backend**
  - Marcar rutas accesibles (ascensores, rampas) con datos complementarios.
  - Alertas hápticas y notificaciones “baja en X paradas”.
- **Mobile**
  - Vista “Viaje en curso” con timeline y replanificación por eventos.
  - Ajustes de accesibilidad (texto dinámico, contraste alto, soporte VoiceOver/TalkBack).
- **Criterio de salida**: flujo completo de viaje accesible y con alertas.

### Sprint 6: Endurecimiento y beta cerrada
- **Backend**
  - Pruebas de carga (Locust/k6) y tuning de índices PostGIS.
  - Versionado de API y documentación OpenAPI.
- **Mobile**
  - Beta TestFlight/Play Console, crash reporting integrado.
- **DevOps**
  - Despliegue en Kubernetes (staging) con autoscaling básico.
  - Backups automáticos y playbooks de incidentes.
- **Criterio de salida**: beta privada con pilotos en ciudades seleccionadas.

## Tablero RACI resumido
| Dominio | Responsible | Accountable | Consulted | Informed |
| --- | --- | --- | --- | --- |
| ETL & PostGIS | Data Lead | CTO | Backend Lead, Partnerships | Producto |
| Motor rutas | Backend Lead | CTO | Data Science, Mobile Leads | Soporte |
| Tiempo real | Backend Lead | CTO | Data Engineering, Operaciones | Producto |
| Mobile Android | Android Lead | CTO | UX/UI, QA | Marketing |
| Mobile iOS | iOS Lead | CTO | UX/UI, QA | Marketing |
| DevOps & Observabilidad | DevOps Lead | CTO | SecOps, Infra Partner | Toda la org |

## Métricas de éxito de la fase
- 95% de solicitudes `/routes/plan` < 1.2 s P95 en staging.
- 90% de cobertura GTFS/GTFS-RT para las líneas priorizadas en ciudades piloto.
- Crash-free rate ≥ 97% en beta móvil.
- Tiempo de recuperación < 30 min ante incidentes críticos.

## Riesgos específicos y mitigación
- **Latencia PostGIS elevada** → Indexar geometrías, caching selectivo en Redis.
- **Datos GTFS incompletos** → Enriquecimiento con APIs municipales, crowdsourcing moderado.
- **Falta de testers beta** → Programas con universidades y empresas locales.
- **Sobrecarga del equipo móvil** → Evaluar Flutter como refuerzo y priorizar features críticos.

## Checklist de salida de fase 1
- [ ] ETL automática y monitoreada para feeds prioritarios.
- [ ] Motor de rutas integrado con preferencias personalizables.
- [ ] App Android/iOS con onboarding, home y planificador funcionales.
- [ ] Observabilidad básica operativa (dashboards + alertas).
- [ ] Pipeline CI/CD desplegando a staging en <30 min.
- [ ] Evaluación post-mortem y plan de endurecimiento para fase 2.

