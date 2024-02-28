import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

from io import StringIO
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

################# Loading & Layout ##########################
st.set_page_config(layout="wide")
@st.cache_data
def load_data():
   df_stackedState = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_state.csv")
   df_stackedDiag = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis.csv")
   return df_stackedState, df_stackedDiag
df_stackedState, df_stackedDiag = load_data()
df_stackedDiag.rename(columns={'MH1': 'Mental Health Outcomes'}, inplace=True)
df_stackedDiag = df_stackedDiag[df_stackedDiag['Mental Health Outcomes'] != 'Missing']
df_stackedState = df_stackedState[df_stackedState['CODE'] != 99]
### Layout ###
st.title("Mental Health Outcomes and Intervention Investigation")
tab1, tab2 = st.tabs(["Mental Health Outcomes", "Access to Mental Health Services"])


################### Tab 1: Mental Health Outcomes #######################
with tab1:
    ### Tab 1, Task 1 ###
   task1 = st.header("Temporal Trends")
   diagnosis = st.multiselect(" ", options=df_stackedDiag["Mental Health Outcomes"].unique(), 
                              default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'])
   filtered_df1BAR = df_stackedDiag[df_stackedDiag["Mental Health Outcomes"].isin(diagnosis)]
   filtered_df = filtered_df1BAR
   filtered_df['YEAR'] = filtered_df1BAR['YEAR'].astype(str)
   chart1_1 = alt.Chart(filtered_df).mark_line().encode(
      x=alt.X("YEAR", axis=alt.Axis(format='', title='Year', labelAngle=0)),
      y=alt.Y("Population", title="Total Number of Patients"),
      color="Mental Health Outcomes:N",  # Color by state if needed
      tooltip=["YEAR", "Population"]
      ).properties(
         title=f"Mental Health Disorder rates of {', '.join(diagnosis)}",
         )
   st.altair_chart(chart1_1, use_container_width=True)
   chart1_1bar = alt.Chart(filtered_df1BAR).mark_bar().encode(
       x=alt.X("YEAR:O", title="Year"),
       y=alt.Y("Population", title="Patients"),
       color='Mental Health Outcomes:N',order=alt.Order('Mental Health Outcomes:O'),
       ).properties(
          title=f"Mental Health Disorder proportion",
          )
   st.altair_chart(chart1_1bar, use_container_width=True)

   ### Tab 1, Task 2 ###
   task2 = st.header("Geospatial Pattern")
   year = st.slider("Year", min_value=df_stackedState["YEAR"].min(), max_value=df_stackedState["YEAR"].max())
   diag = st.selectbox("Mental Health Outcome", options = df_stackedDiag["Mental Health Outcomes"].unique())
   source = alt.topo_feature(data.us_10m.url, 'states')
   width = 900
   height  = 600
   background = alt.Chart(source).mark_geoshape(fill='#aaa', stroke='white').properties(width=width, height=height).project('albersUsa')
   filtered_df12 = df_stackedState[df_stackedState["YEAR"]==year][['STATEFIP', 'YEAR', 'POPULATION', 'CODE', diag]]
   #st.dataframe(filtered_df12)
   rate_scale = alt.Scale(domain=[filtered_df12[diag].min(), filtered_df12[diag].max()], scheme='oranges')
   rate_color = alt.Color(field="Individuals with Disorder", type="quantitative", scale=rate_scale)
   #st.write(rate_color)
   chart1_2 = alt.Chart(source).mark_geoshape().encode(
      color = rate_color,
      ).transform_lookup(
         lookup='id',
         from_=alt.LookupData(filtered_df12, 'CODE', [diag])
      ).properties(
         width=width, height=height,
         title=f'Proportion of Individuals with {diag} in {year}',
         ).project('albersUsa')
   st.altair_chart(background+chart1_2, use_container_width=True)

   ### Tab 1, Task 3 ###
   task3 = st.header("Explore influential factors of mental health outcomes")





############## Tab 2: Access to Psychiatric Care ##########################
with tab2:
   task1 = st.header("Temporal Trends")
   #calculate care accessing proportion
   df_stackedDiag['Prop']=round(df_stackedDiag['SMHAserviceAccess']/df_stackedDiag['Population'],3)
   #create diagnosis selection tab 
   diagnosis = st.multiselect('Mental Health Disorder', options=df_stackedDiag['Mental Health Outcomes'].unique(), 
                              default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'])
   subset1=df_stackedDiag[df_stackedDiag['Mental Health Outcomes'].isin(diagnosis)]
   # create bubble chart
   chart2_1 = alt.Chart(subset1).mark_line().encode(
      x=alt.X('YEAR:O', axis=alt.Axis(format='', title='Year', labelAngle=0)),
      y=alt.Y('Prop:Q', title='Proportion of Patients Received Services',scale=alt.Scale(domain=(0.85,1))),
      color=alt.Color('Mental Health Outcomes:N',title='Mental Health Disorder'),
      tooltip=['YEAR','Prop']
      ).properties(
         title='Proportion of Patients Received Services from Sate Mental Health Agency (SMHA) Funded Community-Based Program',
         )
   st.altair_chart(chart2_1, use_container_width=True)

   task2 = st.header("Factors Impacting Access to Mental Health Services")
   



