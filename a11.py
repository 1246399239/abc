import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
warnings.filterwarnings('ignore')

# 页面配置
st.set_page_config(
    page_title="销售数据仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {background-color: #0e1117; color: #f0f0f0;}
    .main-title {text-align: center; color: #4a9eff; font-size: 2.8rem; font-weight: bold; margin-bottom: 0.5rem;}
    .metric-card {background-color: #262730; border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;}
    .metric-title {color: #aaaaaa; font-size: 0.9rem; margin-bottom: 0.5rem;}
    .metric-value {color: #4a9eff; font-size: 2rem; font-weight: bold;}
    [data-testid="stSidebar"] {background-color: #262730;}
    .chart-container {background-color: #262730; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stLineChart"], [data-testid="stBarChart"] {background-color: #262730; border-radius: 8px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

# 缓存数据加载（优先读取supermarket_sales.xlsx）
@st.cache_data(show_spinner="正在加载数据...")
def load_data(uploaded_file=None):
    """加载销售数据：优先上传文件 → 目标文件 → 示例数据"""
    current_dir = os.getcwd()
    st.sidebar.info(f"当前工作目录：{current_dir}")
    
    # 目标文件名（用户已修改为该名称）
    target_filename = "supermarket_sales.xlsx"
    file_path = os.path.join(current_dir, target_filename)
    
    try:
        # 1. 优先上传文件
        if uploaded_file is not None:
            df = read_excel_with_fallback(uploaded_file)
            st.success("✅ 成功加载上传的Excel文件")
            return df
        
        # 2. 读取目标文件（用户改名后的文件名）
        if os.path.exists(file_path):
            df = read_excel_with_fallback(file_path)
            st.success(f"✅ 成功加载数据文件：{target_filename}")
            return df
        
        # 3. 未找到文件提示
        st.warning(f"⚠️ 未在当前目录找到 {target_filename}！")
        st.warning(f"当前目录文件列表：{os.listdir(current_dir)}")
        st.info("💡 请确保文件与代码在同一文件夹，或通过左侧上传文件")
        return generate_sample_data()
    
    except Exception as e:
        st.error(f"❌ 数据加载失败：{str(e)}")
        return generate_sample_data()

def read_excel_with_fallback(file_path_or_upload):
    """双引擎读取Excel，兼容.xlsx/.xls"""
    try:
        return pd.read_excel(file_path_or_upload, engine="openpyxl")
    except:
        try:
            return pd.read_excel(file_path_or_upload, engine="xlrd")
        except Exception as e:
            raise Exception(f"Excel读取失败：{str(e)}")

def standardize_fields(df):
    """标准化字段（适配原始数据的字段名）"""
    df.columns = [col.strip().replace("（", "").replace("）", "").lower() for col in df.columns]
    
    # 日期字段（原始字段：日期）
    if "日期" in df.columns:
        df["date"] = pd.to_datetime(df["日期"], errors="coerce")
        df = df.dropna(subset=["date"])
    else:
        st.warning("⚠️ 数据中未找到日期字段，无法进行日期筛选")
    
    # 销售额字段（原始字段：总价）
    if "总价" in df.columns:
        df["revenue"] = pd.to_numeric(df["总价"], errors="coerce").fillna(0)
    elif "单价" in df.columns and "数量" in df.columns:
        df["revenue"] = df["单价"] * df["数量"]
        st.info("💡 已通过「单价×数量」计算销售额")
    else:
        df["revenue"] = 0
    
    # 产品类别（原始字段：产品类型）
    df["category"] = df.get("产品类型", "未知")
    # 城市（原始字段：城市）
    df["city"] = df.get("城市", "未知")
    # 客户类型（原始字段：顾客类型）
    df["customer_type"] = df.get("顾客类型", "未知")
    # 评分（原始字段：评分）
    df["rating"] = pd.to_numeric(df.get("评分", 0), errors="coerce").fillna(0)
    # 补充其他字段
    df["payment_method"] = df.get("payment_method", "未知")
    df["unit_price"] = pd.to_numeric(df.get("单价", 0), errors="coerce").fillna(0)
    df["quantity"] = pd.to_numeric(df.get("数量", 0), errors="coerce").fillna(0)
    
    return df

def generate_sample_data():
    """生成示例数据"""
    np.random.seed(42)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    categories = ['电子产品', '服装', '食品饮料', '家居用品', '运动户外', '美妆护肤']
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都']
    
    data = []
    for date in date_range:
        for _ in range(np.random.randint(20, 50)):
            category = np.random.choice(categories)
            price_range = {
                '电子产品': (500, 5000), '服装': (100, 800), '食品饮料': (10, 200),
                '家居用品': (50, 1000), '运动户外': (200, 2000), '美妆护肤': (50, 500)
            }
            unit_price = np.random.uniform(*price_range[category])
            quantity = np.random.randint(1, 10)
            data.append({
                'date': date, 'category': category, 'city': np.random.choice(cities),
                'unit_price': round(unit_price, 2), 'quantity': quantity,
                'revenue': round(unit_price * quantity, 2),
                'rating': round(np.random.uniform(3.0, 5.0), 1),
                'customer_type': np.random.choice(['会员', '普通客户']),
                'payment_method': np.random.choice(['现金', '信用卡', '移动支付'])
            })
    df = pd.DataFrame(data)
    st.info("ℹ️ 当前使用示例数据（2024年1-3月）")
    return df

def create_kpi_metrics(filtered_df):
    """创建KPI指标"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">总销售额</div><div class="metric-value">¥ {filtered_df["revenue"].sum():,.0f}</div></div>', unsafe_allow_html=True)
    with col2:
        avg_rating = filtered_df["rating"].mean()
        st.markdown(f'<div class="metric-card"><div class="metric-title">顾客平均评分</div><div class="metric-value">{avg_rating:.1f} ⭐</div></div>', unsafe_allow_html=True)
    with col3:
        avg_order = filtered_df["revenue"].sum() / len(filtered_df) if len(filtered_df) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-title">每单平均销售额</div><div class="metric-value">¥ {avg_order:.0f}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">订单总数</div><div class="metric-value">{len(filtered_df):,}</div></div>', unsafe_allow_html=True)

def create_charts(filtered_df):
    """创建数据图表"""
    col1, col2 = st.columns(2)
    
    # 销售趋势
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 销售趋势（按日期）")
        if "date" in filtered_df.columns:
            daily_sales = filtered_df.groupby("date")["revenue"].sum()
            st.line_chart(daily_sales, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 产品类别销售
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏪 产品类别销售额")
        category_sales = filtered_df.groupby("category")["revenue"].sum().sort_values(ascending=False)
        st.bar_chart(category_sales, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    # 城市销售分布
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🌍 城市销售分布")
        city_sales = filtered_df.groupby("city")["revenue"].sum().sort_values(ascending=False)
        st.bar_chart(city_sales, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 客户类型分析
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("👥 客户类型分布")
        customer_dist = filtered_df["customer_type"].value_counts()
        st.bar_chart(customer_dist, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """主函数"""
    st.markdown('<h1 class="main-title">📊 销售数据仪表板</h1>', unsafe_allow_html=True)
    
    # 文件上传
    st.sidebar.header("📁 文件上传")
    uploaded_file = st.sidebar.file_uploader("选择Excel文件", type=["xlsx", "xls"])
    
    # 加载数据
    df = load_data(uploaded_file)
    df_filtered = df.copy()
    
    # 数据筛选
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 数据筛选")
    
    # 日期筛选
    if "date" in df.columns:
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        date_range = st.sidebar.date_input("选择日期范围", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        if len(date_range) == 2:
            df_filtered = df_filtered[(df_filtered["date"] >= pd.to_datetime(date_range[0])) & (df_filtered["date"] <= pd.to_datetime(date_range[1]))]
    
    # 类别筛选
    categories = st.sidebar.multiselect("产品类别", df["category"].unique(), default=df["category"].unique())
    df_filtered = df_filtered[df_filtered["category"].isin(categories)]
    
    # 城市筛选
    cities = st.sidebar.multiselect("城市", df["city"].unique(), default=df["city"].unique())
    df_filtered = df_filtered[df_filtered["city"].isin(cities)]
    
    # 客户类型筛选
    customer_types = st.sidebar.multiselect("客户类型", df["customer_type"].unique(), default=df["customer_type"].unique())
    df_filtered = df_filtered[df_filtered["customer_type"].isin(customer_types)]
    
    # 数据概览
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 数据概览")
    st.sidebar.write(f"总记录数: {len(df):,}")
    st.sidebar.write(f"筛选后记录数: {len(df_filtered):,}")
    
    # 空数据处理
    if len(df_filtered) == 0:
        st.warning("⚠️ 无匹配数据，请调整筛选条件")
        return
    
    # 展示KPI和图表
    create_kpi_metrics(df_filtered)
    st.markdown("---")
    create_charts(df_filtered)
    
    # 详细数据和下载
    st.markdown("---")
    st.subheader("📋 详细数据（前1000行）")
    st.dataframe(df_filtered.head(1000).rename(columns=str.title), use_container_width=True, hide_index=True)
    
    csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下载筛选数据",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
