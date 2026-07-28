# Nifty100 Financial Intelligence Platform

## Overview
A financial analytics platform for Nifty100 companies built using Python, SQLite, FastAPI, and Streamlit.

## Features
- ETL pipeline
- Financial ratio engine
- Screening engine
- REST API
- Interactive dashboard
- PDF tearsheets
- Automated tests

## Setup
```bash
pip install -r requirements.txt
```

## Run ETL
```bash
python main.py
```

## Run API
```bash
python -m uvicorn src.api.main:app --reload
```

## Run Dashboard
```bash
python -m streamlit run <your_streamlit_app>.py
```

## Run Tests
```bash
pytest
```

## Technologies
Python, SQLite, FastAPI, Streamlit, Pandas, NumPy, Matplotlib
