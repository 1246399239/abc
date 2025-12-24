import streamlit as st

st.set_page_config(page_title="视频播放器")
st.title("还珠格格第一部")

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
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 显示当前视频
current_video = video_arr[st.session_state['ind']]
st.subheader(current_video['title'])
st.video(current_video['url'])

# 创建分栏布局
col1, col2, col3 = st.columns(3)

# 显示所有集数按钮
st.subheader("选择集数")
cols = st.columns(len(video_arr))

for i in range(len(video_arr)):
    with cols[i]:
        if st.button(f"第{i + 1}集", key=f"episode_{i}"):
            st.session_state['ind'] = i
            st.rerun()

# 播放控制按钮
st.subheader("播放控制")
control_cols = st.columns(3)

with control_cols[0]:
    if st.button("上一集", disabled=(st.session_state['ind'] == 0)):
        st.session_state['ind'] -= 1
        st.rerun()

with control_cols[1]:
    st.write(f"当前: 第{st.session_state['ind'] + 1}集")

with control_cols[2]:
    if st.button("下一集", disabled=(st.session_state['ind'] == len(video_arr) - 1)):
        st.session_state['ind'] += 1
        st.rerun()

# 显示视频信息
st.subheader("视频信息")
st.info(f"正在播放: {current_video['title']}")
st.write(f"总共 {len(video_arr)} 集")