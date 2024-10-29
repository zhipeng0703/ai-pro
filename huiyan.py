'''
基于历史聊天记录的对话模型
1、大模型对象
2、提示词工程对象
3、记忆模块对象
4、chain链对象
'''
import streamlit as st
# langchain调用大模型，导入langchain的代码 大模型对象
from langchain_openai import ChatOpenAI
# 引入一个提示词对象 langchain中有很多提示词对象，只用一个简单的对象PromptTemplate
from langchain.prompts import PromptTemplate
# 引入一个记忆模块对象，记忆模块也是很多种
from langchain.memory import ConversationBufferMemory
# 引入一个langchain的链对象，也有很多种，简单的链LLMChain
from langchain.chains import LLMChain

# 创建大语言模型对象
model = ChatOpenAI(
    temperature=0.8, # 温度，创新性
    model="glm-4-plus", # 大模型的名字
    base_url="https://open.bigmodel.cn/api/paas/v4/", # 大模型的地址
    api_key="909d29c7f1e28c2d92c3f32b453d0b11.U2XRoY1Q7UVd55PV" # 账号信息
)
# 创建记忆模块对象 记忆模块需要结合提示词模块使用，记忆模块保存的数据当作提示词信息传递给大模型即可
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history")
# 创建提示词对象
prompt = PromptTemplate.from_template("你叫柳如烟，你现在扮演的是一个女朋友的角色，你现在要和你的男朋友对话，你男朋友的话是{input},你需要对你男朋友的话做出回应，而且只做回应，你和你男朋友的历史对话为{history}")
# 使用langchain链关联大模型和提示词对象
chain = LLMChain(
    llm=model,
    prompt=prompt,
    memory=st.session_state.memory,
)

st.title("村里有个姑娘叫小芳❀❀❀")
# 构建一个缓存，用来保存聊天记录
if "cache" not in st.session_state:
    st.session_state.cache = []
else:
    # 需要从缓存中获取对话信息在界面上渲染  缓存两块内容 角色 角色的消息
    for message in st.session_state.cache:
        with st.chat_message(message['role']):
            st.write(message["content"])

# 创建一个聊天输入框
problem = st.chat_input("你的小芳正在等待你的回应")
# 判断是用来确定用户有没有输入问题 如果输入问题
if problem:
    # 1、将用户的问题输出到界面上，以用户的角色输出
    with st.chat_message("user"):
        st.write(problem)
    st.session_state.cache.append({"role":"user","content":problem})
    # 2、调用链对象回答问题的
    result = chain.invoke({"input":problem})
    # 3、将大模型回答的问题输出到界面上
    with st.chat_message("assistant"):
        st.write(result['text'])
    st.session_state.cache.append({"role": "assistant", "content":result['text'] })