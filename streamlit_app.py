import altair as alt
import pandas as pd
import streamlit as st

from io import StringIO
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

################# Loading & Layout ##########################
df_mergedState = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/merged_data_state.csv")
df_stackedState = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_state.csv")
df_stackedDiag = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis.csv")
#st.dataframe(df_mergedState)

### General Layout ###
st.write("## Mental Health Outcomes and Intervention Investigation")
tab1, tab2 = st.tabs(["Mental Health Outcomes", "Access to Psychiatric Care"])


################### Tab 1: Mental Health Outcomes #######################
with tab1:
   task1 = st.header("Mental Health Outcomes: Temporal Trends")
   

year = st.slider("Year", min_value=df["Year"].min(), max_value=df["Year"].max())
sex = st.radio("Sex", options = df["Sex"].unique())
countries = st.multiselect("Countries", options=df["Country"].unique(), default=[
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
])
cancer = st.selectbox("Cancer", options = df["Cancer"].unique())
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]
subset = df[(df["Year"] == year) & (df["Sex"] == sex) & (df["Country"].isin(countries)) & (df["Cancer"] == cancer)]
chart = alt.Chart(subset).mark_rect().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Country", title="Country"),
    color=alt.Color("Rate", title="Mortality Rate (log scale)", scale=alt.Scale(type='log', domain=[0.01, 1000], clamp=True)),
    tooltip=["Rate"],
).properties(
    title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)

### P2.5 ###
st.altair_chart(chart, use_container_width=True)
countries_in_subset = subset["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")


### BONUS ###
chart2 = alt.Chart(subset).mark_bar().encode(
    #x=alt.X("Age", sort=ages),
    y=alt.Y("Country", title="Country"),
    x=alt.Y("Pop", title="Population Size"),
    tooltip=["Pop"],
).properties(
    title=f"Population size for {'males' if sex == 'M' else 'females'} in {year}",
)
st.altair_chart(chart2, use_container_width=True)







