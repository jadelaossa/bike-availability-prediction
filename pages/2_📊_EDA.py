import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static


COLUMNS_DROP = ['post_code', 'capacity', 'max_temp', 'min_temp', 'avg_rel_humidity','avg_atm_pressure', 'global_solar_rad', 
                'avg_wind_direction', 'max_wind_speed', 'max_streak_wind_direction', 'avg_wind_speed']

st.set_page_config(
    page_title='Bike Availability prediction',
    page_icon='🚴‍♂️',
)

st.sidebar.markdown('Check out the source code [here](https://github.com/jadelaossa/bike-availability-prediction)')

# Function to load the necessary data
@st.cache_data
def load_data():
    bicing_status = (pd.read_parquet(r'data\processed\bicing_full.parquet')
                     .query('year != 2023')
                     .astype({'weekend': 'uint8', 'is_holiday': 'uint8'})
                     .drop(columns=COLUMNS_DROP))
    
    return bicing_status[::20]

# Function to load the necessary data
bicing = load_data()

# Page title:
st.title('📊 Exploratory Data Analysis (EDA)')
st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

# Printing out the dataframe:
st.dataframe(bicing.sample(25), use_container_width=True)
st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

# First chart: Availability for month by year
st.markdown('### A) Availability for month by year')
st.markdown('The availability by month and year shows the effect of the COVID between abril and june 2020. However, those values are not\
so different from the values in 2019.')

c0 = bicing.select_dtypes('number').groupby(['year', 'month']).mean().reset_index()

fig0 = px.line(c0, x='month', y='percentage_docks_available', color='year', symbol='year', 
               labels={'month': 'Month','percentage_docks_available': 'Percentage of available docks'}, title='Monthly wise yearly availability distribution')

st.plotly_chart(fig0, use_container_width=True)

# Second chart: Availability for hour by season
st.markdown('### B) Availability for hour by season')
st.markdown('The availability by hour in each season shows a similar pattern, availability is lower between 20 pm and 5 am, and increases\
during the day, with maximum values between 3 pm and 6 pm. For the same hour, availavility is lower in spring and higher in autumn.')

c1 = bicing.groupby(['season', 'hour']).mean().reset_index()

fig1 = px.line(c1, x='hour', y='percentage_docks_available', color='season', symbol='season', 
               labels={'hour':'Hour', 'percentage_docks_available': 'Percentage of available docks'}, title='Season wise hourly availability distribution')

st.plotly_chart(fig1, use_container_width=True)

# Third chart: Availability for hour by month
st.markdown('### C) Availability for hour by month')
st.markdown('For the same hour, availavility is lower in April and May and higher in August and October.')

c2 = bicing.select_dtypes('number').groupby(['month', 'hour']).mean().reset_index()

fig2 = px.line(c2, x='hour', y='percentage_docks_available', color='month', symbol='month', 
               labels={'hour': 'Hour','percentage_docks_available': 'Percentage of available docks'}, title='Month wise hourly availability distribution')

st.plotly_chart(fig2, use_container_width=True)

# Forth chart: Availability for hour by weekday
st.markdown('### D) Availability for hour by weekday')
st.markdown('There are differences in the availability for weekdays. From Monday to Friday availability shows the same pattern, increases at 5-6 am while at\
Saturdays and Sundays the rise in availability is more progressive and does not reach the Monday to Friday availability values until 9 am.\
From Friday to Sunday the availability between 5 pm and 7 pm is lower than for the rest of the days.')

c3 = bicing.select_dtypes('number').groupby(['month', 'weekend']).mean().reset_index()

fig3 = px.bar(c3, x='weekend', y='percentage_docks_available', color='month', barmode='group', 
              labels={'percentage_docks_available': 'Percentage of available docks'}, title='Weekday wise hourly availability distribution')

st.plotly_chart(fig3, use_container_width=True)

# Fifth chart: Availability for rainy days
st.markdown('### E) Availability for rainy days')
st.markdown('The availability for rainy days is sligtly lower than for dry days.')

c4 = np.where(bicing['acum_precipitation'] > 0, 1, 0)
bicing['is_rain'] = c4

c4 = bicing.select_dtypes('number').groupby(['is_rain']).mean().reset_index()

fig4 = px.bar(c4, x='is_rain', y='percentage_docks_available', labels={'is_rain': 'Rainy day', 'percentage_docks_available': 'Percentage of available docks'}, 
              title='Availability distribution function of rainy days')

st.plotly_chart(fig4, use_container_width=True)

# Sixth chart: Availability during holidays
st.markdown('### F) Availability during holidays')
st.markdown('The availability for holiday days is sligtly lower.')

c5 = bicing.select_dtypes('number').groupby(['is_holiday']).mean().reset_index()

fig5 = px.bar(c5, x='is_holiday', y='percentage_docks_available', labels={'is_holiday': 'Holiday', 'percentage_docks_available': 'Percentage of available docks'}, 
              title='Availability distribution function of Holdays')

st.plotly_chart(fig5, use_container_width=True)

# Seventh chart: Mean availability distribution
def create_folium_map():
    c6 = bicing.select_dtypes('number').groupby(['station_id'], as_index=False).mean()

    bicing_heatmap = pd.DataFrame({'lat': c6['lat'], 'lon': c6['lon'], 'average': c6['percentage_docks_available']})
    bicing_heatmap.dropna(inplace=True)
    bicing_heatmap=bicing_heatmap.astype(np.float64)

    map1 = folium.Map(location=[41.401205, 2.155007], zoom_start=13)
    HeatMap(bicing_heatmap, min_opacity=0.4, blur=18).add_to(folium.FeatureGroup(name='Heat Map').add_to(map1))
    folium.LayerControl().add_to(map1)
    
    return map1

st.markdown('### G) Mean availability distribution')
st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

map1 = create_folium_map()
folium_static(map1)

st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

# Eigth chart: Correlation matrix heatmap
st.markdown('### H) Correlation matrix')

bicing_corr = bicing.select_dtypes('number').corr()

fig6 = go.Figure()

fig6.add_trace(go.Heatmap(x=bicing_corr.columns,
                          y=bicing_corr.index,
                          z=np.array(bicing_corr),
                          colorscale=px.colors.diverging.RdBu,
                          zmin=-1,
                          zmax=1)
               )

st.plotly_chart(fig6, use_container_width=True)