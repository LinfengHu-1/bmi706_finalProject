import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
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
   df_stackedStateAccess = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_access_state.csv")
   df_em = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis_EducationMarriage.csv")
   df_er = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis_EducationRace.csv")
   df_ge = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis_GenderEducation.csv")
   df_gm = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis_GenderMarriage.csv")
   df_gr = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis_GenderRace.csv")
   df_rm = pd.read_csv("https://raw.githubusercontent.com/LinfengHu-1/bmi706_finalProject/main/stacked_data_diagnosis_RaceMarriage.csv")
   return df_stackedState, df_stackedDiag, df_stackedAccess, df_stackedStateAccess,df_em,df_er,df_ge,df_gm,df_gr,df_rm
df_stackedState, df_stackedDiag, df_stackedAccess, df_stackedStateAccess, df_em,df_er,df_ge,df_gm,df_gr,df_rm= load_data()
df_stackedDiag.rename(columns={'MH1': 'Mental Health Outcomes'}, inplace=True)
df_stackedDiag = df_stackedDiag[df_stackedDiag['Mental Health Outcomes'] != 'Missing']
df_stackedState = df_stackedState[df_stackedState['CODE'] != 99]
df_stackedAccess.rename(columns={'MH1': 'Mental Health Disorder'}, inplace=True)

df_em["EDUC"].replace({1:"Specifal education",2:"Grade 0-8",3:"Grade 9-11",4:"Grade 12/(GED)",5:"More than Grade 12"},inplace = True)
df_em["MARSTAT"].replace({1:"Never Married",2:"Married",3:"Separated",4:"Divorced,widowed"},inplace = True)
df_er["EDUC"].replace({1:"Specifal education",2:"Grade 0-8",3:"Grade 9-11",4:"Grade 12/(GED)",5:"More than Grade 12"},inplace = True)
df_er["RACE"].replace({1:"American Indian",2:"Asian",3:"Black",4:"Pacific Islander",5:"White",6:"Other"},inplace = True)
df_ge["GENDER"].replace({1:"Male",2:"Female"},inplace = True)
df_ge["EDUC"].replace({1:"Specifal education",2:"Grade 0-8",3:"Grade 9-11",4:"Grade 12/(GED)",5:"More than Grade 12"},inplace = True)
df_gm["GENDER"].replace({1:"Male",2:"Female"},inplace = True)
df_gm["MARSTAT"].replace({1:"Never Married",2:"Married",3:"Separated",4:"Divorced,widowed"},inplace = True)
df_gr["GENDER"].replace({1:"Male",2:"Female"},inplace = True)
df_gr["RACE"].replace({1:"American Indian",2:"Asian",3:"Black",4:"Pacific Islander",5:"White",6:"Other"}, inplace=True)
df_rm["RACE"].replace({1:"American Indian",2:"Asian",3:"Black",4:"Pacific Islander",5:"White",6:"Other"},inplace = True)
df_rm["MARSTAT"].replace({1:"Never Married",2:"Married",3:"Separated",4:"Divorced,widowed"},inplace = True)
         
### Layout ###
st.title("Mental Health Outcomes and Intervention Investigation")
tab1, tab2 = st.tabs(["Mental Health Outcomes", "Access to Mental Health Services"])

with st.sidebar:
   intro = st.write('This website uses Mental Health Client-Level Data retrieved from the Substance Abuse and Mental Health Services Administration (SAMHSA.gov), spanning 2013 to 2019, in order to examine the following 2 topics: ')
   st.markdown("- Distribution & Prevalence of Mental Health Outcomes")
   st.markdown("- Access to Mental Health Services")
   st.markdown('''
               <style>
               [data-testid="stMarkdownContainer"] ul{
               list-style-position: inside;
               }
               </style>
               ''', unsafe_allow_html=True)
   st.write('Within each topic, we explored the following tasks:')
   st.markdown("- Temporal Trend")
   st.markdown("- Geospatial Pattern")
   st.markdown("- Influential Factors/Social Determinants of Health")
   option = st.selectbox("Tasks to Explore", 
                         options=['Temporal Trend', 'Geospatial Pattern', 'Influential Factors'])
    
################### Tab 1: Mental Health Outcomes #######################
with tab1:
    ### Tab 1, Task 1 ###
   if 'Temporal Trend' in option:
      task1 = st.header("Temporal Trends")
      diag = st.multiselect("To examine temporal trends, select multiple Mental Health Outcomes", options=df_stackedDiag["Mental Health Outcomes"].unique(), 
                                 default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'],
                                 key = '1-1')
      filtered_df1BAR = df_stackedDiag[df_stackedDiag["Mental Health Outcomes"].isin(diag)]
      filtered_df = filtered_df1BAR
      filtered_df['YEAR'] = filtered_df1BAR['YEAR'].astype(str)
      chart1_1 = alt.Chart(filtered_df).mark_line().encode(
         x=alt.X("YEAR", axis=alt.Axis(format='', title='Year', labelAngle=0)),
         y=alt.Y("Population", title="Total Number of Patients"),
         color="Mental Health Outcomes:N",  # Color by state if needed
         tooltip=["YEAR", "Population"]
         ).properties(
            title=f"Mental Health Disorder rates of {', '.join(diag)}",
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
   if 'Geospatial Pattern' in option:
      task2 = st.header("Geospatial Pattern")
      year = st.slider("Year", min_value=df_stackedState["YEAR"].min(), max_value=df_stackedState["YEAR"].max(),key = '1-2slider')
      diag1_3 = st.selectbox("Mental Health Outcome", options = df_stackedDiag["Mental Health Outcomes"].unique(),key = '1-2select')
      source = alt.topo_feature(data.us_10m.url, 'states')
      width = 900
      height  = 600
      background = alt.Chart(source).mark_geoshape(fill='#aaa', stroke='white').encode(
         tooltip=[
         alt.Tooltip('Missing Data:Q') 
      ]
      ).properties(width=width, height=height).project('albersUsa')
      filtered_df12 = df_stackedState[df_stackedState["YEAR"]==year][['STATEFIP', 'YEAR', 'POPULATION', 'CODE', diag1_3]]
      filtered_df12[diag1_3] = filtered_df12[diag1_3] / filtered_df12['POPULATION']
      rate_scale = alt.Scale(domain=[filtered_df12[diag1_3].min(), filtered_df12[diag1_3].max()], scheme='oranges')
      rate_color = alt.Color(field=diag1_3, type="quantitative", scale=rate_scale,title='Proportion')
      chart1_2 = alt.Chart(source).mark_geoshape().encode(
         color = rate_color,
         tooltip=[
         alt.Tooltip(f'{diag1_3}:Q', title=f'Proportion: ')  
      ]
         ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(filtered_df12, 'CODE', [diag1_3])
         ).properties(
            width=width, height=height,
            title=f'Proportion of Individuals with {diag1_3} in {year}',
            ).project('albersUsa')
      st.altair_chart(background+chart1_2, use_container_width=True)

   ### Tab 1, Task 3 ###
   if 'Influential Factors' in option:
      task3 = st.header("Factors Impacting Mental Health Outcomes")
      diag1_3 = st.selectbox("Mental Health Outcome", options = df_stackedDiag["Mental Health Outcomes"].unique(), key = "dgf")
      filtered_df13 = df_stackedDiag[df_stackedDiag["Mental Health Outcomes"]==diag1_3]
      column_rename_map = {
         'MarriageHistory': 'Ever Married',
         'NeverMarried': 'Never Married',
         'SpecialEdu':'Special Education',
         'Edu8':'School Grade 0 to 8',
         'Edu12':'School Grade 9 to 12',
         'EduHigh':'School Grade >12',
         'OtherRace':'Other'
         }
      filtered_df13 = filtered_df13.rename(columns=column_rename_map)
      filtered_df13['Female'] = filtered_df13['Population']-filtered_df13['Male']
      df13_gender = filtered_df13.melt(
         id_vars = ["YEAR","Mental Health Outcomes"], value_vars = ['Male','Female'], var_name = "Gender",value_name = "Pgender"
      )
      df13_edu = filtered_df13.melt(
         id_vars = ["YEAR","Mental Health Outcomes"], value_vars = ['Special Education','School Grade 0 to 8','School Grade 9 to 12','School Grade >12'], var_name = "Edu",value_name = "Pedu"
      )
      df13_mar = filtered_df13.melt(
         id_vars = ["YEAR","Mental Health Outcomes"], value_vars = ['Never Married','Ever Married'], var_name = "Mar",value_name = "Pmar"
      )
      df13_race = filtered_df13.melt(
         id_vars = ["YEAR","Mental Health Outcomes"], value_vars = ['Black','White','Other'], var_name = "Race",value_name = "Prace"
      )
      
      chart1_3 = alt.Chart(df13_gender).mark_bar().encode(
         x=alt.X('Gender:O',title = None,axis=alt.Axis(labels=False)),
         y=alt.Y('Pgender:Q',title = 'Population'),
         color='Gender:N',
         column=alt.Column('YEAR:N',title=None)
         ).properties(
            title = f'Impacts of Gender on {diag1_3}',
            width=30
         )
      chart1_3edu = alt.Chart(df13_edu).mark_bar().encode(
         x=alt.X('Edu:O',title = None,axis=alt.Axis(labels=False)),
         y=alt.Y('Pedu:Q',title = 'Population'),
         color=alt.Color('Edu:N').title('Education'),
         column=alt.Column('YEAR:N',title=None)
         ).properties(
            title = f'Impacts of Education level on {diag1_3}'
         )
      chart1_3race = alt.Chart(df13_race).mark_bar().encode(
         x=alt.X('Race:O',title = None,axis=alt.Axis(labels=False)),
         y=alt.Y('Prace:Q',title = 'Population'),
         color='Race:N',
         column=alt.Column('YEAR:N',title=None)
         ).properties(
            title = f'Impacts of Race on {diag1_3}'
         )
      chart1_3mar = alt.Chart(df13_mar).mark_bar().encode(
         x=alt.X('Mar:O',title = None,axis=alt.Axis(labels=False)),
         y=alt.Y('Pmar:Q',title = 'Population'),
         color=alt.Color('Mar:N').title('Marital Status'),
         column=alt.Column('YEAR:N',title=None)
         ).properties(
            title = f'Impacts of Marital status on {diag1_3}',
            width=30
         )
      #display charts side-by-side
      c0, c1 = st.columns(2)
      c0.altair_chart(chart1_3)
      c1.altair_chart(chart1_3mar)
      #display charts
      st.altair_chart(chart1_3edu)
      st.altair_chart(chart1_3race)

      ### Tab1, task 3 cont'd ###
      #year1_3 = st.slider("Year", min_value=df_stackedDiag["YEAR"].min(), max_value=df_stackedDiag["YEAR"].max(), key = 'heatmap_year')
      #outcome1_3 = st.selectbox("Mental Health Outcome", options = df_stackedDiag["Mental Health Outcomes"].unique(), key = 'heatmap')
      year = st.slider("Year", min_value=df_stackedState["YEAR"].min(), max_value=df_stackedState["YEAR"].max(),key = '1-3')
   
      heatmap1 = df_em[(df_em['YEAR']==year)&(df_em['MH1']==diag1_3)]
      heatmap2 = df_er[(df_er['YEAR']==year)&(df_er['MH1']==diag1_3)]
      heatmap3 = df_ge[(df_ge['YEAR']==year)&(df_ge['MH1']==diag1_3)]
      heatmap4 = df_gm[(df_gm['YEAR']==year)&(df_gm['MH1']==diag1_3)]
      heatmap5 = df_gr[(df_gr['YEAR']==year)&(df_gr['MH1']==diag1_3)]
      heatmap6 = df_rm[(df_rm['YEAR']==year)&(df_rm['MH1']==diag1_3)]

      heatmap_1 = alt.Chart(heatmap1).mark_rect().encode(
         alt.X("EDUC:O").title("Education level"),
         alt.Y("MARSTAT:O").title("Marital status"),
         alt.Color("Subgroup_Population").title("Subgroup_Population"),
         tooltip=[
            alt.Tooltip("Subgroup_Population", title="Number of individuals"),
            ],
      ).configure_axis(
         domain=False
      ).properties(
         title = f'Impacts of Education level and Marital status'
      )
      heatmap_2 = alt.Chart(heatmap2).mark_rect().encode(
         alt.X("EDUC:O").title("Education level"),
         alt.Y("RACE:O").title("Race"),
         alt.Color("Subgroup_Population").title("Subgroup_Population"),
         tooltip=[
            alt.Tooltip("Subgroup_Population", title="Number of individuals"),
            ],
      ).configure_axis(
         domain=False
      ).properties(
         title = f'Impacts of Education level and Race'
      )
      heatmap_3 = alt.Chart(heatmap3).mark_rect().encode(
         alt.X("EDUC:O").title("Education level"),
         alt.Y("GENDER:O").title("Gender"),
         alt.Color("Subgroup_Population").title("Subgroup_Population"),
         tooltip=[
            alt.Tooltip("Subgroup_Population", title="Number of individuals"),
            ],
      ).configure_axis(
         domain=False
      ).properties(
         title = f'Impacts of Education level and Gender '
      )
      heatmap_4 = alt.Chart(heatmap4).mark_rect().encode(
         alt.X("GENDER:O").title("Gender"),
         alt.Y("MARSTAT:O").title("Marital status"),
         alt.Color("Subgroup_Population").title("Subgroup_Population"),
         tooltip=[
            alt.Tooltip("Subgroup_Population", title="Number of individuals"),
            ],
      ).configure_axis(
         domain=False
      ).properties(
         title = f'Impacts of Gender and Marital status'
      )
      heatmap_5 = alt.Chart(heatmap5).mark_rect().encode(
         alt.X("GENDER:O").title("Gender"),
         alt.Y("RACE:O").title("Race"),
         alt.Color("Subgroup_Population").title("Subgroup_Population"),
         tooltip=[
            alt.Tooltip("Subgroup_Population", title="Number of individuals"),
            ],
      ).configure_axis(
         domain=False
      ).properties(
         title = f'Impacts of Gender and Race'
      )
      heatmap_6 = alt.Chart(heatmap6).mark_rect().encode(
         alt.X("RACE:O").title("Race"),
         alt.Y("MARSTAT:O").title("Marital status"),
         alt.Color("Subgroup_Population").title("Subgroup_Population"),
         tooltip=[
            alt.Tooltip("Subgroup_Population", title="Number of individuals"),
            ],
      ).configure_axis(
         domain=False
      ).properties(
         title = f'Impacts of Race and Marital status'
      )
      h1,h2 = st.columns(2)
      h1.altair_chart(heatmap_1, use_container_width=True)
      h2.altair_chart(heatmap_2, use_container_width=True)
   
      h3,h4 = st.columns(2)
      h3.altair_chart(heatmap_3, use_container_width=True)
      h4.altair_chart(heatmap_4, use_container_width=True)

      h5,h6 = st.columns(2)
      h5.altair_chart(heatmap_5, use_container_width=True)
      h6.altair_chart(heatmap_6, use_container_width=True)


############## Tab 2: Access to Psychiatric Care ##########################
with tab2:
   ### Tab 2, Task 1 ###
   if 'Temporal Trend' in option:
      task1 = st.header("Temporal Trends")
      #calculate care accessing proportion
      df_stackedDiag['Prop']=round(df_stackedDiag['SMHAserviceAccess']/df_stackedDiag['Population'],3)
      #create diagnosis selection tab 
      diag = st.multiselect('Mental Health Outcomes', options=df_stackedDiag['Mental Health Outcomes'].unique(), 
                                 default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'],key = '2-1diag')
      subset1=df_stackedDiag[df_stackedDiag['Mental Health Outcomes'].isin(diag)]
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
   if 'Influential Factors' in option:
      task2 = st.header("Factors Impacting Access to Mental Health Services")
      #keep Service==1
      df_stackedAccess_t=df_stackedAccess[df_stackedAccess['CMPSERVICE']==1]
      df_stackedAccess_t.rename(columns={'Male': 'Male_n'}, inplace=True)
      df_stackedAccess_t.rename(columns={'White': 'White_n'}, inplace=True)
      df_stackedAccess_t.rename(columns={'Black': 'Black_n'}, inplace=True)
      #create diagnosis selection tab 
      diag = st.multiselect('Mental Health Outcomes', options=df_stackedAccess_t['Mental Health Disorder'].unique(), 
                                 default = ['Trauma/Stress-related Disorder', 'Anxiety Disorder', 'ADHD'],
                                 key = '2-2diag')
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
      df_gender_melt_subset=df_gender_melt[df_gender_melt['Mental Health Disorder'].isin(diag)]
      df_marital_melt_subset=df_marital_melt[df_marital_melt['Mental Health Disorder'].isin(diag)]
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
      diag1_3 = st.selectbox('Mental Health Outcomes', df_stackedAccess_t['Mental Health Disorder'].unique(),
                           key = '2-3diag13')
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
      df_race_melt_subset=df_race_melt[df_race_melt['Mental Health Disorder']==diag1_3]
      df_edu_melt_subset=df_edu_melt[df_edu_melt['Mental Health Disorder']==diag1_3]
      
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
   if 'Geospatial Pattern' in option:
      #create user interactive bar&slider
      year = st.slider("Year", min_value=df_stackedState["YEAR"].min(), max_value=df_stackedState["YEAR"].max(),key = '2-3slider')
      diag2_3 = st.selectbox("Mental Health Outcome", options = df_stackedDiag["Mental Health Outcomes"].unique(),key = '2-3select')
      #melt 'df_stackedState'
      select_column=df_stackedDiag["Mental Health Outcomes"].unique()
      select_column = select_column.tolist()
      select_column.extend(['STATEFIP','YEAR'])
      df_stackedState_subset=df_stackedState[select_column]
      df_stackedState_subset_melt=df_stackedState_subset.melt(['STATEFIP','YEAR'],var_name='Mental Health Outcomes',value_name='total_N')
      #join 'df_stackedStateAccess' & 'df_stackedState'
      df_stackedStateAccess_t=df_stackedStateAccess[df_stackedStateAccess['CMPSERVICE']==1]
      df_stackedStateAccess_t.rename(columns={'MH1': 'Mental Health Outcomes'}, inplace=True)
      df_stackedStateAccess_t=df_stackedStateAccess_t[['STATEFIP','YEAR','Population','Mental Health Outcomes','CODE']]
      merged_df=df_stackedStateAccess_t.merge(df_stackedState_subset_melt,on=['STATEFIP','YEAR','Mental Health Outcomes'],how='left')
      #calculate prop access to care for each state in each year
      merged_df['Proportion']=merged_df['Population']/merged_df['total_N']
      merged_df=merged_df[merged_df['Mental Health Outcomes']!='Missing']
      #subset data
      merged_df_subset = merged_df[(merged_df["YEAR"]==year)&(merged_df["Mental Health Outcomes"]==diag2_3)]
      #background map
      source = alt.topo_feature(data.us_10m.url, 'states')
      width = 900
      height  = 600
      background = alt.Chart(source).mark_geoshape(fill='#aaa', stroke='white').encode(
         tooltip=[alt.Tooltip('Missing Data:Q') ]
      ).properties(width=width, height=height).project('albersUsa')
      #create chart
      Proportion=merged_df_subset['Proportion']
      chart2_6 = alt.Chart(source).mark_geoshape().encode(
        color = 'Proportion:Q',
        tooltip=['Proportion:Q']
         ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(merged_df_subset, 'CODE',['Proportion'])
         ).properties(
            width=width, 
            height=height,
            title=f'Proportion of Patients with {diag2_3} in {year} who Received Services'
            ).project('albersUsa')
      st.altair_chart(background+chart2_6, use_container_width=True)


