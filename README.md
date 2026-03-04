# Atributos Derivados PPG

## Objetivo

Este proyecto tiene como objetivo procesar y analizar señales fisiológicas, específicamente fotopletismografía (PPG), para calcular y derivar atributos relevantes como la frecuencia cardíaca y la saturación de oxígeno en sangre (SpO2), apoyando el análisis de datos biomédicos.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

```text
.
├── data/
│   ├── input/       # Carpeta para los archivos CSV de entrada con señales PPG
│   └── output/      # Carpeta donde se guardan los resultados derivados
├── src/
│   ├── cardiac_freq.py  # Módulo con la lógica para el cálculo de la frecuencia cardíaca
│   ├── common.py        # Funciones auxiliares y utilidades comunes
│   ├── config.py        # Parámetros de configuración del proyecto
│   ├── oximetry.py      # Módulo para el cálculo de SpO2 a partir de señales PPG
├── main.py          # Script principal que orquesta la ejecución
└── requirements.txt # Lista de dependencias de Python necesarias
```

## Formato de Datos

Los datos deben estar en formato tabular **CSV**.

- Los archivos en `data/input/` en su estructura deben contener características de la señal a procesar (ej. datos crudos PPG).

  `data/input/2025-11-17T02-01-41Z_ppg.csv`:

  | | RED | IR | GREEN |
  | --- | --- | --- | --- |
  | 1763344895168 | 914855 | 1294302 | 17511 |
  | 1763344895208 | 914928 | 1294175 | 17778 |
  | 1763344895248 | 914959 | 1293861 | 17875 |
  | ... | ... | ... | ... |

- Los resultados en `data/output/` conservarán el nombre del archivo original procesado acompañado del sufijo `_derived-data.csv`.

  `data/output/2025-11-17T02-01-41Z_ppg_derived-data.csv`:

  | Column | Heart Rate (BPM) | Frequency Variability (s) | Tachycardic | Estimated SpO2 |
  | --- | --- | --- | --- | --- |
  | RED | 71.00591715976331 | 0.11213830746002902 | False | 0.7186912844110811 |
  | IR | 68.62745098039215 | 0.07228063223242011 | False | 0.7186912844110811 |
  | GREEN | 67.41573033707866 | 0.03872983346207418 | False | 0.7186912844110811 |

  El plot generado se guardará con el sufijo `_processed-plot.png`:

  `data/output/2025-11-17T02-01-41Z_ppg_processed-plot.png`:

  ![Ejemplo de Plot PPG](data/output/2025-11-17T02-01-41Z_ppg_processed-plot.png)

## Instalación y Configuración (Setup)

1. **Clonar** el repositorio (si aplica) y entrar al directorio del proyecto.
2. **Crear un entorno virtual** (recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Linux/Mac
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Colocar el archivo de muestras PPG en la carpeta `data/input/` (ejemplo: `2025-11-17T02-01-41Z_ppg.csv`).
2. Ejecutar el script principal:

   ```bash
   python -m main 2025-11-17T02-01-41Z_ppg.csv
   ```

3. Los resultados derivados se guardarán automáticamente en `data/output/`. El archivo CSV con los atributos tendrá el sufijo `_derived-data.csv` y el gráfico generado tendrá el sufijo `_processed-plot.png`. Además, el archivo incluirá una columna adicional con el valor estimado de SpO2 calculado a partir de las señales RED e IR.
