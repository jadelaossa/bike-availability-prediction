import streamlit as st

st.set_page_config(
    page_title='Bike Availability prediction',
    page_icon='🚴‍♂️',
)

st.sidebar.markdown('Check out the source code [here](https://github.com/jadelaossa/bike-availability-prediction)')

st.title('🚴‍♂️ Bike Availability prediction')
st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

st.markdown('This project serves as the final project for the Postgraduate Course in [Data Science and Machine Learning](https://datascience.ub.edu/course/postgraduate-dsml)\
            at the University of Barcelona. It was developed as part of the curriculum to demonstrate the application of machine\
            learning techniques in solving real-world problems. The project focuses on predicting the availability of docked bikes\
            at various bike-sharing systems in Barcelona city, utilizing datasets from the Barcelona Open Data platform.')
st.markdown('The project focuses on predicting the availability of docked bikes at various bike-sharing systems in Barcelona city,\
            utilizing datasets from the Barcelona Open Data platform.')
st.markdown('<br>', unsafe_allow_html=True)  # Insert a line break

st.markdown('## Contributors')
st.markdown('This project was developed by:')
st.markdown('- Dorleta Orúe-Echevarría Iglesias')
st.markdown('- María Alejandra Zalles Hoyos')
st.markdown('- Patricia Merchán Guedea')
st.markdown('- Javier Alejandro de la Ossa Fernández')
