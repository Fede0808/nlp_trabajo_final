const slides = Array.from(document.querySelectorAll(".slide"));
const prevButton = document.getElementById("prev-slide");
const nextButton = document.getElementById("next-slide");
const slideCounter = document.getElementById("slide-counter");
const progressBar = document.getElementById("progress-bar");
const apiStatus = document.getElementById("api-status");

const predictionForm = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");
const sampleButton = document.getElementById("sample-button");
const descriptionInput = document.getElementById("descripcion");
const demoMessage = document.getElementById("demo-message");
const resultClass = document.getElementById("result-class");
const resultClean = document.getElementById("result-clean");
const resultPath = document.getElementById("result-path");

const ejemploDescripcion =
  "PH interno de 4 ambientes con patio, orientacion sur, entrada independiente y bajas expensas.";

let currentSlide = 0;

function renderSlide(index) {
  currentSlide = Math.max(0, Math.min(index, slides.length - 1));

  slides.forEach((slide, position) => {
    slide.classList.toggle("is-active", position === currentSlide);
  });

  slideCounter.textContent = `${currentSlide + 1} / ${slides.length}`;
  progressBar.style.width = `${((currentSlide + 1) / slides.length) * 100}%`;
  prevButton.disabled = currentSlide === 0;
  nextButton.disabled = currentSlide === slides.length - 1;
  document.title = `TIF NLP | ${slides[currentSlide].dataset.title}`;
}

function setMessage(message, state = "") {
  demoMessage.textContent = message;
  demoMessage.classList.remove("is-loading", "is-error", "is-success");
  if (state) {
    demoMessage.classList.add(state);
  }
}

function setResults({ clase = "-", limpio = "-", ruta = "-" } = {}) {
  resultClass.textContent = clase;
  resultClean.textContent = limpio;
  resultPath.textContent = ruta;
}

function apiBaseUrl() {
  if (window.location.protocol === "file:") {
    return null;
  }
  return window.location.origin;
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
  setMessage("Consultando el modelo local...", "is-loading");

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

prevButton.addEventListener("click", () => renderSlide(currentSlide - 1));
nextButton.addEventListener("click", () => renderSlide(currentSlide + 1));

document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === "PageDown") {
    renderSlide(currentSlide + 1);
  }
  if (event.key === "ArrowLeft" || event.key === "PageUp") {
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
