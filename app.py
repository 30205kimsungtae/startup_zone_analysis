import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울시 창업 분석", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/상권변화지표.csv", encoding='cp949')

df = load_data()

st.title("🏪 서울시 소상공인 창업 적합 지역 분석")
st.markdown("서울시 **상권변화지표**를 바탕으로 창업 유망지역을 분석합니다.")

# 필터 영역
st.sidebar.header("🔍 필터")
year_quarter = st.sidebar.selectbox("기준 연도/분기", sorted(df['기준_년분기_코드'].unique(), reverse=True))
zone_type = st.sidebar.selectbox("상권 구분", df['상권_구분_코드_명'].unique())

filtered = df[(df['기준_년분기_코드'] == year_quarter) & 
              (df['상권_구분_코드_명'] == zone_type)]

st.markdown(f"### 📊 선택한 기준: `{year_quarter}` | `{zone_type}` 상권")

# 상단 요약 카드
col1, col2, col3 = st.columns(3)
col1.metric("총 상권 수", len(filtered))
col2.metric("평균 운영 기간", round(filtered['운영_영업_개월_평균'].mean(), 1))
col3.metric("평균 폐업 기간", round(filtered['폐업_영업_개월_평균'].mean(), 1))

st.divider()

# 변화 지표 시각화
st.subheader("📈 상권 변화 지표 분포")
change_counts = filtered['상권_변화_지표_명'].value_counts()
fig = px.pie(
    names=change_counts.index,
    values=change_counts.values,
    title="상권 변화 지표 비율"
)
st.plotly_chart(fig, use_container_width=True)

# 유망 상권 추천
st.subheader("🟢 유망 창업 상권 추천")

recommend = filtered[
    (filtered['상권_변화_지표_명'].isin(['상권확장', '다이나믹'])) &
    (filtered['운영_영업_개월_평균'] > filtered['폐업_영업_개월_평균'])
].copy()

recommend = recommend.sort_values(by='운영_영업_개월_평균', ascending=False)

st.dataframe(
    recommend[['상권_코드_명', '상권_변화_지표_명', '운영_영업_개월_평균', '폐업_영업_개월_평균']],
    use_container_width=True,
    height=400
)

