# Template de presentación final — NLP inmobiliario

> **Uso previsto:** este archivo contiene el contenido base de las slides en Markdown/texto plano para integrarlo con el HTML existente y con los resultados generados desde notebooks mediante CODEX.
>
> **Trabajo:** clasificación automática de avisos inmobiliarios con NLP.
>
> **Caso:** tipificación de propiedades en Casa, Departamento y PH.

---

# Slide 1 — Título

## Clasificación automática de avisos inmobiliarios con NLP

**Caso:** tipificación de propiedades en Casa, Departamento y PH  
**Materia:** Procesamiento de Lenguaje Natural  
**Enfoque:** modelos clásicos, Transformers y explicabilidad aplicada a un caso de negocio

---

# Slide 2 — Problema de negocio

## ¿Por qué clasificar propiedades automáticamente?

Como consultores en **Data e Inteligencia Artificial**, abordamos un problema frecuente en plataformas inmobiliarias: convertir publicaciones heterogéneas, ruidosas y escritas en texto libre en información estructurada y accionable.

Las plataformas reciben miles de publicaciones redactadas por usuarios, agentes y corredores. La falta de metadatos confiables obliga a utilizar la descripción textual como fuente principal para inferir el tipo de propiedad.

**Impacto esperado:**

- mejorar la calidad del catálogo;
- reducir errores de carga manual;
- enriquecer datos para analítica de mercado;
- escalar procesos de clasificación;
- generar una base más confiable para productos de datos e IA.

---

# Slide 3 — Objetivo del trabajo

## Objetivo analítico

Construir un modelo capaz de generar una tipología de propiedad basada en la descripción publicada de las mismas.

Las clases objetivo son:

**Casa | Departamento | PH**

El trabajo compara modelos clásicos con modelos basados en Transformer.

---

# Slide 4 — Workflow del trabajo

## Flujo metodológico del proyecto

**PROMPT PARA CODEX**

Generar una slide en HTML que represente visualmente el workflow del trabajo de NLP.  
El diseño debe ser académico pero con lectura de caso de negocio.

El flujo debe incluir las siguientes etapas:

1. **Definición del problema**
   - necesidad de tipificar propiedades a partir de texto libre;
   - enfoque como consultores de Data e IA.

2. **Selección de datos**
   - dataset de publicaciones inmobiliarias;
   - uso de `description` y `property_type`.

3. **Preparación del corpus**
   - muestreo;
   - balanceo del conjunto de entrenamiento;
   - mantenimiento de distribución natural en test.

4. **Preprocesamiento diferenciado**
   - estrategia para modelos clásicos;
   - estrategia para DistilBERT.

5. **Entrenamiento de modelos**
   - TF-IDF + modelos clásicos;
   - DistilBERT con fine-tuning.

6. **Evaluación**
   - Accuracy;
   - F1 Macro;
   - análisis por clase.

7. **Explicabilidad**
   - coeficientes de regresión logística;
   - análisis de Naive Bayes;
   - Integrated Gradients para DistilBERT.

8. **Conclusión de negocio**
   - modelo candidato;
   - limitaciones;
   - criterios para eventual uso operativo.

Sugerencia visual: usar un diagrama horizontal tipo pipeline con bloques conectados por flechas.  
Incluir íconos simples o etiquetas visuales para diferenciar datos, modelos, evaluación y decisión.

---

# Slide 5 — Dataset

## Datos utilizados

Base de anuncios inmobiliarios de Properati, con aproximadamente un millón de registros.

Para este ejercicio se utilizaron únicamente:

- `description`
- `property_type`

La muestra operativa fue reducida por restricciones de cómputo.

**Train:** clases balanceadas  
**Test:** distribución natural del mercado

[INSERTAR GRÁFICO: distribución de clases train vs test]

---

# Slide 6 — Diseño experimental

## Dos escenarios de evaluación

### Escenario base

Los modelos entrenan con las descripciones originales.

### Escenario censurado

Se eliminan términos explícitos como:

`casa`, `departamento`, `depto`, `ph`

Este escenario busca medir si el modelo aprende señales lingüísticas reales o simplemente detecta la etiqueta dentro del texto.

---

# Slide 7 — Modelos evaluados

## Familias de modelos

### Modelos clásicos

- Naive Bayes
- SVM
- Regresión logística
- Vectorización TF-IDF

### Modelo Transformer

- DistilBERT
- Fine-tuning limitado por ejecución en CPU
- Evaluación con 1 y 2 épocas

[INSERTAR DIAGRAMA: pipeline completo]

---

# Slide 8 — Preprocesamiento

## Estrategias diferenciadas por arquitectura

### Para modelos clásicos

Se buscó reducir ruido y consolidar señales léxicas:

- minúsculas;
- eliminación de tildes;
- stop words;
- normalización de abreviaturas;
- n-gramas forzados: `3_ambientes`, `50_m2`.

### Para DistilBERT

Se buscó preservar lenguaje natural:

- conservación de contexto;
- expansión de abreviaturas;
- unidades legibles: `50 metros cuadrados`;
- menor intervención sobre la estructura textual.

---

# Slide 9 — Métricas

## ¿Cómo se evaluó el desempeño?

Se utilizaron dos métricas principales:

### Accuracy

Mide la tasa global de aciertos.

### F1 Macro

Promedia el desempeño por clase y permite observar si el modelo falla en clases minoritarias como PH.

**Mensaje clave:**  
en problemas con clases desbalanceadas, el accuracy no alcanza para evaluar calidad predictiva.

---

# Slide 10 — Resultados principales

## Comparación de modelos

[INSERTAR TABLA DESDE NOTEBOOK: `df_tabla1`]

**Lectura:**  
los resultados deben interpretarse considerando tanto el desempeño predictivo como el escenario metodológico en el que fueron obtenidos.

---

# Slide 11 — Interpretación de resultados

## ¿Qué modelo funcionó mejor?

En el escenario censurado, la regresión logística mostró un desempeño muy competitivo frente a DistilBERT.

Además de las métricas, el **costo computacional** es un criterio relevante para la elección del modelo. Un modelo clásico con TF-IDF puede ser más simple de entrenar, más económico de ejecutar y más fácil de mantener en un contexto operativo.

La explicación principal es que el lenguaje inmobiliario es:

- breve;
- descriptivo;
- altamente lexicalizado;
- dominado por términos como `lote`, `jardín`, `balcón`, `expensas`, `pasillo`.

**Conclusión parcial:**  
para este caso, un modelo simple bien preprocesado puede competir con modelos profundos y ofrecer una mejor relación entre desempeño, costo y mantenibilidad.

---

# Slide 12 — El caso PH

## La clase más difícil de separar

PH aparece como una categoría ambigua.

Comparte señales con:

**Casa**

- patio
- entrada independiente
- sin expensas

**Departamento**

- pasillo
- expensas
- unidades internas

El bajo F1 de PH sugiere que la ambigüedad no es solo algorítmica, sino también semántica y de etiquetado humano.

[INSERTAR MATRIZ DE CONFUSIÓN]

---

# Slide 13 — Explicabilidad

## ¿Qué aprendieron los modelos?

### Regresión logística

Identificó señales estructurales coherentes:

- Casa: jardín, chalet, galería;
- Departamento: edificio, balcón, amenities;
- PH: patio, terraza, pasillo, expensas.

### Naive Bayes

Detectó artefactos no deseados:

- nombres de inmobiliarias;
- zonas geográficas;
- marcas o agentes.

Esto sugiere que algunos modelos aprenden correlaciones del dataset, no necesariamente rasgos de la propiedad.

---

# Slide 14 — Lectura de negocio

## ¿Es desplegable este modelo?

Sí, pero con controles.

Un modelo de clasificación automática podría usarse como:

- sugeridor de tipo de propiedad;
- auditor de inconsistencias;
- enriquecedor de catálogos;
- insumo para analítica inmobiliaria.

Pero no debería operar como decisión final sin monitoreo, especialmente para PH.

---

# Slide 15 — Limitaciones

## Límites del ejercicio

- entrenamiento restringido a CPU;
- fine-tuning limitado de DistilBERT;
- posible sesgo por inmobiliarias o zonas;
- ambigüedad real entre clases;
- ausencia de variables adicionales como ubicación, superficie o precio.

---

# Slide 16 — API del modelo

[INSERTAR AQUÍ LA API]

---

# Slide 17 — Conclusiones

## Aprendizajes principales

1. El control de leakage fue un punto metodológico relevante.
2. La regresión logística con TF-IDF fue altamente competitiva.
3. DistilBERT mostró potencial, pero limitado por recursos.
4. PH es una clase estructuralmente ambigua.
5. La explicabilidad permitió detectar señales útiles y artefactos riesgosos.
6. La selección del modelo debe considerar desempeño, costo computacional y facilidad de mantenimiento.
7. Una API permitiría convertir el modelo en un componente integrable y reutilizable.

**Cierre:**  
el valor del trabajo no está solo en clasificar, sino en auditar qué aprende el modelo antes de pensar en un uso productivo.

---

# Slide 18 — Próximos pasos

## Trabajo futuro

- ejecutar mayor tuning de hiperparámetros;
- entrenar Transformers por más épocas;
- incorporar técnicas de limpieza adicional del corpus;
- agregar variables tabulares;
- analizar calibración de probabilidades;
- diseñar umbrales de abstención para casos ambiguos;
- evaluar el modelo en datos nuevos fuera de muestra;
- construir una API mínima para servir el modelo seleccionado.

---

# Notas para integración con HTML y notebooks

## Elementos a reemplazar desde notebooks

- `df_tabla1`: tabla comparativa de resultados finales.
- Gráfico de distribución de clases train vs test.
- Matriz de confusión.
- Diagrama del pipeline o workflow.
- API o bloque HTML correspondiente en la Slide 16.

## Validaciones recomendadas antes de la presentación final

- Verificar consistencia entre los valores del informe y los outputs de las notebooks.
- Usar los resultados consolidados del notebook como fuente única para métricas.
- Revisar especialmente los valores de Accuracy y F1 Macro del escenario censurado.
- Eliminar textos residuales o incompletos antes de generar el HTML final.
