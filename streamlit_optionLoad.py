import altair as alt
import pandas as pd
import streamlit as st

from io import StringIO
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


##### Option to individually view dataframe ####
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

    return df_2013
#df_2013 = load_data_MH()
