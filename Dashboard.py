import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from datetime import timedelta
from st_aggrid import AgGrid
import statistics
from streamlit_card import card
from streamlit_extras import dataframe_explorer


# Set the page title
st.set_page_config(page_title='Data Kerja Indonesia - Februari 2023', page_icon=':bar_chart:', layout='wide')
keywords = ['Cloud Engineer','Software Developer','Data Analyst',
          'Product Manager','Digital & Social Media Marketing','Content Writer',
          'Geologist','Graphic Design','Cyber Security','Customer Service']

data = pd.read_excel('All_March_2023.xlsx')
data['Keyword'] = data['Keyword'].astype('category')
data['Source'] = data['Source'].astype('category')
data['JobLocation'] = data['JobLocation'].astype('category')
max_date = max(data['DatePublish'])
min_date = min(data['DatePublish'])


# markdown
st.title('Data Kerja Indonesia')

st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
def get_invers(value):
    if value > 0.6:
        text = 'normal'
    else:
        text = 'inverse'
    return text
# Define the sidebar
st.sidebar.header("Data Kerja Indonesia")
st.info('Pilih Lowongan Pekerjaan')
col1_1,col2_1,col3_1 = st.columns(3) 
# Create the multiselect widget
keyword = col1_1.selectbox("Pilih Keyword:", keywords)
date_min = col2_1.date_input("Tanggal Awal",value=min_date)
date_max = col3_1.date_input("Tanggal Akhir",value=max_date)


st.header('{} Jobs'.format(keyword))
data_job = data[data['Keyword']==keyword]
data_job_relevant = data_job[data_job['Relevant']==1]
count_job_all = data_job['JobTitle'].count()
count_job = data_job_relevant['Keyword'].count()
dif_col1 = count_job/count_job_all
start_salary = data_job_relevant['StartingSalary'].mean()
stdev = statistics.stdev(list(data_job_relevant['StartingSalary'].dropna().astype(int)))

col1,col2,col3 = st.columns(3)
col1.metric(label='Hasil Pencarian'.format(keyword),value="%.0f"%count_job_all)
col2.metric(label='Hasil Relevan'.format(keyword),value="%.0f"%count_job,delta="{percent:.2%} Akurasi".format(percent=dif_col1))
col3.metric(label='Rata-rata Starting Salary'.format(keyword),value="Rp. {:,.0f}".format(start_salary),
            delta="∑ Rp. {:,.0f} Deviasi".format(stdev))

# Define the chart title
chart_title = f'Waktu Publish Lowongan Kerja {keyword}'
back_30daysago = datetime.today() - timedelta(days=30)
pivot_timeline = data_job_relevant.pivot_table(index='DatePublish',columns='Source',values='JobTitle',aggfunc='count')
pivot_timeline = pivot_timeline[pivot_timeline.index > back_30daysago]
# Create a line chart using Plotly
fig = px.bar(pivot_timeline, x=pivot_timeline.index,y=pivot_timeline.columns, title=chart_title,
             color_discrete_sequence=px.colors.qualitative.Bold)
fig.add_annotation(text="© Curated by: DataKerja. \t Source from: Jobstreet, Indeed, Kalibrr, Karir.com",
                  xref="paper", yref="paper",
                  x=0, y=1, showarrow=False)
# Display the chart
st.plotly_chart(fig, use_container_width=True)


#All
pivot_df = data_job.pivot_table(index='Source',values=['JobTitle','Relevant','StartingSalary'],aggfunc={'JobTitle':'count','Relevant':'sum','StartingSalary':'mean'})
#Jobstreet
try :
    JT_value = pivot_df.loc[('Jobstreet')]['JobTitle']
    JT_relev = pivot_df.loc[('Jobstreet')]['Relevant']
    JT_delta = JT_relev/JT_value
    JT_salar = pivot_df.loc[('Jobstreet')]['StartingSalary']/1_000_000
except :
    JT_value = 0
    JT_relev = 0
    JT_delta = 0
    JT_salar = 0
#Indeed
try :
    ID_value = pivot_df.loc[('Indeed')]['JobTitle']
    ID_relev = pivot_df.loc[('Indeed')]['Relevant']
    ID_delta = ID_relev/ID_value
    ID_salar = pivot_df.loc[('Indeed')]['StartingSalary']/1_000_000
except :
    ID_value = 0
    ID_relev = 0
    ID_delta = 0
    ID_salar = 0
#Kalibrr
try :
    KB_value = pivot_df.loc[('Kalibrr')]['JobTitle']
    KB_relev = pivot_df.loc[('Kalibrr')]['Relevant']
    KB_delta = KB_relev/KB_value
    KB_salar = pivot_df.loc[('Kalibrr')]['StartingSalary']/1_000_000
except :
    KB_value = 0
    KB_relev = 0
    KB_delta = 0
    KB_salar = 0
#Karir.com
try:
    KR_value = pivot_df.loc[('Karir.com')]['JobTitle']
    KR_relev = pivot_df.loc[('Karir.com')]['Relevant']
    KR_delta = KR_relev/KR_value
    KR_salar = pivot_df.loc[('Karir.com')]['StartingSalary']/1_000_000
except :
    KR_value = 0
    KR_relev = 0
    KR_delta = 0
    KR_salar = 0


st.subheader('Hasil Pencarian Keyword {} tiap Job Portal'.format(keyword))
col1_3, col2_3, col3_3, col4_3 = st.columns(4)
col1_3.metric(label="Jobstreet", value="{:.0f}".format(JT_relev), delta = "{rel:.0f} / {percent:.2%} Akurasi".format(rel=JT_value,percent=JT_delta), delta_color=get_invers(JT_delta))
col2_3.metric(label="Indeed", value="{:.0f}".format(ID_relev), delta = "{rel:.0f} / {percent:.2%} Akurasi".format(rel=ID_value,percent=ID_delta), delta_color=get_invers(ID_delta))
col3_3.metric(label="Kalibrr", value="{:.0f}".format(KB_relev), delta = "{rel:.0f} / {percent:.2%} Akurasi".format(rel=KB_value,percent=KB_delta), delta_color=get_invers(KB_delta))
col4_3.metric(label="Karir.com", value="{:.0f}".format(KR_relev), delta = "{rel:.0f} / {percent:.2%} Akurasi".format(rel=KR_value,percent=KR_delta), delta_color=get_invers(KR_delta))

#st.subheader('Rata-rata Gaji {} tiap Job Portal'.format(keyword))
col1_4, col2_4, col3_4, col4_4 = st.columns(4)
col1_4.metric(label="Jobstreet", value="Rp. {:,.1f}JT".format(JT_salar))
col2_4.metric(label="Indeed", value="Rp. {:,.1f}JT".format(ID_salar))
col3_4.metric(label="Kalibrr", value="Rp. {:,.1f}JT".format(KB_salar))
col4_4.metric(label="Karir.com", value="Rp. {:,.1f}JT".format(KR_salar))


graph_1,graph_2 = st.columns(2)
# Define the chart title
chart_title2 = f'Range Gaji {keyword} '
grouped_salary = data_job_relevant[['RangeSalary','JobTitle']].groupby('RangeSalary').count()
# Create a line chart using Plotly
fig = px.pie(grouped_salary, values=grouped_salary['JobTitle'],names=grouped_salary.index, title=chart_title2,
             color_discrete_sequence=px.colors.sequential.YlGnBu_r,
             hole=0.5,labels=True)

fig.add_annotation(text="© Curated by: DataKerja. \nSource from: Jobstreet, Indeed, Kalibrr, Karir.com",
                  xref="paper", yref="paper",
                  x=0, y=1.1, showarrow=False)
# Display the chart
graph_1.plotly_chart(fig, use_container_width=True)


# Define the chart title
chart_title3 = f'Lokasi Lowongan Kerja {keyword}'
grouped_jobloc = data_job_relevant[['JobLocation','JobTitle']].groupby('JobLocation').count().sort_values(by='JobTitle',ascending=True).tail(10)
pivot_jobloc = data_job_relevant.pivot_table(index='JobLocation',columns='Source',values='JobTitle',aggfunc='count',margins=True).sort_values(by='All',ascending=False).head(10)
# Create a line chart using Plotly
fig = px.bar(grouped_jobloc, x=grouped_jobloc['JobTitle'],y=grouped_jobloc.index, 
             color_discrete_sequence=px.colors.qualitative.T10,
             title=chart_title3,labels=True)
fig.add_annotation(text="© Curated by: DataKerja. \nSource from: Jobstreet, Indeed, Kalibrr, Karir.com",
                  xref="paper", yref="paper",
                  x=0, y=1.1, showarrow=False)
# Display the chart
graph_2.plotly_chart(fig, use_container_width=True)

st.subheader('Detail {} Jobs'.format(keyword))
data_detail = data_job_relevant[['Keyword','Source','JobTitle','Company','JobLocation','DatePublish','Salary','JobUrl']]
#filtered_df = dataframe_explorer(data_detail)
#st.dataframe(filtered_df,use_container_width=True)
AgGrid(data_detail)