# Phoenix Civic Insights & Sustainability Analytics

Real-data analytics for the City of Phoenix using **Python (pandas, matplotlib)** and **SQL (SQLite)**.  
Focus areas: **water production** and **calls for service** (police dispatch).

**Developed by [Mihir Dinanath Hunge](https://github.com/mhrhunge)**

---

##  Project Overview
- Automates download of **official Phoenix Open Data** (water production & calls for service).
- Ingests CSVs → **SQLite** via Python ETL.
- Runs **analytical SQL** + Python aggregations.
- Exports **ready-to-viz CSVs** and **PNG charts** to `outputs/`.
- Includes **Power BI starter assets** (theme + Power Query scripts) to build a PBIX quickly.

---

##  Skills Demonstrated
- **SQL (SQLite):** schema design, indexing, window functions, aggregation, ranking.
- **Python (pandas, matplotlib, requests):** ETL, cleaning, joins, KPIs, charting, automation.
- **Data Engineering:** reproducible pipeline (download → build DB → analyze).
- **Visualization:** KPI charts; CSV outputs for **Power BI / Tableau**.
- **Documentation & GitHub:** clean repo structure, MIT license, readable README.

---

##  Tools Used
- **Python**: pandas, numpy, matplotlib, requests
- **SQL**: SQLite (via `sqlite3`), SQL window functions
- **Jupyter Notebook** for exploration
- **Git + GitHub** for version control
- **Power BI** helper assets (`/powerbi`) to accelerate dashboard creation

---

##  Repository Layout
```
data/        # downloaded CSVs (after running download_data.py)
sql/         # schema + queries
src/         # ETL + analysis scripts
notebooks/   # exploration
outputs/     # charts + summary CSVs
powerbi/     # theme + Power Query scripts to build a PBIX
```

---

##  Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Download official Phoenix Open Data (adjust years in script if desired)
python src/download_data.py

# 2) Build local SQLite DB from CSVs
python src/build_db.py

# 3) Run analysis to produce charts + CSV summaries
python src/analyze_real.py
```

Outputs are saved to `outputs/`:
- `water_production_trend.csv`, `water_production_trend_real.png`
- `calls_top_types.csv`, `calls_top_types.png`

---

##  Power BI (Starter)
- Import `outputs/water_production_trend.csv` and `outputs/calls_top_types.csv` into Power BI.
- Optional: Use theme `powerbi/phoenix_theme.json`.
- Optional: Use Power Query scripts in `powerbi/queries/` to connect directly to the CSV folder.

> Note: A PBIX binary cannot be included here, but all assets are provided to generate it quickly.

---

##  Data Sources (Official)
- City of Phoenix Open Data — Water: Total Produced (million gallons)
- City of Phoenix Open Data — Calls for Service

---

##  License
MIT
