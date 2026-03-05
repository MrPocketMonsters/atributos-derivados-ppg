# Atributos Derivados PPG

## Objetivo

Este proyecto procesa y analiza señales fotopletismográficas (PPG) para calcular y derivar atributos relevantes, como la frecuencia cardíaca y una estimación de SpO2, facilitando análisis y extracción de métricas biomédicas.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

```text
.
├── data/
│   ├── input/       # CSV de entrada con señales PPG (múltiples archivos)
│   └── output/      # Resultados derivados y plots
├── src/
│   ├── cardiac_freq.py  # Cálculo de la frecuencia cardíaca
│   ├── common.py        # Funciones auxiliares
│   ├── config.py        # Parámetros y constantes
│   └── oximetry.py      # Cálculo estimado de SpO2 (RED/IR)
├── main.py          # Script principal que procesa la carpeta `data/input/`
└── requirements.txt # Dependencias de Python
```

## Formato de Datos

Los archivos de entrada deben ser CSV con columnas mínimas para la señal PPG. Cada fila representa una muestra y debe incluir una columna de timestamp seguida de canales (ej. `RED`, `IR`, `GREEN`).

Requisitos del `timestamp` (único formato aceptado):

- Entero en milisegundos (ej.: `1763344895168`)
- O flotante en segundos (ej.: `1763344895.168`)

No se aceptan otros formatos de timestamp (p. ej. ISO-8601 con texto) — el proceso validará y solo admitirá las dos formas anteriores.

Ejemplo de archivo de entrada `data/input/2025-11-17T02-01-41Z_ppg.csv`:

| timestamp | RED | IR | GREEN |
| --- | --- | --- | --- |
| 1763344895168 | 914855 | 1294302 | 17511 |
| 1763344895208 | 914928 | 1294175 | 17778 |
| 1763344895248 | 914959 | 1293861 | 17875 |

Salida prevista en `data/output/`:

- CSV con sufijo `_derived-data.csv` agregando las columnas derivadas (por canal): frecuencia cardíaca, variabilidad, indicador de taquicardia, estimación de SpO2.

   | Column | Heart Rate (BPM) | Frequency Variability (s) | Tachycardic | Estimated SpO2 |
   | --- | --- | --- | --- | --- |
   | RED | 71.00591715976331 | 0.11213830746002902 | False | 0.7186912844110811 |
   | IR | 68.62745098039215 | 0.07228063223242011 | False | 0.7186912844110811 |
   | GREEN | 67.41573033707866 | 0.03872983346207418 | False | 0.7186912844110811 |

- Plot por archivo con sufijo `_processed-plot.png`.

## Instalación y Configuración (Setup)

1. Clonar el repositorio y entrar al directorio del proyecto.
2. Crear y activar un entorno virtual (recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Linux/Mac
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Coloca uno o varios archivos CSV PPG en la carpeta `data/input/`.
2. Ejecuta el script principal para procesar toda la carpeta de entrada:

   ```bash
   python -m main
   ```

3. Los resultados se guardarán en `data/output/`:

- `<original>_derived-data.csv` — atributos derivados por canal.
- `<original>_processed-plot.png` — gráfico generado para el archivo.

Notas:

- El proceso recorrerá todos los CSV en `data/input/` y validará el `timestamp` de cada archivo; los archivos que no cumplan el formato requerido serán reportados y omitidos.
- Si deseas procesar otra carpeta, ajusta la variable correspondiente en `config.py` o modifica la línea de ejecución si `main.py` soporta argumentos de entrada.
