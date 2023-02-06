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
st.title('Exploratory Data Analysis')
st.sidebar.success("Select a page above")

st.markdown("")

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_excel('https://storage.googleapis.com/forest_dashboard/big_merge_meteo_sat.xlsx')
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

danger = pd.DataFrame(data.groupby("PROCESS_SILVA")["PARCELLE"].nunique().reset_index())
danger["x"] = danger["PROCESS_SILVA"].apply(lambda x : str(x))

st.subheader('Different type of protection forest')
fig1 = px.bar(x="x", y = "PARCELLE", data_frame=danger, color="PROCESS_SILVA",
             labels={"PARCELLE":"Number of forests", "x":"Number of danger handled by the forest"},
             text_auto=True, width=600)
fig1.update_coloraxes(showscale=False)
st.plotly_chart(fig1, use_container_width=True)

st.subheader('Differents kind of forests')
tForest = pd.DataFrame(data.groupby(["TYPE_FORET305", "LFI"])["PARCELLE"].nunique().reset_index())
tForest["year"] = tForest["LFI"].apply(lambda x : "1983-1985" if x == "LFI1"
                                                            else "1993-1995" if x == "LFI2"
                                                            else "2004-2006" if x == "LFI3"
                                                            else "2009-2017")

tForest["type"] = tForest["TYPE_FORET305"].apply(lambda x : "Undetermined" if x == -1
                                                                    else "Inaccessible forest" if x == 1
                                                                    else "Bushy forest" if x == 2
                                                                    else "Forest area not always wooded" if x == 3
                                                                    else "Forest area temporarly not wooded" if x == 4
                                                                    else "Roads and banks" if x == 5
                                                                    else "Permanent afforestation" if x == 6
                                                                    else "Selves and plantings" if x == 7
                                                                    else "High forest" if x == 8
                                                                    else "Coppice with standards" if x == 9
                                                                    else "Selection cutting" if  x == 10
                                                                    else "Uneven-aged high stand" if x == 11
                                                                    else "Recruited/Supplied" if x == 12
                                                                    else "Pole" if x == 13
                                                                    else "Low Timber" if x == 14
                                                                    else "Medium Timber" if x == 15
                                                                    else "Strong Timber" if x == 16
                                                                    else "Incomplete record")

typeforest=st.selectbox("Sélectionnez un type de foret que vous voulez regarder", tForest["type"].sort_values().unique())
fig2 = px.bar(x="year", y = "PARCELLE", data_frame=tForest.loc[tForest["type"] == typeforest], color="year",
             labels={"PARCELLE":"Number of forests", "year":"Year"},
             text_auto=True, width=600)
fig2.update_coloraxes(showscale=False)
fig2.update(layout_showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.subheader('Repartition of decidious and coniferous trees')
# violin plot coniferous vs. deciduous forests
conileaf = pd.DataFrame(data.groupby(["FEU_RES", "LFI"])["PARCELLE"].nunique().reset_index())
conileaf["year"] = conileaf["LFI"].apply(lambda x : "1983-1985" if x == "LFI1"
                                                            else "1993-1995" if x == "LFI2"
                                                            else "2004-2006" if x == "LFI3"
                                                            else "2009-2017")

# if color argument is not string, grouped bar option does not work
conileaf["species"] = conileaf["FEU_RES"].apply(lambda x : "Coniferous" if x == 1
                                                                        else "Deciduous" if x == 2
                                                                        else "Not determined")

fig3 = px.bar(x="year", y = "PARCELLE", data_frame=conileaf, color="species",
             barmode = "group",
             labels={"PARCELLE":"Number of forests", "year":"Year", "species":"Dominant group of species"},
             text_auto=True, width=700)
fig3.update_coloraxes(showscale=False)
st.plotly_chart(fig3, use_container_width=True)

st.header("Forest state indicators")

col1, col2, col3 = st.columns(3)

with col1 : 
    st.subheader("Variation of basal area over time")
    surf_ter_dict={
    "Years" : ["1983-1985", "1993-1995", "2004-2006", "2009-2017"],
    "Mean basal area": [29.745839, 31.661357, 33.726300, 34.662601]
    }
    fig4=px.bar(surf_ter_dict, x="Years", y="Mean basal area", color="Years")
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

with col2 : 
    st.subheader("Variation of growth over time")
    accr_dict={
    "Years" : ["1993-1995", "2004-2006", "2009-2017"],
    "Mean growth": [80.709030, 84.831835, 67.498502]
    }
    fig5=px.bar(accr_dict, x="Years", y="Mean growth", color="Years")
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col3 :
    st.subheader("Variation of the regeneration coverage rate of protective forest over time")
    taux_couv_raj_dict={
    "Years" : ["1993-1995", "2004-2006", "2009-2017"],
    "Mean percentage of regeneration coverage rate": [25.481481, 23.829380, 21.032876]
    }
    fig6=px.bar(taux_couv_raj_dict, x="Years", y="Mean percentage of regeneration coverage rate", color="Years")
    fig6.update_layout(showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)