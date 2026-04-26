# Spec Tecnico - Presentacion HTML Final NLP Inmobiliario

## 1. Objetivo del artefacto

Definir de forma decision-complete como debe rehacerse la presentacion HTML final del trabajo de NLP inmobiliario para defensa academica.

Este spec cubre:

- la deck completa de 18 slides definida en `doc/template_presentacion_final_nlp_inmobiliario.md`;
- el contrato de integracion entre `src/static/`, assets exportados desde notebooks y API FastAPI ya existente;
- el sistema visual y las reglas de composicion para que la reimplementacion no tenga que decidir estructura, datos ni fallback.

Queda fuera de alcance:

- cambiar endpoints existentes;
- redisenar la arquitectura backend;
- redefinir metricas del benchmark;
- reescribir notebooks o regenerar assets en este paso.

## 2. Principios de diseno

### 2.1 Criterio narrativo

- La deck debe leerse como defensa academica con lectura de caso de negocio.
- La progresion debe ir de problema y metodologia a evidencia, interpretacion y uso operativo.
- La presentacion no debe depender de conectividad de red externa.

### 2.2 Criterio tecnico

- Las slides narrativas deben poder renderizarse sin API.
- La evidencia principal debe quedar fijada por assets exportados o snapshots consolidados.
- La API en vivo debe reservarse para salud, metadatos operativos y demo.
- Si la API falla, la presentacion debe seguir siendo presentable.

### 2.3 Sistema visual adaptado desde `brand-guidelines`

Se usa la skill como sistema visual, no como marca literal.

- Tipografia de headings: `Poppins, Arial, sans-serif`.
- Tipografia de cuerpo: `Lora, Georgia, serif`.
- Tipografia tecnica y labels: `Inter, Arial, sans-serif` si se incorpora; fallback `Arial, sans-serif`.
- Composicion: sobria, academica, alto contraste, densidad media.
- Paleta principal: identidad UNLaM/NLP con verde institucional dominante.
- Accent colors: usar variantes funcionales inspiradas en `brand-guidelines`, no copiar la paleta como identidad principal.

### 2.4 Tokens visuales obligatorios

La implementacion futura debe exponer estos tokens CSS como minimo:

```css
:root {
  --color-brand-primary: #006341;
  --color-brand-primary-strong: #004f33;
  --color-brand-primary-soft: #e7f3ee;
  --color-ink: #141413;
  --color-paper: #faf9f5;
  --color-surface: #ffffff;
  --color-line: #d9e0e4;
  --color-muted: #5f6b74;
  --color-accent-warm: #d97757;
  --color-accent-cool: #6a9bcc;
  --color-accent-olive: #788c5d;
  --color-danger: #c94b40;
}
```

### 2.5 Reglas de layout

- La portada y slides de evidencia no deben parecer landing page ni dashboard comercial.
- Cada slide debe funcionar en viewport de defensa desktop sin scroll vertical idealmente.
- En viewport reducido se permite scroll, pero no superposiciones de texto ni colapso visual.
- No usar cards dentro de cards.
- Los estados API deben verse como estados operativos, no como contenido principal.

## 3. Arquitectura de integracion

### 3.1 Capas

1. `Narrativa`
   - Fuente primaria: `doc/template_presentacion_final_nlp_inmobiliario.md`.
   - Define el contenido base y el orden conceptual de slides.

2. `Frontend de presentacion`
   - Archivos objetivo: `src/static/presentacion.html`, `src/static/presentacion.css`, `src/static/presentacion.js`.
   - Renderiza la deck, placeholders, estados de carga y demo.

3. `Assets estaticos de evidencia`
   - Carpeta canonica a crear en la reimplementacion: `src/static/assets/presentacion/`.
   - Contiene imagenes y fragmentos estaticos consolidados desde notebooks.

4. `API local`
   - Archivo actual: `src/api_local.py`.
   - Endpoints vigentes: `GET /salud`, `GET /benchmark`, `POST /predecir`, `GET /presentacion`.

### 3.2 Modo de carga por tipo de contenido

- Narrativa base: `estatico`
- Graficos y visuales de notebooks: `estatico`
- Tabla principal de resultados: `estatico`
- Salud y metadatos operativos: `api`
- Demo de prediccion: `api`
- Verificacion del modelo activo y guardrail: `api`

### 3.3 Regla de precedencia

- La evidencia visual mostrada al jurado se toma de assets estaticos consolidados.
- La API no reemplaza esa evidencia; solo la complementa con estado operativo y demo.
- Si hay diferencia entre assets estaticos y `GET /benchmark`, debe mostrarse un warning de inconsistencia operativo, no re-renderizar la slide con valores distintos.

## 4. Contrato de datos

### 4.1 Contrato de assets estaticos

La reimplementacion debe asumir y documentar esta carpeta:

`src/static/assets/presentacion/`

Archivos esperados:

- `workflow_nlp_inmobiliario.svg`
- `distribucion_train_test.png`
- `tabla_resultados_principales.html`
- `matriz_confusion_reglog_censurado.png`
- `explicabilidad_reglog_tokens.png`
- `explicabilidad_bayes_alertas.png`
- `api_flujo_prediccion.svg`

Si algun asset no existe al momento de la implementacion:

- la slide no debe romper;
- debe mostrarse placeholder visual con label `Pendiente de exportacion`;
- el placeholder debe conservar layout y dimensiones finales.

### 4.2 Contrato de `GET /salud`

Payload actual:

```json
{
  "estado": "ok"
}
```

Uso permitido:

- topbar de estado;
- badge operativo de demo;
- degradacion de slides 14 a 16.

### 4.3 Contrato de `GET /benchmark`

Payload actual:

```json
{
  "fecha_benchmark_cpu": "2026-04-26",
  "modelo_api_final": {
    "modelo": "Reg Log",
    "condicion": "censurado",
    "familia": "clasico",
    "accuracy": 0.8515,
    "f1_macro": 0.7483,
    "criterio_seleccion": "Mayor F1 macro; accuracy como desempate entre modelos censurados.",
    "preprocesamiento": "censurado",
    "ruta_artefacto": "..."
  },
  "guardrail_censura": {
    "se_sostiene": false,
    "hallazgo": "...",
    "lectura": "..."
  },
  "resultados": [
    {
      "modelo": "SVM",
      "condicion": "base",
      "familia": "clasico",
      "accuracy": 0.9040,
      "f1_macro": 0.8129
    }
  ]
}
```

Uso obligatorio:

- `fecha_benchmark_cpu`: topbar y metadata operativa.
- `modelo_api_final.*`: slides 14, 15 y 16.
- `guardrail_censura.*`: slides 11 y 14.
- `resultados[]`: validacion cruzada contra la tabla estatica, no fuente principal de render de resultados.

### 4.4 Contrato de `POST /predecir`

Request:

```json
{
  "descripcion": "PH interno de 4 ambientes con patio..."
}
```

Response:

```json
{
  "clase_predicha": "PH",
  "texto_limpio": "...",
  "modelo_activo": "Reg Log",
  "condicion_modelo": "censurado",
  "ruta_modelo": "..."
}
```

Uso obligatorio:

- solo slide 16;
- nunca usar este endpoint para poblar slides analiticas;
- si falla, se degrada solo la demo.

## 5. Mapeo funcional por bloque

### 5.1 Apertura y framing

- Slides 1 a 3
- Carga: estatica
- Objetivo: contextualizar problema, negocio y objetivo analitico

### 5.2 Metodologia y diseno experimental

- Slides 4 a 9
- Carga: estatica
- Objetivo: mostrar flujo, datos, escenarios, modelos, preprocesamiento y metricas

### 5.3 Resultados y lectura tecnica

- Slides 10 a 13
- Carga: estatica con chequeo API no bloqueante
- Objetivo: exhibir evidencia y lectura interpretativa

### 5.4 Lectura operativa y despliegue

- Slides 14 a 16
- Carga: hibrida
- Objetivo: separar recomendacion de negocio, limites y operacion local de la API

### 5.5 Cierre

- Slides 17 y 18
- Carga: estatica
- Objetivo: consolidar aprendizajes y proximo trabajo

## 6. Matriz slide-by-slide exacta

### S01

- `slide_id`: `s01_portada`
- `titulo`: `Clasificacion automatica de avisos inmobiliarios con NLP`
- `objetivo`: abrir la defensa con tema, caso, materia y enfoque
- `mensaje_clave`: el trabajo conecta NLP aplicado, comparacion de modelos y utilidad de negocio
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: hero de texto, subtitulo, metadata compacta, marca UNLaM/curso
- `contenido_fijo`: titulo, caso, materia, enfoque
- `contenido_dinamico`: fecha de benchmark y estado API
- `fuente_de_verdad`: template + `GET /benchmark.fecha_benchmark_cpu` + `GET /salud`
- `modo_de_carga`: `hibrido`
- `fallback`: mostrar fecha estatica del spec y badge `API no disponible`
- `criterio_visual`: slide hero con alto contraste, verde institucional, sin tablas
- `criterio_de_aceptacion`: la slide debe poder abrir sola como portada y dejar clara la tesis del trabajo en menos de 10 segundos

### S02

- `slide_id`: `s02_problema_negocio`
- `titulo`: `Por que clasificar propiedades automaticamente`
- `objetivo`: justificar el problema desde Data e IA aplicada
- `mensaje_clave`: el valor esta en convertir texto libre en metadata accionable
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: bloque de problema + lista de impactos + iconografia discreta
- `contenido_fijo`: texto del problema y lista de impacto esperado
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: composicion 60/40 texto e impactos, sin imagenes decorativas
- `criterio_de_aceptacion`: la slide debe explicar negocio, friccion actual y valor esperado sin depender de oralidad adicional

### S03

- `slide_id`: `s03_objetivo_analitico`
- `titulo`: `Objetivo del trabajo`
- `objetivo`: enunciar la tarea de clasificacion y las clases objetivo
- `mensaje_clave`: se compara clasificacion clasica versus transformer sobre `Casa`, `Departamento`, `PH`
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: statement principal, triada de clases, nota metodologica
- `contenido_fijo`: objetivo analitico y clases
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: destacar visualmente las 3 clases como elementos equivalentes
- `criterio_de_aceptacion`: la audiencia debe entender tarea, input y output del modelo

### S04

- `slide_id`: `s04_workflow`
- `titulo`: `Workflow del trabajo`
- `objetivo`: resumir el flujo metodologico de punta a punta
- `mensaje_clave`: el proyecto sigue un pipeline reproducible desde problema hasta conclusion operativa
- `tipo_de_slide`: `workflow`
- `componentes_visuales`: asset `workflow_nlp_inmobiliario.svg`, leyenda de etapas, banda inferior de lectura
- `contenido_fijo`: etiquetas de etapas y conclusion breve
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template + asset estatico
- `modo_de_carga`: `estatico`
- `fallback`: placeholder del diagrama con lista textual de etapas
- `criterio_visual`: pipeline horizontal, separacion cromatica por datos/modelos/evaluacion/decision
- `criterio_de_aceptacion`: debe poder narrarse el proyecto completo en una sola slide sin scroll

### S05

- `slide_id`: `s05_dataset`
- `titulo`: `Datos utilizados`
- `objetivo`: explicar dataset, columnas usadas y criterio de muestreo
- `mensaje_clave`: se trabajo con Properati, usando `description` y `property_type`, con train balanceado y test natural
- `tipo_de_slide`: `evidencia`
- `componentes_visuales`: resumen textual + asset `distribucion_train_test.png`
- `contenido_fijo`: descripcion del dataset y restricciones de computo
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template + asset estatico exportado desde notebook
- `modo_de_carga`: `estatico`
- `fallback`: placeholder de grafico y nota `export pendiente`
- `criterio_visual`: grafico dominante a derecha o abajo; texto minimo
- `criterio_de_aceptacion`: debe quedar claro por que train y test no siguen la misma distribucion

### S06

- `slide_id`: `s06_escenarios`
- `titulo`: `Diseno experimental`
- `objetivo`: comparar escenario base versus censurado
- `mensaje_clave`: la censura no es cosmetica; es un control de leakage
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: comparador en dos columnas, lista de terminos censurados, callout de leakage
- `contenido_fijo`: definicion de ambos escenarios
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: comparacion simetrica base/censurado, con destaque semantico del leakage
- `criterio_de_aceptacion`: la audiencia debe entender por que el escenario censurado existe aunque rinda peor

### S07

- `slide_id`: `s07_modelos`
- `titulo`: `Modelos evaluados`
- `objetivo`: enumerar familias y alcances del benchmark
- `mensaje_clave`: se comparan modelos clasicos con TF-IDF contra DistilBERT ajustado en CPU
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: dos columnas por familia, mini pipeline o chips de modelo
- `contenido_fijo`: Naive Bayes, SVM, Regresion Logistica, DistilBERT, epochs
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: no usar tabla; usar comparacion de familias
- `criterio_de_aceptacion`: debe quedar clara la cobertura del benchmark y la restriccion CPU-only

### S08

- `slide_id`: `s08_preprocesamiento`
- `titulo`: `Preprocesamiento diferenciado`
- `objetivo`: explicar que clasicos y transformer no comparten exactamente la misma limpieza
- `mensaje_clave`: los clasicos condensan senal lexica; DistilBERT preserva mas lenguaje natural
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: tabla comparativa ligera o dos paneles con bullets
- `contenido_fijo`: reglas para clasicos y reglas para DistilBERT
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: lenguaje tecnico compacto, sin parrafos largos
- `criterio_de_aceptacion`: debe quedar explicitada la razon metodologica de la diferencia de limpieza

### S09

- `slide_id`: `s09_metricas`
- `titulo`: `Metricas de evaluacion`
- `objetivo`: justificar por que se usan Accuracy y F1 Macro
- `mensaje_clave`: Accuracy sola no alcanza para una clase ambigua y menos frecuente como PH
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: tarjetas de metricas + nota metodologica
- `contenido_fijo`: definicion de Accuracy, F1 Macro y mensaje clave
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: una sola idea por metrica
- `criterio_de_aceptacion`: la slide debe preparar la lectura correcta de resultados posteriores

### S10

- `slide_id`: `s10_resultados_principales`
- `titulo`: `Resultados principales`
- `objetivo`: mostrar comparacion consolidada de modelos
- `mensaje_clave`: los resultados deben leerse junto con escenario metodologico y costo operativo
- `tipo_de_slide`: `evidencia`
- `componentes_visuales`: fragmento `tabla_resultados_principales.html`, nota de lectura, badge de fecha benchmark
- `contenido_fijo`: encabezado y lectura
- `contenido_dinamico`: fecha benchmark para cross-check y warning de inconsistencia si aplica
- `fuente_de_verdad`: asset estatico + `GET /benchmark.fecha_benchmark_cpu` + `GET /benchmark.resultados`
- `modo_de_carga`: `hibrido`
- `fallback`: si falla la API, mantener la tabla estatica y ocultar validacion en vivo
- `criterio_visual`: la tabla debe ser el elemento dominante de la slide
- `criterio_de_aceptacion`: la audiencia debe poder ver base y censurado sin depender de scroll ni hover

### S11

- `slide_id`: `s11_interpretacion`
- `titulo`: `Interpretacion de resultados`
- `objetivo`: explicar por que Regresion Logistica censurada resulta competitiva
- `mensaje_clave`: un modelo simple bien preprocesado puede competir con uno profundo en este dominio
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: texto guiado + cajas de costo/lexicalizacion/guardrail
- `contenido_fijo`: explicacion del lenguaje inmobiliario y conclusion parcial
- `contenido_dinamico`: `guardrail_censura.hallazgo` y `guardrail_censura.lectura`
- `fuente_de_verdad`: template + `GET /benchmark.guardrail_censura`
- `modo_de_carga`: `hibrido`
- `fallback`: usar texto estatico equivalente tomado del spec si la API falla
- `criterio_visual`: separar claramente `hallazgo empirico` de `decision metodologica`
- `criterio_de_aceptacion`: la slide debe defender que censurado no gano, pero igual se conserva como control de leakage

### S12

- `slide_id`: `s12_caso_ph`
- `titulo`: `El caso PH`
- `objetivo`: mostrar la dificultad especifica de la clase PH
- `mensaje_clave`: PH es semanticamente ambigua y comparte senal con Casa y Departamento
- `tipo_de_slide`: `evidencia`
- `componentes_visuales`: asset `matriz_confusion_reglog_censurado.png` + bloques de interpretacion
- `contenido_fijo`: rasgos compartidos y lectura del bajo F1 de PH
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template + asset estatico
- `modo_de_carga`: `estatico`
- `fallback`: placeholder de matriz con resumen textual de ambiguedad
- `criterio_visual`: la matriz debe ocupar mas espacio que el texto
- `criterio_de_aceptacion`: la slide debe dejar evidencia concreta de donde falla la clasificacion

### S13

- `slide_id`: `s13_explicabilidad`
- `titulo`: `Explicabilidad`
- `objetivo`: mostrar que aprendieron los modelos y donde aparecen artefactos
- `mensaje_clave`: la explicabilidad permite separar senales utiles de correlaciones espurias
- `tipo_de_slide`: `evidencia`
- `componentes_visuales`: dos subpaneles con `explicabilidad_reglog_tokens.png` y `explicabilidad_bayes_alertas.png`
- `contenido_fijo`: lectura de Regresion Logistica y Naive Bayes
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template + assets estaticos
- `modo_de_carga`: `estatico`
- `fallback`: si falta un asset, mantener el otro y usar placeholder de igual tamano
- `criterio_visual`: comparacion izquierda/derecha con mismo peso visual
- `criterio_de_aceptacion`: la audiencia debe entender que explicabilidad no es adorno sino criterio de confianza

### S14

- `slide_id`: `s14_lectura_negocio`
- `titulo`: `Lectura de negocio`
- `objetivo`: traducir el benchmark a criterio de uso operativo
- `mensaje_clave`: el modelo es util como sugeridor y auditor, no como decision final sin monitoreo
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: tarjetas de uso, badge de modelo activo, estado guardrail
- `contenido_fijo`: usos posibles y condicion de monitoreo
- `contenido_dinamico`: `modelo_api_final.modelo`, `modelo_api_final.condicion`, `guardrail_censura.se_sostiene`
- `fuente_de_verdad`: template + `GET /benchmark`
- `modo_de_carga`: `hibrido`
- `fallback`: mostrar usos y un badge `estado operativo no verificado`
- `criterio_visual`: debe sentirse como lectura de decision, no como slide tecnica
- `criterio_de_aceptacion`: debe quedar claro que utilidad no implica autonomia plena del modelo

### S15

- `slide_id`: `s15_limitaciones`
- `titulo`: `Limitaciones`
- `objetivo`: explicitar los limites metodologicos y operativos del ejercicio
- `mensaje_clave`: la restriccion de CPU, la ambiguedad de clases y la falta de variables tabulares limitan el alcance
- `tipo_de_slide`: `narrativa`
- `componentes_visuales`: lista priorizada de limites + mini bloque operativo
- `contenido_fijo`: lista de limitaciones del template
- `contenido_dinamico`: `modelo_api_final.ruta_artefacto` y `modelo_api_final.criterio_seleccion`
- `fuente_de_verdad`: template + `GET /benchmark.modelo_api_final`
- `modo_de_carga`: `hibrido`
- `fallback`: mantener solo limitaciones narrativas
- `criterio_visual`: no convertirla en slide de disculpas; debe verse como control de alcance
- `criterio_de_aceptacion`: debe anticipar preguntas del jurado sobre sesgo, costo y generalizacion

### S16

- `slide_id`: `s16_api_demo`
- `titulo`: `API del modelo`
- `objetivo`: mostrar operacion local de la API y demo de inferencia
- `mensaje_clave`: el mejor modelo censurado puede exponerse como componente consultable localmente
- `tipo_de_slide`: `demo`
- `componentes_visuales`: diagrama `api_flujo_prediccion.svg`, lista de endpoints, formulario de demo, estado API, resultado
- `contenido_fijo`: endpoints `GET /salud`, `GET /benchmark`, `POST /predecir`, `GET /presentacion`
- `contenido_dinamico`: respuesta de `GET /salud`, metadata de `GET /benchmark`, inferencia de `POST /predecir`
- `fuente_de_verdad`: template + API local + asset estatico de flujo
- `modo_de_carga`: `hibrido`
- `fallback`: si la API falla, mantener el diagrama y describir la demo como no operativa
- `criterio_visual`: la demo no debe ocupar la slide completa; primero explicar el componente, despues mostrar la accion
- `criterio_de_aceptacion`: el formulario debe funcionar cuando la API este arriba y degradar sin romper la deck cuando no lo este

### S17

- `slide_id`: `s17_conclusiones`
- `titulo`: `Conclusiones`
- `objetivo`: consolidar aprendizajes metodologicos y tecnicos
- `mensaje_clave`: el valor del trabajo esta en clasificar y en auditar que aprendio el modelo
- `tipo_de_slide`: `cierre`
- `componentes_visuales`: lista de 7 aprendizajes + cierre destacado
- `contenido_fijo`: aprendizajes principales y cierre
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: slide de cierre tecnico, no celebratoria
- `criterio_de_aceptacion`: la audiencia debe poder recordar 3 a 4 mensajes fuertes sin mirar slides previas

### S18

- `slide_id`: `s18_proximos_pasos`
- `titulo`: `Proximos pasos`
- `objetivo`: cerrar con trabajo futuro realista
- `mensaje_clave`: hay mejoras posibles en tuning, datos, calibracion y despliegue
- `tipo_de_slide`: `cierre`
- `componentes_visuales`: roadmap corto o lista jerarquizada
- `contenido_fijo`: lista de proximos pasos
- `contenido_dinamico`: ninguno
- `fuente_de_verdad`: template
- `modo_de_carga`: `estatico`
- `fallback`: no aplica
- `criterio_visual`: priorizar legibilidad y sentido de continuidad
- `criterio_de_aceptacion`: la slide debe mostrar madurez tecnica y no abrir alcance innecesario

## 7. Reglas de binding frontend

### 7.1 Estructura de archivos esperada

- `src/static/presentacion.html`: shell de slides y placeholders semanticos
- `src/static/presentacion.css`: sistema visual y layout
- `src/static/presentacion.js`: navegacion, binding de API y manejo de estados
- `src/static/assets/presentacion/*`: evidencia estatica

### 7.2 Reglas de render

- Cada slide debe renderizarse como seccion independiente con `data-slide-id`.
- El JS no debe construir la narrativa principal; solo hidratar placeholders dinamicos.
- Los assets estaticos deben estar referenciados directamente desde HTML o por datos de configuracion local en JS.
- La tabla estatica principal debe poder insertarse como fragmento HTML sin recalculo en cliente.

### 7.3 Estados de UI obligatorios

- `loading`: solo para salud/API/demo
- `ok`: API disponible y payload coherente
- `degraded`: API no disponible pero deck usable
- `warning`: API disponible pero inconsistencia entre benchmark vivo y evidencia estatica
- `error`: error puntual de demo

### 7.4 Regla de inconsistencia

Si `GET /benchmark.resultados` no coincide con la fecha o el modelo activo esperados por la evidencia estatica:

- no reemplazar tabla ni graficos;
- mostrar badge `benchmark vivo no alineado con evidencia estatica`;
- permitir continuar con la demo;
- loggear en consola la inconsistencia para revision local.

## 8. Reglas de datos y fallbacks

### 8.1 Si falta un asset estatico

- mantener dimensiones del contenedor;
- mostrar placeholder con nombre del asset faltante;
- no ocultar la slide ni recolapsar layout.

### 8.2 Si `GET /salud` falla

- marcar topbar en `API no disponible`;
- mantener navegacion de slides;
- anular solo interacciones vivas.

### 8.3 Si `GET /benchmark` falla

- no tocar slides 1 a 13 salvo badges operativos;
- slides 14 a 16 deben mostrar estado degradado y copy de fallback;
- la tabla principal estatica debe permanecer visible.

### 8.4 Si `POST /predecir` falla

- mantener la UI del formulario;
- mostrar mensaje de error contextual;
- no borrar el texto ingresado;
- limpiar solo resultados dependientes de la respuesta fallida si hace falta.

## 9. Criterios de aceptacion

La reimplementacion de la presentacion se considera correcta si cumple todo lo siguiente:

- el servidor FastAPI sigue sirviendo `GET /presentacion` sin cambios de endpoint;
- la deck contiene 18 slides navegables;
- cada slide respeta el `mensaje_clave` definido en este spec;
- la evidencia principal se muestra mediante assets estaticos o fragmentos consolidados;
- la API solo se usa para estado operativo, metadatos y demo;
- la falla de API no rompe la narrativa de defensa;
- la slide 16 permite consultar `POST /predecir` cuando la API esta disponible;
- la jerarquia visual es consistente con el sistema definido;
- la lectura desktop no requiere zoom ni produce superposiciones;
- la version reducida conserva legibilidad y orden.

## 10. Checklist de validacion para implementacion futura

- Verificar que `GET /presentacion`, `GET /salud`, `GET /benchmark` y `POST /predecir` sigan respondiendo.
- Verificar que la fecha viva del benchmark coincida con la evidencia estatica consolidada.
- Verificar que el modelo activo vivo coincida con la lectura operativa mostrada.
- Verificar que los placeholders de assets faltantes no rompan layout.
- Verificar que la demo soporta al menos un caso ejemplo y un caso de error.
- Verificar desktop de defensa y viewport reducido.

## 11. Supuestos fijados

- La API embebida en el flujo del servidor ya esta resuelta y no se redisenia.
- La fuente narrativa primaria sigue siendo `doc/template_presentacion_final_nlp_inmobiliario.md`.
- El rebuild debe priorizar estabilidad de defensa sobre dinamismo total.
- La evidencia visual principal no se recalcula en cliente.
- `GET /benchmark` se usa como contrato operativo y de validacion, no como reemplazo de assets analiticos.
