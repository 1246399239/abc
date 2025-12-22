import streamlit as st

# 页面基础配置
st.set_page_config(page_title='相册网站', page_icon='🐱')

# 图片数据列表（URL+描述文本）
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

# 初始化会话状态的索引（避免首次访问报错）
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 显示当前索引对应的图片和标题
st.image(
    image_ua[st.session_state['ind']]['url'],
    caption=image_ua[st.session_state['ind']]['text']
)

# 定义“下一张”函数：索引+1，超出列表长度则取模（循环）
def next_img():
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(image_ua)

# 定义“上一张”函数：索引-1，为负数时取模（循环）
def prev_img():
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(image_ua)

# 分栏放置按钮（左：上一张，右：下一张）
c1, c2 = st.columns(2)
with c1:
    st.button('上一张', use_container_width=True, on_click=prev_img)
with c2:
    st.button('下一张', use_container_width=True, on_click=next_img)