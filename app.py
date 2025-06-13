import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("data/상권변화지표.csv", encoding='cp949')

df = load_data()

st.title("서울시 소상공인 창업 적합 지역 분석")
st.markdown("서울시 상권변화지표를 바탕으로 창업에 유리한 지역을 시각화하고 추천합니다.")

# 필터
year_quarter = st.selectbox("기준 연도/분기", sorted(df['기준_년분기_코드'].unique(), reverse=True))
zone_type = st.selectbox("상권 구분", df['상권_구분_코드_명'].unique())

filtered = df[(df['기준_년분기_코드'] == year_quarter) & (df['상권_구분_코드_명'] == zone_type)]

# 상권 변화 지표 시각화
st.subheader("상권 변화 지표 분포")
st.bar_chart(filtered['상권_변화_지표_명'].value_counts())

# 추천 상권 목록
st.subheader("유망 상권 추천")
recommend = filtered[
    (filtered['상권_변화_지표_명'].isin(['상권확장', '다이나믹'])) &
    (filtered['운영_영업_개월_평균'] > filtered['폐업_영업_개월_평균'])
]
st.dataframe(recommend[['상권_코드_명', '상권_변화_지표_명', '운영_영업_개월_평균', '폐업_영업_개월_평균']])
