import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt

# 设置页面配置
st.set_page_config(
    page_title="销售数据仪表板",
    page_icon="📊",
    layout="wide"
)

# 生成模拟销售数据
@st.cache_data
def generate_sales_data():
    """生成模拟销售数据"""
    np.random.seed(42)
    
    # 基础设置
    cities = ['太原', '临汾', '大同']
    customer_types = ['会员用户', '普通用户']
    genders = ['男性', '女性']
    product_categories = ['食品饮料', '运动旅行', '电子配件', '时尚配饰', '家居生活', '健康美容']
    
    # 生成1000条销售记录
    n_records = 1000
    data = {
        'date': [datetime.now() - timedelta(days=np.random.randint(1, 30)) for _ in range(n_records)],
        'city': np.random.choice(cities, n_records),
        'customer_type': np.random.choice(customer_types, n_records),
        'gender': np.random.choice(genders, n_records),
        'product_category': np.random.choice(product_categories, n_records),
        'sales_amount': np.random.uniform(50, 1000, n_records),
        'rating': np.random.uniform(3, 10, n_records),
        'hour': np.random.randint(0, 24, n_records)
    }
    
    df = pd.DataFrame(data)
    return df

def main():
    """主函数：构建销售数据仪表板"""
    # 加载数据
    df = generate_sales_data()
    
    st.title("📊 销售数据仪表板")
    
    # 侧边栏筛选器
    st.sidebar.header("🔍 数据筛选")
    
    # 城市筛选（多选）
    selected_cities = st.sidebar.multiselect(
        "选择城市:",
        options=sorted(df['city'].unique()),
        default=sorted(df['city'].unique())
    )
    
    # 顾客类型筛选（多选）
    selected_customer_types = st.sidebar.multiselect(
        "选择顾客类型:",
        options=sorted(df['customer_type'].unique()),
        default=sorted(df['customer_type'].unique())
    )
    
    # 性别筛选（多选）
    selected_genders = st.sidebar.multiselect(
        "选择性别:",
        options=sorted(df['gender'].unique()),
        default=sorted(df['gender'].unique())
    )
    
    # 应用筛选条件
    filtered_df = df[
        (df['city'].isin(selected_cities)) &
        (df['customer_type'].isin(selected_customer_types)) &
        (df['gender'].isin(selected_genders))
    ].copy()
    
    # 显示当前筛选状态
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 当前筛选状态")
    st.sidebar.write(f"**城市:** {', '.join(selected_cities) if selected_cities else '全部'}")
    st.sidebar.write(f"**顾客类型:** {', '.join(selected_customer_types) if selected_customer_types else '全部'}")
    st.sidebar.write(f"**性别:** {', '.join(selected_genders) if selected_genders else '全部'}")
    st.sidebar.write(f"**数据量:** {len(filtered_df)} 条记录")
    
    # KPI指标卡片
    st.markdown("---")
    st.subheader("📈 核心指标")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_sales = filtered_df['sales_amount'].sum()
        st.metric(
            label="💰 总销售额",
            value=f"¥{total_sales:,.0f}",
            delta=f"{((total_sales / 300000) - 1) * 100:.1f}%" if total_sales > 300000 else None
        )
    
    with col2:
        avg_rating = filtered_df['rating'].mean()
        st.metric(
            label="⭐ 平均评分",
            value=f"{avg_rating:.1f}",
            delta=f"{avg_rating - 6.5:+.1f}" if avg_rating != 6.5 else None
        )
        
        # 显示星级
        stars = "⭐" * int(avg_rating)
        st.write(f"**{stars}**")
    
    with col3:
        avg_order_value = filtered_df['sales_amount'].mean()
        st.metric(
            label="🛒 平均订单额",
            value=f"¥{avg_order_value:.0f}",
            delta=f"{avg_order_value - 300:+.0f}" if avg_order_value != 300 else None
        )
    
    # 图表区域
    st.markdown("---")
    st.subheader("📊 销售数据分析")
    
    col4, col5 = st.columns(2)
    
    with col4:
        # 按小时划分的销售额 - 使用Altair
        st.write("#### 🕒 按小时划分的销售额")
        
        # 计算小时销售额
        hourly_sales = filtered_df.groupby('hour')['sales_amount'].sum().reset_index()
        hourly_sales = hourly_sales.sort_values('hour')
        
        # 创建Altair图表
        hourly_chart = alt.Chart(hourly_sales).mark_bar(color='#3498db').encode(
            x=alt.X('hour:O', title='小时', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('sales_amount:Q', title='销售额 (元)')
        ).properties(
            width=600,
            height=400
        )
        
        st.altair_chart(hourly_chart, use_container_width=True)
    
    with col5:
        # 按产品类型划分的销售额 - 使用Altair
        st.write("#### 📦 按产品类型划分的销售额")
        
        # 计算产品类型销售额
        category_sales = filtered_df.groupby('product_category')['sales_amount'].sum().reset_index()
        category_sales = category_sales.sort_values('sales_amount', ascending=True)
        
        # 创建水平条形图
        category_chart = alt.Chart(category_sales).mark_bar(color='#2ecc71').encode(
            y=alt.Y('product_category:N', title='产品类型', sort='-x'),
            x=alt.X('sales_amount:Q', title='销售额 (元)'),
            tooltip=['product_category', 'sales_amount']
        ).properties(
            width=600,
            height=400
        )
        
        st.altair_chart(category_chart, use_container_width=True)
    
    # 数据详情表格
    st.markdown("---")
    st.subheader("📋 销售数据详情")
    
    # 计算各产品类型的统计数据
    summary_data = []
    for category in sorted(filtered_df['product_category'].unique()):
        category_data = filtered_df[filtered_df['product_category'] == category]
        if len(category_data) > 0:
            category_sales_total = category_data['sales_amount'].sum()
            category_avg_rating = category_data['rating'].mean()
            category_order_count = len(category_data)
            category_avg_sales = category_sales_total / category_order_count
            
            # 判断趋势
            overall_avg_sales = filtered_df['sales_amount'].mean()
            trend = '📈 上升' if category_avg_sales > overall_avg_sales else '📉 下降'
            
            summary_data.append({
                '产品类型': category,
                '总销售额': f"¥{category_sales_total:,.0f}",
                '平均评分': f"{category_avg_rating:.1f}",
                '订单数量': f"{category_order_count}",
                '趋势': trend
            })
    
    # 创建数据框并显示
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(
        summary_df,
        use_container_width=True,
        column_config={
            "产品类型": st.column_config.TextColumn("产品类型", width="medium"),
            "总销售额": st.column_config.TextColumn("总销售额", width="medium"),
            "平均评分": st.column_config.TextColumn("平均评分", width="small"),
            "订单数量": st.column_config.TextColumn("订单数量", width="small"),
            "趋势": st.column_config.TextColumn("趋势", width="small")
        },
        hide_index=True
    )
    
    # 原始数据查看（可选）
    with st.expander("📄 查看原始数据"):
        st.dataframe(filtered_df, use_container_width=True)
    
    # 数据统计信息
    st.markdown("---")
    st.subheader("📈 数据统计信息")
    
    col6, col7, col8 = st.columns(3)
    
    with col6:
        st.write("**📅 数据时间范围**")
        st.write(f"开始日期: {filtered_df['date'].min().strftime('%Y-%m-%d')}")
        st.write(f"结束日期: {filtered_df['date'].max().strftime('%Y-%m-%d')}")
    
    with col7:
        st.write("**👥 客户分布**")
        customer_dist = filtered_df['customer_type'].value_counts()
        for customer_type, count in customer_dist.items():
            percentage = (count / len(filtered_df)) * 100
            st.write(f"{customer_type}: {count} ({percentage:.1f}%)")
    
    with col8:
        st.write("**🌍 城市分布**")
        city_dist = filtered_df['city'].value_counts()
        for city, count in city_dist.items():
            percentage = (count / len(filtered_df)) * 100
            st.write(f"{city}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
