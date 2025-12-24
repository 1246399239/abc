import streamlit as st

# 页面基础配置
st.set_page_config(page_title='相册网站', page_icon='🐱')

# 图片数据列表（URL+描述文本）
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

# 初始化会话状态的索引（避免首次访问报错）
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 显示当前索引对应的图片和标题
st.image(
    image_ua[st.session_state['ind']]['url'],
    caption=image_ua[st.session_state['ind']]['text']
)
st.audio(image_ua[st.session_state['ind']]['audio_file'])

# 定义“下一张”函数：索引+1，超出列表长度则取模（循环）
def next_img():
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(image_ua)

# 定义“上一张”函数：索引-1，为负数时取模（循环）
def prev_img():
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(image_ua)

# 分栏放置按钮（左：上一张，右：下一张）
c1, c2 = st.columns(2)
with c1:
    st.button('上一首', use_container_width=True, on_click=prev_img)
with c2:
    st.button('下一首', use_container_width=True, on_click=next_img)


