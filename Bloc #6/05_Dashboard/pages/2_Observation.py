import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk

### Config
st.set_page_config(
    page_title="Protection Forest Project",
    layout="wide"
)

### App
st.title('Observations')
st.sidebar.success("Select a page above")

st.markdown("")

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_excel('https://storage.googleapis.com/forest_dashboard/big_merge_meteo_sat.xlsx')
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data, please wait...')
data = load_data(None)
data_load_state.text("")

data_lfi1= data.loc[data['LFI']=='LFI1']
data_lfi4= data.loc[data['LFI']=='LFI4']
data_lfi4_lfi1= pd.concat([data_lfi1,data_lfi4], ignore_index=False)
data_lfi4_lfi1["SURF_TER_HA_DIFF"]=data_lfi4_lfi1.groupby("PARCELLE")['SURF_TER_HA'].diff()
data_lfi4_v2= data_lfi4_lfi1.loc[data_lfi4_lfi1['LFI']=='LFI4']
data_lfi4_v2["SURF_TER_HA_DIFF_pos"]=data_lfi4_v2["SURF_TER_HA_DIFF"].apply(lambda x: "Diminution" if x >= 0
else 'Augmentation')
data_lfi4_v2["Biomass volume"]=data_lfi4_v2["ACCR"].apply(lambda x: "Augmentation" if x >= 0
else 'Diminution')
group_1 = [1, 2]
group_2 = [3, 4]
group_3 = [5, 6]
data_lfi4_lfi1["Coverage rate percentage"] = data_lfi4_lfi1["TAUX_COUV_RAJ"].apply(lambda x: "Undetermined" if x == -1 
                                        else "Low" if x in group_1
                                        else "Medium" if x in group_2
                                        else "Intense" if x in group_3
                                        else x)
data["Campaign"] = data["LFI"].apply(lambda x: "1983-1985" if x == "LFI1" 
                                        else "1993-1995" if x == "LFI2"
                                        else "2004-2006" if x == "LFI3"
                                        else "2009-2017" if x == "LFI4"
                                        else x)

st.header("Basal area")
col1, col2 = st.columns(2)

with col1: 
    # Deuxieme Plot
    st.subheader('Per campaign')
    fig1 = px.scatter_mapbox(data, lat="LAT", lon="LON", color="Campaign", size="SURF_TER_HA", zoom=6, mapbox_style="carto-positron", category_orders={"Campagne": ["1983-1985", "1993-1995", "2004-2006", "2009-2017"]})
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

with col2:
    #Deuxième plot bis
    st.subheader('Evolution between the first and the last campaign to date')
    data_lfi4_v2["SURF_TER_HA_DIFF_value"] = data_lfi4_v2["SURF_TER_HA_DIFF"].apply(lambda x: abs(x))
    fig2 = px.scatter_mapbox(data_lfi4_v2, lat="LAT", lon="LON", size="SURF_TER_HA_DIFF_value", color='SURF_TER_HA_DIFF_pos', zoom=6, mapbox_style="carto-positron",category_orders={"SURF_TER_HA_DIFF_pos":["Augmentation", "Diminution"]})
    fig2.update_layout(
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
    st.plotly_chart(fig2, use_container_width=True)

st.header('Growth')
col3, col4 = st.columns(2)

with col3:
    ### Premier Plot
    st.subheader('Per campaign')
    data["UNIT_ACCR_pos"] = data["UNIT_ACCR"].apply(lambda x: x if x >= 0
    else 0) 
    fig3 = px.scatter_mapbox(data, lat="LAT", lon="LON", color="Campaign", size="SURF_TER_HA", zoom=6, mapbox_style="carto-positron", category_orders={"Campagne": ["1983-1985", "1993-1995", "2004-2006", "2009-2017"]})
    fig3.update_layout(
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
    st.plotly_chart(fig3, use_container_width=True)

with col4: 
    # Premier plot bis 
    st.subheader('Evolution between the first and the last campaign to date')
    data_lfi4_v2["ACCR_value"] = data_lfi4_v2["ACCR"].apply(lambda x: abs(x))
    fig4 = px.scatter_mapbox(data_lfi4_v2, lat="LAT", lon="LON", color='Biomass volume', zoom=6, mapbox_style="carto-positron")
    fig4.update_layout(
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
    st.plotly_chart(fig4, use_container_width=True)

st.header("Regeneration coverage rate")
col5, col6 = st.columns(2)

with col5: 
    #Troisième Plot
    st.subheader('Per campaign')
    data["TAUX_COUV_RAJ_pos"] = data["TAUX_COUV_RAJ"].apply(lambda x: x if x >= 0 else 0) 
    fig5 = px.scatter_mapbox(data, lat="LAT", lon="LON", color="Campaign", size="SURF_TER_HA", zoom=6, mapbox_style="carto-positron", category_orders={"Campagne": ["1983-1985", "1993-1995", "2004-2006", "2009-2017"]})
    fig5.update_layout(
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
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    #Troisièmeplot bis
    st.subheader('Evolution between the first and the last campaign to date')
    fig6 = px.scatter_mapbox(data_lfi4_lfi1, lat="LAT", lon="LON", color="Coverage rate percentage", zoom=6, category_orders={"Pourcentage du Taux de couverture":["Faible", "Moyen", "Intense"]})
    fig6.update_layout(
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
    st.plotly_chart(fig6, use_container_width=True)
