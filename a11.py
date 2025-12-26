import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')


# 页面配置（完全匹配效果图）
st.set_page_config(
    page_title="销售仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 自定义CSS（复刻效果图样式）
st.markdown("""
<style>
    .main {background-color: #ffffff; color: #333333;}
    .main-title {text-align: center; color: #2c3e50; font-size: 2.5rem; font-weight: bold; margin: 1rem 0;}
    .metric-card {padding: 1rem; margin: 0.5rem; text-align: center;}
    .metric-title {color: #6c757d; font-size: 1rem; margin-bottom: 0.3rem;}
    .metric-value {color: #2c3e50; font-size: 1.8rem; font-weight: bold;}
    [data-testid="stSidebar"] {background-color: #f8f9fa; padding: 1rem;}
    .chart-container {padding: 1rem; margin-bottom: 1rem;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stMultiSelect"] {margin-bottom: 1rem;}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="加载数据中...")
def load_data():
    """精准读取你的Excel（适配实际列名+容错处理）"""
    target_file = "supermarket_sales.xlsx"
    if not os.path.exists(target_file):
        st.error(f"未找到数据文件：{target_file}，请确保文件在当前目录")
        return pd.DataFrame()

    # 跳过第一行标题，用第二行作为列名（匹配你的Excel结构）
    df = pd.read_excel(
        target_file,
        engine="openpyxl",
        header=1  # 跳过“2022年前3个月销售数据”行
    )

    # 字段100%映射你的Excel列名
    df_standard = df.rename(columns={
        "分店": "branch",
        "城市": "city",
        "顾客类型": "customer_type",
        "性别": "gender",
        "产品类型": "category",
        "总价": "revenue",  # 你的“总价”对应销售额
        "日期": "date",
        "时间": "time",
        "评分": "rating"
    })

    # 修复时间列转换错误（核心容错）
    df_standard["time"] = df_standard["time"].astype(str).str.strip()  # 清理空格
    # 提取小时（转换失败则设为0）
    df_standard["hour"] = pd.to_datetime(
        df_standard["time"], 
        format="%H:%M", 
        errors="coerce"  # 无效格式设为NaT
    ).dt.hour.fillna(0).astype(int)

    return df_standard


def create_kpi_metrics(filtered_df):
    """复刻效果图的KPI模块"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">总销售额：</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMB ¥ {filtered_df["revenue"].sum():,.0f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">顾客评分的平均值：</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{filtered_df["rating"].mean():.1f} ⭐</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">每单的平均销售额：</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">RMB ¥ {filtered_df["revenue"].mean():.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def create_charts(filtered_df):
    """复刻效果图的图表模块"""
    col1, col2 = st.columns(2)

    # 按小时划分的销售额（匹配效果图）
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("按小时数划分的销售额")
        hour_sales = filtered_df.groupby("hour")["revenue"].sum()
        st.bar_chart(hour_sales, color="#007bff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 按产品类型划分的销售额（匹配效果图）
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
        return

    df_filtered = df.copy()

    # 侧边栏筛选（完全匹配效果图的筛选项）
    st.sidebar.header("请筛选数据：")

    # 1. 城市筛选
    cities = st.sidebar.multiselect(
        "请选择城市：",
        options=df["city"].unique(),
        default=df["city"].unique()
    )
    df_filtered = df_filtered[df_filtered["city"].isin(cities)]

    # 2. 顾客类型筛选
    customer_types = st.sidebar.multiselect(
        "请选择顾客类型：",
        options=df["customer_type"].unique(),
        default=df["customer_type"].unique()
    )
    df_filtered = df_filtered[df_filtered["customer_type"].isin(customer_types)]

    # 3. 性别筛选
    genders = st.sidebar.multiselect(
        "请选择性别：",
        options=df["gender"].unique(),
        default=df["gender"].unique()
    )
    df_filtered = df_filtered[df_filtered["gender"].isin(genders)]


    # 展示KPI和图表（与效果图一致）
    create_kpi_metrics(df_filtered)
    create_charts(df_filtered)


if __name__ == "__main__":
    main()
