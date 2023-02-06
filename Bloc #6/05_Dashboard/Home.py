import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk

st.set_page_config(
    page_title="Protection Forest Project",
    layout="wide"
)

### App
st.title("Welcome to our dashboard 👋")
 
st.sidebar.success("Select a page above")

st.markdown("Hello and welcome to our dashboard for our projet on Protection Forest in Switzerland. \
Here, you will be able to track the evolution of the protection forests from 1984 to 2017.")

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_excel('https://storage.googleapis.com/forest_dashboard/big_merge_meteo_sat.xlsx')
    return data

data_load_state = st.text('Loading data, please wait...')
data = load_data(None)
data_load_state.text("")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Map of our forest plot')

data["species"] = data["FEU_RES"].apply(lambda x : "Coniferous" if x == 1
                                                                        else "Deciduous" if x == 2
                                                                        else "Not determined")
fig1 = px.scatter_mapbox(data, lat="LAT", lon="LON", zoom=6, color="species")
fig1.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
st.plotly_chart(fig1, use_container_width=True)