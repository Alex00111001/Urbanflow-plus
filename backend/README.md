# UrbanFlow+ Backend

Este paquete contiene el backend de referencia de UrbanFlow+, construido con FastAPI. Incluye:

- Motor de rutas multimodal con heurísticas y explicaciones.
- Ingesta simplificada de feeds GTFS para poblar el grafo de transporte.
- Intérprete de lenguaje natural para búsquedas conversacionales.
- Simulación determinística de llegadas en tiempo real.
- Servicios premium como cronograma inteligente y mapa de calor personal.

Consulta el README de la raíz del repositorio para más contexto.

## Cargar datos GTFS de ejemplo

El módulo `app.services.gtfs_loader` permite convertir un feed GTFS (directorio o `.zip`) en el grafo interno del motor de rutas. Ejemplo rápido usando el feed reducido utilizado en las pruebas automatizadas:

```python
from pathlib import Path

from app.services import gtfs_loader, route_engine

feed_path = Path("backend/tests/data/sample_gtfs")
data = gtfs_loader.load_gtfs_feed(feed_path)
graph = gtfs_loader.build_transit_graph(data)
route_engine.set_transit_graph(graph)
```

Tras ejecutar el snippet anterior, las peticiones a `POST /routes/plan` utilizarán el grafo construido desde GTFS, lo que acerca el comportamiento del backend a datos reales de agencias de transporte.
