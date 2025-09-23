# Lineamientos UX/UI e internacionalización

## Principios de diseño
- **Acceso inmediato**: home con botones de 1 toque a "Casa", "Trabajo" y "Favoritos" más buscador conversacional siempre visible.
- **Velocidad cognitiva**: tarjetas resumidas con KPIs clave (tiempo, costo, transbordos) y filtros rápidos arriba del pliegue.
- **Accesibilidad integral**: cumplimiento WCAG 2.1 AA, soporte VoiceOver/TalkBack, tamaños de texto dinámicos, modo alto contraste.
- **Consistencia multilenguaje**: uso de ICU MessageFormat, pluralización correcta y localización de unidades, moneda y hora.
- **Confianza y seguridad**: alertas claras, feedback háptico, opción de compartir viaje con contactos.

## Estructura de navegación
1. **Onboarding** → selección de idioma, permisos, definición de Casa/Trabajo, favoritos y preferencias de accesibilidad.
2. **Home** → buscador natural, accesos rápidos, historial reciente y widgets contextuales (clima, alertas).
3. **Planificación de ruta** → mapa + lista sincronizados; filtros: *Más rápido*, *Más barato*, *Menos caminata*, *Menos transbordos*, *Accesible*.
4. **Viaje en curso** → pasos detallados, vista de progreso, vibración 2 paradas antes, opción de replanificar.
5. **Premium Hub** → cronograma inteligente, bitácora, mapa de calor, widgets iOS/Android, exportaciones calendario.
6. **Perfil** → suscripciones, privacidad, idioma, accesibilidad, historial, modo privado.

## Componentes clave
- **Tarjetas de ruta**: muestran tiempo estimado, hora de llegada, costo, CO₂, transbordos, accesibilidad (iconos) y explicaciones IA.
- **FAB "Ruta rápida"**: abre planificador con parámetros basados en contexto (ubicación, hora, hábitos aprendidos).
- **Mapa MapLibre** con capas personalizadas: tráfico, accesibilidad (rampas, elevadores), densidad crowdsourcing.
- **Alertas multicanal**: push, hápticas, sonoras y texto; personalizables por usuario y modo.
- **Widgets & atajos**: iOS (WidgetKit, Siri Shortcuts) y Android (App Widgets, Intents) para acceso rápido a rutas frecuentes.

## Temas y tokens
- **Tipografía**: Inter/Roboto, escalas 12–20–28–34 px.
- **Tema claro**: fondo #FFFFFF, texto #111111, primario #3B82F6, estados accesibles con contraste AA/AAA.
- **Tema oscuro**: fondo #0B0F14, texto #EAEAEA, primario #60A5FA; fondos de tarjetas #111827.
- **Iconografía**: sistema vectorial adaptado a Material/Apple HIG, soporte para variantes accesibles.

## Internacionalización (i18n)
- Locales iniciales: `es-419`, `pt-BR`, `en`.
- Catálogo gestionado con ICU MessageFormat + traducción asistida (Crowdin/Localized).
- Localización de formatos: fecha/hora (24h/12h), unidades de distancia (km/mi), moneda regional para precios ride-hailing y tarifas.
- Soporte RTL preparado para escalabilidad futura.

## Experiencia offline
- Pantalla dedicada que muestra rutas descargadas, mapas y líneas frecuentes disponibles sin conexión.
- Indicadores claros de sincronización, tamaño de descarga y fecha de actualización.

## Accesibilidad avanzada
- Rutas accesibles marcadas con metadatos (ascensores, rampas, caminos sin escaleras).
- Ajustes de contraste y vibración configurable; modo "baja visión" con iconos simplificados.
- Compatibilidad con lectores de pantalla: orden lógico, labels descriptivos, acciones personalizadas.

## Copywriting y NLU
- Tono empático y orientado a logro: "Llegarás a tiempo, sin estrés".
- Microcopy positivo: "Todo listo", "Ruta optimizada".
- Comandos naturales soportados: "Quiero llegar a las 8", "Avísame cuando falten 2 paradas".

## Métricas UX
- Tiempo medio para planificar primera ruta < 30 s en onboarding.
- Puntuación SUS > 85 en pruebas de usabilidad.
- Error rate en búsqueda conversacional < 5% tras entrenamiento inicial.
