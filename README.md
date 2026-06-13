# Analizador de Chats de WhatsApp

Trabajo Práctico — Ingeniería de Software III — Grupo 7 — 2026

Aplicación web para analizar conversaciones exportadas de WhatsApp y visualizar
estadísticas: mensajes por usuario, emojis más usados, franjas horarias,
días con más actividad y nube de palabras.

El usuario sube el `.zip` exportado desde WhatsApp y la aplicación procesa el
`.txt` que contiene, devolviendo gráficos interactivos y un resumen del chat.

## Características

- Total de mensajes y lista de participantes.
- Mensajes por participante, por hora del día y por día de la semana.
- Top 5 días más activos.
- Emoji más usado (a nivel general y por usuario).
- Nube de palabras (excluyendo *stopwords* en español).

## Stack tecnológico

| Capa       | Tecnología                              |
|------------|-----------------------------------------|
| Backend    | Python 3.11 + Flask                     |
| Frontend   | HTML5 + JavaScript vanilla + CSS3       |
| Gráficos   | Chart.js                                |
| Análisis   | pandas · emoji · WordCloud · Matplotlib · NLTK |
| Servidor   | Gunicorn (producción)                   |
| Contenedor | Docker + Docker Compose                 |
| Tests      | pytest                                  |

## Estructura del proyecto

```
tp-is3-grupo-7/
├── docker-compose.yml      # Orquestación backend + frontend
├── Dockerfile              # Imagen del backend
├── README.md               # Este archivo
│
├── backend/
│   ├── app.py              # API Flask (endpoints /health y /analyze)
│   ├── parser.py           # Parseo y validación del export de WhatsApp
│   ├── stats.py            # Cálculo de estadísticas
│   ├── text_utils.py       # Limpieza de texto y nube de palabras
│   ├── requirements.txt    # Dependencias Python
│   ├── conftest.py         # Fixtures de pytest
│   └── tests/              # Pruebas unitarias y de integración
│
└── frontend/
    ├── index.html          # Página principal
    ├── app.js              # Lógica de cliente (subida y render de gráficos)
    └── style.css           # Estilos
```

## Requisitos

- **Opción Docker:** Docker Desktop, con los puertos `80` y `5000` libres.
- **Opción manual:** Python 3.11 y los puertos `5000` (backend) y `8000` (frontend) libres.

## Instalación y ejecución

### Opción 1 — Docker Compose (recomendada)

```bash
docker-compose up --build
```

- Frontend: <http://localhost>
- Backend (API): <http://localhost:5000>

Para detener: `Ctrl+C` y luego `docker-compose down`.

### Opción 2 — Manual (dos terminales)

**Terminal A — backend:**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

El backend queda en <http://localhost:5000>.

**Terminal B — frontend:**

```bash
cd frontend
python -m http.server 8000
```

Abrí <http://localhost:8000> en el navegador.

> El frontend detecta el backend en el puerto `5000` del mismo host de forma
> automática, por lo que no requiere configuración adicional.

## Uso

1. **Exportar el chat desde WhatsApp:** abrí el chat → *Más opciones* →
   *Exportar chat* → *Sin multimedia*. Se descarga un archivo `.zip`.
2. **Subirlo:** en la aplicación, seleccioná el `.zip` y hacé clic en *Analizar*.
3. **Ver resultados:** tras unos segundos se muestran el resumen, los gráficos
   y la nube de palabras.

## Tests

El backend cuenta con pruebas unitarias (de cada función) y de integración
*end-to-end* (a través del endpoint HTTP).

```bash
cd backend
pip install -r requirements.txt
python -m pytest -v
```

## API REST

Base: `http://localhost:5000`

### `GET /health`

Verifica que el servidor esté activo.

```json
{ "status": "ok" }
```

### `POST /analyze`

Recibe un `.zip` exportado de WhatsApp (campo `file`, `multipart/form-data`) y
devuelve las estadísticas del chat.

**Respuesta `200 OK` (resumida):**

```json
{
  "total_messages": 2547,
  "participants": ["Juan", "María", "Pedro"],
  "messages_per_user": { "Juan": 812, "María": 745, "Pedro": 654 },
  "messages_by_hour": { "0": 15, "23": 42 },
  "messages_by_weekday": { "0": 385, "6": 298 },
  "top_days": [["2024-06-15", 145], ["2024-06-10", 138]],
  "emojis_per_user": { "Juan": { "😂": 45, "👍": 28 } },
  "most_frequent_emoji": ["😂", 289],
  "wordcloud_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Errores:**

| Código | Condición                          |
|--------|------------------------------------|
| `400`  | No se envió archivo                |
| `400`  | El archivo no es un `.zip`         |
| `400`  | El `.zip` está corrupto o sin `.txt` |
| `422`  | El contenido no es un export de WhatsApp |

## Integrantes

| Nombre                  | GitHub                                               |
|-------------------------|------------------------------------------------------|
| Juan Cruz Trinidad      | [@JuanCruzTrinidad](https://github.com/JuanCruzTrinidad) |
| Agustín Federico Corno  | [@AgustinCorno](https://github.com/AgustinCorno)     |
| Ignacio Daniel Maria    | [@ignaciomaria](https://github.com/ignaciomaria)     |
| Iván Bravo              | [@ivann-bravo](https://github.com/ivann-bravo)       |
| Leandro Ivan Vera       | [@Lean-IV](https://github.com/Lean-IV)               |
