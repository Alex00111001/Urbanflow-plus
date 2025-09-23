# Motor de rutas e inteligencia artificial

## Objetivos
- Entregar rutas multimodales óptimas considerando tiempo, costo, CO₂, transbordos y accesibilidad.
- Replanificar en tiempo real frente a retrasos o incidencias usando datos GTFS-RT y crowdsourcing.
- Aprender hábitos individuales para ofrecer recomendaciones proactivas y cronogramas inteligentes.
- Explicar cada sugerencia con transparencia y métricas cuantificables.

## Arquitectura del motor
1. **Ingesta de datos**:
   - GTFS estático → PostGIS para redes base (paradas, líneas, horarios).
   - GTFS-Realtime → Redis Streams para llegadas, cancelaciones, ocupación.
   - Datos crowdsourced → API móvil (reportes de retraso/aforo), normalizados con verificaciones de confianza.
   - Datos externos → clima, eventos, tráfico.
2. **Preprocesamiento**:
   - Construcción de grafos multimodales con pesos dinámicos.
   - Indexación de ubicaciones frecuentes y POIs.
   - Generación de features para modelos ML (tiempo histórico, varianza, fiabilidad por línea).
3. **Planificación base**:
   - Algoritmo A* adaptado para multimodalidad (walk/bike/transit/ride-hailing).
   - Penalizaciones configurables: tiempo de espera, caminata, transbordos, accesibilidad.
   - Uso de heurísticas específicas por ciudad (ventanas de metro, restricciones nocturnas).
4. **Optimización IA**:
   - Modelo Gradient Boosting / NN ligera que estima utilidad total de cada ruta.
   - Ranking multiobjetivo con explainers SHAP/Integrated Gradients para resaltar factores.
   - Aprendizaje federado opcional para entrenar hábitos sin exponer datos personales.
5. **Explicabilidad**:
   - Mensajes naturales: "12 min más rápido, 1 transbordo menos y 20% menos CO₂".
   - Visualización de trade-offs en tarjetas (badges e íconos).
6. **Replanificación**:
   - Trigger por eventos (atrasos > X min, saturación de aforo, clima adverso).
   - Cálculo incremental: reutiliza subgrafos, genera rutas alternativas ordenadas.
   - Notificaciones push/hápticas y actualizaciones en UI en <3s.

## Modo offline
- Cacheo de grafos locales para rutas favoritas y zonas específicas.
- Paquetes de datos comprimidos (Protocol Buffers + delta updates) sincronizados cuando hay Wi-Fi.
- Inferencia on-device: modelos convertidos a CoreML/TF Lite para tiempos de viaje estimados.

## Cronograma inteligente (Premium)
- Predice hora óptima de salida combinando clima, tráfico histórico, objetivos del usuario y margen de seguridad.
- Envía notificaciones "sal ahora" o "puedes esperar 5 minutos" con explicación.
- Ajusta la recomendación si detecta cambios de hábitos (home office, vacaciones).

## Bitácora y rutas predictivas (Premium)
- Permite planificar múltiples paradas con dependencias (ej. dejar hijos en escuela → ir al trabajo).
- Aprende secuencias frecuentes para sugerir rutas antes de que el usuario lo pida.
- Exporta itinerarios a Google/Apple Calendar con recordatorios contextuales.

## Métricas de desempeño
- Latencia promedio de cálculo: < 500 ms para rutas urbanas (en backend), < 200 ms para replanificación incremental.
- Precisión ETA: ±2 min en 80% de viajes, ±5 min en 95%.
- Tasa de aceptación de recomendaciones IA > 60%.
- Reducción de tiempo promedio vs rutas estáticas > 10%.

## Gobernanza y ética
- Logs auditables de decisiones IA (sin datos personales) para revisión.
- Controles para reportar rutas inapropiadas y retroalimentación del usuario.
- Cumplimiento de principios de transparencia, no discriminación y minimización de datos.
