# PondRecharge
Computational framework for pond-based groundwater recharge estimation using multi-source geospatial data and machine learning models (GB, XGBoost, Random Forest) in the Ramganga Basin, India. Includes data processing workflows, model implementation, and recharge prediction outputs.

# PondRecharge

Computational framework for pond-based groundwater recharge estimation using multi-source geospatial data and machine learning models in the Ramganga Basin, India.

## Overview
This repository contains the code, sample data, and processing workflow used to support the manuscript:

**A Computational Framework for Basin-Scale Pond Recharge Estimation Using Multi-Source Geospatial Data**

The workflow combines:
- Google Earth Engine (GEE) scripts for pond inventory generation
- Python scripts for preprocessing, visualization, and machine learning
- geospatial factor tables and sample inputs for a minimal test run

## Repository Structure

- `GEE_scripts/`  
  Google Earth Engine scripts used for pond extraction and pond inventory preparation.

- `python_scripts/scripts/`  
  Python scripts for raster preprocessing, KDE analysis, correlation analysis, and machine learning recharge modeling.

- `Recharge_Factors/`  
  Processed geospatial attribute tables used as predictor inputs.

- `Pond_Points/`  
  Pond point datasets used in the workflow.

- `Pond_Shape/`  
  Pond polygon / shape datasets used in the workflow.

- `example_data/`  
  Minimal working example dataset for test execution.

- `example_output/`  
  Example results generated from the test workflow.

## Software Requirements

This repository was tested with:
- Python 3.10+
- Google Earth Engine
- pandas
- numpy
- matplotlib
- scikit-learn
- xgboost
- rasterio
- geopandas

Install dependencies using:

```bash
pip install -r requirements.txt
