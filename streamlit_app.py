import altair as alt
import pandas as pd
import streamlit as st

from io import StringIO
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

################# Loading & Layout ##########################
@st.cache_data
def load_data():
   #df_mergedState = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/merged_data_state.csv")
   df_stackedState = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_state.csv")
   df_stackedDiag = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis.csv")
   return df_stackedState, df_stackedDiag
df_stackedState, df_stackedDiag = load_data()

st.dataframe(df_stackedDiag.head())

### General Layout ###
st.write("## Mental Health Outcomes and Intervention Investigation")
tab1, tab2 = st.tabs(["Mental Health Outcomes", "Access to Psychiatric Care"])

################### Tab 1: Mental Health Outcomes #######################
with tab1:
   task1 = st.header("Mental Health Outcomes: Temporal Trends")
   diagnosis = st.multiselect("Mental Health Outcome", options=df_stackedDiag["MH1"].unique())
   #filtered_df = df_stackedDiag[df_stackedDiag["STATEFIP"].isin(diagnosis)]
   chart = alt.Chart(df_stackedDiag).mark_line().encode(
      x="YEAR",
      y=alt.Y("Population", title="Total Number of Patients"),
      color="MH1:N",  # Color by state if needed
      tooltip=["YEAR", "Population"]
      ).properties(
         title=f"Mental Health Disorder rates of {diagnosis}",
         )
   st.altair_chart(chart, use_container_width=True)



   ### Tab 1, Task 3 ###
   task3 = st.header("Explore influential factors of mental health outcomes")





#year = st.slider("Year", min_value=df["Year"].min(), max_value=df["Year"].max())
#sex = st.radio("Sex", options = df["Sex"].unique())
#ages = ["Age <5", "Age 5-14",]
#subset = df[(df["Year"] == year) & (df["Sex"] == sex) & (df["Country"].isin(countries)) & (df["Cancer"] == cancer)]


############## Tab 2: Mental Health Outcomes ##########################
with tab2:
   task1 = st.header("Access to Care: Temporal Trends")











