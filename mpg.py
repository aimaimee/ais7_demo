import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px

st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

# 마크다운 제목
st.markdown("# 자동차 연비 🚗")
st.sidebar.markdown("# 자동차 연비 🚗")

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
mpg = pd.read_csv(url)

# uber.py를 참고하여 캐시에서 데이터를 불러 올 수 있도록 설정
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data = load_data(url)
data_load_state.text("Done! (using st.cache)")

# Sidebar - year
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',
   list(reversed(range(mpg.model_year.min(),mpg.model_year.max())))
   )

if selected_year > 0 :
   mpg = mpg[mpg.model_year == selected_year]

# Sidebar - origin
sorted_unique_origin = sorted(mpg.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

if len(selected_origin) > 0:
   mpg = mpg[mpg.origin.isin(selected_origin)]


st.dataframe(mpg)

# Streamlit에서 제공하는 Chart
st.line_chart(mpg["mpg"])

st.bar_chart(mpg["mpg"])

fig, ax = plt.subplots(figsize=(10,3))
sns.countplot(data=mpg, x="origin").set_title("지역별 자동차 연비 데이터 수")
st.pyplot(fig)

pxh = px.histogram(mpg, x="origin", title="지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)

fig, ax = plt.subplots(figsize=(10,3))
sns.scatterplot(data=mpg, x="mpg", y="weight", hue="origin")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10,3))
sns.lmplot(data=mpg, x="mpg", y="weight", hue="origin")
st.pyplot(fig)