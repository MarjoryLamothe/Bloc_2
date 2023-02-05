import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk

### Config
st.set_page_config(
    page_title="Get Around Project",
    layout="wide"
)

### App
st.title('Data Analysis')
st.sidebar.success("Select a page above")

st.markdown("")

@st.cache(allow_output_mutation=True)
def load_data(nrows):
    dataset = pd.read_excel()
    return dataset

data_load_state = st.text('Loading data, please wait...')
dataset = load_data(None)
data_load_state.text("")

dataset["delay_category"] = dataset["delay_at_checkout_in_minutes"].apply(lambda x: "No delay" if x < 0 
                                        else "Less than 15 minutes" if x >= 0 and x < 15
                                        else "15 to 30 minutes" if x >= 15 and x < 30
                                        else "30 minutes to 1 hours" if x >= 30 and x < 60
                                        else "1 to 2 hours" if x >= 60 and x < 120 
                                        else "2 to 3 hours" if x >= 120 and x < 180 
                                        else "3 to 4 hours" if x >= 180 and x < 240 
                                        else "4 to 5 hours" if x >= 240 and x < 300 
                                        else "5 to 6 hours" if x >= 300 and x < 360 
                                        else "6 to 12 hours" if x >= 360 and x < 720 
                                        else "12 hours to a day" if x >= 720 and x < 1440 
                                        else "1 to 5 days" if x >= 1440 and x < 7200
                                        else "5 to 10 days" if x >= 7200 and x < 14400 
                                        else "10 to 15 days" if x >= 14400 and x < 21600 
                                        else "More than 15 days" if x > 21600
                                        else x)

delay=pd.DataFrame(dataset["delay_category"].value_counts())

late_drivers = 100*len(dataset[dataset['time_delta_with_previous_rental_in_minutes']>0])/dataset.shape[0]
drivers_not_late=100-late_drivers
percentage_late_next_checkin={
    'Category' : ['Late for next check-in', 'Not Late for next chek-in'],
    'Percent' : [late_drivers, drivers_not_late]
}

state_late=pd.DataFrame(dataset['state'].loc[dataset['delay_category'] != 'No delay'])
cancelation_late=100*len(state_late[state_late['state']=='canceled'])/state_late.shape[0]
late_not_canceled=100-cancelation_late
percentage_cancelation_when_late={
    'Category' : ['Canceled', 'Not canceled'],
    'Percent' : [cancelation_late, late_not_canceled]
}

state_not_late=pd.DataFrame(dataset['state'].loc[dataset['delay_category'] == 'No delay'])
cancelation_not_late=100*len(state_not_late[state_not_late['state']=='canceled'])/state_not_late.shape[0]
not_late_not_canceled=100-cancelation_not_late
percentage_cancelation_when_not_late={
    'Category' : ['Canceled', 'Not canceled'],
    'Percent' : [cancelation_not_late, not_late_not_canceled]
}

st.header('How many rentals would be affected by the feature depending on the threshold and scope we choose?')

fig1 = px.bar(delay, y='delay_category', color='delay_category')
st.plotly_chart(fig1, use_container_width=True)

st.header('How often are drivers late for the next check-in?')

fig2 = px.pie(percentage_late_next_checkin, values='Percent', names='Category')
st.plotly_chart(fig2, use_container_width=True)

st.header('How does it impact the next driver?')

col1, col2 = st.columns(2)

with col1:
    st.subheader()
    fig3 = px.pie(percentage_cancelation_when_late, values='Percent', names='Category')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader()
    fig4 = px.pie(percentage_cancelation_when_not_late, values='Percent', names='Category')
    st.plotly_chart(fig4, use_container_width=True)

st.header('How many problematic cases will it solve depending on the chosen threshold and scope?')