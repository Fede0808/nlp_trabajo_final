# Repository Analysis: nlp_trabajo_final

## Overview

This repository is a CPU-first academic NLP project focused on classifying real-estate listings in Argentina into `Casa`, `Departamento`, and `PH` from free-text descriptions. Its central goal is not just to train a model, but to compare a classical baseline (`TF-IDF + LinearSVC`) against a distilled Transformer under strict local-hardware constraints, then package the result in a way that is defensible for a final course assignment.

The repo is shaped around reproducibility and academic storytelling. The codebase balances reusable Python modules in `src/`, phase-oriented notebooks in `notebooks/`, local-only datasets in `data/`, and assignment-facing documentation in `doc/`.

## Architecture

The repository follows a hybrid structure:

- `src/` contains the reusable source-of-truth modules.
- `notebooks/` contains the narrative, phase-by-phase academic workflow.
- `doc/` contains the assignment context, planning artifacts, and delivery guidance.
- `artifacts/` stores serialized model outputs, currently including the SVM artifact.
- `data/` is intentionally unversioned and expected to exist only in the local environment.

The architecture is organized around the assignment phases:

- **Hardware and execution policy** in `src/infraestructura_cpu.py`
- **Corpus loading, filtering, and stratified sampling** in `src/corpus_inmuebles.py`
- **Shared text cleaning and feature preparation** in `src/property_text_pipeline.py`
- **Evaluation and reporting helpers** in `src/evaluacion_modelos.py`
- **Artifact persistence and inference reuse** in `src/artefactos_modelos.py`
- **Local serving layer** in `src/api_local.py`
- **Transformer offline/CPU workflow** in `src/transformer_cpu.py`
- **Shared frozen project settings** in `src/configuracion_proyecto.py`

## Key Components

- **`src/infraestructura_cpu.py`**: reads hardware constraints, sets conservative Torch thread counts, and suggests sample sizes according to available RAM.
- **`src/corpus_inmuebles.py`**: loads the core dataset, filters to the three target classes, applies stratified sampling, and performs the train/test split.
- **`src/property_text_pipeline.py`**: defines the canonical `texto_limpio` column, removes HTML and `_x000d_` noise, preserves domain-critical terms, and builds the SVM pipeline.
- **`src/evaluacion_modelos.py`**: computes comparable metrics, cross-validation summaries, confusion matrices, and per-class error analysis.
- **`src/transformer_cpu.py`**: handles tokenizer/model availability, offline cache inspection, dataloader construction, minimal CPU-only training, inference, and dynamic quantization.
- **`src/artefactos_modelos.py`**: saves and loads the SVM artifact and reuses the same cleaning path for inference.
- **`src/api_local.py`**: exposes the baseline model through FastAPI with a health endpoint and a prediction endpoint.
- **`notebooks/00_cpu_shared_cleaning.py`**: acts as a reproducible smoke test that exercises hardware setup, sampling, cleaning, SVM training, evaluation, and Transformer-readiness checks in one run.

## Technologies Used

- **Language**: Python 3.11+
- **ML / NLP**: `scikit-learn`, `torch`, `transformers`
- **Data handling**: `pandas`
- **Serving**: `fastapi`, `uvicorn`
- **Notebook workflow**: `ipykernel`, Jupyter notebooks
- **Visualization dependencies**: `matplotlib`, `seaborn`
- **Environment management**: `uv`, local `.venv`

## Data Flow

The main data path is straightforward and intentionally traceable:

1. Raw CSV rows are loaded from `data/entrenamiento.csv`.
2. Listings are filtered to `Casa`, `Departamento`, and `PH`.
3. A stratified sample is taken, then split into train and test sets with a fixed seed.
4. Text is normalized into the canonical `texto_limpio` column.
5. The same cleaned text powers both model families:
   - the SVM consumes it through `TfidfVectorizer`
   - the Transformer consumes it through tokenization without additional cleaning logic
6. Evaluation helpers convert predictions into global metrics, confusion matrices, and class-specific diagnostics.
7. The trained SVM pipeline is serialized into `artifacts/modelo_svm.joblib` and reused by the API.

## Team and Ownership

All visible commits in the repository are authored by **Federico Blasco**, and the current design suggests a single-maintainer workflow. That shows up in the repo shape: the documentation, modules, and notebooks move in lockstep rather than through separate feature branches or merge-heavy collaboration.

The current ownership pattern is:

- **Documentation and assignment framing**: `doc/`, `README.md`, `instructions.md`
- **Reusable pipeline modules**: `src/`
- **Academic execution narrative**: `notebooks/`
- **Operational output**: `artifacts/`

## Current State

The repository has reached a strong “deliverable baseline” state:

- The SVM baseline is operational and serialized.
- The API layer is functional around the baseline.
- The shared preprocessing path is in place.
- The Transformer workflow exists and now includes explicit contingency handling for offline weight availability.

At the time of analysis, the working tree also contains uncommitted changes focused on delivery hardening: centralized project configuration, richer evaluation summaries, and stronger documentation around the Transformer contingency. That means the repository is currently in the middle of shifting from “working prototype” to “defensible final submission.”
