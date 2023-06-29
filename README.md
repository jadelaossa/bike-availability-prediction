# Bike Availability Prediction


This project serves as the final project for the Postgraduate Course in [Data Science and Machine Learning](https://datascience.ub.edu/course/postgraduate-dsml) at the University of Barcelona. It was developed as part of the curriculum to demonstrate the application of machine learning techniques in solving real-world problems.

The project focuses on predicting the availability of docked bikes at various bike-sharing systems in Barcelona city, utilizing datasets from the Barcelona Open Data platform.

## Structure of the repository

The directory structure of your new project looks like this: 

```
├── README.md
│
├── app.py                  <- Script to run a web app created with Streamlit.
│
├── data
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
│
├── models                  <- Trained and serialized models.
│
├── notebooks               <- Jupyter notebooks.
│
├── reports            
│   └── figures             <- Generated graphics and figures.
│
├── requirements.txt
│
├── setup.py                <- Makes project pip installable (pip install -e .).
│ 
└── src                     <- Source code for use in this project.
    ├── __init__.py  
    │
    ├── components          <- Scripts to download or generate data.
    │   ├── __init__.py
    │   └── data_collection.py
    │
    ├── pipeline            <- Script to make predictions from metadata_sample_submission.csv file.
    │    ├── __init__.py
    │    ├── artifacts              <- Model predictions.
    │    └── make_prediction.py
    │
    └── utils.py            <- Helper functions used in the project.
```
## Quick-start

To set up the project, follow these steps:

- Clone this repo:

```bash
git clone https://github.com/jadelaossa/bike-availability-prediction.git
```
- Create and activate a virtual enviroment:

```bash
conda create -n bike-availability-prediction python=3.9
conda activate bike-availability-prediction
```

- Install the requiered dependencies:

```bash
pip install -r requirements.txt
```

## Data Source

The data used in this project can be obtained from the [Open Data BCN](https://opendata-ajuntament.barcelona.cat/en) platform. Follow the links below to access and download the required datasets:

1. Bicing station status can be found [here](https://opendata-ajuntament.barcelona.cat/data/en/dataset/estat-estacions-bicing).
2. Bicing stations information can be found [here](https://opendata-ajuntament.barcelona.cat/data/en/dataset/informacio-estacions-bicing).
3. Statistical resources of the meteorological stations of Barcelona can be found [here](https://opendata-ajuntament.barcelona.cat/data/en/dataset/mesures-estacions-meteorologiques).

## Results

In this project, we applied several machine learning algorithms to predict bike availability. The best performing model is a combination of an XGBoost model and a neural network (NN), where we employed an ensemble technique. The ensemble model leverages the predictions from both the XGBoost model and the NN and calculates the average of these predictions to obtain the final prediction.

## Contributors

This project was developed by:

- Dorleta Orúe-Echeverría Iglesias
- María Alejandra Zalles Hoyos
- Patricia Merchán Guedea
- Javier Alejandro de la Ossa Fernández

