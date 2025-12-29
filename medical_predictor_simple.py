import streamlit as st
import pandas as pd
import numpy as np
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ 机器学习库未安装，将使用规则引擎模式")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ===================== 页面配置 =====================
st.set_page_config(
    page_title="🏥 医疗费用预测系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== 自定义样式 =====================
st.markdown("""
<style>
    /* 全局样式 */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    .main .block-container {
        padding-top: 1rem;
        max-width: 800px;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* 表单控件样式 */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 8px 12px;
    }
    
    /* 单选按钮水平排列 */
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
    }
    
    /* 按钮样式 */
    .stFormSubmitButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        width: 100%;
        font-weight: 500;
    }
    
    .stFormSubmitButton > button:hover {
        background-color: #0056b3;
    }
    
    /* 导航按钮 */
    .sidebar .stButton > button {
        background-color: #ffffff;
        color: #495057;
        border: 1px solid #dee2e6;
        margin-bottom: 8px;
        text-align: left;
    }
    
    .sidebar .stButton > button:hover {
        background-color: #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# ===================== 数据加载和预处理 =====================
@st.cache_data
def load_and_preprocess_data():
    """加载并预处理医疗保险数据"""
    try:
        # 尝试不同编码读取CSV文件
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv('insurance-chinese.csv', encoding=encoding)
                st.success(f"✅ 成功读取CSV文件 (编码: {encoding})")
                break
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        if df is None:
            st.info("📊 CSV文件未找到，使用示例数据")
            return generate_sample_data()
        
        # 重命名列名为英文（便于处理）
        df.columns = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
        
        # 数据清洗
        df = df.dropna()
        
        if SKLEARN_AVAILABLE:
            # 标签编码
            le_sex = LabelEncoder()
            le_smoker = LabelEncoder()
            le_region = LabelEncoder()
            
            df['sex_encoded'] = le_sex.fit_transform(df['sex'])
            df['smoker_encoded'] = le_smoker.fit_transform(df['smoker'])
            df['region_encoded'] = le_region.fit_transform(df['region'])
            
            return df, le_sex, le_smoker, le_region
        else:
            return df, None, None, None
            
    except Exception as e:
        st.warning(f"⚠️ 数据加载失败: {e}")
        st.info("📊 使用示例数据")
        return generate_sample_data()

@st.cache_data
def generate_sample_data():
    """生成示例数据"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'age': np.random.randint(18, 80, n_samples),
        'sex': np.random.choice(['男性', '女性'], n_samples),
        'bmi': np.random.normal(25, 5, n_samples),
        'children': np.random.randint(0, 6, n_samples),
        'smoker': np.random.choice(['否', '是'], n_samples, p=[0.8, 0.2]),
        'region': np.random.choice(['东南部', '西南部', '西北部', '东北部'], n_samples)
    }
    
    df = pd.DataFrame(data)
    df['bmi'] = np.clip(df['bmi'], 15, 50)
    
    # 生成费用数据
    base_cost = 5000
    age_factor = df['age'] * 100
    bmi_factor = np.where(df['bmi'] > 30, (df['bmi'] - 30) * 500, 0)
    smoker_factor = np.where(df['smoker'] == '是', 15000, 0)
    children_factor = df['children'] * 1000
    
    df['charges'] = (base_cost + age_factor + bmi_factor + 
                    smoker_factor + children_factor + 
                    np.random.normal(0, 2000, n_samples))
    
    df['charges'] = np.maximum(df['charges'], 1000)
    
    return df, None, None, None

# ===================== 机器学习模型训练 =====================
@st.cache_resource
def train_random_forest_model(df):
    """训练随机森林模型"""
    if df is None or not SKLEARN_AVAILABLE:
        return None, None
    
    try:
        # 准备特征和目标变量
        features = ['age', 'sex_encoded', 'bmi', 'children', 'smoker_encoded', 'region_encoded']
        X = df[features]
        y = df['charges']
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 训练随机森林模型
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # 模型评估
        rf_pred = rf_model.predict(X_test)
        
        metrics = {
            'MAE': mean_absolute_error(y_test, rf_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, rf_pred)),
            'R2': r2_score(y_test, rf_pred)
        }
        
        return rf_model, metrics
        
    except Exception as e:
        st.error(f"❌ 随机森林模型训练失败: {e}")
        return None, None
# ===================== 预测函数 =====================
def predict_medical_cost(age, sex, bmi, children, smoker, region, rf_model=None):
    """使用随机森林模型预测，如果模型不可用则使用规则引擎"""
    if rf_model is not None and SKLEARN_AVAILABLE:
        try:
            # 编码输入数据
            sex_encoded = 1 if sex == '男性' else 0
            smoker_encoded = 1 if smoker == '是' else 0
            region_map = {'东南部': 0, '西南部': 1, '西北部': 2, '东北部': 3}
            region_encoded = region_map.get(region, 0)
            
            # 准备预测数据
            input_data = np.array([[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]])
            
            # 使用随机森林预测
            prediction = rf_model.predict(input_data)[0]
            return max(prediction, 1000), "随机森林"
            
        except Exception as e:
            st.warning(f"⚠️ 随机森林预测失败，使用规则引擎: {e}")
            return predict_with_rules(age, sex, bmi, children, smoker, region), "规则引擎"
    else:
        # 使用规则引擎作为备用
        return predict_with_rules(age, sex, bmi, children, smoker, region), "规则引擎"

def predict_with_rules(age, sex, bmi, children, smoker, region):
    """基于规则的医疗费用预测（备用方案）"""
    base_cost = 5000
    age_factor = age * 100
    
    if bmi > 30:
        bmi_factor = (bmi - 30) * 500
    elif bmi < 18.5:
        bmi_factor = (18.5 - bmi) * 300
    else:
        bmi_factor = 0
    
    smoker_factor = 15000 if smoker == '是' else 0
    children_factor = children * 1000
    sex_factor = 500 if sex == '男性' else 0
    
    region_factors = {
        '东南部': 1000, '西南部': 800, 
        '西北部': 600, '东北部': 1200
    }
    region_factor = region_factors.get(region, 800)
    
    total_cost = (base_cost + age_factor + bmi_factor + 
                 smoker_factor + children_factor + 
                 sex_factor + region_factor)
    
    return max(total_cost, 1000)

# ===================== 页面函数 =====================
def show_introduction():
    """显示简介页面"""
    st.markdown("## 使用说明")
    
    st.markdown("""
    这个应用基于机器学习技术预测医疗费用，为您提供个性化的医疗费用预估。
    
    • **输入信息**: 在下面输入您的个人信息，系统将为您预测
    • **预测模型**: 应用会综合您输入的个人信息来预测医疗费用支出
    """)
    
    st.markdown("### 功能特点")
    st.markdown("""
    - 基于多因素分析的智能预测
    - 考虑年龄、性别、BMI、生活习惯等因素
    - 提供个性化的医疗费用估算
    - 简单易用的操作界面
    """)
    
    st.markdown("### 注意事项")
    st.markdown("""
    - 预测结果仅供参考，不能替代专业医疗建议
    - 实际医疗费用可能因多种因素而有所不同
    - 建议定期体检，保持健康的生活方式
    """)

def show_prediction():
    """显示预测页面"""
    st.markdown("## 使用说明")
    
    st.markdown("""
    这个应用基于机器学习技术预测医疗费用，为您提供个性化的医疗费用预估。
    
    • **输入信息**: 在下面输入您的个人信息，系统将为您预测
    • **预测模型**: 应用使用随机森林算法进行智能预测
    """)
    
    # 加载数据和训练模型
    df, le_sex, le_smoker, le_region = load_and_preprocess_data()
    
    if SKLEARN_AVAILABLE:
        rf_model, metrics = train_random_forest_model(df)
        if rf_model is not None:
            st.success("🌲 随机森林模型训练完成！")
            
            # 显示模型性能
            with st.expander("📊 模型性能指标"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("平均绝对误差", f"{metrics['MAE']:.2f}")
                with col2:
                    st.metric("均方根误差", f"{metrics['RMSE']:.2f}")
                with col3:
                    st.metric("决定系数 R²", f"{metrics['R2']:.3f}")
        else:
            st.warning("⚠️ 随机森林训练失败，将使用规则引擎")
            rf_model = None
    else:
        st.info("📢 使用规则引擎模式（请安装scikit-learn获得随机森林功能）")
        rf_model = None
    
    # 表单
    with st.form("prediction_form"):
        # 年龄
        age = st.number_input("年龄", min_value=0, max_value=100, value=30, step=1)
        
        # 性别
        sex = st.radio("性别", ["男性", "女性"], horizontal=True)
        
        # BMI
        bmi = st.number_input("BMI", min_value=0.0, max_value=100.0, value=25.0, step=0.1, format="%.2f")
        
        # 子女数量
        children = st.number_input("子女数量", min_value=0, max_value=10, value=0, step=1)
        
        # 是否吸烟
        smoker = st.radio("是否吸烟", ["否", "是"], horizontal=True)
        
        # 区域
        region = st.selectbox("区域", ["东南部", "西南部", "西北部", "东北部"])
        
        # 预测按钮
        submitted = st.form_submit_button("预测费用")
        
        if submitted:
            if age > 0 and bmi > 0:
                # 使用随机森林进行预测
                prediction, model_name = predict_medical_cost(age, sex, bmi, children, smoker, region, rf_model)
                
                # 显示预测结果
                st.markdown("---")
                st.success("预测完成！")
                
                # 大字体显示预测金额
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background-color: #f0f8ff; 
                           border: 2px solid #007bff; border-radius: 10px; margin: 1rem 0;">
                    <h1 style="color: #007bff; font-size: 3rem; margin: 0;">¥{prediction:,.2f}</h1>
                    <p style="color: #666; font-size: 1.2rem; margin: 0.5rem 0;">预测医疗费用</p>
                    <p style="color: #888; font-size: 1rem;">使用模型: {model_name}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示输入信息回顾
                with st.expander("📋 输入信息回顾"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**年龄**: {age}岁")
                        st.write(f"**性别**: {sex}")
                        st.write(f"**BMI**: {bmi}")
                    with col2:
                        st.write(f"**子女数量**: {children}个")
                        st.write(f"**吸烟状况**: {smoker}")
                        st.write(f"**所在区域**: {region}")
                
                # 如果使用规则引擎，显示费用构成
                if model_name == "规则引擎":
                    with st.expander("💡 费用构成分析"):
                        base_cost = 5000
                        age_factor = age * 100
                        bmi_factor = max(0, (bmi - 30) * 500) if bmi > 30 else max(0, (18.5 - bmi) * 300) if bmi < 18.5 else 0
                        smoker_factor = 15000 if smoker == '是' else 0
                        children_factor = children * 1000
                        
                        st.write(f"**基础费用**: ¥{base_cost:,.2f}")
                        st.write(f"**年龄因子**: ¥{age_factor:,.2f}")
                        if bmi_factor > 0:
                            st.write(f"**BMI因子**: ¥{bmi_factor:,.2f}")
                        if smoker_factor > 0:
                            st.write(f"**吸烟因子**: ¥{smoker_factor:,.2f}")
                        if children_factor > 0:
                            st.write(f"**子女因子**: ¥{children_factor:,.2f}")
                elif model_name == "随机森林":
                    with st.expander("🌲 随机森林预测说明"):
                        st.markdown("""
                        随机森林是一种集成学习算法，具有以下特点：
                        
                        - **高准确度**: 通过多个决策树投票得出结果
                        - **抗过拟合**: 随机性降低模型复杂度
                        - **处理非线性**: 能够捕捉复杂的特征关系
                        - **特征重要性**: 自动识别关键影响因素
                        
                        预测结果综合考虑了您输入的所有信息，并基于大量历史数据进行智能分析。
                        """)
            else:
                st.error("请输入有效的年龄和BMI值")

# ===================== 主应用 =====================
def main():
    # 初始化session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = '简介'
    
    # 侧边栏导航
    st.sidebar.markdown("### 导航")
    
    if st.sidebar.button("📖 简介", use_container_width=True):
        st.session_state.current_page = '简介'
    
    if st.sidebar.button("💰 预测分析", use_container_width=True):
        st.session_state.current_page = '预测分析'
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**当前页面**: {st.session_state.current_page}")
    
    # 根据选择显示不同页面
    if st.session_state.current_page == '简介':
        show_introduction()
    elif st.session_state.current_page == '预测分析':
        show_prediction()

if __name__ == "__main__":
    main()