import streamlit as st
import datetime
import time
import numpy as np
import pandas as pd
import xgboost as xgb
from joblib import load

COLUMNS_KEEP = ['station_id', 'month', 'day', 'hour', 'ctx_1', 'ctx_2', 'ctx_3', 'ctx_4', 'altitude', 'is_holiday', 'weekday',
                'weekend', 'season', 'avg_temp', 'acum_precipitation']
COLUMNS_DROP = ['post_code', 'lat', 'lon', 'capacity', 'max_temp', 'min_temp', 'avg_rel_humidity','avg_atm_pressure', 
                'global_solar_rad', 'avg_wind_direction', 'max_wind_speed', 'max_streak_wind_direction', 'avg_wind_speed']

st.set_page_config(
    page_title='Bike Availability prediction',
    page_icon='🚴‍♂️',
)

st.sidebar.markdown('Check out the source code [here](https://github.com/jadelaossa/bike-availability-prediction)')

# Function to load the necessary data
@st.cache_data
def load_data():
    bicing_status = (pd.read_parquet(r'data\processed\bicing_full.parquet')
                     .query('year == 2022')
                     .drop(columns=COLUMNS_DROP))
    bicing_info = pd.read_parquet(r'data\processed\bicing_info.parquet')
    calendar = pd.read_parquet(r'data\processed\calendar.parquet').query('year == 2023').drop(columns='year')
    
    return bicing_status, bicing_info, calendar

# Function to load the model and the pipeline that transform the features
@st.cache_resource
def load_model():
    model = load(r'models\model_app.joblib')
    pipeline = load(r'models\pipe_app.joblib')
    
    return model, pipeline

# Function to get current month, day, and hour+1
def get_time():
    current_datetime = datetime.datetime.now()
    
    month = current_datetime.month
    day = current_datetime.day
    hour = current_datetime.hour
    
    if hour == 23:
        hour_plus = 0
    else:
        hour_plus = hour + 1
    
    return month, day, hour_plus

    
# Loading datasets, models, and current time    
bicing, bicing_info, calendar = load_data()
model, bicing_pl = load_model()
month_default, day_default, hour_default = get_time()

def main():

    # Page title:
    st.title('🔮 Cycle-seeker')
    st.markdown('_DISCOVER BIKE AVAILABILITY BEFORE YOU GO! Because empty bike stations are no fun!_')
    st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

    # Select a bike station
    station = st.selectbox(':bike: Select a bike station:', options=np.unique(bicing_info['name']))
    st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

    # Select a date
    date = st.date_input(':date: Choose a date for your ride:', min_value=datetime.date(2023, 1, 1), max_value=datetime.date(2023, 12, 31))
    st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

    month = date.month
    day = date.day

    # Select an hour
    hour = st.select_slider(':watch: Select an hour for your ride:', options=(hour for hour in range(24)), value=hour_default)
    st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break
    
    # Select the temperature
    avg_temp = st.number_input(':thermometer: Enter the expected temperature:', min_value=-5, max_value=40, value=20)
    st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

    # Select if it is raining
    precipitation = st.radio(':rain_cloud: Is rain expected for the time selected?', options=('Yes...', 'NO!'), index=1)
    st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

    # Calculate accumulated precipitation based on user input
    if precipitation == 'Yes...':
        acum_precipitation = (bicing
                              .loc[(bicing['month'] == month) & (bicing['hour'] == hour), 'acum_precipitation']
                              .median())
    else:
        acum_precipitation = 0

    # PREDICT BUTTON!
    if st.button('Predict!'):
    
        # Calculate additional features for the model based on user's previous inputs
    
        # Calculate station_id and altitude based on the station name selected
        station_id = (bicing_info
                      .loc[bicing_info['name'] == station, 'station_id']
                      .values[0])
       
        altitude = (bicing_info
                    .loc[bicing_info['name'] == station, 'altitude']
                    .values[0])
    
        # Calculate weekday, weekend, public holiday and season based on the month a day selected
        weekday = date.isoweekday()
    
        weekend = (weekday > 5)
    
        is_holiday = (calendar
                      .loc[(calendar['month'] == month) & (calendar['day'] == day), 'is_holiday']
                      .values[0])

        season = (calendar
                  .loc[(calendar['month'] == month) & (calendar['day'] == day), 'season']
                  .values[0])
    
        # Calculate lag features based on the bike station, month and hour
        ctx_1 = (bicing
                 .loc[(bicing['station_id'] == station_id) & (bicing['month'] == month) & (bicing['hour'] == hour), 'ctx_1']
                 .median())

        ctx_2 = (bicing
                 .loc[(bicing['station_id'] == station_id) & (bicing['month'] == month) & (bicing['hour'] == hour), 'ctx_2']
                 .median())

        ctx_3 = (bicing
                 .loc[(bicing['station_id'] == station_id) & (bicing['month'] == month) & (bicing['hour'] == hour), 'ctx_3']
                 .median())

        ctx_4 = (bicing
                 .loc[(bicing['station_id'] == station_id) & (bicing['month'] == month) & (bicing['hour'] == hour), 'ctx_4']
                 .median())
    
        # Create a DataFrame with all the information retrieved
        sample_data = [station_id, month, day, hour, ctx_1, ctx_2, ctx_3, ctx_4, altitude, is_holiday, weekday, weekend, season, 
                       avg_temp, acum_precipitation]
    
        sample = (pd.DataFrame([sample_data], columns=COLUMNS_KEEP)
                  .astype({'station_id': 'category', 'hour': 'uint8','season': 'category', 'avg_temp': 'float32', 
                           'acum_precipitation': 'float32'}))
    
        # Transform the sample using the preprocessing pipeline
        X_sample = bicing_pl.transform(sample)
        
        # Subliminal message :D
        sub_placeholder = st.empty()
        sub_placeholder.text('The answer is 42')
        time.sleep(0.5)
        sub_placeholder.empty()
        
        # Make predictions using the loaded model
        y_pred = model.predict(X_sample)[0]
    
        # Display the predicition
        st.success(f'The predicted availability at the selected station is {y_pred * 100:.2f}%')

if __name__ == '__main__':
    main()