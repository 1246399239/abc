import streamlit as st
from datetime import datetime, date
from PIL import Image

st.set_page_config(page_title="个人简历生成器", page_icon="📄", layout="wide")

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
    uploaded_photo = st.file_uploader("上传个人照片", type=['png', 'jpg', 'jpeg'])
    
    # 基本信息
    st.subheader("👤 基本信息")
    name = st.text_input("姓名", placeholder="请输入您的姓名")
    age = st.number_input("年龄", min_value=18, max_value=100, value=25)
    gender = st.radio("性别", ["男", "女","其他"], horizontal=True)
    phone = st.text_input("联系电话", placeholder="请输入手机号码")
    email = st.text_input("邮箱地址", placeholder="请输入邮箱地址")
    address = st.text_input("居住地址", placeholder="请输入居住地址")
    
    # 求职意向
    st.subheader("🎯 求职意向")
    job_position = st.text_input("期望职位", placeholder="如：Python开发工程师")
    salary_expectation = st.selectbox("期望薪资", 
                                    ["请选择", "3K-5K", "5K-8K", "8K-12K", "12K-15K", "15K-20K", "20K以上"])
    work_location = st.multiselect("期望工作地点", 
                                 ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "南宁"])
    
    # 语言能力
    st.subheader("🌐 语言能力")
    
    # 初始化语言技能会话状态
    if 'language_skills' not in st.session_state:
        st.session_state.language_skills = []
    
    # 添加语言技能
    new_language = st.text_input("添加语言", placeholder="如：中文、英语、日语等", key="language_input")
    
    if new_language:
        if st.button("➕ 添加语言", key="add_language_btn"):
            if new_language not in st.session_state.language_skills:
                st.session_state.language_skills.append(new_language)
                st.rerun()
    
    # 显示语言标签
    if st.session_state.language_skills:
        st.write("**已添加的语言：**")
        cols_per_row = 3
        for i in range(0, len(st.session_state.language_skills), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, language in enumerate(st.session_state.language_skills[i:i+cols_per_row]):
                with cols[j]:
                    if st.button(f"{language} ❌", key=f"lang_{i+j}", 
                               help=f"点击删除 {language}",
                               use_container_width=True):
                        st.session_state.language_skills.remove(language)
                        st.rerun()
    
    # 计算机技能
    st.subheader("💻 计算机技能")
    
    # 初始化会话状态
    if 'computer_skills' not in st.session_state:
        st.session_state.computer_skills = []
    
    # 预设的计算机技能选项
    available_skills = [
        "Python", "Java", "JavaScript", "HTML/CSS", "React", 
        "Vue.js", "Node.js", "MySQL", "MongoDB", "Git"
    ]
    
    # 过滤掉已选择的技能
    remaining_skills = [skill for skill in available_skills if skill not in st.session_state.computer_skills]
    
    # 显示可选择的技能标签
    if remaining_skills:
        st.write("**点击添加技能：**")
        cols_per_row = 3
        for i in range(0, len(remaining_skills), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, skill in enumerate(remaining_skills[i:i+cols_per_row]):
                with cols[j]:
                    if st.button(f"➕ {skill}", key=f"add_{skill}", 
                               help=f"点击添加 {skill}",
                               use_container_width=True):
                        st.session_state.computer_skills.append(skill)
                        st.rerun()
    else:
        st.info("所有技能都已添加完毕！")
    
    # 显示已添加的技能标签
    if st.session_state.computer_skills:
        st.write("**已添加的技能：**")
        
        # 使用columns来显示标签
        cols_per_row = 3
        skills = st.session_state.computer_skills
        
        for i in range(0, len(skills), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, skill in enumerate(skills[i:i+cols_per_row]):
                with cols[j]:
                    # 创建带删除按钮的技能标签
                    if st.button(f"{skill} ❌", key=f"skill_{i+j}", 
                               help=f"点击删除 {skill}",
                               use_container_width=True):
                        st.session_state.computer_skills.remove(skill)
                        st.rerun()
    
    # 个人介绍
    st.subheader("💡 个人介绍")
    personal_intro = st.text_area("个人简介", 
                                placeholder="请简要介绍您的个人特点、优势和职业目标...",
                                height=100)
    
    # 工作经历
    st.subheader("💼 工作经历")
    work_experience = st.text_area("工作经历", 
                                 placeholder="请按时间倒序填写工作经历，包括公司名称、职位、工作时间和主要职责...",
                                 height=120)
    
    # 教育背景
    st.subheader("🎓 教育背景")
    education = st.selectbox("最高学历", ["请选择", "高中", "大专", "本科", "硕士", "博士"])
    school = st.text_input("毕业院校", placeholder="请输入毕业院校名称")
    major = st.text_input("所学专业", placeholder="请输入专业名称")
    graduation_date = st.date_input("毕业时间", value=date.today())
    
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
    if st.session_state.get('language_skills'):
        st.subheader("🌐 语言能力")
        language_tags = ""
        for language in st.session_state.language_skills:
            language_tags += f'<span class="skill-tag">{language}</span> '
        st.markdown(language_tags, unsafe_allow_html=True)
    
    # 计算机技能
    if st.session_state.get('computer_skills'):
        st.subheader("💻 计算机技能")
        skill_tags = ""
        for skill in st.session_state.computer_skills:
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