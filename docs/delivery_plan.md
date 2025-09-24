# Plan de entrega UrbanFlow+

Este documento aterriza la **fase 0 (descubrimiento y backlog)** y prepara la transición hacia la fase 1 del roadmap. Resume objetivos, OKRs, épicas priorizadas, dependencias y responsables.

## Objetivos de la fase 0
- Validar alcance del MVP gratuito y del paquete Premium inicial.
- Definir el backlog accionable para los dos primeros trimestres (T1-T2).
- Asignar responsables, gobernanza y cadencia de seguimiento.
- Establecer criterios de salida y riesgos controlados.

## OKRs propuestos (fase 0)
| Objetivo | KR1 | KR2 | KR3 |
| --- | --- | --- | --- |
| **Alinear al equipo en visión y prioridades** | Taller cross-funcional con >90% de asistencia | Declarar "north star metrics" y KPIs secundarios | Definir el alcance detallado del MVP en Notion/Jira |
| **Preparar ejecución técnica y de datos** | Identificar fuentes GTFS/GTFS-RT para las 3 ciudades piloto | Seleccionar stack definitivo (Kotlin/Swift + FastAPI + PostGIS/Redis) | Completar plan de infraestructura (IaC, observabilidad, seguridad) |
| **Diseñar oferta Premium viable** | Definir paquete de features inicial, pricing y trial | Diseñar roadmap IA (cronograma, mapa de calor, predicciones) | Documentar flujos de monetización y referidos |

## Épicas y entregables prioritarios

### T1 – MVP gratuito (12 semanas)
1. **Ingesta de datos y motor base**
   - Pipeline ETL GTFS → PostGIS.
   - Motor A* multimodal con heurísticas (sin ML) + API `/routes/plan` endurecida.
   - Cache Redis para llegadas en tiempo real (GTFS-RT + crowdsourcing).
2. **Aplicaciones móviles núcleo**
   - Onboarding multilenguaje (es-419, pt-BR, en).
   - Home con accesos rápidos (Casa/Trabajo/Favoritos), buscador conversacional.
   - Planificador con filtros: rápido, barato, accesible, menos transbordos.
3. **Plataforma y observabilidad**
   - Infraestructura Docker + Terraform + Kubernetes (entorno staging).
   - OpenTelemetry → Grafana + Sentry, alertas básicas.
   - Autenticación OAuth2 + control de permisos.

### T2 – IA y premium temprano (14 semanas)
1. **Motor IA y explicabilidad**
   - Modelo ETA (Gradient Boosting) con entrenamiento incremental.
   - Explicaciones textuales y visuales (diferencias de tiempo/costo/CO₂).
   - Replanificación reactiva vía WebSocket/SSE.
2. **Funciones Premium**
   - Cronograma inteligente con integración clima/eventos.
   - Bitácora de viaje (multi-destino) + exportación a Google/Apple Calendar.
   - Mapa de calor personal y widgets iOS/Android.
3. **Experiencia offline y accesibilidad avanzada**
   - Descarga de tiles vectoriales + rutas favoritas.
   - Rutas accesibles (ascensores, rampas) con datos enriquecidos.
   - VoiceOver/TalkBack y tamaños dinámicos certificados.

## Historias de usuario representativas
| Épica | Historia | Criterios de aceptación |
| --- | --- | --- |
| Ingesta de datos | "Como planificador, quiero cargar feeds GTFS para generar rutas exactas" | Validar feed, normalizar zonas horarias, actualizar grafo en <30 min |
| Motor IA | "Como usuario, quiero que la app explique por qué recomienda una ruta" | Mostrar resumen textual (tiempo, costo, CO₂, transbordos), accesible en lector de pantalla |
| Cronograma inteligente | "Quiero recibir un aviso cuando deba salir para llegar a tiempo" | Notificación push ≥15 min antes, recalculada con clima/incidencias |
| Modo offline | "Necesito planificar una ruta sin conexión" | Ver últimos itinerarios guardados, mapa vectorial local, advertir datos desactualizados |
| Seguridad | "Quiero compartir mi trayecto en vivo" | Enviar enlace seguro con ETA, paradas restantes y botón de SOS |

## Asignación de responsables (RACI)
| Área | Responsible | Accountable | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Producto & UX | Product Lead | CPO | UX Research, Data Science | Support, Marketing |
| Backend & IA | Tech Lead Backend | CTO | Data Engineering, Mobile Leads | Customer Success |
| Mobile Android | Android Lead | CTO | UX/UI, QA | Producto |
| Mobile iOS | iOS Lead | CTO | UX/UI, QA | Producto |
| Datos & Integraciones | Data Lead | CTO | Partnerships, Legal | Producto |
| DevOps & Seguridad | DevOps Lead | CTO | SecOps, Infra Partner | Toda la org |

## Gobernanza y cadencia
- **Ceremonias**: weekly sync (30 min), revisión quincenal de roadmap, steering mensual con C-level.
- **Herramientas**: Jira para backlog, Linear para bugs, Notion para documentación, Slack + canales dedicados por dominio.
- **Métricas de seguimiento**: % historias completadas por sprint, cobertura de pruebas, latencia promedio API, crash-free rate apps.

## Criterios de salida fase 0
- OKRs aprobados y registrados.
- Backlog T1-T2 priorizado y estimado (story points o t-shirt sizing).
- Equipo núcleo asignado y con disponibilidad comprometida.
- Riesgos críticos documentados con planes de mitigación.

## Riesgos y acciones
| Riesgo | Impacto | Probabilidad | Mitigación |
| --- | --- | --- | --- |
| Retrasos en acuerdos de datos GTFS | Alto | Medio | Paralelizar con scraping/API públicas, alianzas tempranas |
| Complejidad IA vs hardware móvil | Medio | Alto | Prototipos con modelos ligeros, fallback server-side |
| Cumplimiento LGPD/GDPR | Alto | Medio | Asesor legal temprano, privacy by design, DPO dedicado |
| Capacidad del equipo móvil | Alto | Alto | Contrataciones puente, posible adopción Flutter para acelerar |
| Dependencia de proveedores ride-hailing | Medio | Medio | Múltiples integraciones + mecanismos de fallback |

---
**Estado actual (abrir cada sprint)**
- Épicas T1 definidas: ✅
- Estimaciones iniciales: ⏳ en progreso
- Equipo asignado: ⏳ pendiente confirmación
- Integraciones clave investigadas: 🚧 (GTFS SP y CDMX evaluados)

