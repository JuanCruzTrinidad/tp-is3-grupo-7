# Plan — WhatsApp Chat Analyzer

## Problem Statement

Aplicación web que recibe un `.zip` exportado de WhatsApp, lo procesa en un backend Flask
y muestra estadísticas visuales en un frontend HTML/JS vanilla con Chart.js.

## Requirements

- El usuario sube un `.zip` (export de WhatsApp) desde el frontend
- El backend lo descomprime, parsea el `.txt` y devuelve todas las stats en una sola respuesta JSON stateless
- Stats: mensajes por usuario, emojis más usados, actividad por hora, días top (ranking de fechas + distribución por día de semana), word cloud (generada en backend como base64)
- Limpieza de texto: remover stop words y puntuación antes de generar el word cloud
- Frontend con Chart.js para los gráficos y la imagen del word cloud embebida
- Docker Compose levanta backend (gunicorn) + frontend (nginx)
- Al terminar cada task, proveer un `curl` de prueba antes de pushear la rama

## Stack

| Capa      | Tecnología                           |
|-----------|--------------------------------------|
| Backend   | Python 3.11 + Flask + gunicorn       |
| Frontend  | HTML5 + JS vanilla + CSS3 + Chart.js |
| Infra     | Docker Compose — nginx + gunicorn    |

## Decisiones de diseño

- **Word cloud:** backend genera PNG → base64; frontend embebe en `<img>`
- **Días top:** ranking top-5 fechas + distribución por día de semana (0=lunes…6=domingo)
- **Stateless:** un único endpoint `POST /analyze` devuelve todo el JSON
- **Frontend:** sin frameworks, Chart.js desde CDN

## Arquitectura del endpoint principal

```
POST /analyze  ←  multipart/form-data (.zip)
                  ↓
         descomprimir en memoria (zipfile stdlib)
                  ↓
         validar y parsear .txt (parser.py)
                  ↓
         calcular stats (stats.py)
         limpiar texto + generar wordcloud (text_utils.py)
                  ↓
         JSON response con todo
```

### Estructura del JSON de respuesta

```json
{
  "total_messages": 1234,
  "participants": ["Ana", "Luis"],
  "messages_per_user": {"Ana": 700, "Luis": 534},
  "messages_by_hour": {"0": 10, "1": 5},
  "messages_by_weekday": {"0": 200, "1": 180},
  "top_days": [["2024-03-15", 87], ["2024-01-01", 65]],
  "emojis_per_user": {"Ana": {"😂": 30}},
  "most_frequent_emoji": ["😂", 80],
  "wordcloud_base64": "iVBORw0KGgo..."
}
```

## Branch strategy

| Branch                  | Task                                    |
|-------------------------|-----------------------------------------|
| `feat/sortDays`         | Task 1 — top_days + messages_by_weekday |
| `feat/clean-text`       | Task 2 — clean_text en text_utils.py    |
| `feat/wordcloud`        | Task 3 — generate_wordcloud_base64      |
| `feat/frontend-setup`   | Task 4 — frontend + Docker Compose      |
| `feat/frontend-layout`  | Task 5 — layout HTML/CSS                |
| `feat/analyze-endpoint` | Task 6 — POST /analyze + Chart.js       |

---

## Tasks

### Task 1 — Ordenar y seleccionar los días top
**Branch:** `feat/sortDays`

Agregar en `stats.py`:
- `top_days(messages, n=5)` → lista de `[fecha, count]` ordenada desc
- `messages_by_weekday(messages)` → dict `{0..6: count}`, siempre 7 claves

Reutilizar `messages_by_date()` para `top_days`.
Usar `parse_timestamp().weekday()` para `messages_by_weekday`.

Exponer `GET /stats/top-days` en `app.py` con datos hardcodeados para verificación.

---

### Task 2 — Limpiar texto
**Branch:** `feat/clean-text`

Crear `backend/text_utils.py` con:
- `clean_text(messages, lang="spanish")` → string limpio (sin puntuación, stop words, URLs, tokens de WhatsApp como `<Multimedia omitido>`)

Agregar `nltk` a `requirements.txt`.

---

### Task 3 — Generar word cloud
**Branch:** `feat/wordcloud`

Agregar en `text_utils.py`:
- `generate_wordcloud_base64(messages)` → string base64 de PNG (800×400, fondo blanco)

Usar `WordCloud` + `matplotlib` en memoria, sin escribir a disco.

---

### Task 4 — Configurar proyecto web
**Branch:** `feat/frontend-setup`

- Crear `frontend/index.html`, `frontend/style.css`, `frontend/app.js` (stubs)
- Actualizar `docker-compose.yml`: agregar servicio `frontend` con `nginx:alpine`
- Agregar `gunicorn` a `requirements.txt` y actualizar `Dockerfile` para usarlo
- Frontend en puerto 80, backend en puerto 5000

---

### Task 5 — Layout básico
**Branch:** `feat/frontend-layout`

Implementar HTML/CSS con secciones:
- `#upload` — formulario con `<input type="file" accept=".zip">`
- `#summary` — total mensajes, participantes, emoji top
- `#chart-hour` — gráfico por hora
- `#chart-user` — gráfico por usuario
- `#chart-weekday` — gráfico por día de semana
- `#chart-top-days` — gráfico días top
- `#wordcloud` — imagen word cloud

---

### Task 6 — Endpoint /analyze + Chart.js
**Branch:** `feat/analyze-endpoint`

Backend:
- `POST /analyze` en `app.py`: recibe `.zip`, descomprime en memoria, parsea, calcula todas las stats, devuelve JSON completo

Frontend:
- `app.js`: `fetch` a `POST /analyze`, renderiza todos los gráficos con Chart.js (CDN), embebe word cloud en `<img>`
