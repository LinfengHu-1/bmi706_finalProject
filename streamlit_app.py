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
   df_stackedAccess = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_access_diagnosis.csv")
   return df_stackedState, df_stackedDiag, df_stackedAccess
df_stackedState, df_stackedDiag, df_stackedAccess= load_data()
df_stackedDiag.rename(columns={'MH1': 'Mental Health Outcomes'}, inplace=True)
df_stackedDiag = df_stackedDiag[df_stackedDiag['Mental Health Outcomes'] != 'Missing']
df_stackedState = df_stackedState[df_stackedState['CODE'] != 99]
df_stackedAccess.rename(columns={'MH1': 'Mental Health Disorder'}, inplace=True)
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
   ### Tab 2, Task 1 ###
   task1 = st.header("Temporal Trends")
   #calculate care accessing proportion
   df_stackedDiag['Prop']=round(df_stackedDiag['SMHAserviceAccess']/df_stackedDiag['Population'],3)
   #create diagnosis selection tab 
   diagnosis_tab2_1 = st.multiselect('Mental Health Disorder', options=df_stackedDiag['Mental Health Outcomes'].unique(), 
                              default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'])
   subset1=df_stackedDiag[df_stackedDiag['Mental Health Outcomes'].isin(diagnosis_tab2_1)]
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

   ### Tab 2, Task 2 ###
   task2 = st.header("Factors Impacting Access to Mental Health Services")
   #keep Service==1
   df_stackedAccess_t=df_stackedAccess[df_stackedAccess['CMPSERVICE']==1]
   df_stackedAccess_t.rename(columns={'Male': 'Male_n'}, inplace=True)
   df_stackedAccess_t.rename(columns={'White': 'White_n'}, inplace=True)
   df_stackedAccess_t.rename(columns={'Black': 'Black_n'}, inplace=True)
   #create diagnosis selection tab 
   diagnosis_tab2_2 = st.multiselect('Mental Health Disorder', options=df_stackedAccess_t['Mental Health Disorder'].unique(), 
                              default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'])
   ### Gender & Marital Status
   #calculate care accessing proportion
   ##gender
   df_stackedAccess_t['Male']=round(df_stackedAccess_t['Male_n']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['Female']=round(1-df_stackedAccess_t['Male'],3)
   df_gender=df_stackedAccess_t[['Mental Health Disorder','Male','Female']]
   df_gender_melt=df_gender.melt('Mental Health Disorder',var_name='Gender',value_name="Proportion")
   ##marital status
   df_stackedAccess_t['Never Married']=round(df_stackedAccess_t['NeverMarried']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['Ever Married']=round(df_stackedAccess_t['MarriageHistory']/df_stackedAccess_t['Population'],3)
   df_marital=df_stackedAccess_t[['Mental Health Disorder','Never Married','Ever Married']]
   df_marital_melt=df_marital.melt('Mental Health Disorder',var_name='Marital Status',value_name="Proportion")
   #add selection tab
   df_gender_melt_subset=df_gender_melt[df_gender_melt['Mental Health Disorder'].isin(diagnosis_tab2_2)]
   df_marital_melt_subset=df_marital_melt[df_marital_melt['Mental Health Disorder'].isin(diagnosis_tab2_2)]
   # create bar charts
   ##gender
   chart2_2 = alt.Chart(df_gender_melt_subset).mark_bar().encode(
      x=alt.X('Proportion:Q', title='Proportion of Patients Received Services'),
      y=alt.Y('Gender',title=None),
      row=alt.Row('Mental Health Disorder',header=alt.Header(labelAngle=0,labelAlign='left')),
      color=alt.Color('Gender'),
      tooltip=['Mental Health Disorder','Gender','Proportion']
      ).properties(
         title='Proportion of Patients Received Services by Gender',
         width=700
         )
   st.altair_chart(chart2_2)
   ##marital status
   chart2_3 = alt.Chart(df_marital_melt_subset).mark_bar().encode(
      x=alt.X('Proportion:Q', title='Proportion of Patients Received Services'),
      y=alt.Y('Marital Status',title=None),
      row=alt.Row('Mental Health Disorder',header=alt.Header(labelAngle=0,labelAlign='left')),
      color=alt.Color('Marital Status'),
      tooltip=['Mental Health Disorder','Marital Status','Proportion']
      ).properties(
         title='Proportion of Patients Received Services by Marital Status',
         width=700
         )
   st.altair_chart(chart2_3)
   
   ### Race & Education Level
   #create diagnosis selection tab 
   diagnosis_tab2_3 = st.selectbox('Mental Health Disorder', df_stackedAccess_t['Mental Health Disorder'].unique())
   #calculate care accessing proportion
   ##race
   df_stackedAccess_t['Black']=round(df_stackedAccess_t['Black_n']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['White']=round(df_stackedAccess_t['White_n']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['Other']=round(df_stackedAccess_t['OtherRace']/df_stackedAccess_t['Population'],3)
   df_race=df_stackedAccess_t[['Mental Health Disorder','Black','White','Other']]
   df_race_melt=df_race.melt('Mental Health Disorder',var_name='Race',value_name="Proportion")
   ##education level
   df_stackedAccess_t['Special Education']=round(df_stackedAccess_t['SpecialEdu']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['School Grade 0 to 8']=round(df_stackedAccess_t['Edu8']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['School Grade 9 to 12']=round(df_stackedAccess_t['Edu12']/df_stackedAccess_t['Population'],3)
   df_stackedAccess_t['School Grade >12']=round(df_stackedAccess_t['EduHigh']/df_stackedAccess_t['Population'],3)
   df_edu=df_stackedAccess_t[['Mental Health Disorder','Special Education','School Grade 0 to 8',
                              'School Grade 9 to 12','School Grade >12']]
   df_edu_melt=df_edu.melt('Mental Health Disorder',var_name='Education',value_name="Proportion")
   
   #add selection tab
   df_race_melt_subset=df_race_melt[df_race_melt['Mental Health Disorder']==diagnosis_tab2_3]
   df_edu_melt_subset=df_edu_melt[df_edu_melt['Mental Health Disorder']==diagnosis_tab2_3]
   
   #create donut charts
   ##marital status
   chart2_4 = alt.Chart(df_race_melt_subset).mark_arc(innerRadius=50).encode(
      theta='Proportion:Q',
      color='Race:N',
      tooltip=['Mental Health Disorder','Race','Proportion']
      ).properties(
         title='Proportion of Patients Received Services by Race'
         )
   ##education level
   chart2_5 = alt.Chart(df_edu_melt_subset).mark_arc(innerRadius=50).encode(
      theta='Proportion:Q',
      color='Education:N',
      tooltip=['Mental Health Disorder','Education','Proportion']
      ).properties(
         title='Proportion of Patients Received Services by Education Level'
         )
   #display charts side-by-side
   col1, col2 = st.columns(2)
   col1.altair_chart(chart2_4, use_container_width=True)
   col2.altair_chart(chart2_5, use_container_width=True)

   ### Tab 2, Task 3 ###
   
   task2 = st.header("Geospatial Pattern")
   test = df_stackedState[df_stackedState['YEAR']==2013]
   test['prop'] = test['CMPSERVICE']/(test['POPULATION']-test['Missing'])
   test.rename(columns={'STATEFIP': 'state'}, inplace=True)
   
   #US states background
   #states = alt.topo_feature(data.us_10m.url, feature='states')
   #background = alt.Chart(states).mark_geoshape(
    #fill='lightgray',
    #stroke='white'
  # ).properties(
   # width=500,
   # height=300
  # ).project('albersUsa')
   #create diagnosis selection tab 
   #diagosis_tab2_4 = st.selectbox("Mental Health Disorder", options = df_stackedDiag["Mental Health Outcomes"].unique())
   #test_subset = test2[test2['Mental Health Outcome']==diagnosis_tab2_4]
   #prop_scale = alt.Scale(domain=[test['prop'].min(), test['prop'].max()], scheme='orangered')
   #prop_color = alt.Color(field="prop", type="quantitative", scale=prop_scale)

#chart_rate = alt.Chart(test).mark_geoshape().encode(
    #color=('prop:Q'),
#).properties(
    #width=500,
    #height=300
   #).project('albersUsa')

# Display the map in Streamlit
#st.map(background+chart_rate, use_container_width=True)

   