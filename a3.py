import streamlit as st
import pandas as pd
import altair as alt

# ---------------------- 1. 数据准备（罗文大道知名连锁餐饮）----------------------
# 罗文大道知名连锁餐厅基础数据（模拟真实坐标和品牌特征）
restaurants_data = [
    {
        "名称": "三品王(罗文大道店)",
        "类型": "快餐",
        "评分": 4.3,
        "人均消费(元)": 15,
        "latitude": 22.856800,  # 罗文大道核心坐标
        "longitude": 108.205629,
        "推荐菜品": ["原汤牛肉粉", "杂酱粉", "腐竹"],
        "拥挤程度": 0.85  # 快餐连锁高峰拥挤
    },
    {
        "名称": "柳厨螺蛳粉(罗文店)",
        "类型": "快餐",
        "评分": 4.5,
        "人均消费(元)": 13,
        "latitude": 22.858105,
        "longitude": 108.208664,
        "推荐菜品": ["经典螺蛳粉", "干捞螺蛳粉", "炸蛋"],
        "拥挤程度": 0.90
    },
    {
        "名称": "益禾堂(罗文大学城店)",
        "类型": "饮品",
        "评分": 4.4,
        "人均消费(元)": 9,
        "latitude": 22.859838,
        "longitude": 108.202177,
        "推荐菜品": ["烤奶", "杨枝甘露", "西瓜啵啵"],
        "拥挤程度": 0.82
    },
    {
        "名称": "绝味鸭脖(罗文店)",
        "类型": "卤味",
        "评分": 4.2,
        "人均消费(元)": 25,
        "latitude": 22.855046,
        "longitude": 108.213921,
        "推荐菜品": ["招牌鸭脖", "鸭爪", "毛豆"],
        "拥挤程度": 0.65
    },
    {
        "名称": "蜜雪冰城(罗文大道店)",
        "类型": "饮品",
        "评分": 4.6,
        "人均消费(元)": 7,
        "latitude": 22.857699,
        "longitude": 108.208804,
        "推荐菜品": ["冰鲜柠檬水", "摩天脆脆", "芝士奶盖"],
        "拥挤程度": 0.88
    }
]
df_restaurants = pd.DataFrame(restaurants_data)

# 用餐高峰时段数据（适配连锁餐饮特征）
peak_hours_data = {
    "时段": [11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0],
    "快餐": [45, 88, 95, 90, 78, 68, 58, 50, 45, 50, 55, 65, 75, 85, 90, 85, 78],
    "饮品": [20, 40, 50, 45, 40, 35, 30, 25, 40, 55, 65, 70, 75, 80, 85, 80, 70],
    "卤味": [15, 35, 45, 40, 35, 30, 25, 20, 18, 22, 28, 35, 40, 45, 50, 45, 40],
    "中餐": [12, 28, 38, 33, 28, 23, 18, 15, 12, 18, 23, 28, 33, 38, 42, 38, 32]
}
df_peak_hours = pd.melt(
    pd.DataFrame(peak_hours_data),
    id_vars="时段",
    var_name="餐厅类型",
    value_name="用餐人数"
)

# ---------------------- 2. 页面布局（完全保留原有标题和结构）----------------------
# 标题与介绍（恢复原始标题）
st.title("🍔 南宁美食探索")
st.write("探索广西南宁最受欢迎的美食地点！选择你感兴趣的餐厅类型，查看评分和位置。")
st.markdown("---")

# 南宁美食地图（恢复原始标题）
st.subheader("📍 南宁美食地图")
st.map(df_restaurants[["latitude", "longitude", "名称"]], zoom=15)  # 聚焦罗文大道
st.markdown("---")

# 餐厅评分（柱状图）【保留原始标题】
st.subheader("⭐ 餐厅评分")
chart_rating = alt.Chart(df_restaurants).mark_bar(color="#1f77b4").encode(
    x=alt.X("名称:N", axis=alt.Axis(labelAngle=-45)),
    y=alt.Y(
        "评分:Q", 
        scale=alt.Scale(domain=[0, 5]),
        axis=alt.Axis(grid=False)
    ),
    tooltip=["名称:N", "评分:Q"]
).properties(
    width=600,
    height=300
)
st.altair_chart(chart_rating, use_container_width=True)
st.markdown("---")

# 不同类型餐厅价格（折线图）【保留原始标题】
st.subheader("💰 不同类型餐厅价格")
# 聚合各类型的平均人均
df_type_price = df_restaurants.groupby("类型")["人均消费(元)"].mean().reset_index()
chart_price = alt.Chart(df_type_price).mark_line(
    point=True, strokeWidth=3, color="#4682B4"
).encode(
    x=alt.X("类型:N", axis=alt.Axis(labelAngle=0)),
    y=alt.Y(
        "人均消费(元):Q", 
        scale=alt.Scale(domain=[0, 30]),  # 适配连锁餐饮价格区间
        axis=alt.Axis(grid=False)
    ),
    tooltip=["类型:N", "人均消费(元):Q"]
).properties(
    width=600,
    height=300
)
st.altair_chart(chart_price, use_container_width=True)
st.markdown("---")

# 用餐高峰时段（面积图）【保留原始标题】
st.subheader("⏰ 用餐高峰时段")
chart_peak = alt.Chart(df_peak_hours).mark_area(
    opacity=0.7, line=True
).encode(
    x=alt.X("时段:Q", axis=alt.Axis(grid=False)),
    y=alt.Y("用餐人数:Q", axis=alt.Axis(grid=False)),
    color=alt.Color("餐厅类型:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])),
    tooltip=["时段:Q", "餐厅类型:N", "用餐人数:Q"]
).properties(
    width=800,
    height=300
)
st.altair_chart(chart_peak, use_container_width=True)
st.markdown("---")

# 餐厅详情（下拉选择+进度条）【保留原始标题】
st.subheader("🍴 餐厅详情")
st.write("选择餐厅查看详情")
selected_restaurant = st.selectbox(
    label="",  # 隐藏默认标签
    options=df_restaurants["名称"].tolist(),
    index=1  # 默认选中“柳厨螺蛳粉(罗文店)”
)
# 获取选中餐厅的详情
selected_data = df_restaurants[df_restaurants["名称"] == selected_restaurant].iloc[0]

# 展示详情信息
col1, col2 = st.columns(2)
with col1:
    st.subheader(selected_data["名称"])
    st.write(f"评分：{selected_data['评分']}/5.0")
    st.write(f"人均消费：{selected_data['人均消费(元)']}元")
with col2:
    st.write("推荐菜品：")
    for dish in selected_data["推荐菜品"]:
        st.write(f"• {dish}")

# 拥挤程度进度条
st.write("当前拥挤程度")
st.progress(selected_data["拥挤程度"])
st.markdown("---")

# 今日午餐推荐（保留原始标题）
st.subheader("🎲 今日午餐推荐")
if st.button("帮我选午餐"):
    # 随机推荐一个低拥挤度的连锁品牌
    recommended = df_restaurants[df_restaurants["拥挤程度"] <= 0.85].sample(1).iloc[0]
    st.success(f"推荐：{recommended['名称']}（类型：{recommended['类型']}，人均：{recommended['人均消费(元)']}元）")
