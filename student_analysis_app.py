import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
from PIL import Image

# 页面配置
st.set_page_config(
    page_title="学生成绩分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv('student_data_adjusted_rounded.csv')
    return df

# 加载模型
@st.cache_resource
def load_model():
    try:
        with open('student_score_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except:
        return None

# 侧边栏导航
st.sidebar.markdown("## 🎓 学生成绩分析平台")
page = st.sidebar.radio(
    "选择功能模块",
    ["📖 项目介绍", "📊 专业数据分析", "🔮 期末成绩预测"]
)

# 加载数据
df = load_data()

# ==================== 界面1：项目介绍 ====================
if page == "📖 项目介绍":
    st.markdown('<h1 class="main-title">🎓 学生成绩分析与预测系统</h1>', unsafe_allow_html=True)
    
    # 项目概述
    st.markdown("---")
    st.markdown("## 📋 项目概述")
    st.write("""
    本项目是一个基于Streamlit开发的课程学生成绩分析平台，通过可视化展示学习数据，
    并利用机器学习模型预测学生成绩。系统整合了数据分析、可视化和机器学习技术，
    为教育工作者提供全面的学生学业表现分析工具。
    """)
    
    # 项目目标
    st.markdown("---")
    st.markdown("## 🎯 项目目标")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 目标一</h3>
            <p><strong>分析关键因素</strong></p>
            <ul>
                <li>识别影响成绩的主要因素</li>
                <li>探索学习行为与成绩关系</li>
                <li>提供数据驱动的洞察</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 目标二</h3>
            <p><strong>可视化展示</strong></p>
            <ul>
                <li>多维度数据可视化</li>
                <li>直观展示学业表现</li>
                <li>专业对比分析</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔮 目标三</h3>
            <p><strong>成绩预测</strong></p>
            <ul>
                <li>机器学习模型预测</li>
                <li>个性化成绩评估</li>
                <li>及时干预建议</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 技术架构
    st.markdown("---")
    st.markdown("## 🛠️ 技术架构")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("**前端框架**\n\nStreamlit")
    with col2:
        st.info("**数据处理**\n\nPandas\nNumPy")
    with col3:
        st.info("**可视化**\n\nPlotly\nMatplotlib")
    with col4:
        st.info("**机器学习**\n\nScikit-learn\nRandomForest")
    
    # 主要功能
    st.markdown("---")
    st.markdown("## ✨ 主要功能")
    
    st.markdown("### 📊 专业数据分析")
    st.write("""
    - **数据统计表格**：展示各专业的平均学时、期中成绩和期末成绩
    - **性别比例分析**：双层柱状图展示各专业男女比例
    - **成绩对比分析**：折线图对比期中与期末成绩趋势
    - **出勤率分析**：柱状图展示各专业平均出勤率
    - **专业深度分析**：大数据管理专业的详细分析
    """)
    
    st.markdown("### 🔮 期末成绩预测")
    st.write("""
    - **多维度输入**：学号、性别、专业、学习时长、出勤率、期中成绩、作业完成率
    - **智能预测**：基于随机森林模型的成绩预测
    - **可视化反馈**：预测结果的直观展示
    - **激励机制**：根据预测结果展示恭喜或鼓励图片
    """)
    
    # 数据概览
    st.markdown("---")
    st.markdown("## 📊 数据概览")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("学生总数", f"{len(df):,}")
    with col2:
        st.metric("专业数量", df['专业'].nunique())
    with col3:
        st.metric("平均期末成绩", f"{df['期末考试分数'].mean():.2f}")
    with col4:
        st.metric("平均出勤率", f"{df['上课出勤率'].mean():.1%}")
    
    # 系统截图展示区域
    st.markdown("---")
    st.markdown("## 🖼️ 系统界面预览")
    st.info("💡 请使用左侧导航栏切换到不同功能模块，体验完整的分析和预测功能！")

# ==================== 界面2：专业数据分析 ====================
elif page == "📊 专业数据分析":
    st.markdown('<h1 class="main-title">📊 专业数据分析</h1>', unsafe_allow_html=True)
    
    # 1. 各专业统计表格
    st.markdown("### 1. 各专业男女性别比例")
    
    # 计算性别比例
    gender_stats = df.groupby(['专业', '性别']).size().unstack(fill_value=0)
    gender_stats['总人数'] = gender_stats.sum(axis=1)
    
    # 创建双层柱状图
    fig_gender = go.Figure()
    
    majors = gender_stats.index.tolist()
    male_counts = gender_stats['男'].tolist() if '男' in gender_stats.columns else [0] * len(majors)
    female_counts = gender_stats['女'].tolist() if '女' in gender_stats.columns else [0] * len(majors)
    
    fig_gender.add_trace(go.Bar(
        name='男',
        x=majors,
        y=male_counts,
        marker_color='lightblue',
        text=male_counts,
        textposition='auto',
    ))
    
    fig_gender.add_trace(go.Bar(
        name='女',
        x=majors,
        y=female_counts,
        marker_color='lightpink',
        text=female_counts,
        textposition='auto',
    ))
    
    fig_gender.update_layout(
        title='各专业男女性别比例',
        xaxis_title='专业',
        yaxis_title='人数',
        barmode='group',
        height=400,
        template='plotly_white'
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig_gender, use_container_width=True)
    with col2:
        st.markdown("#### 性别比例详情")
        st.dataframe(gender_stats, use_container_width=True)
    
    # 2. 各专业学习数据统计表
    st.markdown("---")
    st.markdown("### 2. 各专业学习数据统计")
    
    major_stats = df.groupby('专业').agg({
        '每周学习时长（小时）': 'mean',
        '期中考试分数': 'mean',
        '期末考试分数': 'mean'
    }).round(2)
    
    major_stats.columns = ['平均每周学时', '期中考试平均分', '期末考试平均分']
    major_stats = major_stats.reset_index()
    
    st.dataframe(major_stats, use_container_width=True, height=300)
    
    # 3. 各专业出勤率分析
    st.markdown("---")
    st.markdown("### 3. 各专业出勤率分析")
    
    attendance_stats = df.groupby('专业')['上课出勤率'].mean().sort_values(ascending=False)
    
    fig_attendance = px.bar(
        x=attendance_stats.index,
        y=attendance_stats.values * 100,
        labels={'x': '专业', 'y': '平均出勤率 (%)'},
        title='各专业平均上课出勤率',
        color=attendance_stats.values,
        color_continuous_scale='Viridis'
    )
    
    fig_attendance.update_traces(text=[f'{v:.1f}%' for v in attendance_stats.values * 100], textposition='outside')
    fig_attendance.update_layout(height=400, template='plotly_white', showlegend=False)
    
    st.plotly_chart(fig_attendance, use_container_width=True)
    
    # 4. 各专业成绩对比分析（折线图）
    st.markdown("---")
    st.markdown("### 4. 各专业出勤率分析")
    
    score_comparison = df.groupby('专业').agg({
        '期中考试分数': 'mean',
        '期末考试分数': 'mean'
    }).round(2)
    
    fig_scores = go.Figure()
    
    fig_scores.add_trace(go.Scatter(
        x=score_comparison.index,
        y=score_comparison['期中考试分数'],
        mode='lines+markers',
        name='期中考试分数',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10)
    ))
    
    fig_scores.add_trace(go.Scatter(
        x=score_comparison.index,
        y=score_comparison['期末考试分数'],
        mode='lines+markers',
        name='期末考试分数',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=10)
    ))
    
    fig_scores.update_layout(
        title='各专业期中与期末考试分数对比',
        xaxis_title='专业',
        yaxis_title='平均分数',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_scores, use_container_width=True)
    
    # 5. 大数据管理专业深度分析
    st.markdown("---")
    st.markdown("### 5. 大数据管理专业专项分析")
    
    bigdata_df = df[df['专业'] == '大数据管理']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_attendance = bigdata_df['上课出勤率'].mean()
        st.metric("平均出勤率", f"{avg_attendance:.1%}")
    
    with col2:
        avg_midterm = bigdata_df['期中考试分数'].mean()
        st.metric("平均期中成绩", f"{avg_midterm:.2f}")
    
    with col3:
        avg_final = bigdata_df['期末考试分数'].mean()
        st.metric("平均期末成绩", f"{avg_final:.2f}")
    
    # 大数据管理专业的出勤率与期末成绩关系
    col1, col2 = st.columns(2)
    
    with col1:
        # 出勤率分布直方图
        fig_hist = px.histogram(
            bigdata_df,
            x='上课出勤率',
            nbins=20,
            title='大数据管理专业出勤率分布',
            labels={'上课出勤率': '出勤率', 'count': '学生人数'},
            color_discrete_sequence=['#2ECC71']
        )
        fig_hist.update_layout(height=350, template='plotly_white')
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # 出勤率与期末成绩散点图
        fig_scatter = px.scatter(
            bigdata_df,
            x='上课出勤率',
            y='期末考试分数',
            title='大数据管理专业：出勤率 vs 期末成绩',
            labels={'上课出勤率': '出勤率', '期末考试分数': '期末成绩'},
            trendline='ols',
            color_discrete_sequence=['#3498DB']
        )
        fig_scatter.update_layout(height=350, template='plotly_white')
        st.plotly_chart(fig_scatter, use_container_width=True)

# ==================== 界面3：期末成绩预测 ====================
elif page == "🔮 期末成绩预测":
    st.markdown('<h1 class="main-title">🔮 期末成绩预测</h1>', unsafe_allow_html=True)
    
    st.info("💡 请输入学生的基本信息和学习数据，系统将预测该学生的期末考试分数。")
    
    # 加载模型
    model = load_model()
    
    if model is None:
        st.warning("⚠️ 预测模型未找到，请先运行 train_model.py 生成 student_score_model.pkl 文件。")
    
    # 输入表单
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("学号", value="2023000001", help="请输入10位学号")
            gender = st.selectbox("性别", ["男", "女"])
            major = st.selectbox("专业", sorted(df['专业'].unique()))
            study_hours = st.slider("每周学习时长（小时）", 5.0, 40.0, 20.0, 0.5)
        
        with col2:
            attendance = st.slider("上课出勤率", 0.0, 1.0, 0.85, 0.01, format="%.2f")
            midterm_score = st.slider("期中考试分数", 0.0, 100.0, 75.0, 0.5)
            homework_rate = st.slider("作业完成率", 0.0, 1.0, 0.85, 0.01, format="%.2f")
        
        submitted = st.form_submit_button("🔮 预测期末成绩", use_container_width=True)
    
    if submitted:
        if model is not None:
            # 准备预测数据
            # 性别编码
            gender_encoded = 1 if gender == "男" else 0
            
            # 专业编码（使用训练数据中的专业顺序）
            major_list = sorted(df['专业'].unique())
            major_encoded = major_list.index(major) if major in major_list else 0
            
            # 构建特征向量
            features = np.array([[gender_encoded, major_encoded, study_hours, 
                                 attendance, midterm_score, homework_rate]])
            
            # 预测
            try:
                predicted_score = model.predict(features)[0]
                predicted_score = max(0, min(100, predicted_score))  # 限制在0-100之间
                
                st.markdown("---")
                st.markdown("## 📊 预测结果")
                
                # 显示预测分数
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    if predicted_score >= 60:
                        st.success(f"### 🎉 预测期末成绩：{predicted_score:.2f} 分")
                        st.balloons()
                    else:
                        st.warning(f"### 📝 预测期末成绩：{predicted_score:.2f} 分")
                
                # 成绩评级
                if predicted_score >= 90:
                    grade = "优秀"
                    color = "#2ECC71"
                elif predicted_score >= 80:
                    grade = "良好"
                    color = "#3498DB"
                elif predicted_score >= 70:
                    grade = "中等"
                    color = "#F39C12"
                elif predicted_score >= 60:
                    grade = "及格"
                    color = "#E67E22"
                else:
                    grade = "不及格"
                    color = "#E74C3C"
                
                # 显示成绩条
                st.markdown(f"""
                <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;">
                    <h2 style="color: white; margin: 0;">成绩等级：{grade}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # 显示激励图片
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    if predicted_score >= 60:
                        st.markdown("### 🎊 恭喜！预测成绩及格！")
                        st.image("https://media.giphy.com/media/g9582DNuQppxC/giphy.gif", 
                                caption="继续保持，你很棒！", use_container_width=True)
                    else:
                        st.markdown("### 💪 加油！还有提升空间！")
                        st.image("https://media.giphy.com/media/9Jcw5pUQlgQLe5NonJ/giphy.gif", 
                                caption="不要气馁，继续努力！", use_container_width=True)
                
                # 学习建议
                st.markdown("---")
                st.markdown("## 💡 学习建议")
                
                suggestions = []
                
                if study_hours < 15:
                    suggestions.append("📚 建议增加每周学习时长，至少保持15小时以上")
                if attendance < 0.8:
                    suggestions.append("✅ 提高课堂出勤率，保持在80%以上")
                if homework_rate < 0.8:
                    suggestions.append("📝 按时完成作业，作业完成率应保持在80%以上")
                if midterm_score < 70:
                    suggestions.append("📖 加强基础知识学习，提高期中考试成绩")
                
                if suggestions:
                    for suggestion in suggestions:
                        st.warning(suggestion)
                else:
                    st.success("🌟 各项指标表现良好，继续保持！")
                
            except Exception as e:
                st.error(f"预测过程中出现错误：{str(e)}")
        else:
            st.error("模型未加载，无法进行预测")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p>🎓 学生成绩分析与预测系统 | 基于 Streamlit 开发</p>
    <p>© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
