# 🌍 Proyecto ETL + Power BI - Consumo Energético

**Fecha de última actualización:** 18/07/2025

Este proyecto implementa un proceso ETL para transformar y cargar datos de consumo y producción de energía a una base de datos relacional en **SQL Server**, permitiendo su análisis mediante **Power BI**. Utiliza un dataset público con cobertura global, desglosado por año y tipo de energía.

---

## 📦 Dataset Utilizado

* **Nombre:** World Energy Consumption
* **Fuente:** [Our World in Data - Kaggle](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption)
* **Formato:** CSV
* **Columnas:** 129
* **Años:** 1965 - 2022
* **Cobertura geográfica:** Mundial (países, regiones, organizaciones como OPEC, ASEAN...)

**Indicadores incluidos:**

* Consumo y producción de energía por tipo (solar, eólica, hidroeléctrica, nuclear, petróleo, gas, etc.)
* Cambios porcentuales año a año
* Datos per cápita y participación porcentual

El archivo fue renombrado como `World Energy Consumption.csv` y ubicado en la carpeta `/data`.

---

## 🔄 Proceso ETL

**Archivo principal:** `etl_script.py`

El script realiza:

* Carga de datos desde el CSV
* Limpieza y transformación
* Creación de dimensiones:

  * `countries` (países)
  * `energy_types` (tipos de energía)
* Creación de la tabla de hechos:

  * `energy_consumption` con consumo y producción anual
* Inserción en **SQL Server** mediante `SQLAlchemy` + `pyodbc`
* Conexión local mediante `Trusted Connection` a la base de datos **EnergiaDB**

---

## 🧱 Estructura de la Base de Datos

```
Table: countries
- country_id [PK]
- country_name

Table: energy_types
- energy_type_id [PK]
- energy_type

Table: energy_consumption
- id [PK]
- country_id [FK] → countries.country_id
- energy_type_id [FK] → energy_types.energy_type_id
- year
- consumption
- production
```

---

## 📊 Visualización en Power BI

**Archivo:** `dashboard_energy_etl.pbix`

**Conexión a SQL Server:**

* **Servidor:** `localhost`
* **Base de datos:** `EnergiaDB`

**Relaciones:**

* `energy_consumption.country_id` → `countries.country_id`
* `energy_consumption.energy_type_id` → `energy_types.energy_type_id`

### Visualizaciones incluidas:

* 🔹 Tarjetas: Consumo y producción total
* 📈 Gráfico de líneas: Evolución anual por tipo de energía
* 🗺️ Mapa: Consumo energético global por país
* 🧮 Comparaciones por país y tipo de energía
* 🎛️ Segmentadores: Año, país y tipo de energía

---

## ⚙️ Requisitos

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Crear entorno virtual (opcional)

```bash
python -m venv venv
venv\\Scripts\\activate  # En Windows
```

---

## 🚫 Exclusiones

Agrega al `.gitignore`:

```
venv/
*.pyc
__pycache__/
```

---

## 📁 Estructura del Proyecto

```
ETL-Project/
├── data/
│   └── World Energy Consumption.csv
├── documentation/
│   └── Documentacion_ETL_Energia.pdf
├── Power bi/
│   └── dashboard_energy_etl.pbix
├── screenshots/
│   └── db_World_Energy_Consumption.png
├── script/
│   └── etl_script.py
├── requirements.txt
├── .gitignore
└── README.md
```

---



---
