import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# ---------------------- 1. 数据准备 ----------------------
# 1.1 餐厅基础数据（5+家南宁知名连锁/本地特色店）
restaurants_data = [
    {
        "名称": "三品王(朝阳店)",
        "类型": "快餐",
        "评分": 4.3,
        "人均消费(元)": 15,
        "latitude": 22.812200,
        "longitude": 108.266629,
        "推荐菜品": ["原汤牛肉粉", "杂酱粉", "腐竹"],
        "拥挤程度": 0.85
    },
    {
        "名称": "柳厨螺蛳粉(中山路店)",
        "类型": "快餐",
        "评分": 4.5,
        "人均消费(元)": 13,
        "latitude": 22.809105,
        "longitude": 108.378664,
        "推荐菜品": ["经典螺蛳粉", "干捞螺蛳粉", "炸蛋"],
        "拥挤程度": 0.90
    },
    {
        "名称": "复记老友粉(七星店)",
        "类型": "快餐",
        "评分": 4.2,
        "人均消费(元)": 18,
        "latitude": 22.853838,
        "longitude": 108.222177,
        "推荐菜品": ["老友粉", "酸笋炒肉", "猪杂粉"],
        "拥挤程度": 0.88
    },
    {
        "名称": "高峰柠檬鸭(北湖店)",
        "类型": "中餐",
        "评分": 4.6,
        "人均消费(元)": 58,
        "latitude": 22.965046,
        "longitude": 108.353921,
        "推荐菜品": ["柠檬鸭", "爆炒鸭杂", "鸭血汤"],
        "拥挤程度": 0.75
    },
    {
        "名称": "益禾堂(大学城店)",
        "类型": "饮品",
        "评分": 4.4,
        "人均消费(元)": 9,
        "latitude": 22.839699,
        "longitude": 108.245804,
        "推荐菜品": ["烤奶", "杨枝甘露", "西瓜啵啵"],
        "拥挤程度": 0.82
    },
    {
        "名称": "邕州老街南宁饭店",
        "类型": "中餐",
        "评分": 4.7,
        "人均消费(元)": 88,
        "latitude": 22.821567,
        "longitude": 108.283456,
        "推荐菜品": ["柠檬鸭", "老友扣肉", "粉饺"],
        "拥挤程度": 0.68
    }
]
df_restaurants = pd.DataFrame(restaurants_data)

# 1.2 用餐高峰时段数据（area_chart）
peak_hours_data = {
    "时段": [11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0],
    "快餐": [45, 88, 95, 90, 78, 68, 58, 50, 45, 50, 55, 65, 75, 85, 90, 85, 78],
    "中餐": [15, 35, 45, 40, 35, 30, 25, 20, 18, 22, 28, 35, 40, 45, 50, 45, 40],
    "饮品": [20, 40, 50, 45, 40, 35, 30, 25, 40, 55, 65, 70, 75, 80, 85, 80, 70],
    "卤味": [12, 28, 38, 33, 28, 23, 18, 15, 12, 18, 23, 28, 33, 38, 42, 38, 32]
}
df_peak_hours = pd.melt(
    pd.DataFrame(peak_hours_data),
    id_vars="时段",
    var_name="餐厅类型",
    value_name="用餐人数"
)

# 1.3 新增：5家餐厅12个月价格走势数据（line_chart 多折线）
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
price_trend_data = {
    "月份": months,
    "三品王(朝阳店)": [13, 13, 14, 14, 15, 15, 15, 15, 14, 15, 15, 15],
    "柳厨螺蛳粉(中山路店)": [11, 12, 12, 13, 13, 13, 13, 13, 12, 13, 13, 13],
    "复记老友粉(七星店)": [16, 17, 17, 18, 18, 18, 18, 18, 17, 18, 18, 18],
    "高峰柠檬鸭(北湖店)": [55, 56, 57, 58, 58, 59, 59, 58, 57, 58, 58, 58],
    "邕州老街南宁饭店": [80, 82, 85, 86, 88, 88, 89, 88, 87, 88, 88, 88]
}
df_price_trend = pd.DataFrame(price_trend_data)
# 转换为Altair所需格式
df_price_trend_melt = pd.melt(
    df_price_trend,
    id_vars="月份",
    var_name="餐厅名称",
    value_name="人均消费(元)"
)

# ---------------------- 2. 页面布局（还原界面效果）----------------------
# 页面配置
st.set_page_config(page_title="南宁美食数据仪表盘", layout="wide")

# 标题与介绍
st.title("🍜 南宁美食数据仪表盘")
st.write("全方位探索南宁本地特色美食，可视化呈现餐厅评分、价格、客流等核心数据！")
st.markdown("---")

# 分栏布局：左侧地图 + 右侧评分柱状图
col1, col2 = st.columns(2)

with col1:
    # 南宁美食地图（map）
    st.subheader("📍 南宁美食地图")
    st.map(df_restaurants[["latitude", "longitude", "名称"]], zoom=12)

with col2:
    # 餐厅评分柱状图（bar_chart）
    st.subheader("⭐ 餐厅评分")
    chart_rating = alt.Chart(df_restaurants).mark_bar(color="#1f77b4").encode(
        x=alt.X("名称:N", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("评分:Q", scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(grid=False)),
        tooltip=["名称:N", "评分:Q"]
    ).properties(width=500, height=300)
    st.altair_chart(chart_rating, use_container_width=True)

st.markdown("---")

# 新增：5家餐厅12个月价格走势折线图（核心要求）
st.subheader("📈 5家餐厅12个月价格走势")
chart_price_trend = alt.Chart(df_price_trend_melt).mark_line(point=True, strokeWidth=3).encode(
    x=alt.X("月份:O", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("人均消费(元):Q", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True)),
    color=alt.Color("餐厅名称:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"])),
    tooltip=["餐厅名称:N", "月份:O", "人均消费(元):Q"]
).properties(width=800, height=400)
st.altair_chart(chart_price_trend, use_container_width=True)

st.markdown("---")

# 分栏布局：价格折线图 + 高峰时段面积图
col3, col4 = st.columns(2)

with col3:
    # 不同类型餐厅价格折线图（line_chart）
    st.subheader("💰 不同类型餐厅均价")
    df_type_price = df_restaurants.groupby("类型")["人均消费(元)"].mean().reset_index()
    chart_type_price = alt.Chart(df_type_price).mark_line(point=True, strokeWidth=3, color="#4682B4").encode(
        x=alt.X("类型:N", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("人均消费(元):Q", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=False)),
        tooltip=["类型:N", "人均消费(元):Q"]
    ).properties(width=400, height=300)
    st.altair_chart(chart_type_price, use_container_width=True)

with col4:
    # 用餐高峰时段面积图（area_chart）
    st.subheader("⏰ 用餐高峰时段")
    chart_peak = alt.Chart(df_peak_hours).mark_area(opacity=0.7, line=True).encode(
        x=alt.X("时段:Q", axis=alt.Axis(grid=False)),
        y=alt.Y("用餐人数:Q", axis=alt.Axis(grid=False)),
        color=alt.Color("餐厅类型:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])),
        tooltip=["时段:Q", "餐厅类型:N", "用餐人数:Q"]
    ).properties(width=400, height=300)
    st.altair_chart(chart_peak, use_container_width=True)

st.markdown("---")

# 餐厅详情（下拉选择+进度条）
st.subheader("🍴 餐厅详情")
selected_restaurant = st.selectbox(
    label="选择餐厅查看详情",
    options=df_restaurants["名称"].tolist(),
    index=0
)
selected_data = df_restaurants[df_restaurants["名称"] == selected_restaurant].iloc[0]

# 详情展示
col5, col6 = st.columns(2)
with col5:
    st.write(f"**名称**：{selected_data['名称']}")
    st.write(f"**类型**：{selected_data['类型']}")
    st.write(f"**评分**：{selected_data['评分']}/5.0")
    st.write(f"**人均消费**：{selected_data['人均消费(元)']}元")

with col6:
    st.write("**推荐菜品**：")
    for dish in selected_data["推荐菜品"]:
        st.write(f"• {dish}")
    st.write("**当前拥挤程度**：")
    st.progress(selected_data["拥挤程度"])
    st.write(f"{round(selected_data['拥挤程度']*100)}%")
