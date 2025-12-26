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

# 缓存数据加载
@st.cache_data(show_spinner="正在加载数据...")
def load_data(uploaded_file=None):
    current_dir = os.getcwd()
    st.sidebar.info(f"当前工作目录：{current_dir}")
    target_filename = "supermarket_sales.xlsx"
    file_path = os.path.join(current_dir, target_filename)
    
    try:
        # 优先上传文件
        if uploaded_file is not None:
            df = read_excel_with_fallback(uploaded_file)
            st.success("✅ 成功加载上传的Excel文件")
        # 读取目标文件
        elif os.path.exists(file_path):
            df = read_excel_with_fallback(file_path)
            st.success(f"✅ 成功加载数据文件：{target_filename}")
        else:
            st.warning(f"⚠️ 未找到 {target_filename}，使用示例数据")
            return generate_sample_data()
        
        # 显示你的Excel原始列名（方便你确认字段）
        st.info(f"你的Excel原始字段名：{list(df.columns)}")
        # 标准化字段（兼容中英文）
        df_standard = standardize_fields(df)
        return df_standard
    
    except Exception as e:
        st.error(f"❌ 数据加载失败：{str(e)}")
        return generate_sample_data()

def read_excel_with_fallback(file_path_or_upload):
    """双引擎读取Excel"""
    try:
        return pd.read_excel(file_path_or_upload, engine="openpyxl")
    except:
        try:
            return pd.read_excel(file_path_or_upload, engine="xlrd")
        except Exception as e:
            raise Exception(f"Excel读取失败：{str(e)}")

def standardize_fields(df):
    """兼容中英文字段名的标准化（核心修复）"""
    # 先统一字段名小写，方便匹配
    df.columns = [col.strip().lower() for col in df.columns]
    standardized = pd.DataFrame()

    # 1. 日期字段（匹配：日期 / date）
    date_cols = [col for col in df.columns if col in ["日期", "date"]]
    if date_cols:
        standardized["date"] = pd.to_datetime(df[date_cols[0]], errors="coerce")
        standardized = standardized.dropna(subset=["date"])
    else:
        st.warning("⚠️ 未找到日期字段（需要：日期 / Date），无法日期筛选")
        standardized["date"] = pd.NaT

    # 2. 销售额字段（匹配：总价 / total）
    revenue_cols = [col for col in df.columns if col in ["总价", "total"]]
    if revenue_cols:
        standardized["revenue"] = pd.to_numeric(df[revenue_cols[0]], errors="coerce").fillna(0)
    # 备选：单价×数量（匹配：单价/unit_price + 数量/quantity）
    elif "unit_price" in df.columns and "quantity" in df.columns:
        standardized["revenue"] = df["unit_price"] * df["quantity"]
        st.info("💡 通过「单价×数量」计算了销售额")
    else:
        st.warning("⚠️ 未找到销售额字段（需要：总价 / Total / 单价+数量），默认销售额0")
        standardized["revenue"] = 0

    # 3. 产品类别（匹配：产品类型 / product line）
    category_cols = [col for col in df.columns if col in ["产品类型", "product line"]]
    standardized["category"] = df[category_cols[0]] if category_cols else "未知"

    # 4. 城市（匹配：城市 / city）
    city_cols = [col for col in df.columns if col in ["城市", "city"]]
    standardized["city"] = df[city_cols[0]] if city_cols else "未知"

    # 5. 客户类型（匹配：顾客类型 / customer type）
    customer_cols = [col for col in df.columns if col in ["顾客类型", "customer type"]]
    standardized["customer_type"] = df[customer_cols[0]] if customer_cols else "未知"

    # 6. 支付方式（匹配：支付方式 / payment）
    payment_cols = [col for col in df.columns if col in ["支付方式", "payment"]]
    standardized["payment_method"] = df[payment_cols[0]] if payment_cols else "未知"

    # 7. 评分（匹配：评分 / rating）
    rating_cols = [col for col in df.columns if col in ["评分", "rating"]]
    standardized["rating"] = pd.to_numeric(df[rating_cols[0]], errors="coerce").fillna(0) if rating_cols else 0

    # 8. 单价 & 数量（匹配：单价/unit_price、数量/quantity）
    standardized["unit_price"] = pd.to_numeric(df.get("单价", df.get("unit_price", 0)), errors="coerce").fillna(0)
    standardized["quantity"] = pd.to_numeric(df.get("数量", df.get("quantity", 0)), errors="coerce").fillna(0)

    return standardized

# 以下generate_sample_data、create_kpi_metrics等函数保持不变（沿用之前版本）
def generate_sample_data():
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 销售趋势（按日期）")
        if not filtered_df["date"].isna().all():
            daily_sales = filtered_df.groupby("date")["revenue"].sum()
            st.line_chart(daily_sales, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏪 产品类别销售额")
        category_sales = filtered_df.groupby("category")["revenue"].sum().sort_values(ascending=False)
        st.bar_chart(category_sales, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🌍 城市销售分布")
        city_sales = filtered_df.groupby("city")["revenue"].sum().sort_values(ascending=False)
        st.bar_chart(city_sales, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("👥 客户类型分布")
        customer_dist = filtered_df["customer_type"].value_counts()
        st.bar_chart(customer_dist, color="#4a9eff", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
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
    
    # 日期筛选（有日期时才显示）
    if not df["date"].isna().all():
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
