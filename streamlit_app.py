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

st.dataframe(df_stackedState.head())

### General Layout ###
st.write("## Mental Health Outcomes and Intervention Investigation")
tab1, tab2 = st.tabs(["Mental Health Outcomes", "Access to Psychiatric Care"])

################### Tab 1: Mental Health Outcomes #######################
with tab1:
   task1 = st.header("Mental Health Outcomes: Temporal Trends")
   states = st.multiselect("States", options=df_stackedState["STATEFIP"].unique())
   chart = alt.Chart(df_stackedState).mark_line().encode(
      x=alt.X("Year"),
      y=alt.Y("MH1_values_1", title="MH1_values_1"),
      #color=alt.Color("Rate", title="Mortality Rate (log scale)", scale=alt.Scale(type='log', domain=[0.01, 1000], clamp=True)),
      #tooltip=["Rate"],
      ).properties(
         title=f"Mental Health Disorder rates in {states}",
         )
   st.altair_chart(chart, use_container_width=True)

#year = st.slider("Year", min_value=df["Year"].min(), max_value=df["Year"].max())
#sex = st.radio("Sex", options = df["Sex"].unique())
#cancer = st.selectbox("Cancer", options = df["Cancer"].unique())
#ages = ["Age <5", "Age 5-14",]
#subset = df[(df["Year"] == year) & (df["Sex"] == sex) & (df["Country"].isin(countries)) & (df["Cancer"] == cancer)]














