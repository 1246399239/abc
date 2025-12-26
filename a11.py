# 导入依赖（严格匹配你的requirements.txt，无额外库）
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')  # 屏蔽无关警告


# 1. 页面配置（复刻效果图布局）
st.set_page_config(
    page_title="销售仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 自定义CSS（1:1匹配效果图样式）
st.markdown("""
<style>
    /* 全局样式：白色背景+深色文字 */
    .main {
        background-color: #ffffff;
        color: #333333;
        padding: 0 1rem;
    }
    
    /* 标题样式：居中+加粗 */
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1.5rem 0;
    }
    
    /* KPI卡片样式：轻灰背景+居中对齐 */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-title {
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #2c3e50;
        font-size: 1.9rem;
        font-weight: bold;
    }
    
    /* 侧边栏样式：轻灰背景+内边距 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding: 1.2rem 1rem;
    }
    
    /* 图表容器样式：内边距+间距 */
    .chart-container {
        background-color: #ffffff;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 筛选器样式：增加底部间距 */
    [data-testid="stMultiSelect"] {
        margin-bottom: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


# 3. 数据加载（核心修复：Excel读取+时间列容错）
@st.cache_data(show_spinner="正在加载销售数据...")
def load_excel_data():
    """
    读取本地Excel文件（supermarket_sales.xlsx）
    修复点：1. 跳过标题行 2. 时间列格式容错 3. 字段精准映射
    """
    # 确认文件路径（当前代码所在目录）
    excel_path = "supermarket_sales.xlsx"
    if not os.path.exists(excel_path):
        st.error(f"❌ 未找到数据文件：{excel_path}")
        st.info("💡 请确保Excel文件与代码放在同一目录")
        return pd.DataFrame()  # 空表兜底，避免崩溃

    # 读取Excel：跳过第一行（"2022年前3个月销售数据"），用第二行做列名
    df = pd.read_excel(
        excel_path,
        engine="openpyxl",  # 匹配你的openpyxl==3.1.5
        header=1  # 关键：跳过标题行，解决Unnamed列问题
    )

    # 字段100%映射你的Excel列名（避免KeyError）
    df_standard = df.rename(columns={
        "分店": "branch",
        "城市": "city",
        "顾客类型": "customer_type",
        "性别": "gender",
        "产品类型": "category",
        "单价": "unit_price",
        "数量": "quantity",
        "总价": "revenue",  # 你的"总价"即销售额
        "日期": "date",
        "时间": "time",
        "评分": "rating"
    })

    # 核心修复：时间列格式容错（解决ValueError）
    # 步骤1：清理时间列脏数据（空格、特殊字符）
    df_standard["time"] = df_standard["time"].astype(str).str.strip()  # 去空格
    df_standard["time"] = df_standard["time"].str.replace(r"[^\d:]", "", regex=True)  # 删特殊字符
    # 步骤2：转换时间（兼容%H:%M、%H:%M:%S等格式，无效值填0）
    time_series = pd.to_datetime(
        df_standard["time"],
        format="mixed",  # 自动识别常见时间格式（关键修复）
        errors="coerce"  # 无法识别的时间→NaT
    )
    # 步骤3：提取小时，NaT填充为0（避免后续图表报错）
    df_standard["hour"] = time_series.dt.hour.fillna(0).astype(int)

    # 日期列转换（确保筛选器正常）
    df_standard["date"] = pd.to_datetime(df_standard["date"], errors="coerce")

    st.success(f"✅ 数据加载成功！共{len(df_standard)}条销售记录")
    return df_standard


# 4. KPI指标生成（匹配效果图的3个核心指标）
def generate_kpi(filtered_df):
    """生成：总销售额、顾客平均评分、每单平均销售额"""
    # 分3列展示KPI
    col1, col2, col3 = st.columns(3, gap="medium")

    # 总销售额
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">总销售额：</div>', unsafe_allow_html=True)
        total_revenue = filtered_df["revenue"].sum()
        st.markdown(f'<div class="metric-value">RMB ¥ {total_revenue:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 顾客平均评分
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">顾客评分的平均值：</div>', unsafe_allow_html=True)
        avg_rating = filtered_df["rating"].mean()
        st.markdown(f'<div class="metric-value">{avg_rating:.1f} ⭐</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 每单平均销售额
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">每单的平均销售额：</div>', unsafe_allow_html=True)
        avg_order = filtered_df["revenue"].mean()
        st.markdown(f'<div class="metric-value">RMB ¥ {avg_order:.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# 5. 图表生成（复刻效果图的2个核心图表）
def generate_charts(filtered_df):
    """生成：按小时销售额、按产品类型销售额"""
    # 分2列展示图表
    col1, col2 = st.columns(2, gap="medium")

    # 图表1：按小时划分的销售额
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 按小时数划分的销售额")
        # 按小时聚合销售额
        hour_sales = filtered_df.groupby("hour")["revenue"].sum().reset_index()
        # 绘制柱状图（匹配效果图风格）
        st.bar_chart(
            hour_sales,
            x="hour",
            y="revenue",
            color="#007bff",  # 蓝色柱体
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # 图表2：按产品类型划分的销售额
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 按产品类型划分的销售额")
        # 按产品类型聚合销售额（降序排列）
        category_sales = filtered_df.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
        # 绘制柱状图
        st.bar_chart(
            category_sales,
            x="category",
            y="revenue",
            color="#007bff",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)


# 6. 主函数（整合所有功能+侧边栏筛选）
def main():
    # 标题
    st.markdown('<h1 class="main-title">📊 销售仪表板</h1>', unsafe_allow_html=True)

    # 加载数据
    df = load_excel_data()
    if df.empty:
        return  # 数据为空时终止运行

    # 筛选后的数据副本
    df_filtered = df.copy()

    # 侧边栏筛选器（匹配效果图的3个筛选项）
    st.sidebar.header("🔍 请筛选数据：")

    # 筛选1：城市（默认全选）
    city_options = df["city"].unique()
    selected_cities = st.sidebar.multiselect(
        "选择城市：",
        options=city_options,
        default=city_options
    )
    df_filtered = df_filtered[df_filtered["city"].isin(selected_cities)]

    # 筛选2：顾客类型（默认全选）
    customer_options = df["customer_type"].unique()
    selected_customers = st.sidebar.multiselect(
        "选择顾客类型：",
        options=customer_options,
        default=customer_options
    )
    df_filtered = df_filtered[df_filtered["customer_type"].isin(selected_customers)]

    # 筛选3：性别（默认全选）
    gender_options = df["gender"].unique()
    selected_genders = st.sidebar.multiselect(
        "选择性别：",
        options=gender_options,
        default=gender_options
    )
    df_filtered = df_filtered[df_filtered["gender"].isin(selected_genders)]

    # 筛选后数据量提示
    st.sidebar.markdown("---")
    st.sidebar.info(f"筛选后记录数：{len(df_filtered)} 条")

    # 生成KPI和图表（筛选后的数据）
    generate_kpi(df_filtered)
    generate_charts(df_filtered)


# 7. 运行入口
if __name__ == "__main__":
    main()
