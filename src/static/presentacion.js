const slides = Array.from(document.querySelectorAll(".slide"));
const bodyDataset = document.body.dataset;

const apiStatus = document.getElementById("api-status");
const benchmarkDate = document.getElementById("benchmark-date");
const heroBenchmarkDate = document.getElementById("hero-benchmark-date");
const currentSlideLabel = document.getElementById("current-slide");
const totalSlidesLabel = document.getElementById("total-slides");
const progressFill = document.getElementById("progress-fill");
const currentSlideTitle = document.getElementById("current-slide-title");
const consistencyWarning = document.getElementById("consistency-warning");
const resultsConsistency = document.getElementById("results-consistency");

const guardrailHallazgo = document.getElementById("guardrail-hallazgo");
const guardrailLectura = document.getElementById("guardrail-lectura");
const negocioModelo = document.getElementById("negocio-modelo");
const negocioGuardrail = document.getElementById("negocio-guardrail");
const limitacionesModelo = document.getElementById("limitaciones-modelo");
const limitacionesCriterio = document.getElementById("limitaciones-criterio");
const liveModelName = document.getElementById("live-model-name");
const liveModelFamily = document.getElementById("live-model-family");
const liveModelPath = document.getElementById("live-model-path");

const predictionForm = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");
const sampleButton = document.getElementById("sample-button");
const descriptionInput = document.getElementById("descripcion");
const demoMessage = document.getElementById("demo-message");
const resultClass = document.getElementById("result-class");
const resultClean = document.getElementById("result-clean");
const resultModel = document.getElementById("result-model");
const resultPath = document.getElementById("result-path");

const ejemploDescripcion =
  "PH interno de 4 ambientes con patio, entrada independiente y bajas expensas.";

let currentSlide = 0;
let healthState = "loading";
let benchmarkState = "loading";

function renderSlide(index) {
  currentSlide = Math.max(0, Math.min(index, slides.length - 1));
  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle("is-active", slideIndex === currentSlide);
  });

  const activeSlide = slides[currentSlide];
  currentSlideLabel.textContent = String(currentSlide + 1);
  totalSlidesLabel.textContent = String(slides.length);
  currentSlideTitle.textContent = activeSlide.dataset.title;
  progressFill.style.width = `${((currentSlide + 1) / slides.length) * 100}%`;
  document.title = `TIF NLP | ${activeSlide.dataset.title}`;
}

function apiBaseUrl() {
  if (window.location.protocol === "file:") {
    return null;
  }
  return window.location.origin;
}

function assetsBaseUrl() {
  if (window.location.protocol === "file:") {
    return "./assets/presentacion";
  }
  return `${window.location.origin}/static/assets/presentacion`;
}

function setApiStatus(label, statusClass) {
  apiStatus.textContent = label;
  apiStatus.classList.remove("status-loading", "status-ok", "status-degraded", "status-error");
  apiStatus.classList.add(statusClass);
}

function syncOverallStatus() {
  if (window.location.protocol === "file:") {
    setApiStatus("Abrir por HTTP", "status-degraded");
    return;
  }

  if (healthState === "ok" && (benchmarkState === "ok" || benchmarkState === "warning")) {
    setApiStatus("Operativa", "status-ok");
    return;
  }

  if (healthState === "ok" && benchmarkState === "degraded") {
    setApiStatus("Benchmark degradado", "status-degraded");
    return;
  }

  if (healthState === "degraded" || healthState === "error") {
    setApiStatus("No disponible", "status-error");
    return;
  }

  setApiStatus("Verificando", "status-loading");
}

function setMessage(message, state = "") {
  demoMessage.textContent = message;
  demoMessage.classList.remove("is-loading", "is-success", "is-error");
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

function hydrateAssetImages() {
  const base = assetsBaseUrl();
  document.querySelectorAll("img[data-asset-src]").forEach((image) => {
    image.src = `${base}/${image.dataset.assetSrc}`;
  });
}

async function hydrateTableFragment() {
  const base = assetsBaseUrl();

  const fragmentTargets = Array.from(document.querySelectorAll("[data-asset-fragment]"));
  for (const fragmentTarget of fragmentTargets) {
    try {
      const response = await fetch(`${base}/${fragmentTarget.dataset.assetFragment}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const html = await response.text();
      if (html.trim()) {
        fragmentTarget.innerHTML = html;
      }
    } catch (error) {
      console.warn("No fue posible cargar un fragmento estático.", {
        fragment: fragmentTarget.dataset.assetFragment,
        error,
      });
    }
  }
}

function showConsistencyWarning(message, status = "warning") {
  consistencyWarning.textContent = message;
  consistencyWarning.classList.remove("is-hidden");
  if (resultsConsistency) {
    resultsConsistency.textContent = message;
    resultsConsistency.classList.toggle("status-chip", true);
  }
  benchmarkState = status;
  syncOverallStatus();
}

function hideConsistencyWarning() {
  consistencyWarning.classList.add("is-hidden");
  if (resultsConsistency) {
    resultsConsistency.textContent = "Benchmark alineado con evidencia estática";
  }
  benchmarkState = "ok";
  syncOverallStatus();
}

function evaluateConsistency(payload) {
  const expectedDate = bodyDataset.staticBenchmarkDate;
  const expectedModel = bodyDataset.staticApiModel;
  const expectedCondition = bodyDataset.staticApiCondition;
  const liveModel = payload?.modelo_api_final?.modelo;
  const liveCondition = payload?.modelo_api_final?.condicion;
  const liveDate = payload?.fecha_benchmark_cpu;

  const problems = [];
  if (liveDate && expectedDate && liveDate !== expectedDate) {
    problems.push(`fecha ${liveDate}`);
  }
  if (liveModel && expectedModel && liveModel !== expectedModel) {
    problems.push(`modelo ${liveModel}`);
  }
  if (liveCondition && expectedCondition && liveCondition !== expectedCondition) {
    problems.push(`condición ${liveCondition}`);
  }

  if (problems.length > 0) {
    console.warn("Benchmark vivo no alineado con evidencia estática.", {
      expectedDate,
      expectedModel,
      expectedCondition,
      payload,
    });
    showConsistencyWarning("Benchmark vivo no alineado con evidencia estática");
    return;
  }

  hideConsistencyWarning();
}

function hydrateBenchmark(payload) {
  const liveDate = payload.fecha_benchmark_cpu || bodyDataset.staticBenchmarkDate;
  benchmarkDate.textContent = liveDate;
  heroBenchmarkDate.textContent = liveDate;

  const guardrail = payload.guardrail_censura || {};
  const activeModel = payload.modelo_api_final || {};

  if (guardrail.hallazgo) {
    guardrailHallazgo.textContent = guardrail.hallazgo;
  }
  if (guardrail.lectura) {
    guardrailLectura.textContent = guardrail.lectura;
    if (negocioGuardrail) {
      negocioGuardrail.textContent = guardrail.lectura;
    }
  }

  const modelLabel = activeModel.modelo
    ? `${activeModel.modelo} · ${activeModel.condicion || "sin condición"}`
    : "Pendiente de validación";

  negocioModelo.textContent = modelLabel;
  limitacionesModelo.textContent = modelLabel;
  limitacionesCriterio.textContent =
    activeModel.criterio_seleccion || limitacionesCriterio.textContent;
  if (liveModelName) {
    liveModelName.textContent = activeModel.modelo || "Pendiente";
  }
  if (liveModelFamily) {
    liveModelFamily.textContent = activeModel.familia
      ? `${activeModel.condicion || "-"} · ${activeModel.familia}`
      : "Pendiente de validación";
  }
  if (liveModelPath) {
    liveModelPath.textContent = activeModel.ruta_artefacto || "Pendiente de validación";
  }

  evaluateConsistency(payload);
}

async function checkHealth() {
  const base = apiBaseUrl();

  if (!base) {
    healthState = "degraded";
    syncOverallStatus();
    setMessage(
      "La presentación fue abierta con file://. Para estados vivos y demo, abrir http://127.0.0.1:8000/presentacion.",
      "is-error",
    );
    return;
  }

  try {
    const response = await fetch(`${base}/salud`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    healthState = "ok";
  } catch (error) {
    healthState = "error";
  }

  syncOverallStatus();
}

async function loadBenchmark() {
  const base = apiBaseUrl();

  if (!base) {
    benchmarkState = "degraded";
    if (resultsConsistency) {
      resultsConsistency.textContent = "Abrir por HTTP para validar benchmark vivo";
    }
    syncOverallStatus();
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
    console.warn("No fue posible recuperar el benchmark vivo.", error);
    benchmarkState = "degraded";
    if (resultsConsistency) {
      resultsConsistency.textContent = "No fue posible validar el benchmark vivo";
    }
    syncOverallStatus();
  }
}

async function handlePrediction(event) {
  event.preventDefault();

  const descripcion = descriptionInput.value.trim();
  const base = apiBaseUrl();

  if (!base) {
    setMessage(
      "No se puede consultar la API desde file://. Abrir la presentación desde http://127.0.0.1:8000/presentacion.",
      "is-error",
    );
    setResults();
    return;
  }

  if (!descripcion) {
    setMessage("Ingresar una descripción antes de consultar la API.", "is-error");
    setResults();
    return;
  }

  predictButton.disabled = true;
  setMessage("Consultando el modelo activo...", "is-loading");

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

    setMessage("Predicción completada correctamente.", "is-success");
  } catch (error) {
    setResults();
    setMessage(error.message || "No fue posible obtener una predicción.", "is-error");
  } finally {
    predictButton.disabled = false;
  }
}

function wireNavigation() {
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
}

function wireDemo() {
  sampleButton.addEventListener("click", () => {
    descriptionInput.value = ejemploDescripcion;
    descriptionInput.focus();
    setMessage("Ejemplo cargado. La demo está lista para consultar la API.");
  });

  predictionForm.addEventListener("submit", handlePrediction);
}

async function init() {
  renderSlide(0);
  hydrateAssetImages();
  wireNavigation();
  wireDemo();
  await hydrateTableFragment();
  await checkHealth();
  await loadBenchmark();
}

init();
