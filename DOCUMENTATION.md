# Documentación — WhatsApp Chat Analyzer

**Trabajo Práctico — Ingeniería de Software III — Grupo 7 — 2026**

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Características](#características)
3. [Arquitectura](#arquitectura)
4. [Stack Tecnológico](#stack-tecnológico)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Componentes del Backend](#componentes-del-backend)
7. [Componentes del Frontend](#componentes-del-frontend)
8. [Flujo de Datos](#flujo-de-datos)
9. [API REST](#api-rest)
10. [Testing](#testing)
11. [Instalación y Configuración](#instalación-y-configuración)
12. [Uso de la Aplicación](#uso-de-la-aplicación)
13. [Integrantes del Equipo](#integrantes-del-equipo)

---

## Descripción General

**WhatsApp Chat Analyzer** es una aplicación web que permite analizar
conversaciones exportadas de WhatsApp y visualizar estadísticas detalladas sobre
los patrones de comunicación del grupo.

La aplicación procesa archivos ZIP descargados desde WhatsApp (que contienen un
archivo `.txt` con los mensajes) y genera visualizaciones interactivas con
gráficos, análisis de emojis, actividad por hora, nube de palabras y más.

---

## Características

- **Análisis de conversaciones:** procesa exports nativos de WhatsApp en formato ZIP.
- **Estadísticas básicas:** total de mensajes, número de participantes, emoji más usado.
- **Gráficos interactivos:**
  - Mensajes por participante.
  - Actividad por hora del día.
  - Distribución por día de la semana.
  - Top 5 días más activos.
- **Análisis de emojis:** emoji más usado a nivel general y por usuario.
- **Nube de palabras:** palabras más frecuentes, excluyendo *stopwords* en español.
- **Interfaz responsive:** con validación de archivo y feedback de carga.
- **Contenerización:** preparada para ejecutarse con Docker.
- **Cobertura de pruebas:** suite de tests unitarios y de integración con pytest.

---

## Arquitectura

La aplicación sigue una arquitectura **cliente-servidor** de dos capas:

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Cliente)                      │
│              HTML5 + CSS3 + JavaScript Vanilla               │
│              (nginx en Docker o servidor HTTP local)         │
└─────────────────────────────────────────────────────────────┘
                              │
                    HTTP/JSON (CORS habilitado)
                              │
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (Servidor)                      │
│              Python 3.11 + Flask (puerto 5000)               │
│                                                              │
│  - Parser de WhatsApp          (parser.py)                   │
│  - Cálculo de estadísticas     (stats.py)                    │
│  - Procesamiento de texto      (text_utils.py)               │
│  - API REST                    (app.py)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

| Aspecto | Tecnología | Versión |
|---------|-----------|---------|
| **Backend Runtime** | Python | 3.11 |
| **Framework Backend** | Flask | ≥ 3.0.0 |
| **CORS** | Flask-CORS | ≥ 4.0.0 |
| **Frontend** | HTML5 + CSS3 + JavaScript | vanilla |
| **Gráficos** | Chart.js | 4.4.0 |
| **Procesamiento de Datos** | pandas | ≥ 2.2.0 |
| **Análisis de Emojis** | emoji | ≥ 2.10.0 |
| **Nube de Palabras** | WordCloud | ≥ 1.9.3 |
| **Visualización** | Matplotlib | ≥ 3.8.0 |
| **Parser de Fechas** | python-dateutil | ≥ 2.9.0 |
| **NLP (stopwords)** | NLTK | ≥ 3.8.0 |
| **Servidor WSGI** | Gunicorn | ≥ 21.2.0 |
| **Testing** | pytest | ≥ 8.0.0 |
| **Contenerización** | Docker + Docker Compose | - |

---

## Estructura del Proyecto

```
tp-is3-grupo-7/
├── docker-compose.yml          # Orquestación de servicios Docker
├── Dockerfile                  # Imagen del backend
├── README.md                   # Guía rápida de instalación y uso
├── DOCUMENTATION.md            # Esta documentación
│
├── backend/
│   ├── app.py                  # Aplicación Flask principal (API REST)
│   ├── parser.py               # Parser de archivos de WhatsApp
│   ├── stats.py                # Cálculo de estadísticas
│   ├── text_utils.py           # Procesamiento de texto y nube de palabras
│   ├── requirements.txt        # Dependencias Python
│   ├── conftest.py             # Configuración y fixtures de pytest
│   └── tests/
│       ├── test_parser.py      # Pruebas unitarias de parser.py
│       ├── test_stats.py       # Pruebas unitarias de stats.py
│       ├── test_text_utils.py  # Pruebas unitarias de text_utils.py
│       └── test_integration.py # Pruebas de integración end-to-end
│
└── frontend/
    ├── index.html              # Página principal
    ├── app.js                  # Lógica de cliente
    └── style.css               # Estilos
```

---

## Componentes del Backend

### 1. `app.py` — Aplicación Flask Principal

Define la API REST con dos endpoints (`/health` y `/analyze`), habilita CORS,
recibe y valida los uploads ZIP, orquesta el parsing y el análisis, y retorna
los datos como JSON.

**Flujo de `/analyze`:**

1. Valida que se haya enviado un archivo y que sea un `.zip`.
2. Abre el ZIP en memoria y extrae el primer `.txt`.
3. Valida que el contenido sea un export real de WhatsApp.
4. Parsea los mensajes y calcula todas las estadísticas.
5. Genera la nube de palabras y retorna el JSON completo.

### 2. `parser.py` — Parser de WhatsApp

Transforma el texto crudo del export en estructuras de datos manejables.

| Función | Descripción |
|---------|-------------|
| `load_file(filepath)` | Carga un `.txt` desde disco (UTF-8 con fallback a latin-1). Valida extensión y existencia. |
| `parse_lines(raw_text)` | Divide el texto en una lista de mensajes `{timestamp, sender, message}`. Une mensajes multilínea y filtra líneas del sistema. |
| `get_participants(messages)` | Lista de participantes únicos, en orden de primera aparición. |
| `count_emojis(messages)` | Cuenta los emojis de todo el chat, ordenados por frecuencia. |
| `parse_timestamp(timestamp_str)` | Convierte un timestamp de WhatsApp a `datetime` (formato day-first). |
| `validate_format(raw_text)` | Verifica que el texto sea un export de WhatsApp (≥ 5 líneas con el patrón de timestamp). |

**Patrón de timestamp:**

```regex
^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s(.+?):\s(.*)$
```

Soporta formatos con y sin cero inicial: `8/11/2018, 19:51` y `08/11/2018, 19:51`.

### 3. `stats.py` — Cálculo de Estadísticas

| Función | Entrada | Salida | Descripción |
|---------|---------|--------|-------------|
| `count_messages_per_user()` | `list[dict]` | `dict[str, int]` | Mensajes por participante (orden descendente). |
| `count_emojis_per_user()` | `list[dict]` | `dict[str, dict[str, int]]` | Emojis usados por cada usuario. |
| `most_frequent_emoji()` | `list[dict]` | `tuple[str, int] \| None` | Emoji más usado globalmente. |
| `messages_by_hour()` | `list[dict]` | `dict[int, int]` | Mensajes por hora (0–23, las 24 claves). |
| `messages_by_weekday()` | `list[dict]` | `dict[int, int]` | Mensajes por día de semana (0=lunes … 6=domingo). |
| `messages_by_date()` | `list[dict]` | `dict[str, int]` | Mensajes por fecha (ISO `YYYY-MM-DD`, cronológico). |
| `top_days()` | `list[dict], n=5` | `list[list]` | N días más activos, descendente. |
| `peak_hour()` | `list[dict]` | `tuple[int, int]` | Hora con más mensajes. |

### 4. `text_utils.py` — Procesamiento de Texto

| Función | Descripción |
|---------|-------------|
| `clean_text(messages, lang="spanish")` | Limpia el texto de todos los mensajes: elimina URLs, tokens de WhatsApp (`<archivo omitido>`, `<media omitted>`), puntuación y *stopwords*; normaliza a minúsculas. |
| `generate_wordcloud_base64(messages)` | Genera una imagen PNG (800×400) de nube de palabras a partir del texto limpio y la retorna codificada en base64. Usa WordCloud + Matplotlib (backend `Agg`). |

---

## Componentes del Frontend

### 1. `index.html` — Interfaz Principal

Estructura HTML5 con:

- **Header:** título y descripción.
- **Formulario de subida:** input `.zip` y botón *Analizar*.
- **Feedback de carga:** contenedor `#upload-feedback` con un *spinner* y el texto de estado.
- **Contenedor de resultados** (oculto hasta recibir datos): resumen, 4 gráficos
  con `<canvas>` de Chart.js y la imagen de la nube de palabras.

### 2. `app.js` — Lógica de Cliente

Script JavaScript vanilla que orquesta la interacción con el backend.

| Función | Descripción |
|---------|-------------|
| `handleUpload(e)` | Maneja el evento `submit`: previene la recarga, valida el archivo, lo envía al backend y muestra resultados o errores. |
| `validateFile(file)` | Validación *client-side* antes de enviar: archivo presente, extensión `.zip` y tamaño máximo (25 MB). Evita un *round-trip* innecesario. |
| `sendToBackend(file)` | Arma el `FormData` y hace `POST /analyze`. Devuelve el JSON o lanza `Error` con un mensaje claro (conexión o validación del servidor). |
| `setLoading(isLoading)` | Centraliza el feedback de carga: muestra/oculta el *spinner*, deshabilita el botón y marca `aria-busy` en el formulario. |
| `renderAll(data)` | Actualiza el resumen, la nube de palabras y renderiza los 4 gráficos de Chart.js. |
| `chart(sectionId, type, labels, values, label)` | Crea/actualiza un gráfico de Chart.js, destruyendo la instancia previa si existe. |

**Constantes:**

```javascript
const BACKEND = `${window.location.protocol}//${window.location.hostname}:5000`;
const WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25 MB
```

### 3. `style.css` — Estilos

Diseño responsive con colores coherentes con WhatsApp, disposición en
flexbox/grid, animación del *spinner* de carga (`@keyframes spin`) y estado
visual del botón deshabilitado.

---

## Flujo de Datos

```
Usuario
  │
  ├─► Selecciona archivo .zip y hace clic en "Analizar"
  │
  ├─► app.js: handleUpload()
  │      ├─► validateFile()      (validación client-side)
  │      ├─► setLoading(true)    (spinner + botón deshabilitado)
  │      └─► sendToBackend()  ──►  POST /analyze (FormData)
  │                         │
  │                         ▼
  │              app.py: recibe POST
  │                    ├─► zipfile.ZipFile() → extrae el .txt
  │                    ├─► validate_format()
  │                    ├─► parser.parse_lines()
  │                    ├─► stats.*()  (todas las estadísticas)
  │                    ├─► text_utils.generate_wordcloud_base64()
  │                    └─► JSON response
  │
  ├─► app.js: renderAll()  (resumen + gráficos + nube de palabras)
  │      └─► setLoading(false)
  │
  └─► Usuario ve las estadísticas
```

---

## API REST

### Configuración base

- **Host:** `0.0.0.0` · **Puerto:** `5000` · **CORS:** habilitado.

### `GET /health`

Verifica que el servidor esté activo.

**Respuesta `200 OK`:**

```json
{ "status": "ok" }
```

### `POST /analyze`

Recibe un archivo ZIP exportado desde WhatsApp.

```http
POST /analyze HTTP/1.1
Content-Type: multipart/form-data

file: <archivo.zip>
```

**Validaciones:** el archivo debe estar presente, tener extensión `.zip`,
contener al menos un `.txt`, no estar corrupto y coincidir con el formato de WhatsApp.

**Respuesta `200 OK`:**

```json
{
  "total_messages": 2547,
  "participants": ["Juan", "María", "Pedro", "Ana"],
  "messages_per_user": { "Juan": 812, "María": 745 },
  "messages_by_hour": { "0": 15, "23": 42 },
  "messages_by_weekday": { "0": 385, "6": 298 },
  "top_days": [["2024-06-15", 145], ["2024-06-10", 138]],
  "emojis_per_user": { "Juan": { "😂": 45, "👍": 28 } },
  "most_frequent_emoji": ["😂", 289],
  "wordcloud_base64": "iVBORw0KGgoAAAANSUhEUgAAAAUA..."
}
```

**Respuestas de error:**

| Código | Condición | Mensaje |
|--------|-----------|---------|
| 400 | No se envió archivo | "No se recibió ningún archivo." |
| 400 | No es ZIP | "El archivo debe ser un .zip." |
| 400 | ZIP corrupto | "El archivo .zip está corrupto." |
| 400 | ZIP sin `.txt` | "No se encontró un .txt dentro del .zip." |
| 422 | Formato inválido | "El archivo no parece un export de WhatsApp." |

---

## Testing

El backend cuenta con una suite de **37 pruebas** ejecutadas con **pytest**,
divididas en pruebas unitarias (funciones aisladas) y de integración
(*end-to-end* a través del endpoint HTTP).

### Estructura

| Archivo | Tipo | Cobertura |
|---------|------|-----------|
| `backend/conftest.py` | Configuración | Ajusta el `sys.path` para los imports planos del backend y define fixtures compartidas (`sample_chat`, `sample_messages`) con un chat sintético de ejemplo. |
| `backend/tests/test_parser.py` | Unitario | `parse_lines` (campos, multilínea, líneas de sistema, vacío), `get_participants`, `parse_timestamp`, `count_emojis`, `validate_format`, `load_file`. |
| `backend/tests/test_stats.py` | Unitario | `count_messages_per_user`, `messages_by_hour`, `peak_hour`, `messages_by_weekday`, `messages_by_date`, `top_days`, `most_frequent_emoji`, `count_emojis_per_user`. |
| `backend/tests/test_text_utils.py` | Unitario | `clean_text` (URLs, *stopwords*, puntuación, tokens de WhatsApp) y `generate_wordcloud_base64` (devuelve un PNG válido en base64). |
| `backend/tests/test_integration.py` | Integración | `GET /health` y `POST /analyze` (flujo completo con `.zip` armado en memoria + caminos de error: sin archivo, no-zip, zip sin txt, formato inválido, zip corrupto). |

### Datos de prueba

Las pruebas **no usan datos reales**: emplean un chat sintético definido en
`conftest.py` (participantes ficticios, fechas de 2018 y un par de emojis), lo
que garantiza resultados deterministas y reproducibles.

### Ejecución

```bash
cd backend
pip install -r requirements.txt
python -m pytest -v
```

Resultado esperado: **37 passed**.

---

## Instalación y Configuración

### Opción 1 — Docker Compose (recomendada)

```bash
docker-compose up --build
```

- Frontend: <http://localhost>
- Backend: <http://localhost:5000>

### Opción 2 — Instalación manual

**Backend:**

```bash
cd backend
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

**Frontend:**

```bash
cd frontend
python -m http.server 8000   # http://localhost:8000
```

---

## Uso de la Aplicación

1. **Exportar el chat desde WhatsApp:** abrir el chat → *Más opciones* →
   *Exportar chat* → *Sin multimedia*. Se descarga un archivo `.zip`.
2. **Subirlo:** seleccionar el `.zip` en la aplicación y hacer clic en *Analizar*.
3. **Ver resultados:** se muestran el resumen, los 4 gráficos y la nube de palabras.

---

## Integrantes del Equipo

| Nombre | GitHub |
|--------|--------|
| Juan Cruz Trinidad | [@JuanCruzTrinidad](https://github.com/JuanCruzTrinidad) |
| Agustín Federico Corno | [@AgustinCorno](https://github.com/AgustinCorno) |
| Ignacio Daniel Maria | [@ignaciomaria](https://github.com/ignaciomaria) |
| Iván Bravo | [@ivann-bravo](https://github.com/ivann-bravo) |
| Leandro Ivan Vera | [@Lean-IV](https://github.com/Lean-IV) |

---

**Última actualización:** Junio 2026 · **Versión:** 1.0
