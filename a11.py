import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import warnings  # 确保导入warnings
warnings.filterwarnings('ignore')  # 修复乱码问题


# 页面配置
st.set_page_config(
    page_title="销售数据仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 自定义CSS（匹配效果图风格）
st.markdown("""
<style>
    .main {background-color: #ffffff; color: #333333;}
    .main-title {text-align: center; color: #2c3e50; font-size: 2.5rem; font-weight: bold; margin: 1rem 0;}
    .metric-card {background-color: #f8f9fa; border-radius: 8px; padding: 1rem; margin: 0.5rem; text-align: center;}
    .metric-title {color: #6c757d; font-size: 1rem; margin-bottom: 0.3rem;}
    .metric-value {color: #2c3e50; font-size: 1.8rem; font-weight: bold;}
    [data-testid="stSidebar"] {background-color: #f8f9fa;}
    .chart-container {padding: 1rem; margin-bottom: 1rem;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="加载数据中...")
def load_data():
    """适配你的Excel文件（supermarket_sales.xlsx）"""
    target_file = "supermarket_sales.xlsx"
    if not os.path.exists(target_file):
        st.error(f"未找到文件：{target_file}，请确保文件在代码目录下")
        return pd.DataFrame()  # 返回空表避免崩溃

    # 读取你的Excel（精准匹配你的字段）
    df = pd.read_excel(target_file, engine="openpyxl")
    # 显示你的原始字段（确认匹配）
    st.success(f"成功读取数据！你的Excel字段：{list(df.columns)}")

    # 字段标准化（100%匹配你的Excel）
    df_standard = df.rename(columns={
        "城市": "city",
        "顾客类型": "customer_type",
        "产品类型": "category",
        "单价": "unit_price",
        "数量": "quantity",
        "总价": "revenue",  # 你的“总价”就是销售额
        "日期": "date",
        "时间": "time",
        "评分": "rating",
        "分店": "branch",
        "性别": "gender"
    })

    # 处理日期+时间（提取小时用于图表）
    df_standard["date"] = pd.to_datetime(df_standard["date"], errors="coerce")
    df_standard["hour"] = pd.to_datetime(df_standard["time"], format="%H:%M").dt.hour  # 提取小时

    return df_standard


def create_kpi_metrics(filtered_df):
    """创建效果图中的KPI（总销售额、平均评分等）"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">总销售额</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMB ¥ {filtered_df["revenue"].sum():,.0f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">顾客评分的平均值</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{filtered_df["rating"].mean():.1f} ⭐</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">每单的平均销售额</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMB ¥ {filtered_df["revenue"].mean():.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def create_charts(filtered_df):
    """创建效果图中的图表（按小时、产品类型）"""
    col1, col2 = st.columns(2)

    # 按小时统计销售额（匹配效果图）
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("按小时数划分的销售额")
        hour_sales = filtered_df.groupby("hour")["revenue"].sum()
        st.bar_chart(hour_sales, color="#007bff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 按产品类型统计销售额（匹配效果图）
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("按产品类型划分的销售额")
        category_sales = filtered_df.groupby("category")["revenue"].sum().sort_values(ascending=False)
        st.bar_chart(category_sales, color="#007bff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-title">销售仪表板</h1>', unsafe_allow_html=True)

    # 加载数据
    df = load_data()
    if df.empty:
        return  # 数据为空则终止

    df_filtered = df.copy()

    # 侧边栏筛选（匹配效果图：分店、城市、顾客类型、性别）
    st.sidebar.header("请筛选数据：")

    # 1. 分店筛选
    branches = st.sidebar.multiselect("选择分店", df["branch"].unique(), default=df["branch"].unique())
    df_filtered = df_filtered[df_filtered["branch"].isin(branches)]

    # 2. 城市筛选
    cities = st.sidebar.multiselect("选择城市", df["city"].unique(), default=df["city"].unique())
    df_filtered = df_filtered[df_filtered["city"].isin(cities)]

    # 3. 顾客类型筛选
    customer_types = st.sidebar.multiselect("选择顾客类型", df["customer_type"].unique(), default=df["customer_type"].unique())
    df_filtered = df_filtered[df_filtered["customer_type"].isin(customer_types)]

    # 4. 性别筛选（匹配效果图）
    genders = st.sidebar.multiselect("选择性别", df["gender"].unique(), default=df["gender"].unique())
    df_filtered = df_filtered[df_filtered["gender"].isin(genders)]


    # 显示KPI和图表
    create_kpi_metrics(df_filtered)
    create_charts(df_filtered)


if __name__ == "__main__":
    main()
