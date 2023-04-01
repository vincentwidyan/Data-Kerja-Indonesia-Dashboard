import streamlit as st
import pandas as pd
import statistics
from annotated_text import annotated_text
import plotly.express as px
from datetime import datetime
from datetime import timedelta

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

st.header('Dokumentasi')
st.write("---")
st.subheader('Latar Belakang')
annotated_text("Pada bulan",("Maret","date") ,"tahun",("2023","date") ,"ini, tim Data Kerja sudah mengumpulkan data-data dari beberapa Job Portal yang ada di Indonesia. Total hingga saat ini, kami mengumpulkan",("{}".format(juml_jobportal),"int"),"Job Portal yakni",("{}".format(jobportal_text),"list"),"Pada dokumentasi ini, tim Data Kerja akan menjelaskan mengenai kondisi lowongan kerja untuk",("{}".format(keyword),"text"),"di beberapa Job Portal di Indoensia")

st.write("---")

st.subheader('Overview')
col1,col2,col3 = st.columns(3)
col1.metric(label='Hasil Pencarian'.format(keyword),value="%.0f"%count_job_all)
col2.metric(label='Hasil Relevan'.format(keyword),value="%.0f"%count_job,delta="{percent:.2%} Akurasi".format(percent=dif_col1))
col3.metric(label='Rata-rata Starting Salary'.format(keyword),value="Rp. {:,.0f}".format(start_salary),
            delta="∑ Rp. {:,.0f} Deviasi".format(stdev))

annotated_text("Saat ini, terdapat total",("{}".format(count_job_all),"int"),"lowongan pekerjaan untuk",("{}".format(keyword),"text"),"beberapa Job Portal tersebut. Dari semua hasil pencarian tersebut, terdapat",("{}".format(count_job),"int")," hasil pencarian yang relevan dari keyword tersebut. Banyak dari hasil pencarian yang tidak sesuai dengan keyword yang dicari. Maka dari itu, untuk keyword pencarian",("{}".format(keyword),"text"),"di beberapa Job Portal itu memiliki akurasi sebesar",("{:.2%}".format(dif_col1),"percent"))
st.write("\n")
annotated_text(("{}".format(keyword),"text")," di Indonesia saat ini memilki rata-rata gaji awal/Starting Salary sebesar",("Rp. {:,.0f}".format(start_salary),"float"),"Adapun deviasi dari rata-rata gaji yang kami kumpulkan adalah sebesar",("Rp. {:,.0f}".format(stdev),"float"))

st.write("---")

st.subheader('Timeline')
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
                  x=0, y=1.1, showarrow=False)
# Display the chart
st.plotly_chart(fig, use_container_width=True)

pivot_timeline = data_job_relevant.pivot_table(index='DatePublish',values='JobTitle',aggfunc='count')
pivot_timeline = pivot_timeline[pivot_timeline.index > back_30daysago]
maxDateHighest = max(pivot_timeline['JobTitle'])
minDateLowest = min(pivot_timeline['JobTitle'])
date_highest = pivot_timeline.index[pivot_timeline['JobTitle']==maxDateHighest][0].strftime('%-d %B %Y')
date_lowest = pivot_timeline.index[pivot_timeline['JobTitle']==minDateLowest][0].strftime('%-d %B %Y')

annotated_text("Pada sebulan terakhir, grafik datas menunjukkan peningkatan/penurunan lowongan kerja",("{}".format(keyword),"text"),"di beberapa Job Portal. Terlihat pada grafik tersebut, lowongan kerja ",("{}".format(keyword),"text"), "paling banyak dipublish sebanyak",("{}".format(maxDateHighest),"int"),"buah lowongan pada tanggal",("{}".format(date_highest),"date"),"dan paling sedikit dipublish sebanyak",("{}".format(minDateLowest),"int"),"buah lowongan pada tanggal",("{}".format(date_lowest),"date"))
st.write("\n")         
annotated_text("Grafik ini dapat menunjukkan apakah lowongan kerja",("{}".format(keyword),"text"),"masih menjadi propsek atau tidak pada waktu sekarang ini. Jika grafik publishnya meningkat, tedapat besar kemungkinan lowongan ini akan terus menerus ada, dan sebalikanya, jika grafik publishnya selalu menurun, terdapat kemungkinan bahwa lowongan kerja",("{}".format(keyword),"text"),"belum menjadi prospek lowongan kerja yang baik di Indonesia. Namun pada nyatanya, banyak faktor yang mempengaruhi jumlah lowongan kerja",("{}".format(keyword),"text"),"tersebut")

st.write("---")
def get_invers(value):
    if value > 0.6:
        text = 'normal'
    else:
        text = 'inverse'
    return text
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

annotated_text("Dari data metric di atas, dapat dilihat hasil pencarian lowongan kerja",("{}".format(keyword),"text"),"dari",("{}".format(juml_jobportal),"int"),"job portal yang kami kumpulkan saat ini. Dari hasil pencarian tersebut pula, kami juga sudah menyeleksi beberapa hasil pencarian tersebut yang masih relevan dengan",("{}".format(keyword),"text"),"dan juga persentase akurasi dari hasil yang relevan dibanding semua hasil pencariannya")
st.write("\n")
max_result = max(pivot_df['JobTitle'])
min_result = min(pivot_df['JobTitle'])
max_result_jp = pivot_df.index[pivot_df['JobTitle']==max_result][0]
min_result_jp = pivot_df.index[pivot_df['JobTitle']==min_result][0]

st.markdown("#### Hasil Pencarian")
annotated_text("Dari jumlah hasil pencarian yang dikumpulkan dengan lowongan kerja",("{}".format(keyword),"text"),"dari ke-",("{}".format(juml_jobportal),"int"),"job portal",("{}".format(max_result_jp),"text"),"memiliki hasil yang paling banyak yakni sebanyak",("{}".format(max_result),"int"),"sedangkan job portal",("{}".format(min_result_jp),"text"),"memiliki hasil yang paling sedikit yakni sebanyak ",("{}".format(min_result),"int"),"dan ke-",("{}".format(juml_jobportal-2),"int"),"job portal lain berada diantaranya. Namun perlu diketahui terkadang hasil pencarian mungkin tidak mencerminkan hasil relevannya.")
st.write("\n")
max_result_relev = max(pivot_df['Relevant'])
min_result_relev = min(pivot_df['Relevant'])
max_result_jp_relev = pivot_df.index[pivot_df['Relevant']==max_result_relev][0]
min_result_jp_relev = pivot_df.index[pivot_df['Relevant']==min_result_relev][0]
pivot_df['Akurasi'] = pivot_df['Relevant']/pivot_df["JobTitle"]
ave_relev_max = max(pivot_df['Akurasi'])
ave_relev_min = min(pivot_df['Akurasi'])
max_ave_jp_relev = pivot_df.index[pivot_df['Akurasi']==ave_relev_max][0]
min_ave_jp_relev = pivot_df.index[pivot_df['Akurasi']==ave_relev_min][0]

st.markdown("#### Hasil Relevan dan Akurasi")
annotated_text("Untuk hasil pencarian yang relevan, job portal",("{}".format(max_result_jp_relev),"text"),"mendapatkan hasil relevan yang paling banyak yakni sejumlah ",("{:.0f}".format(max_result_relev),"int"),"sedangkan job portal",("{}".format(min_result_jp_relev),"text"),"mendapatkan hasil relevan yang paling sedikit yakni sejumlah ",("{:.0f}".format(min_result_relev),"int"),"Sedangkan untuk akurasinya, job portal",("{}".format(max_ave_jp_relev),"text"),"memiliki akurasi yang paling baik sebesar",("{:.2%}".format(ave_relev_max),"float"))
st.write("\n")

max_salary_relev = max(pivot_df['StartingSalary'])
max_salary_jp_relev = pivot_df.index[pivot_df['StartingSalary']==max_salary_relev][0]
st.markdown("#### Rata-rata Gaji Awal")
annotated_text("Untuk rata-rata gaji awal lowongan kerja",("{}".format(keyword),"text")," pada job portal",("{}".format(max_salary_jp_relev),"text"),"memiliki rata-rata gaji yang paling banyak yakni sebesar",("Rp {:,.0f}".format(max_salary_relev),"float"),"juta rupiah.")

st.write("\n")
annotated_text("Dari jumlah hasil pencarian, jumlah hasil yang relevan, persentse akurasi, dan rata-rata gaji awal tersebut, silahkan kalian tentukan job portal mana yang terbaik untuk kalian telusuri untuk lowongan kerja",("{}".format(keyword),"text"))

st.write("---")
st.subheader('Jangkauan Gaji')
col1, col2, col3 = st.columns([1, 3, 1])
# Define the chart title
chart_title2 = f'Jangkauan Gaji {keyword} '
grouped_salary = data_job_relevant[['RangeSalary','JobTitle']].groupby('RangeSalary').count()
# Create a line chart using Plotly
fig = px.pie(grouped_salary, values=grouped_salary['JobTitle'],names=grouped_salary.index, title=chart_title2,
             color_discrete_sequence=px.colors.sequential.YlGnBu_r,
             hole=0.5,labels=True)

fig.add_annotation(text="© Curated by: DataKerja. \nSource from: Jobstreet, Indeed, Kalibrr, Karir.com",
                  xref="paper", yref="paper",
                  x=0, y=1.1, showarrow=False)
# Display the chart
disclosed = (grouped_salary.loc[('0. Disclosed')]['JobTitle'])/grouped_salary['JobTitle'].sum()

col2.plotly_chart(fig, use_container_width=True)
print(disclosed)
grouped_salary = grouped_salary.sort_values(by='JobTitle',ascending=False)
annotated_text("Dari data yang kita himpun, grafik di atas menunjukkan jangkauan (Range) gaji awal lowongan kerja",("{}".format(keyword),"text"),". Kategori",('0. Disclosed',"category"),"adalah lowongan pekerjaan yang tidak menampikan gaji yakni dalam pencarian ini sebesar",("{:.2%}".format(disclosed),"float"),"dari total lowongan yang ada. Kemudian untuk sisa",("{:.2%}".format(1-disclosed),"float"),"dari total lowongan kerja tersebut menampilkan gaji sesuai jangkauan (Range) pada grafik di atas.")
st.write("\n")
annotated_text("Dari data ini kita dapat melihat persebaran lowongan pekerjaan",("{}".format(keyword),"text"), "yang menampilkan gaji awal pada saat rekrutmen awal. Dari data ini juga kita dapat melihat seberapa baiknya propek lowongan kerja",("{}".format(keyword),"text"),"di Indonesia.")





st.write("---")
st.subheader('Lokasi Lowongan Kerja')
col1, col2, col3 = st.columns([1, 3, 1])
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
col2.plotly_chart(fig, use_container_width=True)

grouped_jobloc = data_job_relevant.pivot_table(index='JobLocation',values='JobTitle',aggfunc='count').sort_values(by='JobTitle',ascending=False).head(10)

annotated_text("Data grafik di atas merupakan data persebaran jumlah lowongan kerja",("{}".format(keyword),"text"),"di Indonesia. Pada saat ini, lowongan kerja",("{}".format(keyword),"text"), "terbanyak berada di",("{}".format(grouped_jobloc.index[0]),"text"),"sebanyak",("{}".format(grouped_jobloc.values[0][0]),"int"),"Di urutan selanjutnya, lowongan kerja tersebut paling banyak berada di",("{}".format(grouped_jobloc.index[1]),"text"),",",("{}".format(grouped_jobloc.index[2]),"text"),", dan",("{}".format(grouped_jobloc.index[3]),"text"),"sebanyak",("{}".format(grouped_jobloc.values[1][0]),"int"),",",("{}".format(grouped_jobloc.values[2][0]),"int"),", dan",("{}".format(grouped_jobloc.values[3][0]),"int"),"Data ini dapat menjadi acuan para pencari kerja untuk melihat daerah terbaik untuk lowongan kerja",("{}".format(keyword),"text"))

location = ['Yogyakarta','Bali','Bandung','Jawa Tengah','Jawa Timur','Banten','Bantul','Batam','Bekasi','Bogor','Denpasar','Kalimantan','Makassar','Malang','Medan','Palembang','Pekanbaru','Semarang','Sidoarjo']