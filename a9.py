import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, date
from PIL import Image

# ===================== 页面配置 =====================
st.set_page_config(
    page_title="多功能应用集合",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== 侧边栏导航 =====================
st.sidebar.title("🚀 应用导航")
st.sidebar.markdown("---")

# 页面选项
pages = {
    "🏠 首页": "home",
    "⚔️ 威龙干员档案": "vyron_profile", 
    "🍜 南宁美食仪表盘": "nanning_food",
    "🖼️ 相册浏览": "photo_gallery",
    "🎵 音乐播放器": "music_player", 
    "🎬 视频播放器": "video_player",
    "📄 简历生成器": "resume_generator"
}

# 侧边栏页面选择
selected_page = st.sidebar.selectbox(
    "选择应用",
    options=list(pages.keys()),
    index=0
)

# 获取当前页面标识
current_page = pages[selected_page]

# 侧边栏信息
st.sidebar.markdown("---")
st.sidebar.info("💡 **使用说明**\n\n选择上方应用即可切换到对应功能页面")
st.sidebar.markdown("---")
st.sidebar.markdown("**🔧 技术栈**")
st.sidebar.markdown("- Streamlit")
st.sidebar.markdown("- Pandas") 
st.sidebar.markdown("- Altair")
st.sidebar.markdown("- PIL")

# ===================== 页面内容 =====================

if current_page == "home":
    # ===================== 首页 =====================
    st.title("🚀 多功能应用集合")
    st.markdown("### 欢迎使用多功能应用平台！")
    
    st.markdown("---")
    
    # 应用介绍卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3>⚔️ 威龙干员档案</h3>
            <p>游戏角色数字档案展示系统，包含技能矩阵、任务日志等详细信息</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3>🍜 南宁美食仪表盘</h3>
            <p>数据可视化展示南宁美食信息，包含地图、评分、价格走势等</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3>🖼️ 相册浏览</h3>
            <p>图片轮播展示系统，支持上一张/下一张切换功能</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3>🎵 音乐播放器</h3>
            <p>在线音乐播放系统，支持音频播放和歌曲切换</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 20px; border-radius: 10px; color: black; text-align: center;">
            <h3>🎬 视频播放器</h3>
            <p>视频播放系统，支持多集视频播放和集数选择</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                    padding: 20px; border-radius: 10px; color: black; text-align: center;">
            <h3>📄 简历生成器</h3>
            <p>个人简历制作工具，支持实时预览和多项信息编辑</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 使用统计
    st.markdown("### 📊 平台统计")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("总应用数", "6", "个")
    
    with col_stat2:
        st.metric("技术栈", "4", "种")
    
    with col_stat3:
        st.metric("功能模块", "15+", "个")
    
    with col_stat4:
        st.metric("代码行数", "800+", "行")

elif current_page == "vyron_profile":
    # ===================== 威龙干员档案页面 =====================
    # 全局样式自定义
    st.markdown("""
    <style>
    /* 1. 全局重置：统一字体和文字颜色 */
    * {
        color: #ffffff !important;
        font-family: 'Consolas', 'Microsoft YaHei', sans-serif !important;
    }

    /* 2. 页面背景：设置为纯黑色 */
    .stApp {
        background-color: #000000 !important;
    }

    /* 3. 标题样式：添加底部边框、内边距和间距 */
    .stTitle {
        border-bottom: 2px solid #40a9ff;
        padding-bottom: 8px;
        margin-bottom: 25px;
        font-weight: bold;
        font-size: 1.5em;
    }

    /* 4. 小标题样式：设置上下间距、字体粗细和大小 */
    .stHeader {
        margin-top: 30px;
        margin-bottom: 15px;
        font-weight: bold;
        font-size: 1.2em;
    }

    /* 5. 战术技能矩阵（Metric组件）样式：深色背景+蓝色边框 */
    .stMetric {
        background-color: #111111;
        border: 1px solid #40a9ff;
        border-radius: 6px;
        padding: 15px;
        margin: 5px 0;
    }
    /* Metric组件的增量文字颜色：浅绿色 */
    .stMetric div[data-testid="stMetricDelta"] {
        color: #90ee90 !important;
    }

    /* 6. 代码块（pre+code）样式：纯黑底+浅蓝边框+左边界突出 */
    pre {
        background-color: #000000 !important;
        border: 1px solid #40a9ff !important;
        border-left: 6px solid #40a9ff !important;
        border-radius: 8px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
        overflow-x: auto !important; /* 适配长代码横向滚动 */
    }
    /* 代码文字样式：纯白字+等宽字体+增大行高 */
    code {
        color: #ffffff !important;
        font-size: 1.1em !important;
        line-height: 1.8 !important;
        font-family: 'Consolas', 'Monaco', monospace !important;
    }

    /* 7. 表格样式：深色背景+蓝色边框，单元格居中对齐 */
    .stTable {
        border: 1px solid #40a9ff;
        border-radius: 6px;
        background-color: #111111;
        width: 100%;
    }
    .stTable th, .stTable td {
        border: 1px solid #40a9ff;
        padding: 10px;
        text-align: center;
        font-size: 1em;
    }
    /* 表格表头样式：深色背景+加粗 */
    .stTable th {
        background-color: #1e293b;
        font-weight: bold;
    }

    /* 8. 链接样式：浅蓝色+下划线 */
    a {
        color: #40a9ff !important;
        text-decoration: underline !important;
    }

    /* 9. 说明文字（Caption）样式：设置字体大小和下间距 */
    .stCaption {
        font-size: 1em;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 页面布局控制
    main_col = st.columns([1, 8, 1])[1]

    # 主要内容区域
    with main_col:
        # 1. 页面主标题和副标题
        st.title("三角洲干员「威龙」数字档案", anchor="vyron-main")
        st.text("——G.T.I.亚洲分部突击兵战术档案 v1.0（2025年12月更新）")

        # 2. 基础信息模块
        st.header("一、基础信息 📋", anchor="basic-info")
        # 使用Markdown表格展示干员基础档案信息
        st.markdown("""
        | 档案项          | 详细信息                                                                 |
        |-----------------|--------------------------------------------------------------------------|
        | 干员代号        | 威龙（Vyron，源自希腊语"英雄"，象征高机动战术定位）                     |
        | 真实姓名        | 王宇昊                                                                   |
        | 所属阵营        | G.T.I.（全球战术干预组织）亚洲分部                                       |
        | 兵种类型        | 突击兵（专精载具破袭与快速突袭）                                         |
        | 核心装备        | 动能辅助系统、磁吸炸弹（代号"红包"）、QLL32肩射榴弹发射器（虎蹲炮）      |
        | 档案等级        | 机密（仅战术指挥层可见）                                                 |
        | 数据采集来源    | 寒沙行动实战记录、模拟训练系统、干员心理评估报告                         |
        """)

        # 3. 战术技能矩阵模块
        st.header("二、战术技能矩阵 🚀", anchor="skill-matrix")
        # 分三列展示技能指标，设置列间距为medium
        skill_col1, skill_col2, skill_col3 = st.columns(3, gap="medium")
        with skill_col1:
            # 动能辅助系统指标：效能值+增量+说明
            st.metric(
                label="动能辅助系统",
                value="92% 效能",
                delta="+8%（对比上季度）",
                help="喷气式单兵装置，支持快速位移与坠落缓冲"
            )
        with skill_col2:
            # 磁吸炸弹指标：破甲率+增量+说明
            st.metric(
                label="磁吸炸弹（载具破袭）",
                value="98% 破甲率",
                delta="+5%（适配新装甲）",
                help="吸附含铁表面，2颗可摧毁轻型载具"
            )
        with skill_col3:
            # 虎蹲炮指标：震慑效能+增量+说明
            st.metric(
                label="虎蹲炮（区域压制）",
                value="87% 震慑效能",
                delta="-3%（复杂地形修正）",
                help="维和镇暴专用，覆盖5米半径压制范围"
            )

        # 4. 实战任务日志模块
        st.header("三、实战任务日志 📅", anchor="mission-log")
        st.text("任务记录按季度分类，包含核心战术指标与完成状态")
        # 定义任务日志数据
        mission_data = {
            "任务编号": ["TA-20251005", "TA-20251012", "TA-20251101", "TA-20251115"],
            "任务名称": ["寒沙行动-载具攻坚", "城区渗透-人质解救", "边境维和-区域压制", "训练场模拟-新装备测试"],
            "任务状态": ["✅ 已完成", "✅ 已完成", "✅ 已完成", "🔄 进行中"],
            "任务难度": ["★★★★☆", "★★★★★", "★★★☆☆", "★★☆☆☆"],
            "完成率": ["100%", "98%", "100%", "75%"],
            "核心贡献": ["摧毁3辆敌方装甲车", "成功解救6名人质", "控制2个关键据点", "完成磁吸炸弹效能测试"]
        }
        # 设置任务季度为索引
        mission_index = pd.Series(["第1季度", "第1季度", "第2季度", "第2季度"], name="任务季度")
        mission_df = pd.DataFrame(mission_data, index=mission_index)
        # 展示任务日志表格
        st.table(mission_df)

        # 5. 战术数据采集代码模块
        st.header("四、战术数据采集代码 💻", anchor="code-snippet")
        st.caption("代码功能：从G.T.I.接口获取威龙干员实时战术数据（简化版）")
        # 定义代码内容：模拟获取任务日志数据的函数
        code_content = '''import pandas as pd
from datetime import datetime

def get_vyron_mission_data():
    """
    模拟获取威龙干员任务日志数据
    返回：结构化任务数据DataFrame
    """
    # 1. 定义任务数据（与档案中任务日志一致）
    mission_data = {
        "任务编号": ["TA-20251005", "TA-20251012", "TA-2025101", "TA-20251115"],
        "任务名称": ["寒沙行动-载具攻坚", "城区渗透-人质解救", "边境维和-区域压制", "训练场模拟-新装备测试"],
        "任务状态": ["✅ 已完成", "✅ 已完成", "✅ 已完成", "🔄 进行中"],
        "完成率": ["100%", "98%", "100%", "75%"]
    }
    # 2. 添加数据采集时间（数据预处理步骤）
    mission_index = pd.Series(["第1季度", "第1季度", "第2季度", "第2季度"], name="任务季度")
    df = pd.DataFrame(mission_data, index=mission_index)
    df["采集时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return df

# 调用函数生成任务日志数据
if __name__ == "__main__":
    vyron_mission_log = get_vyron_mission_data()
    print("威龙干员实战任务日志：")
    print(vyron_mission_log)
    # 保存为Excel（需安装openpyxl：pip install openpyxl）
    # vyron_mission_log.to_excel("威龙任务日志.xlsx", index=True)'''
        # 渲染原生代码块（使用HTML的pre和code标签，保留样式）
        st.markdown(f"<pre><code>{code_content}</code></pre>", unsafe_allow_html=True)

        # 6. 档案备注模块
        st.header("五、档案备注 ⚠️", anchor="notes")
        st.text("1. 任务日志表格采用静态Table格式，适配不同浏览器渲染，避免动态加载问题；")
        st.text("2. 技能矩阵效能值基于10次实战平均计算，复杂地形（雨林/城区）下允许±5%波动；")

elif current_page == "nanning_food":
    # ===================== 南宁美食仪表盘页面 =====================
    # 数据准备
    restaurants_data = [
        {
            "名称": "三品王(朝阳店)",
            "类型": "快餐",
            "评分": 4.3,
            "人均消费(元)": 15,
            "latitude": 22.812200,
            "longitude": 108.266629,
            "推荐菜品": ["原汤牛肉粉", "杂酱粉", "腐竹"],
            "拥挤程度": 0.85
        },
        {
            "名称": "柳厨螺蛳粉(中山路店)",
            "类型": "快餐",
            "评分": 4.5,
            "人均消费(元)": 13,
            "latitude": 22.809105,
            "longitude": 108.378664,
            "推荐菜品": ["经典螺蛳粉", "干捞螺蛳粉", "炸蛋"],
            "拥挤程度": 0.90
        },
        {
            "名称": "复记老友粉(七星店)",
            "类型": "快餐",
            "评分": 4.2,
            "人均消费(元)": 18,
            "latitude": 22.853838,
            "longitude": 108.222177,
            "推荐菜品": ["老友粉", "酸笋炒肉", "猪杂粉"],
            "拥挤程度": 0.88
        },
        {
            "名称": "高峰柠檬鸭(北湖店)",
            "类型": "中餐",
            "评分": 4.6,
            "人均消费(元)": 58,
            "latitude": 22.965046,
            "longitude": 108.353921,
            "推荐菜品": ["柠檬鸭", "爆炒鸭杂", "鸭血汤"],
            "拥挤程度": 0.75
        },
        {
            "名称": "益禾堂(大学城店)",
            "类型": "饮品",
            "评分": 4.4,
            "人均消费(元)": 9,
            "latitude": 22.839699,
            "longitude": 108.245804,
            "推荐菜品": ["烤奶", "杨枝甘露", "西瓜啵啵"],
            "拥挤程度": 0.82
        },
        {
            "名称": "邕州老街南宁饭店",
            "类型": "中餐",
            "评分": 4.7,
            "人均消费(元)": 88,
            "latitude": 22.821567,
            "longitude": 108.283456,
            "推荐菜品": ["柠檬鸭", "老友扣肉", "粉饺"],
            "拥挤程度": 0.68
        }
    ]
    df_restaurants = pd.DataFrame(restaurants_data)

    # 用餐高峰时段数据
    peak_hours_data = {
        "时段": [11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0],
        "快餐": [45, 88, 95, 90, 78, 68, 58, 50, 45, 50, 55, 65, 75, 85, 90, 85, 78],
        "中餐": [15, 35, 45, 40, 35, 30, 25, 20, 18, 22, 28, 35, 40, 45, 50, 45, 40],
        "饮品": [20, 40, 50, 45, 40, 35, 30, 25, 40, 55, 65, 70, 75, 80, 85, 80, 70],
        "卤味": [12, 28, 38, 33, 28, 23, 18, 15, 12, 18, 23, 28, 33, 38, 42, 38, 32]
    }
    df_peak_hours = pd.melt(
        pd.DataFrame(peak_hours_data),
        id_vars="时段",
        var_name="餐厅类型",
        value_name="用餐人数"
    )

    # 5家餐厅12个月价格走势数据
    months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    price_trend_data = {
        "月份": months,
        "三品王(朝阳店)": [13, 13, 14, 14, 15, 15, 15, 15, 14, 15, 15, 15],
        "柳厨螺蛳粉(中山路店)": [11, 12, 12, 13, 13, 13, 13, 13, 12, 13, 13, 13],
        "复记老友粉(七星店)": [16, 17, 17, 18, 18, 18, 18, 18, 17, 18, 18, 18],
        "高峰柠檬鸭(北湖店)": [55, 56, 57, 58, 58, 59, 59, 58, 57, 58, 58, 58],
        "邕州老街南宁饭店": [80, 82, 85, 86, 88, 88, 89, 88, 87, 88, 88, 88]
    }
    df_price_trend = pd.DataFrame(price_trend_data)
    df_price_trend_melt = pd.melt(
        df_price_trend,
        id_vars="月份",
        var_name="餐厅名称",
        value_name="人均消费(元)"
    )

    # 页面布局
    st.title("🍜 南宁美食数据仪表盘")
    st.write("全方位探索南宁本地特色美食，可视化呈现餐厅评分、价格、客流等核心数据！")
    st.markdown("---")

    # 分栏布局：左侧地图 + 右侧评分柱状图
    col1, col2 = st.columns(2)

    with col1:
        # 南宁美食地图
        st.subheader("📍 南宁美食地图")
        st.map(df_restaurants[["latitude", "longitude", "名称"]], zoom=12)

    with col2:
        # 餐厅评分柱状图
        st.subheader("⭐ 餐厅评分")
        chart_rating = alt.Chart(df_restaurants).mark_bar(color="#1f77b4").encode(
            x=alt.X("名称:N", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("评分:Q", scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(grid=False)),
            tooltip=["名称:N", "评分:Q"]
        ).properties(width=500, height=300)
        st.altair_chart(chart_rating, use_container_width=True)

    st.markdown("---")

    # 5家餐厅12个月价格走势折线图
    st.subheader("📈 5家餐厅12个月价格走势")
    chart_price_trend = alt.Chart(df_price_trend_melt).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("月份:O", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("人均消费(元):Q", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True)),
        color=alt.Color("餐厅名称:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"])),
        tooltip=["餐厅名称:N", "月份:O", "人均消费(元):Q"]
    ).properties(width=800, height=400)
    st.altair_chart(chart_price_trend, use_container_width=True)

    st.markdown("---")

    # 分栏布局：价格折线图 + 高峰时段面积图
    col3, col4 = st.columns(2)

    with col3:
        # 不同类型餐厅价格折线图
        st.subheader("💰 不同类型餐厅均价")
        df_type_price = df_restaurants.groupby("类型")["人均消费(元)"].mean().reset_index()
        chart_type_price = alt.Chart(df_type_price).mark_line(point=True, strokeWidth=3, color="#4682B4").encode(
            x=alt.X("类型:N", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("人均消费(元):Q", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=False)),
            tooltip=["类型:N", "人均消费(元):Q"]
        ).properties(width=400, height=300)
        st.altair_chart(chart_type_price, use_container_width=True)

    with col4:
        # 用餐高峰时段面积图
        st.subheader("⏰ 用餐高峰时段")
        chart_peak = alt.Chart(df_peak_hours).mark_area(opacity=0.7, line=True).encode(
            x=alt.X("时段:Q", axis=alt.Axis(grid=False)),
            y=alt.Y("用餐人数:Q", axis=alt.Axis(grid=False)),
            color=alt.Color("餐厅类型:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])),
            tooltip=["时段:Q", "餐厅类型:N", "用餐人数:Q"]
        ).properties(width=400, height=300)
        st.altair_chart(chart_peak, use_container_width=True)

    st.markdown("---")

    # 餐厅详情
    st.subheader("🍴 餐厅详情")
    selected_restaurant = st.selectbox(
        label="选择餐厅查看详情",
        options=df_restaurants["名称"].tolist(),
        index=0
    )
    selected_data = df_restaurants[df_restaurants["名称"] == selected_restaurant].iloc[0]

    # 详情展示
    col5, col6 = st.columns(2)
    with col5:
        st.write(f"**名称**：{selected_data['名称']}")
        st.write(f"**类型**：{selected_data['类型']}")
        st.write(f"**评分**：{selected_data['评分']}/5.0")
        st.write(f"**人均消费**：{selected_data['人均消费(元)']}元")

    with col6:
        st.write("**推荐菜品**：")
        for dish in selected_data["推荐菜品"]:
            st.write(f"• {dish}")
        st.write("**当前拥挤程度**：")
        st.progress(selected_data["拥挤程度"])
        st.write(f"{round(selected_data['拥挤程度']*100)}%")

elif current_page == "photo_gallery":
    # ===================== 相册浏览页面 =====================
    st.title("🖼️ 相册浏览")
    
    # 图片数据列表
    image_ua = [
        {
            'url': 'https://tse1-mm.cn.bing.net/th/id/OIP-C.U3bOzKUR-5borHoCsmPJAwHaEz?w=307&h=199&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1',
            'text': '鱼'
        },
        {
            'url': 'https://tse4-mm.cn.bing.net/th/id/OIP-C.3vlwqaXDF8hgNAYsoDpZdwHaFj?w=238&h=180&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1',
            'text': '鸟'
        },
        {
            'url': 'https://tse4-mm.cn.bing.net/th/id/OIP-C.F15Td8baE_F5y4UzxGppDwHaE7?w=295&h=197&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1',
            'text': '猫'
        },
    ]

    # 初始化会话状态的索引
    if 'photo_ind' not in st.session_state:
        st.session_state['photo_ind'] = 0

    # 显示当前索引对应的图片和标题
    st.image(
        image_ua[st.session_state['photo_ind']]['url'],
        caption=image_ua[st.session_state['photo_ind']]['text']
    )

    # 定义"下一张"函数
    def next_photo():
        st.session_state['photo_ind'] = (st.session_state['photo_ind'] + 1) % len(image_ua)

    # 定义"上一张"函数
    def prev_photo():
        st.session_state['photo_ind'] = (st.session_state['photo_ind'] - 1) % len(image_ua)

    # 分栏放置按钮
    c1, c2 = st.columns(2)
    with c1:
        st.button('上一张', use_container_width=True, on_click=prev_photo, key="prev_photo")
    with c2:
        st.button('下一张', use_container_width=True, on_click=next_photo, key="next_photo")

elif current_page == "music_player":
    # ===================== 音乐播放器页面 =====================
    st.title("🎵 音乐播放器")
    
    # 音乐数据列表
    image_ua = [
        {
            'audio_file':'https://music.163.com/song/media/outer/url?id=2137661995.mp3',
            'url': 'http://p1.music.126.net/XR65faE5ZmTmFvqy_ndtfQ==/109951169427192489.jpg?param=130y130',
            'text': '赤伶--HITA'
        },
        {
            'audio_file':'https://music.163.com/song/media/outer/url?id=27591660.mp3',
            'url': 'http://p2.music.126.net/9KeyafHLjadqSQTRS_tN5Q==/5741649720318487.jpg?param=130y130',
            'text': 'First Date--陈光荣'
        },
        {
            'audio_file':'https://music.163.com/song/media/outer/url?id=409654818.mp3',
            'url': 'http://p1.music.126.net/dq3YI-xJ03SyMJwIk0dvig==/17808789835268501.jpg?param=130y130',
            'text': '灌篮高手《直到世界尽头》--姜创钢琴'
        },
    ]

    # 初始化会话状态的索引
    if 'music_ind' not in st.session_state:
        st.session_state['music_ind'] = 0

    # 显示当前索引对应的图片和标题
    st.image(
        image_ua[st.session_state['music_ind']]['url'],
        caption=image_ua[st.session_state['music_ind']]['text']
    )
    st.audio(image_ua[st.session_state['music_ind']]['audio_file'])

    # 定义"下一首"函数
    def next_music():
        st.session_state['music_ind'] = (st.session_state['music_ind'] + 1) % len(image_ua)

    # 定义"上一首"函数
    def prev_music():
        st.session_state['music_ind'] = (st.session_state['music_ind'] - 1) % len(image_ua)

    # 分栏放置按钮
    c1, c2 = st.columns(2)
    with c1:
        st.button('上一首', use_container_width=True, on_click=prev_music, key="prev_music")
    with c2:
        st.button('下一首', use_container_width=True, on_click=next_music, key="next_music")

elif current_page == "video_player":
    # ===================== 视频播放器页面 =====================
    st.title("🎬 视频播放器")
    st.subheader("还珠格格第一部")

    # 视频数据
    video_arr = [
        {
            'url': 'https://www.w3school.com.cn/example/html5/mov_bbb.mp4',
            'title': '还珠格格第一部-第1集'
        },
        {
            'url': 'https://www.w3schools.com/html/movie.mp4',
            'title': '还珠格格第一部-第2集'
        },
        {
            'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4',
            'title': '还珠格格第一部-第3集'
        }
    ]

    # 初始化会话状态
    if 'video_ind' not in st.session_state:
        st.session_state['video_ind'] = 0

    # 显示当前视频
    current_video = video_arr[st.session_state['video_ind']]
    st.subheader(current_video['title'])
    st.video(current_video['url'])

    # 显示所有集数按钮
    st.subheader("选择集数")
    cols = st.columns(len(video_arr))

    for i in range(len(video_arr)):
        with cols[i]:
            if st.button(f"第{i + 1}集", key=f"video_episode_{i}"):
                st.session_state['video_ind'] = i
                st.rerun()

    # 播放控制按钮
    st.subheader("播放控制")
    control_cols = st.columns(3)

    with control_cols[0]:
        if st.button("上一集", disabled=(st.session_state['video_ind'] == 0), key="prev_video"):
            st.session_state['video_ind'] -= 1
            st.rerun()

    with control_cols[1]:
        st.write(f"当前: 第{st.session_state['video_ind'] + 1}集")

    with control_cols[2]:
        if st.button("下一集", disabled=(st.session_state['video_ind'] == len(video_arr) - 1), key="next_video"):
            st.session_state['video_ind'] += 1
            st.rerun()

    # 显示视频信息
    st.subheader("视频信息")
    st.info(f"正在播放: {current_video['title']}")
    st.write(f"总共 {len(video_arr)} 集")

elif current_page == "resume_generator":
    # ===================== 简历生成器页面 =====================
    # 自定义CSS样式
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .resume-preview {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        color: #333333;
        min-height: 800px;
    }
    .profile-section {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    .info-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    .skill-tag {
        background-color: #dc3545;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header"><h1>📄 个人简历生成器</h1></div>', unsafe_allow_html=True)

    # 创建两列布局
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.header("个人信息输入")
        
        # 照片上传
        st.subheader("📷 个人照片")
        uploaded_photo = st.file_uploader("上传个人照片", type=['png', 'jpg', 'jpeg'], key="resume_photo")
        
        # 基本信息
        st.subheader("👤 基本信息")
        name = st.text_input("姓名", placeholder="请输入您的姓名", key="resume_name")
        age = st.number_input("年龄", min_value=18, max_value=100, value=25, key="resume_age")
        gender = st.radio("性别", ["男", "女","其他"], horizontal=True, key="resume_gender")
        phone = st.text_input("联系电话", placeholder="请输入手机号码", key="resume_phone")
        email = st.text_input("邮箱地址", placeholder="请输入邮箱地址", key="resume_email")
        address = st.text_input("居住地址", placeholder="请输入居住地址", key="resume_address")
        
        # 求职意向
        st.subheader("🎯 求职意向")
        job_position = st.text_input("期望职位", placeholder="如：Python开发工程师", key="resume_job")
        salary_expectation = st.selectbox("期望薪资", 
                                        ["请选择", "3K-5K", "5K-8K", "8K-12K", "12K-15K", "15K-20K", "20K以上"], key="resume_salary")
        work_location = st.multiselect("期望工作地点", 
                                     ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "南宁"], key="resume_location")
        
        # 语言能力
        st.subheader("🌐 语言能力")
        
        # 初始化语言技能会话状态
        if 'resume_language_skills' not in st.session_state:
            st.session_state.resume_language_skills = []
        
        # 添加语言技能
        new_language = st.text_input("添加语言", placeholder="如：中文、英语、日语等", key="resume_language_input")
        
        if new_language:
            if st.button("➕ 添加语言", key="resume_add_language_btn"):
                if new_language not in st.session_state.resume_language_skills:
                    st.session_state.resume_language_skills.append(new_language)
                    st.rerun()
        
        # 显示语言标签
        if st.session_state.resume_language_skills:
            st.write("**已添加的语言：**")
            cols_per_row = 3
            for i in range(0, len(st.session_state.resume_language_skills), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, language in enumerate(st.session_state.resume_language_skills[i:i+cols_per_row]):
                    with cols[j]:
                        if st.button(f"{language} ❌", key=f"resume_lang_{i+j}", 
                                   help=f"点击删除 {language}",
                                   use_container_width=True):
                            st.session_state.resume_language_skills.remove(language)
                            st.rerun()
        
        # 计算机技能
        st.subheader("💻 计算机技能")
        
        # 初始化会话状态
        if 'resume_computer_skills' not in st.session_state:
            st.session_state.resume_computer_skills = []
        
        # 预设的计算机技能选项
        available_skills = [
            "Python", "Java", "JavaScript", "HTML/CSS", "React", 
            "Vue.js", "Node.js", "MySQL", "MongoDB", "Git"
        ]
        
        # 过滤掉已选择的技能
        remaining_skills = [skill for skill in available_skills if skill not in st.session_state.resume_computer_skills]
        
        # 显示可选择的技能标签
        if remaining_skills:
            st.write("**点击添加技能：**")
            cols_per_row = 3
            for i in range(0, len(remaining_skills), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, skill in enumerate(remaining_skills[i:i+cols_per_row]):
                    with cols[j]:
                        if st.button(f"➕ {skill}", key=f"resume_add_{skill}", 
                                   help=f"点击添加 {skill}",
                                   use_container_width=True):
                            st.session_state.resume_computer_skills.append(skill)
                            st.rerun()
        else:
            st.info("所有技能都已添加完毕！")
        
        # 显示已添加的技能标签
        if st.session_state.resume_computer_skills:
            st.write("**已添加的技能：**")
            
            # 使用columns来显示标签
            cols_per_row = 3
            skills = st.session_state.resume_computer_skills
            
            for i in range(0, len(skills), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, skill in enumerate(skills[i:i+cols_per_row]):
                    with cols[j]:
                        # 创建带删除按钮的技能标签
                        if st.button(f"{skill} ❌", key=f"resume_skill_{i+j}", 
                                   help=f"点击删除 {skill}",
                                   use_container_width=True):
                            st.session_state.resume_computer_skills.remove(skill)
                            st.rerun()
        
        # 个人介绍
        st.subheader("💡 个人介绍")
        personal_intro = st.text_area("个人简介", 
                                    placeholder="请简要介绍您的个人特点、优势和职业目标...",
                                    height=100, key="resume_intro")
        
        # 工作经历
        st.subheader("💼 工作经历")
        work_experience = st.text_area("工作经历", 
                                     placeholder="请按时间倒序填写工作经历，包括公司名称、职位、工作时间和主要职责...",
                                     height=120, key="resume_work")
        
        # 教育背景
        st.subheader("🎓 教育背景")
        education = st.selectbox("最高学历", ["请选择", "高中", "大专", "本科", "硕士", "博士"], key="resume_education")
        school = st.text_input("毕业院校", placeholder="请输入毕业院校名称", key="resume_school")
        major = st.text_input("所学专业", placeholder="请输入专业名称", key="resume_major")
        graduation_date = st.date_input("毕业时间", value=date.today(), key="resume_graduation")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.header("简历预览")
        
        # 个人信息区域
        if name or uploaded_photo:
            
            # 显示照片
            if uploaded_photo:
                image = Image.open(uploaded_photo)
                # 调整图片大小
                image = image.resize((150, 150))
                col_photo, col_info = st.columns([1, 2])
                with col_photo:
                    st.image(image, width=150)
                with col_info:
                    if name:
                        st.markdown(f"# {name}")
                    if job_position:
                        st.markdown(f"**{job_position}**")
            else:
                if name:
                    st.markdown(f"# {name}")
                if job_position:
                    st.markdown(f"**{job_position}**")
        
        # 联系方式
        if phone or email or address:
            st.subheader("📞 联系方式")
            if phone:
                st.write(f"电话：{phone}")
            if email:
                st.write(f"邮箱：{email}")
            if address:
                st.write(f"地址：{address}")
        
        # 基本信息
        if age > 18 or gender or salary_expectation != "请选择" or work_location:
            st.subheader("👤 基本信息")
            if age > 18:
                st.write(f"年龄：{age}岁")
            if gender:
                st.write(f"性别：{gender}")
            if salary_expectation != "请选择":
                st.write(f"期望薪资：{salary_expectation}")
            if work_location:
                st.write(f"期望工作地点：{', '.join(work_location)}")
        
        # 个人介绍
        if personal_intro:
            st.subheader("💡 个人介绍")
            st.write(personal_intro)
        
        # 语言能力
        if st.session_state.get('resume_language_skills'):
            st.subheader("🌐 语言能力")
            language_tags = ""
            for language in st.session_state.resume_language_skills:
                language_tags += f'<span class="skill-tag">{language}</span> '
            st.markdown(language_tags, unsafe_allow_html=True)
        
        # 计算机技能
        if st.session_state.get('resume_computer_skills'):
            st.subheader("💻 计算机技能")
            skill_tags = ""
            for skill in st.session_state.resume_computer_skills:
                skill_tags += f'<span class="skill-tag">{skill}</span> '
            st.markdown(skill_tags, unsafe_allow_html=True)
        
        # 工作经历
        if work_experience:
            st.subheader("💼 工作经历")
            st.write(work_experience)
        
        # 教育背景
        if education != "请选择" or school or major:
            st.subheader("🎓 教育背景")
            if education != "请选择":
                st.write(f"学历：{education}")
            if school:
                st.write(f"毕业院校：{school}")
            if major:
                st.write(f"专业：{major}")
            st.write(f"毕业时间：{graduation_date}")