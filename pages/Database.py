import streamlit as st
import pandas as pd
import statistics
from annotated_text import annotated_text
import plotly.express as px
from datetime import datetime
from datetime import timedelta
from st_aggrid import AgGrid

st.set_page_config(page_title='Data Kerja Indonesia - Februari 2023', page_icon=':bar_chart:', layout='wide')
keywords = ['Cloud Engineer','Software Developer','Data Analyst',
          'Product Manager','Digital & Social Media Marketing','Content Writer',
          'Geologist','Graphic Design','Cyber Security','Customer Service']

data = pd.read_excel('All_April_2023.xlsx')
max_date = max(data['DatePublish'])
min_date = min(data['DatePublish'])

# markdown
st.sidebar.header("Data Kerja Indonesia")
st.title('Data Kerja Indonesia')

# Define the sidebar
st.info('Pilih Lowongan Pekerjaan')
col1_1,col2_1,col3_1 = st.columns(3) 
# Create the multiselect widget
keyword = col1_1.selectbox("Pilih Keyword:", keywords)
date_min = col2_1.date_input("Tanggal Awal",value=min_date)
date_max = col3_1.date_input("Tanggal Akhir",value=max_date)

jobportal = data['Source'].unique()
juml_jobportal = len(data['Source'].unique())
jobportal_text = ''
for x in jobportal:
    jobportal_text = jobportal_text + ', ' + x
data_job = data[data['Keyword']==keyword]
data_job_relevant = data_job[data_job['Relevant']==1]
count_job_all = data_job['JobTitle'].count()
count_job = data_job_relevant['Keyword'].count()
dif_col1 = count_job/count_job_all
start_salary = data_job_relevant['StartingSalary'].mean()
stdev = statistics.stdev(list(data_job_relevant['StartingSalary'].dropna().astype(int)))

st.subheader('Detail {} Jobs'.format(keyword))
data_detail = data_job_relevant[['Keyword','Source','JobTitle','Company','JobLocation','DatePublish','Salary','JobUrl']]
#filtered_df = dataframe_explorer(data_detail)
#st.dataframe(filtered_df,use_container_width=True)
AgGrid(data_detail)

