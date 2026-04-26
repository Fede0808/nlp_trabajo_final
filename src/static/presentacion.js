const slides = Array.from(document.querySelectorAll(".slide"));
const apiStatus = document.getElementById("api-status");

const predictionForm = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");
const sampleButton = document.getElementById("sample-button");
const descriptionInput = document.getElementById("descripcion");
const demoMessage = document.getElementById("demo-message");
const resultClass = document.getElementById("result-class");
const resultClean = document.getElementById("result-clean");
const resultModel = document.getElementById("result-model");
const resultPath = document.getElementById("result-path");

const benchmarkDate = document.getElementById("benchmark-date");
const bestBaseModel = document.getElementById("best-base-model");
const bestCensoredModel = document.getElementById("best-censored-model");
const baseResultsBody = document.getElementById("base-results-body");
const censoredResultsBody = document.getElementById("censored-results-body");
const baseSummary = document.getElementById("base-summary");
const apiModelName = document.getElementById("api-model-name");
const apiModelPath = document.getElementById("api-model-path");
const guardrailStatus = document.getElementById("guardrail-status");
const guardrailHallazgo = document.getElementById("guardrail-hallazgo");
const guardrailLectura = document.getElementById("guardrail-lectura");
const implementationModel = document.getElementById("implementation-model");
const implementationCriterion = document.getElementById("implementation-criterion");

const ejemploDescripcion =
  "PH interno de 4 ambientes con patio, orientacion sur, entrada independiente y bajas expensas.";

let currentSlide = 0;

function renderSlide(index) {
  currentSlide = Math.max(0, Math.min(index, slides.length - 1));

  slides.forEach((slide, position) => {
    slide.classList.toggle("is-active", position === currentSlide);
  });

  document.title = `TIF NLP | ${slides[currentSlide].dataset.title}`;
}

function setMessage(message, state = "") {
  demoMessage.textContent = message;
  demoMessage.classList.remove("is-loading", "is-error", "is-success");
  if (state) {
    demoMessage.classList.add(state);
  }
}

function setResults({ clase = "-", limpio = "-", modelo = "-", ruta = "-" } = {}) {
  resultClass.textContent = clase;
  resultClean.textContent = limpio;
  resultModel.textContent = modelo;
  resultPath.textContent = ruta;
}

function apiBaseUrl() {
  if (window.location.protocol === "file:") {
    return null;
  }
  return window.location.origin;
}

function formatMetric(value) {
  return Number(value).toFixed(4);
}

function renderResultsTable(target, rows) {
  target.innerHTML = "";

  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${row.modelo}</strong></td>
      <td>${row.familia}</td>
      <td>${formatMetric(row.accuracy)}</td>
      <td>${formatMetric(row.f1_macro)}</td>
    `;
    target.appendChild(tr);
  });
}

function sortByScore(left, right) {
  if (right.f1_macro !== left.f1_macro) {
    return right.f1_macro - left.f1_macro;
  }
  return right.accuracy - left.accuracy;
}

function pickBestByF1(rows) {
  return [...rows].sort(sortByScore)[0];
}

function hydrateBenchmark(payload) {
  const rows = payload.resultados || [];
  const baseRows = rows.filter((row) => row.condicion === "base").sort(sortByScore);
  const censoredRows = rows.filter((row) => row.condicion === "censurado").sort(sortByScore);
  const bestBase = pickBestByF1(baseRows);
  const activeModel = payload.modelo_api_final;
  const guardrail = payload.guardrail_censura;

  benchmarkDate.textContent = "2026-04-27";
  bestBaseModel.textContent = `${bestBase.modelo} · F1 ${formatMetric(bestBase.f1_macro)}`;
  bestCensoredModel.textContent = `${activeModel.modelo} · F1 ${formatMetric(activeModel.f1_macro)}`;
  apiModelName.textContent = `${activeModel.modelo} (${activeModel.condicion})`;
  apiModelPath.textContent = activeModel.ruta_artefacto.split(/[\\/]/).pop();
  implementationModel.textContent = `${activeModel.modelo} · ${activeModel.familia}`;
  implementationCriterion.textContent = activeModel.criterio_seleccion;

  renderResultsTable(baseResultsBody, baseRows);
  renderResultsTable(censoredResultsBody, censoredRows);

  const bestBaseAccuracy = [...baseRows].sort((left, right) => right.accuracy - left.accuracy)[0];
  baseSummary.textContent =
    `Los modelos base quedan por encima de sus versiones censuradas en todos los casos. ` +
    `${bestBase.modelo} lidera F1 macro (${formatMetric(bestBase.f1_macro)}) y ` +
    `${bestBaseAccuracy.modelo} lidera accuracy (${formatMetric(bestBaseAccuracy.accuracy)}).`;

  guardrailStatus.textContent = guardrail.se_sostiene
    ? "El guardrail de censura mejoro el rendimiento y se sostiene en esta corrida."
    : "El guardrail de censura no mejoro las metricas en esta corrida y queda marcado como hallazgo a revisar.";
  guardrailHallazgo.textContent = guardrail.hallazgo;
  guardrailLectura.textContent = guardrail.lectura;
}

async function checkHealth() {
  const base = apiBaseUrl();

  if (!base) {
    apiStatus.textContent = "Abrir por HTTP";
    apiStatus.classList.remove("status-pending", "status-ok");
    apiStatus.classList.add("status-error");
    setMessage(
      "Esta presentacion fue abierta con file://. Para usar la API, abrir http://127.0.0.1:8000/presentacion.",
      "is-error",
    );
    return;
  }

  try {
    const response = await fetch(`${base}/salud`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    apiStatus.textContent = "Operativa";
    apiStatus.classList.remove("status-pending", "status-error");
    apiStatus.classList.add("status-ok");
  } catch (error) {
    apiStatus.textContent = "No disponible";
    apiStatus.classList.remove("status-pending", "status-ok");
    apiStatus.classList.add("status-error");
  }
}

async function loadBenchmark() {
  const base = apiBaseUrl();

  if (!base) {
    return;
  }

  try {
    const response = await fetch(`${base}/benchmark`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const payload = await response.json();
    hydrateBenchmark(payload);
  } catch (error) {
    baseResultsBody.innerHTML = `<tr><td colspan="4">No fue posible cargar el benchmark.</td></tr>`;
    censoredResultsBody.innerHTML = `<tr><td colspan="4">No fue posible cargar el benchmark.</td></tr>`;
    baseSummary.textContent = "La comparativa final no pudo cargarse desde la API.";
    guardrailStatus.textContent = "No fue posible recuperar la conclusion metodologica.";
    guardrailHallazgo.textContent = "-";
    guardrailLectura.textContent = "-";
  }
}

async function handlePrediction(event) {
  event.preventDefault();
  const descripcion = descriptionInput.value.trim();
  const base = apiBaseUrl();

  if (!base) {
    setMessage(
      "No se puede consultar la API desde file://. Abrir la presentacion desde http://127.0.0.1:8000/presentacion.",
      "is-error",
    );
    setResults();
    return;
  }

  if (!descripcion) {
    setMessage("Ingresar una descripcion antes de consultar la API.", "is-error");
    setResults();
    return;
  }

  predictButton.disabled = true;
  setMessage("Consultando el modelo censurado activo...", "is-loading");

  try {
    const response = await fetch(`${base}/predecir`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ descripcion }),
    });

    const payload = await response.json();

    if (!response.ok) {
      const detail =
        typeof payload.detail === "string" ? payload.detail : "Error al consultar la API.";
      throw new Error(detail);
    }

    setResults({
      clase: payload.clase_predicha,
      limpio: payload.texto_limpio,
      modelo: `${payload.modelo_activo} (${payload.condicion_modelo})`,
      ruta: payload.ruta_modelo,
    });
    setMessage("Prediccion completada correctamente.", "is-success");
  } catch (error) {
    setResults();
    setMessage(error.message || "No fue posible obtener una prediccion.", "is-error");
  } finally {
    predictButton.disabled = false;
  }
}

function hydrateFromQueryString() {
  const params = new URLSearchParams(window.location.search);
  const descripcion = params.get("descripcion");

  if (descripcion) {
    descriptionInput.value = descripcion;
    setMessage("Descripcion cargada desde la URL. Se puede ejecutar la prediccion.");
  }
}

document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === "PageDown") {
    event.preventDefault();
    renderSlide(currentSlide + 1);
  }
  if (event.key === "ArrowLeft" || event.key === "PageUp") {
    event.preventDefault();
    renderSlide(currentSlide - 1);
  }
});

sampleButton.addEventListener("click", () => {
  descriptionInput.value = ejemploDescripcion;
  descriptionInput.focus();
  setMessage("Ejemplo cargado. Ahora se puede ejecutar la prediccion.");
});

predictionForm.addEventListener("submit", handlePrediction);

renderSlide(0);
hydrateFromQueryString();
checkHealth();
loadBenchmark();
