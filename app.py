import numpy as np
import pandas as pd
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import healper

# load data base
df = pd.read_csv('Data/covid_19_india.csv')
# pre-processing
df = df[df['State/UnionTerritory'] != 'Unassigned']
df = df[df['State/UnionTerritory'] != 'Cases being reassigned to states']
states_list = np.sort(df['State/UnionTerritory'].unique())
states_list = np.insert(states_list, 0, 'All India')
add_select_box = st.sidebar.selectbox("Select a State", states_list)
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 30))
end_date = st.sidebar.date_input("End Date", datetime.date(2021, 5, 16))

# total cases, cured, deaths, active_cases
total_cases = healper.return_total_cases(df, start_date, end_date, add_select_box, 'Confirmed')
cured = healper.return_total_cases(df, start_date, end_date, add_select_box, 'Cured')
deaths = healper.return_total_cases(df, start_date, end_date, add_select_box, 'Deaths')
active_cases = total_cases - (cured + deaths)

# daily state data
new_df1 = healper.return_daily_cases(df, start_date, end_date, add_select_box, 'Confirmed', 'Cases')
new_df2 = healper.return_daily_cases(df, start_date, end_date, add_select_box, 'Deaths', 'Deaths')
new_df3 = healper.return_daily_cases(df, start_date, end_date, add_select_box, 'Cured', 'Cured')

# Data of all india
total_confirmed_chart = healper.return_cases_chart(df, start_date, end_date, 'Confirmed')
total_cured_chart = healper.return_cases_chart(df, start_date, end_date, 'Cured')
total_deaths_chart = healper.return_cases_chart(df, start_date, end_date, 'Deaths')

# title
st.title("Covid India")

# make columns
col1, col2, col3, col4 = st.beta_columns(4)
with col1:
    st.title("Total Cases")
    st.header(total_cases)
with col2:
    st.title("Active Cases")
    st.header(active_cases)
with col3:
    st.title("Total Cured")
    st.header(cured)
with col4:
    st.title("Total Deaths")
    st.header(deaths)

# daily state graphs
fig1 = px.bar(new_df1, x=new_df1['Date'], y=new_df1['Cases'], title='Daily Cases of ' + str(add_select_box) + ' in given time interval')
st.plotly_chart(fig1)

fig2 = px.bar(new_df2, x=new_df2['Date'], y=new_df2['Deaths'], title='Daily Deaths of ' + str(add_select_box) + ' in given time interval')
st.plotly_chart(fig2)

st.header('Daily Cases vs Recovered of ' + str(add_select_box) + ' in given time interval')
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=new_df1['Date'], y=new_df1['Cases'], mode='lines', name='Daily Cases'))
fig3.add_trace(go.Scatter(x=new_df3['Date'], y=new_df3['Cured'], mode='lines', name='Daily Recovered'))
st.plotly_chart(fig3)

# make columns for pie charts of all india
col5, col6, col7 = st.beta_columns(3)
with col5:
    fig4 = px.pie(df, values=total_confirmed_chart['Confirmed'], names=total_confirmed_chart['State/UnionTerritory'], title='Total Cases of India in given time interval')
    st.plotly_chart(fig4)
with col6:
    fig6 = px.pie(df, values=total_cured_chart['Cured'], names=total_cured_chart['State/UnionTerritory'], title='Total Cured of India in given time interval')
    st.plotly_chart(fig6)
with col7:
    fig7 = px.pie(df, values=total_deaths_chart['Deaths'], names=total_deaths_chart['State/UnionTerritory'], title='Total Deaths of India in given time interval')
    st.plotly_chart(fig7)
