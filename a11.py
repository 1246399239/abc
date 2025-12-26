import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

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
    .sidebar .sidebar-content {
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
    except FileNotFoundError:
        # 如果文件不存在，生成示例数据
        st.warning("未找到销售数据文件，使用示例数据")
        return generate_sample_data()

def generate_sample_data():
    """生成示例销售数据"""
    np.random.seed(42)
    
    # 生成日期范围
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 产品类别
    categories = ['电子产品', '服装', '食品饮料', '家居用品', '运动户外', '美妆护肤']
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '重庆']
    
    data = []
    for date in date_range:
        # 每天生成多条销售记录
        daily_records = np.random.randint(50, 200)
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
    
    return pd.DataFrame(data)

def create_kpi_metrics(df, filtered_df):
    """创建KPI指标"""
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
        daily_avg = filtered_df.groupby('Date')['Revenue'].sum().mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">每单的平均销售额</div>
            <div class="metric-value">¥ {daily_avg:.0f}</div>
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
    """创建图表"""
    
    # 第一行：时间趋势和类别分析
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 按小时销售趋势的销售额")
        
        # 按日期聚合销售额
        daily_sales = df.groupby('Date')['Revenue'].sum().reset_index()
        
        fig_trend = px.line(
            daily_sales, 
            x='Date', 
            y='Revenue',
            title="",
            color_discrete_sequence=['#4a9eff']
        )
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333')
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏪 按产品类别的销售额")
        
        # 按类别聚合销售额
        category_sales = df.groupby('Category')['Revenue'].sum().sort_values(ascending=True)
        
        fig_category = px.bar(
            x=category_sales.values,
            y=category_sales.index,
            orientation='h',
            title="",
            color=category_sales.values,
            color_continuous_scale='Blues'
        )
        fig_category.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333'),
            showlegend=False
        )
        st.plotly_chart(fig_category, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 第二行：地区分析和支付方式
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🌍 按城市销售分布")
        
        if 'City' in df.columns:
            city_sales = df.groupby('City')['Revenue'].sum().sort_values(ascending=False).head(10)
            
            fig_city = px.pie(
                values=city_sales.values,
                names=city_sales.index,
                title="",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_city.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_city, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💳 支付方式分析")
        
        if 'Payment_Method' in df.columns:
            payment_dist = df['Payment_Method'].value_counts()
            
            fig_payment = px.bar(
                x=payment_dist.index,
                y=payment_dist.values,
                title="",
                color=payment_dist.values,
                color_continuous_scale='Viridis'
            )
            fig_payment.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis=dict(gridcolor='#333333'),
                yaxis=dict(gridcolor='#333333'),
                showlegend=False
            )
            st.plotly_chart(fig_payment, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """主函数"""
    # 标题
    st.markdown('<h1 class="main-title">📊 销售仪表板</h1>', unsafe_allow_html=True)
    
    # 加载数据
    df = load_data()
    
    # 侧边栏筛选器
    st.sidebar.header("🔍 数据筛选")
    
    # 日期范围筛选
    if 'Date' in df.columns:
        date_range = st.sidebar.date_input(
            "选择日期范围",
            value=(df['Date'].min(), df['Date'].max()),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )
        
        # 确保date_range是元组
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[(df['Date'] >= pd.Timestamp(start_date)) & 
                           (df['Date'] <= pd.Timestamp(end_date))]
        else:
            df_filtered = df
    else:
        df_filtered = df
    
    # 类别筛选
    if 'Category' in df.columns:
        categories = st.sidebar.multiselect(
            "选择产品类别",
            options=df['Category'].unique(),
            default=df['Category'].unique()
        )
        df_filtered = df_filtered[df_filtered['Category'].isin(categories)]
    
    # 城市筛选
    if 'City' in df.columns:
        cities = st.sidebar.multiselect(
            "选择城市",
            options=df['City'].unique(),
            default=df['City'].unique()
        )
        df_filtered = df_filtered[df_filtered['City'].isin(cities)]
    
    # 显示数据概览
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 数据概览")
    st.sidebar.write(f"总记录数: {len(df):,}")
    st.sidebar.write(f"筛选后记录数: {len(df_filtered):,}")
    st.sidebar.write(f"数据时间范围: {df['Date'].min().strftime('%Y-%m-%d')} 至 {df['Date'].max().strftime('%Y-%m-%d')}")
    
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
        use_container_width=True
    )
    
    # 下载按钮
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 下载筛选数据 (CSV)",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
