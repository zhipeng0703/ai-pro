'''
文生图大模型应用
'''
import streamlit as st
from zhipuai import ZhipuAI
# 先构建智谱AI的大模型
model = ZhipuAI(api_key="909d29c7f1e28c2d92c3f32b453d0b11.U2XRoY1Q7UVd55PV")
st.title("设计大师")

if "cache" not in st.session_state:
    st.session_state.cache = []
else:
    # 需要从缓存中获取对话信息在界面上渲染  缓存两块内容 角色 角色的消息
    for message in st.session_state.cache:
        if message['role'] == 'user':
            with st.chat_message(message['role']):
                st.write(message["content"])
        else:
            with st.chat_message(message['role']):
                st.image(message["content"],width=300)




# 创建输入框
desc = st.chat_input("请输入图片的描述")
if desc:
    # 将用户输入的内容以用户角色输出到界面上
    with st.chat_message("user"):
        st.write(desc)
    st.session_state.cache.append({"role":"user","content":desc})
    # 调用智谱AI的文生图大模型生成图片
    response = model.images.generations(
        model="cogview-3-plus",  # 填写需要调用的模型编码
        prompt=desc,
    )
    # 以AI的角色展示图片
    with st.chat_message("assistant"):
        st.image(response.data[0].url,width=300)
    st.session_state.cache.append({"role": "assistant", "content": response.data[0].url})
