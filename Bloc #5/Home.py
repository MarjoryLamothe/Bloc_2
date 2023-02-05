import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk

st.set_page_config(
    page_title='Get Around Project',
    layout='wide'
)

### App
st.title('Welcome on the project dashboard')

st.sidebar.success('Select a page above')

st.markdown('Hello and welcome on this app\
Use the sidebar to access the dashboard for our analysis\
or make a prediction thanks to machine learning algorithms')

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_excel('')
    return data

data_load_state = st.text('Loading data, please wait...')
data = load_data(None)
data_load_state.text("")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)