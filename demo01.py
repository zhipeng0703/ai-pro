# 制作一个聊天界面
# 解决聊天界面不能渲染以往旧对话信息
# streamlit每次输入框发送完成数据之后，页面都会重新加载
# 只要当streamlit重新加载的时候，保证聊天记录不被清空  信息缓存起来
import streamlit as st
# langchain调用大模型，导入langchain的代码
from langchain_openai import ChatOpenAI

# 构建一个大模型 --智谱AI公司提供的大模型
model = ChatOpenAI(
    temperature=0.8, # 温度，创新性
    model="glm-4-plus", # 大模型的名字
    base_url="https://open.bigmodel.cn/api/paas/v4/", # 大模型的地址
    api_key="909d29c7f1e28c2d92c3f32b453d0b11.U2XRoY1Q7UVd55PV" # 账号信息
)
st.title("AI demo小程序👏👏👏👏")
# 构建一个缓存，用来保存聊天记录
if "cache" not in st.session_state:
    st.session_state.cache = []
else:
    # 需要从缓存中获取对话信息在界面上渲染  缓存两块内容 角色 角色的消息
    for message in st.session_state.cache:
        with st.chat_message(message['role']):
            st.write(message["content"])

# 创建一个聊天输入框
problem = st.chat_input("请输入你的问题")
# 判断是用来确定用户有没有输入问题 如果输入问题
if problem:
    # 1、将用户的问题输出到界面上，以用户的角色输出
    with st.chat_message("user"):
        st.write(problem)
    st.session_state.cache.append({"role":"user","content":problem})
    # 2、调用大模型回答问题的
    result = model.invoke(problem)
    # 3、将大模型回答的问题输出到界面上
    with st.chat_message("assistant"):
        st.write(result.content)
    st.session_state.cache.append({"role": "assistant", "content":result.content })