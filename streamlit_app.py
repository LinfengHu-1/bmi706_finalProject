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

### Layout ###
st.title("Mental Health Outcomes and Intervention Investigation")
tab1, tab2 = st.tabs(["Mental Health Outcomes", "Access to Psychiatric Care"])
################### Tab 1: Mental Health Outcomes #######################
with tab1:
    ### Tab 1, Task 1 ###
   task1 = st.header("Temporal Trends")
   diagnosis = st.multiselect(" ", options=df_stackedDiag["Mental Health Outcomes"].unique(), 
                              default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'])
   filtered_df = df_stackedDiag[df_stackedDiag["Mental Health Outcomes"].isin(diagnosis)]
   filtered_df['YEAR'] = filtered_df['YEAR'].astype(str)
   chart1_1 = alt.Chart(filtered_df).mark_line().encode(
      x=alt.X("YEAR", axis=alt.Axis(format='', title='Year', labelAngle=0)),
      y=alt.Y("Population", title="Total Number of Patients"),
      color="Mental Health Outcomes:N",  # Color by state if needed
      tooltip=["YEAR", "Population"]
      ).properties(
         title=f"Mental Health Disorder rates of {', '.join(diagnosis)}",
         )
   st.altair_chart(chart1_1, use_container_width=True)
   chart1_1bar = alt.Chart(df_stackedDiag).mark_bar().encode(
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
   project = 'albers'
   # gray background of all states in the US
   background = alt.Chart(source).mark_geoshape(
      fill='#aaa', stroke='white').properties(width=width, height=height).project(project)
   chart_base = alt.Chart(source).properties(
      width=width, height=height).project(project).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df_stackedState, "state-code"),
    )
   rate_scale = alt.Scale(domain=[df_stackedState['ADHD'].min(), df_stackedState['ADHD'].max()], scheme='oranges')
   rate_color = alt.Color(field="Rate", type="quantitative", scale=rate_scale)
   chart1_2 = chart_base.mark_geoshape().encode(
      color=rate_color, 
      #tooltip=['Country:N', 'Rate:Q'],
      ).properties(
        title=f'Proportion of Individuals with {diag} in {year}'
        )
   st.altair_chart(chart1_2, use_container_width=True)


   ### Tab 1, Task 3 ###
   task3 = st.header("Explore influential factors of mental health outcomes")





#sex = st.radio("Sex", options = df["Sex"].unique())
#ages = ["Age <5", "Age 5-14",]
#subset = df[(df["Year"] == year) & (df["Sex"] == sex) & (df["Country"].isin(countries)) & (df["Cancer"] == cancer)]


############## Tab 2: Mental Health Outcomes ##########################
with tab2:
   task1 = st.header("Temporal Trends")











