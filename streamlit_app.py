import altair as alt
import pandas as pd
import streamlit as st

from io import StringIO
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

def cluster_dataframe(df):
    aggregated_df = df.groupby('STATEFIP').agg({
        'YEAR': 'first',  
        'SPHSERVICE': lambda x: (x == 1).sum(),  
        'CMPSERVICE': lambda x: (x == 1).sum(),
        'OPISERVICE': lambda x: (x == 1).sum(),
        'RTCSERVICE': lambda x: (x == 1).sum(),
        'IJSSERVICE': lambda x: (x == 1).sum(),
        'MH1': lambda x: x.value_counts().get(1, 0), 
    }).reset_index()
    aggregated_df.rename(columns={'MH1': 'MH1_1'}, inplace=True)      
    for value in range(2, 15):  
        column_name = f'MH1_{value}'
        aggregated_df[column_name] = df['MH1'].apply(lambda x: 1 if x == value else 0)
    return aggregated_df

### Merge & Preprocess data ###
@st.cache_data
def load_data_MH():
    resp = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2021/MH-CLD-2021-datasets/MH-CLD-2021-DS0001/MH-CLD-2021-DS0001-bundles-with-study-info/MH-CLD-2021-DS0001-bndl-data-csv_v1.zip")
    myzip = ZipFile(BytesIO(resp.read()))  
    df_2021 = pd.read_csv(myzip.open('mhcld_puf_2021.csv'))
    resp_2020 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2020/MH-CLD-2020-datasets/MH-CLD-2020-DS0001/MH-CLD-2020-DS0001-bundles-with-study-info/MH-CLD-2020-DS0001-bndl-data-csv_v2.zip")
    myzip_2020 = ZipFile(BytesIO(resp_2020.read()))  
    df_2020 = pd.read_csv(myzip_2020.open('mhcld_puf_2020.csv'))
    resp_2019 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2019/MH-CLD-2019-datasets/MH-CLD-2019-DS0001/MH-CLD-2019-DS0001-bundles-with-study-info/MH-CLD-2019-DS0001-bndl-data-csv_v3.zip")
    myzip_2019 = ZipFile(BytesIO(resp_2019.read()))  
    df_2019 = pd.read_csv(myzip_2019.open('mhcld_puf_2019.csv'))
    resp_2018 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2018/MH-CLD-2018-datasets/MH-CLD-2018-DS0001/MH-CLD-2018-DS0001-bundles-with-study-info/MH-CLD-2018-DS0001-bndl-data-csv_v3.zip")
    myzip_2018 = ZipFile(BytesIO(resp_2018.read()))  
    df_2018 = pd.read_csv(myzip_2018.open('mhcld_puf_2018.csv'))
    resp_2017 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2017/MH-CLD-2017-datasets/MH-CLD-2017-DS0001/MH-CLD-2017-DS0001-bundles-with-study-info/MH-CLD-2017-DS0001-bndl-data-csv_v3.zip")
    myzip_2017 = ZipFile(BytesIO(resp_2017.read()))  
    df_2017 = pd.read_csv(myzip_2017.open('mhcld_puf_2017.csv'))
    resp_2016 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2016/MH-CLD-2016-datasets/MH-CLD-2016-DS0001/MH-CLD-2016-DS0001-bundles-with-study-info/MH-CLD-2016-DS0001-bndl-data-csv_v3.zip")
    myzip_2016 = ZipFile(BytesIO(resp_2016.read()))  
    df_2016 = pd.read_csv(myzip_2016.open('mhcld_puf_2016.csv'))
    resp_2015 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2015/MH-CLD-2015-datasets/MH-CLD-2015-DS0001/MH-CLD-2015-DS0001-bundles-with-study-info/MH-CLD-2015-DS0001-bndl-data-csv_v3.zip")
    myzip_2015 = ZipFile(BytesIO(resp_2015.read()))  
    df_2015 = pd.read_csv(myzip_2015.open('mhcld_puf_2015.csv'))
    resp_2014 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2014/MH-CLD-2014-datasets/MH-CLD-2014-DS0001/MH-CLD-2014-DS0001-bundles-with-study-info/MH-CLD-2014-DS0001-bndl-data-csv_v3.zip")
    myzip_2014 = ZipFile(BytesIO(resp_2014.read()))  
    df_2014 = pd.read_csv(myzip_2014.open('mhcld_puf_2014.csv'))
    resp_2013 = urlopen("https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/MH-CLD-2013/MH-CLD-2013-datasets/MH-CLD-2013-DS0001/MH-CLD-2013-DS0001-bundles-with-study-info/MH-CLD-2013-DS0001-bndl-data-csv_v3.zip")
    myzip_2013 = ZipFile(BytesIO(resp_2013.read()))  
    df_2013 = pd.read_csv(myzip_2013.open('mhcld_puf_2013.csv'))
    
    #dfs = [df_2021, df_2020, df_2019, df_2018, df_2017, df_2016, df_2015, df_2014, df_2013]
    #clustered_dfs = [cluster_dataframe(df) for df in dfs]
    return df_2013

df = load_data_MH()
st.dataframe(df)
sex = st.radio("GENDER", options = df["GENDER"].unique())

### P1.2 ###
st.write("## Age-specific cancer mortality rates")

### P2.1 ###
year = st.slider("Year", min_value=df["Year"].min(), max_value=df["Year"].max())

### P2.2 ###
sex = st.radio("Sex", options = df["Sex"].unique())

### P2.3 ###
countries = st.multiselect("Countries", options=df["Country"].unique(), default=[
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
])

### P2.4 ###
cancer = st.selectbox("Cancer", options = df["Cancer"].unique())

### P2.5 ###
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