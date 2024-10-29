'''
制作一个带有自定义角色的一个大模型应用
用到三个知识点：
1、大模型对象
2、提示词对象
3、链chain
使用流程：首先需要构建一个大模型对象，然后创建提示词工程对象，然后使用langchain中的chain链将大模型对象和提示词工程对象组合起来，此时回答问题的时候使用链来回答
'''
import streamlit as st
# langchain调用大模型，导入langchain的代码 大模型对象
from langchain_openai import ChatOpenAI
# 引入一个提示词对象 langchain中有很多提示词对象，只用一个简单的对象PromptTemplate
from langchain.prompts import PromptTemplate
# 引入一个langchain的链对象，也有很多种，简单的链LLMChain
from langchain.chains import LLMChain

# 创建大语言模型对象
model = ChatOpenAI(
    temperature=0.8, # 温度，创新性
    model="glm-4-plus", # 大模型的名字
    base_url="https://open.bigmodel.cn/api/paas/v4/", # 大模型的地址
    api_key="909d29c7f1e28c2d92c3f32b453d0b11.U2XRoY1Q7UVd55PV" # 账号信息
)
# 创建提示词对象
prompt = PromptTemplate.from_template("你现在是一个专业的律师，你的名字是张伟，你现在要对你的委托人员的法律问题做回答，你只会回答法律方面的问题，其他类型的问题你一概回答你不知道，不要给自己加戏，你的委托人的问题是{input}")
# 使用langchain链关联大模型和提示词对象
chain = LLMChain(
    llm=model,
    prompt=prompt
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