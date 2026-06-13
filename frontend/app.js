const BACKEND = `${window.location.protocol}//${window.location.hostname}:5000`;
const WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25 MB

const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const submitButton = form.querySelector("button[type='submit']");
const status = document.getElementById("upload-status");
const results = document.getElementById("results");

form.addEventListener("submit", handleUpload);

// Maneja el evento de carga: valida el archivo, lo envía al backend y muestra resultados.
async function handleUpload(e) {
  e.preventDefault();

  const file = fileInput.files[0];
  const validationError = validateFile(file);
  if (validationError) {
    status.textContent = validationError;
    return;
  }

  status.textContent = "Analizando…";
  results.hidden = true;
  submitButton.disabled = true;

  try {
    const data = await sendToBackend(file);
    status.textContent = "";
    renderAll(data);
    results.hidden = false;
  } catch (err) {
    status.textContent = err.message;
  } finally {
    submitButton.disabled = false;
  }
}

// Validación client-side antes de enviar (evita un round-trip innecesario).
function validateFile(file) {
  if (!file) return "Seleccioná un archivo .zip antes de analizar.";
  if (!file.name.toLowerCase().endsWith(".zip")) return "El archivo debe ser un .zip.";
  if (file.size > MAX_FILE_SIZE) return "El archivo supera el tamaño máximo de 25 MB.";
  return null;
}

// Envía el archivo por POST a /analyze y devuelve el JSON, lanzando Error si algo falla.
async function sendToBackend(file) {
  const body = new FormData();
  body.append("file", file);

  let res;
  try {
    res = await fetch(`${BACKEND}/analyze`, { method: "POST", body });
  } catch {
    throw new Error("No se pudo conectar con el servidor.");
  }

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Error al analizar.");
  return data;
}

function renderAll(data) {
  // Resumen
  document.getElementById("summary-total").textContent = data.total_messages;
  document.getElementById("summary-participants").textContent = data.participants.join(", ");
  document.getElementById("summary-emoji").textContent = data.most_frequent_emoji
    ? `${data.most_frequent_emoji[0]} (${data.most_frequent_emoji[1]} veces)`
    : "—";

  // Word cloud
  document.getElementById("wordcloud-img").src = `data:image/png;base64,${data.wordcloud_base64}`;

  // Gráficos
  chart("chart-user", "bar",
    Object.keys(data.messages_per_user),
    Object.values(data.messages_per_user),
    "Mensajes"
  );

  chart("chart-hour", "bar",
    Object.keys(data.messages_by_hour).map(h => `${h}h`),
    Object.values(data.messages_by_hour),
    "Mensajes"
  );

  chart("chart-weekday", "bar",
    Object.keys(data.messages_by_weekday).map(d => WEEKDAYS[d]),
    Object.values(data.messages_by_weekday),
    "Mensajes"
  );

  chart("chart-top-days", "bar",
    data.top_days.map(([date]) => date),
    data.top_days.map(([, count]) => count),
    "Mensajes"
  );
}

function chart(sectionId, type, labels, values, label) {
  const canvas = document.querySelector(`#${sectionId} canvas`);
  // Destruir instancia previa si existe
  if (canvas._chart) canvas._chart.destroy();
  canvas._chart = new Chart(canvas, {
    type,
    data: {
      labels,
      datasets: [{ label, data: values, backgroundColor: "#25d36699", borderColor: "#25d366", borderWidth: 1 }],
    },
    options: { responsive: true, plugins: { legend: { display: false } } },
  });
}
