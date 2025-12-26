import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 页面配置（保持原功能）
st.set_page_config(
    page_title="销售数据仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式（保持原样式）
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background-color: #0e1117;
        color: #f0f0f0;
    }
    
    /* 标题样式 */
    .main-title {
        text-align: center;
        color: #4a9eff;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .metric-title {
        color: #aaaaaa;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #4a9eff;
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    
    /* 图表容器样式 */
    .chart-container {
        background-color: #262730;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 调整图表颜色 */
    [data-testid="stLineChart"], [data-testid="stBarChart"] {
        background-color: #262730;
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 缓存数据加载（增加文件上传支持）
@st.cache_data(show_spinner="正在加载数据...")
def load_data(uploaded_file=None, default_path="（商场销售数据）supermarket_sales.xlsx"):
    """加载销售数据：支持上传文件/默认文件/示例数据"""
    try:
        # 1. 优先使用用户上传的文件
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file, engine="openpyxl")  # 显式指定引擎，避免兼容问题
            st.success("✅ 成功加载上传的Excel文件")
        # 2. 无上传文件时，尝试加载默认本地文件
        else:
            df = pd.read_excel(default_path, engine="openpyxl")
            st.success(f"✅ 成功加载本地文件：{default_path}")
        
        # 数据标准化：处理字段名（去除空格、小写化后匹配）
        df.columns = [col.strip().lower() for col in df.columns]  # 字段名统一为小写+去空格
        standardized_df = standardize_fields(df)
        return standardized_df
    
    # 细分异常处理，给出具体提示
    except FileNotFoundError:
        st.warning(f"⚠️ 本地文件 '{default_path}' 未找到，将使用示例数据")
        return generate_sample_data()
    except Exception as e:
        st.error(f"❌ 数据加载失败：{str(e)}")
        st.info("💡 建议检查：1. Excel文件格式是否正确（.xlsx）；2. 文件是否损坏；3. 字段是否包含日期、销售额等关键信息")
        return generate_sample_data()

def standardize_fields(df):
    """标准化关键字段：确保Date、Revenue、Unit_Price等字段存在"""
    # 1. 日期字段标准化（支持date、transaction date等常见命名）
    date_cols = [col for col in df.columns if "date" in col]
    if date_cols:
        df["date"] = pd.to_datetime(df[date_cols[0]], errors="coerce")  # 转换失败的日期设为NaT
        df = df.dropna(subset=["date"])  # 删除无效日期行
    else:
        st.warning("⚠️ 数据中未找到日期字段，将无法进行日期筛选")
    
    # 2. 销售额字段标准化（支持total、revenue、sales等）
    revenue_cols = [col for col in df.columns if any(key in col for key in ["total", "revenue", "sales"])]
    if revenue_cols:
        df["revenue"] = pd.to_numeric(df[revenue_cols[0]], errors="coerce").fillna(0)  # 转换为数值，缺失值填0
    else:
        # 若无销售额字段，尝试用单价×数量计算
        if "unit_price" in df.columns and "quantity" in df.columns:
            df["revenue"] = df["unit_price"] * df["quantity"]
            st.info("💡 数据中无直接销售额字段，已通过「单价×数量」自动计算")
        else:
            st.warning("⚠️ 数据中无销售额、单价、数量字段，将默认销售额为0")
            df["revenue"] = 0
    
    # 3. 补充其他关键字段（无则创建空字段，避免后续报错）
    required_fields = ["category", "city", "customer_type", "payment_method", "rating", "unit_price", "quantity"]
    for field in required_fields:
        if field not in df.columns:
            df[field] = "未知" if field in ["category", "city", "customer_type", "payment_method"] else 0
            st.warning(f"⚠️ 数据中缺少 '{field}' 字段，已填充默认值")
    
    return df

def generate_sample_data():
    """生成示例销售数据（保持原逻辑，增加字段标准化）"""
    np.random.seed(42)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    categories = ['电子产品', '服装', '食品饮料', '家居用品', '运动户外', '美妆护肤']
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '重庆']
    
    data = []
    for date in date_range:
        daily_records = np.random.randint(20, 50)
        for _ in range(daily_records):
            category = np.random.choice(categories)
            city = np.random.choice(cities)
            
            # 按类别设置单价
            price_ranges = {
                '电子产品': (500, 5000), '服装': (100, 800), '食品饮料': (10, 200),
                '家居用品': (50, 1000), '运动户外': (200, 2000), '美妆护肤': (50, 500)
            }
            unit_price = np.random.uniform(*price_ranges[category])
            quantity = np.random.randint(1, 10)
            revenue = unit_price * quantity
            
            data.append({
                'date': date,
                'category': category,
                'city': city,
                'unit_price': round(unit_price, 2),
                'quantity': quantity,
                'revenue': round(revenue, 2),
                'rating': round(np.random.uniform(3.0, 5.0), 1),
                'customer_type': np.random.choice(['会员', '普通客户']),
                'payment_method': np.random.choice(['现金', '信用卡', '移动支付'])
            })
    
    df = pd.DataFrame(data)
    st.info("ℹ️ 当前使用示例数据（2024年1-3月销售记录）")
    return df

def create_kpi_metrics(filtered_df):
    """创建KPI指标（优化空值处理和提示）"""
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. 总销售额
    total_revenue = filtered_df['revenue'].sum()
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">总销售额</div>
            <div class="metric-value">¥ {total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 2. 顾客平均评分（无评分时显示提示）
    avg_rating = filtered_df['rating'].mean() if filtered_df['rating'].nunique() > 1 else "无数据"
    with col2:
        value_display = f"{avg_rating:.1f} ⭐" if isinstance(avg_rating, (int, float)) else avg_rating
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">顾客平均评分</div>
            <div class="metric-value">{value_display}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 3. 每单平均销售额（避免除以0）
    avg_order_value = filtered_df['revenue'].sum() / len(filtered_df) if len(filtered_df) > 0 else 0
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">每单平均销售额</div>
            <div class="metric-value">¥ {avg_order_value:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 4. 订单总数
    total_orders = len(filtered_df)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">订单总数</div>
            <div class="metric-value">{total_orders:,}</div>
        </div>
        """, unsafe_allow_html=True)

def create_charts(filtered_df):
    """创建图表（优化数据为空时的提示）"""
    # 第一行：时间趋势 + 产品类别
    col1, col2 = st.columns(2)
    
    # 1. 按日期销售趋势（仅当有日期字段时显示）
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 按日期销售趋势")
        if "date" in filtered_df.columns and len(filtered_df) > 0:
            daily_sales = filtered_df.groupby('date')['revenue'].sum()
            st.line_chart(daily_sales, color="#4a9eff", use_container_width=True)
        else:
            st.info("⚠️ 无有效日期数据，无法显示销售趋势")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. 按产品类别销售额
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏪 按产品类别的销售额")
        if filtered_df['category'].nunique() > 1:
            category_sales = filtered_df.groupby('category')['revenue'].sum().sort_values(ascending=False)
            st.bar_chart(category_sales, color="#4a9eff", use_container_width=True)
        else:
            st.info("⚠️ 产品类别数据不足，无法显示类别分析")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 第二行：城市分布 + 支付方式
    col3, col4 = st.columns(2)
    
    # 3. 按城市销售分布（去除head(10)，显示所有城市）
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🌍 按城市销售分布")
        if filtered_df['city'].nunique() > 1:
            city_sales = filtered_df.groupby('city')['revenue'].sum().sort_values(ascending=False)
            st.bar_chart(city_sales, color="#4a9eff", use_container_width=True)
        else:
            st.info("⚠️ 城市数据不足，无法显示地区分析")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. 支付方式分析
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💳 支付方式分析")
        if filtered_df['payment_method'].nunique() > 1:
            payment_dist = filtered_df['payment_method'].value_counts()
            st.bar_chart(payment_dist, color="#4a9eff", use_container_width=True)
        else:
            st.info("⚠️ 支付方式数据不足，无法显示支付分析")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """主函数（优化筛选逻辑和交互）"""
    # 标题
    st.markdown('<h1 class="main-title">📊 销售仪表板</h1>', unsafe_allow_html=True)
    
    # 侧边栏：文件上传（新增）
    st.sidebar.header("📁 文件上传")
    uploaded_file = st.sidebar.file_uploader("选择Excel文件（.xlsx）", type="xlsx")
    
    # 加载数据（支持上传/默认/示例）
    df = load_data(uploaded_file)
    df_filtered = df.copy()
    
    # 侧边栏：筛选器（优化容错）
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 数据筛选")
    
    # 1. 日期筛选（仅当有日期字段时显示）
    if "date" in df.columns and len(df) > 0:
        try:
            min_date = df['date'].min().date()
            max_date = df['date'].max().date()
            date_range = st.sidebar.date_input(
                "选择日期范围",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            # 处理日期筛选：仅当选择完整范围时应用
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                df_filtered = df_filtered[
                    (df_filtered['date'] >= pd.to_datetime(start_date)) & 
                    (df_filtered['date'] <= pd.to_datetime(end_date))
                ]
        except Exception as e:
            st.sidebar.error(f"日期筛选错误：{str(e)}")
    
    # 2. 产品类别筛选（未选中时不筛选）
    categories = st.sidebar.multiselect(
        "选择产品类别",
        options=df['category'].unique(),
        default=df['category'].unique()
    )
    if categories:  # 仅当选中非空时应用筛选
        df_filtered = df_filtered[df_filtered['category'].isin(categories)]
    
    # 3. 城市筛选（未选中时不筛选）
    cities = st.sidebar.multiselect(
        "选择城市",
        options=df['city'].unique(),
        default=df['city'].unique()
    )
    if cities:
        df_filtered = df_filtered[df_filtered['city'].isin(cities)]
    
    # 4. 客户类型筛选（未选中时不筛选）
    customer_types = st.sidebar.multiselect(
        "选择客户类型",
        options=df['customer_type'].unique(),
        default=df['customer_type'].unique()
    )
    if customer_types:
        df_filtered = df_filtered[df_filtered['customer_type'].isin(customer_types)]
    
    # 侧边栏：数据概览（增加筛选后日期范围）
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 数据概览")
    st.sidebar.write(f"总记录数: {len(df):,}")
    st.sidebar.write(f"筛选后记录数: {len(df_filtered):,}")
    if "date" in df.columns:
        st.sidebar.write(f"原始时间范围: {df['date'].min().strftime('%Y-%m-%d')} 至 {df['date'].max().strftime('%Y-%m-%d')}")
        if len(df_filtered) > 0:
            st.sidebar.write(f"筛选后时间范围: {df_filtered['date'].min().strftime('%Y-%m-%d')} 至 {df_filtered['date'].max().strftime('%Y-%m-%d')}")
    
    # 空数据处理（优化提示）
    if len(df_filtered) == 0:
        st.warning("⚠️ 筛选条件下无匹配数据，请调整筛选选项（如取消部分类别/城市限制）")
        return
    
    # 生成KPI和图表
    create_kpi_metrics(df_filtered)
    st.markdown("---")
    create_charts(df_filtered)
    
    # 详细数据和下载（保持原功能）
    st.markdown("---")
    st.subheader("📋 详细数据（前1000行）")
    st.dataframe(
        df_filtered.head(1000).rename(columns=str.title),  # 列名首字母大写，更美观
        use_container_width=True,
        hide_index=True
    )
    
    # 下载CSV（支持中文）
    csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下载筛选数据 (CSV)",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
