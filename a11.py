@st.cache_data(show_spinner="加载数据中...")
def load_data():
    """精准读取你的Excel（强化时间列容错）"""
    target_file = "supermarket_sales.xlsx"
    if not os.path.exists(target_file):
        st.error(f"未找到数据文件：{target_file}，请确保文件在当前目录")
        return pd.DataFrame()

    # 跳过第一行标题，用第二行作为列名
    df = pd.read_excel(
        target_file,
        engine="openpyxl",
        header=1
    )

    # 字段100%映射你的Excel列名
    df_standard = df.rename(columns={
        "分店": "branch",
        "城市": "city",
        "顾客类型": "customer_type",
        "性别": "gender",
        "产品类型": "category",
        "总价": "revenue",
        "日期": "date",
        "时间": "time",
        "评分": "rating"
    })

    # ------------------------------
    # 核心修复：时间列超级容错处理
    # ------------------------------
    # 1. 先把时间列转成字符串，清理空格/特殊字符
    df_standard["time"] = df_standard["time"].astype(str).str.strip().str.replace(r"[^\d:]", "", regex=True)
    # 2. 尝试转换（兼容%H:%M、%H:%M:%S等格式，无效值转成NaT）
    time_series = pd.to_datetime(
        df_standard["time"],
        format="mixed",  # 自动识别常见时间格式
        errors="coerce"  # 无法识别的格式→NaT
    )
    # 3. 提取小时，NaT对应的小时→填0（避免报错）
    df_standard["hour"] = time_series.dt.hour.fillna(0).astype(int)

    return df_standard
