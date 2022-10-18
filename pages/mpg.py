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
   list(reversed(range(data.model_year.min(), data.model_year.max())))
   )

if selected_year > 0 :
   data = data[data.model_year == selected_year]

# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

if len(selected_origin) > 0:
   data = data[data.origin.isin(selected_origin)]


st.dataframe(data)

# Streamlit에서 제공하는 Chart
st.line_chart(data["mpg"])

st.bar_chart(data["mpg"])

pxh = px.histogram(data, x="origin", title="지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)

pxh = px.histogram(data, x="origin", y="horsepower", histfunc="avg", title="지역별 자동차 마력 평균")
st.plotly_chart(pxh)

fig, ax = plt.subplots(figsize=(10,3))
sns.countplot(data=data, x="origin").set_title("지역별 자동차 연비 데이터 수")
st.pyplot(fig)

# data에 덮어씌운 데이터셋이 아니라 전체 데이터셋을 가지고 그리는게 더 적합
fig = sns.lmplot(data=data, x="weight", y="horsepower", hue="origin", ci=None)
plt.title("지역별 무게와 마력")
st.pyplot(fig)

# 마찬가지로 전체 데이터셋을 가지고 그리는게 더 적합
fig, ax = plt.subplots()
sns.scatterplot(data=data, x="mpg", y="weight", hue='origin').set_title("mpg 별 origin 별 weight 시각화")
st.pyplot(fig)

fig, ax = plt.subplots()
sns.scatterplot(data=data, x="horsepower", y="mpg")
st.pyplot(fig)

fig, ax = plt.subplots()
sns.violinplot(data=data, x="cylinders", y="mpg")
st.pyplot(fig)
