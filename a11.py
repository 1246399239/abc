import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
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

@st.cache_data
def load_data():
    """加载销售数据"""
    try:
        # 尝试加载Excel文件
        df = pd.read_excel("（商场销售数据）supermarket_sales.xlsx")
        
        # 数据预处理
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        elif 'date' in df.columns:
            df['Date'] = pd.to_datetime(df['date'])
        
        # 添加一些计算字段
        if 'Total' in df.columns:
            df['Revenue'] = df['Total']
        elif 'total' in df.columns:
            df['Revenue'] = df['total']
        
        return df
    except Exception as e:
        # 如果文件不存在或读取失败，生成示例数据
        st.warning(f"无法读取销售数据文件，使用示例数据。错误: {str(e)}")
        return generate_sample_data()

def generate_sample_data():
    """生成示例销售数据（优化版本，减少数据量）"""
    np.random.seed(42)
    
    # 生成日期范围（缩短为3个月，避免内存溢出）
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 产品类别
    categories = ['电子产品', '服装', '食品饮料', '家居用品', '运动户外', '美妆护肤']
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '重庆']
    
    data = []
    for date in date_range:
        # 每天生成较少的销售记录，避免内存问题
        daily_records = np.random.randint(20, 50)
        for _ in range(daily_records):
            category = np.random.choice(categories)
            city = np.random.choice(cities)
            
            # 根据类别设置不同的价格范围
            if category == '电子产品':
                unit_price = np.random.uniform(500, 5000)
            elif category == '服装':
                unit_price = np.random.uniform(100, 800)
            elif category == '食品饮料':
                unit_price = np.random.uniform(10, 200)
            elif category == '家居用品':
                unit_price = np.random.uniform(50, 1000)
            elif category == '运动户外':
                unit_price = np.random.uniform(200, 2000)
            else:  # 美妆护肤
                unit_price = np.random.uniform(50, 500)
            
            quantity = np.random.randint(1, 10)
            total = unit_price * quantity
            
            # 客户评分
            rating = np.random.uniform(3.0, 5.0)
            
            data.append({
                'Date': date,
                'Category': category,
                'City': city,
                'Unit_Price': round(unit_price, 2),
                'Quantity': quantity,
                'Revenue': round(total, 2),
                'Rating': round(rating, 1),
                'Customer_Type': np.random.choice(['会员', '普通客户']),
                'Payment_Method': np.random.choice(['现金', '信用卡', '移动支付'])
            })
    
    df = pd.DataFrame(data)
    return df

def create_kpi_metrics(df, filtered_df):
    """创建KPI指标（修复计算逻辑）"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_df['Revenue'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">总销售额</div>
            <div class="metric-value">¥ {total_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rating = filtered_df['Rating'].mean() if 'Rating' in filtered_df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">顾客评分的平均值</div>
            <div class="metric-value">{avg_rating:.1f} ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # 修复：每单平均销售额 = 总销售额 / 订单数
        avg_order_value = filtered_df['Revenue'].sum() / len(filtered_df) if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">每单的平均销售额</div>
            <div class="metric-value">¥ {avg_order_value:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_orders = len(filtered_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">订单总数</div>
            <div class="metric-value">{total_orders:,}</div>
        </div>
        """, unsafe_allow_html=True)

def create_charts(df):
    """创建图表（优化显示）"""
    
    # 第一行：时间趋势和类别分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 按日期销售趋势")
        
        # 按日期聚合销售额
        daily_sales = df.groupby('Date')['Revenue'].sum()
        
        # 使用Streamlit内置的线图
        st.line_chart(daily_sales, color="#4a9eff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏪 按产品类别的销售额")
        
        # 按类别聚合销售额
        category_sales = df.groupby('Category')['Revenue'].sum()
        
        # 使用Streamlit内置的柱状图
        st.bar_chart(category_sales, color="#4a9eff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 第二行：地区分析和支付方式
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🌍 按城市销售分布")
        
        if 'City' in df.columns and len(df) > 0:
            city_sales = df.groupby('City')['Revenue'].sum().sort_values(ascending=False).head(10)
            st.bar_chart(city_sales, color="#4a9eff")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💳 支付方式分析")
        
        if 'Payment_Method' in df.columns and len(df) > 0:
            payment_dist = df['Payment_Method'].value_counts()
            st.bar_chart(payment_dist, color="#4a9eff")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """主函数"""
    # 标题
    st.markdown('<h1 class="main-title">📊 销售仪表板</h1>', unsafe_allow_html=True)
    
    # 加载数据
    df = load_data()
    
    # 侧边栏筛选器
    st.sidebar.header("🔍 数据筛选")
    
    # 日期范围筛选（修复核心问题）
    df_filtered = df.copy()
    if 'Date' in df.columns and len(df) > 0:
        try:
            # 获取最小和最大日期
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            
            # 日期输入控件
            date_range = st.sidebar.date_input(
                "选择日期范围",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            # 处理日期筛选
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                # 正确的日期筛选方式
                df_filtered = df[
                    (df['Date'] >= pd.to_datetime(start_date)) & 
                    (df['Date'] <= pd.to_datetime(end_date))
                ]
        except Exception as e:
            st.sidebar.error(f"日期筛选错误: {str(e)}")
    
    # 类别筛选
    if 'Category' in df.columns and len(df) > 0:
        categories = st.sidebar.multiselect(
            "选择产品类别",
            options=df['Category'].unique(),
            default=df['Category'].unique()
        )
        df_filtered = df_filtered[df_filtered['Category'].isin(categories)]
    
    # 城市筛选
    if 'City' in df.columns and len(df) > 0:
        cities = st.sidebar.multiselect(
            "选择城市",
            options=df['City'].unique(),
            default=df['City'].unique()
        )
        df_filtered = df_filtered[df_filtered['City'].isin(cities)]
    
    # 客户类型筛选（新增）
    if 'Customer_Type' in df.columns and len(df) > 0:
        customer_types = st.sidebar.multiselect(
            "选择客户类型",
            options=df['Customer_Type'].unique(),
            default=df['Customer_Type'].unique()
        )
        df_filtered = df_filtered[df_filtered['Customer_Type'].isin(customer_types)]
    
    # 显示数据概览
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 数据概览")
    st.sidebar.write(f"总记录数: {len(df):,}")
    st.sidebar.write(f"筛选后记录数: {len(df_filtered):,}")
    if 'Date' in df.columns and len(df) > 0:
        st.sidebar.write(f"数据时间范围: {df['Date'].min().strftime('%Y-%m-%d')} 至 {df['Date'].max().strftime('%Y-%m-%d')}")
    
    # 空数据处理
    if len(df_filtered) == 0:
        st.warning("⚠️ 筛选条件下没有找到数据，请调整筛选条件！")
        return
    
    # 创建KPI指标
    create_kpi_metrics(df, df_filtered)
    
    # 创建图表
    create_charts(df_filtered)
    
    # 数据表格
    st.markdown("---")
    st.subheader("📋 详细数据")
    
    # 显示筛选后的数据
    st.dataframe(
        df_filtered.head(1000),  # 限制显示1000行以提高性能
        use_container_width=True,
        hide_index=True
    )
    
    # 下载按钮
    csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下载筛选数据 (CSV)",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
