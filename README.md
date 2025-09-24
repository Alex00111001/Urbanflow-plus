# UrbanFlow+

UrbanFlow+ es una plataforma de movilidad urbana centrada en ofrecer rutas multimodales ultrarrápidas, confiables y personalizables. El proyecto combina aplicaciones móviles nativas, un backend escalable y un motor de planificación asistido por IA para superar la experiencia de uso de soluciones actuales como Moovit.

## Pilares clave

- **Usabilidad superior**: Inicio de un toque, accesos rápidos y microcopys motivadores.
- **IA explicable**: Rutas optimizadas con contexto de decisiones y aprendizaje de hábitos.
- **Cobertura global**: Integraciones con GTFS/GTFS-RT, ride-hailing y datos municipales.
- **Modo offline de alto valor**: Mapas vectoriales comprimidos, rutas y líneas frecuentes en caché.
- **Privacidad primero**: Controles granulares, anonimización y cumplimiento LGPD/GDPR.

## Contenido del repositorio

- [`docs/product_strategy.md`](docs/product_strategy.md): visión de producto, posicionamiento y roadmap.
- [`docs/architecture.md`](docs/architecture.md): arquitectura técnica, flujos de datos e infraestructura.
- [`docs/ux_ui.md`](docs/ux_ui.md): lineamientos de UX/UI, accesibilidad e internacionalización.
- [`docs/ai_routing.md`](docs/ai_routing.md): diseño del motor híbrido de rutas e IA de optimización.
- [`docs/delivery_plan.md`](docs/delivery_plan.md): plan de entrega con OKRs, backlog priorizado y responsables por fase.
- [`backend/`](backend/): API FastAPI con buscador natural, rutas multimodales, llegadas en tiempo real simuladas y servicios premium.

### Ejecutar el backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
uvicorn app.main:app --reload
```

Endpoints principales:

- `POST /search/interpret`: interpreta comandos conversacionales multiidioma y devuelve origen/destino/horario.
- `POST /search/plan`: genera rutas a partir de lenguaje natural usando el motor interno.
- `POST /routes/plan`: devuelve múltiples itinerarios explicables con métricas de duración, costo y CO₂.
- `POST /routes/replan`: propone recuperación ante incidencias.
- `GET /realtime/{line_id}`: simulación determinística de llegadas en tiempo real.
- `POST /premium/schedule`: cronograma inteligente con buffer dinámico según clima/tráfico.
- `POST /premium/heatmap`: mapa de calor personal con recomendaciones proactivas.

## Próximos pasos sugeridos

1. Validar hipótesis clave con pruebas de usabilidad y pilotos en 2 ciudades.
2. Implementar MVP con funciones núcleo gratuitas y telemetría de observabilidad.
3. Activar gradualmente funcionalidades premium y experimentos de pricing adaptativo.

---

> "Llegarás a tiempo, sin estrés." — Lema de UrbanFlow+
