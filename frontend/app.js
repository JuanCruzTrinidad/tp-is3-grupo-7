const BACKEND = `${window.location.protocol}//${window.location.hostname}:5000`;
const WEEKDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];

const form = document.getElementById("upload-form");
const status = document.getElementById("upload-status");
const results = document.getElementById("results");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = document.getElementById("file-input").files[0];
  if (!file) return;

  status.textContent = "Analizando…";
  results.hidden = true;

  const body = new FormData();
  body.append("file", file);

  let data;
  try {
    const res = await fetch(`${BACKEND}/analyze`, { method: "POST", body });
    data = await res.json();
    if (!res.ok) { status.textContent = data.error || "Error al analizar."; return; }
  } catch {
    status.textContent = "No se pudo conectar con el servidor.";
    return;
  }

  status.textContent = "";
  renderAll(data);
  results.hidden = false;
});

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
