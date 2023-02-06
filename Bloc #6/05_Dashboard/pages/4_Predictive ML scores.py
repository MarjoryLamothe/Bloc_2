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
st.title('Predictive machine learning')
st.sidebar.success("Select a page above")

st.markdown("")

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    score_model = pd.read_excel('https://storage.googleapis.com/forest_dashboard/score_total.xlsx')
    return score_model

data_load_state = st.text('Loading data, please wait...')
score_model = load_data(None)
data_load_state.text("")


score_model["Score"] = round(score_model["Score"], 2)
score_model_pred = score_model.loc[score_model["Mode"] == "Predictive",:]

score_model_pred['simple_name'] = score_model_pred['Model'].apply(lambda x: "RR" if x == "Ridge Regression"
else "XGBoost" if x == "XGBoost"
else "DL_dense" if x == "Deep Learning (Multi-Layers Denses)"
else "AT" if x == "Average Trend"
else "CT" if x == "Constant Trend"
else "DL_gru" if x == "Deep Learning (Multi-Layers GRU for time series)"
else "DL_gru_mld" if x == "Deep Learning (Multi-Layers GRU for time series + MLD parallele)"
else "RC" if x == "Ridge Classifier"
else "XGBoost" if x == "XG_Boost"
else x)


st.header("Predictive machine learning scores for basal area")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(x="simple_name", y = "Score", data_frame=score_model_pred.loc[score_model_pred["Target"] == "Basal Area (m2 / ha)",:],
             labels={"simple_name":"model tested", "Score":"determination coefficient"},
             hover_data=['Score'], color='Score', color_continuous_scale='Spectral',
             text_auto=True, width=1000)
    fig1.update_coloraxes(showscale=False)
    fig1.update(layout_showlegend=False)
    fig1.update_yaxes(range=[0,1])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown('Correspondances : RR = Rigde Regression')
    st.markdown('XGBoost = XGBoost')
    st.markdown('DL_dense = Deep Learning (Multi-Layers Denses)')
    st.markdown('AT = Average Trend')
    st.markdown('CT = Constant Trend (Assumes no change since previous campaign)')
    st.markdown('DL_gru = Deep Learning (Multi-Layers GRU for time series)')
    st.markdown('DL_gru_mld = Deep Learning (Multi-Layers GRU for time series + MLD parallele)')
    st.markdown('RC = Ridge Classifier')


st.header("Predictive machine learning scores for growth")
col3, col4 = st.columns(2)
with col3: 
    fig2 = px.bar(x="simple_name", y = "Score", data_frame=score_model_pred.loc[score_model_pred["Target"] == "Growth",:],
             labels={"simple_name":"model tested", "Score":"determination coefficient"},
             category_orders={"simple_name": ["LR", "Lasso", "DT", "RF", "HGBr"]},
             hover_data=['Score'], color='Score', color_continuous_scale='Spectral',
             text_auto=True, width=1000)
    fig2.update_coloraxes(showscale=False)
    fig2.update(layout_showlegend=False)
    fig2.update_yaxes(range=[0,1])
    st.plotly_chart(fig2, use_container_width=True)

with col4: 
    st.markdown('Correspondances : RR = Rigde Regression')
    st.markdown('DL_dense = Deep Learning (Multi-Layers Denses)')
    st.markdown('DL_gru = Deep Learning (Multi-Layers GRU for time series)')
    st.markdown('DL_gru_mld = Deep Learning (Multi-Layers GRU for time series + MLD parallele)')


st.header("Predictive machine learning scores for regeneration coverage rate")
col5, col6 =st.columns(2)
with col5:
    fig3 = px.bar(x="simple_name", y = "Score", data_frame=score_model_pred.loc[score_model_pred["Target"] == "Regeneration coverate rate",:],
             labels={"simple_name":"model tested", "Score":"Performance"},
             hover_data=['Score'], color='Score', color_continuous_scale='Spectral',
             text_auto=True, width=1000)
    fig3.update_coloraxes(showscale=False)
    fig3.update(layout_showlegend=False)
    fig3.update_yaxes(range=[0,1])
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    st.markdown('Correspondances : RC = Ridge Classifier')
    st.markdown('AT = Average Trend')
    st.markdown('CT = Constant Trend (Assumes no change since previous campaign)')
    st.markdown('XGBoost = XGBoost')
    st.markdown('DL_dense = Deep Learning (Multi-Layers Denses)')
    st.markdown('DL_gru = Deep Learning (Multi-Layers GRU for time series)')
    st.markdown('DL_gru_mld = Deep Learning (Multi-Layers GRU for time series + MLD parallele)')