# 核心思路：把数据库和大模型整合起来
# 实现：1、把数据库在代码中表示出来
# 2、定义大模型
# 3、langchain的链create_sql_query_chain把大模型和数据库链接起来 create_sql_query_chain链把用户的提问转换成为SQL查询语句
# 4、使用链把提问的问题转借助大模型生成SQL语句
# 5、通过数据库执行SQL得到结果
# 6、创建LLMChain这个链，在这个链中使用提示词工程把数据库执行的结果美化一下
# 大模型要从数据库进行问答，必须需要四个python库：langchain langchain-openai langchain-community pymysql
# 导入项目所需要的包和类
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import LLMChain,create_sql_query_chain
from langchain.prompts import PromptTemplate
import streamlit as st
st.title("就业岗位智能问答系统")
# 缓存历史对话
if "history" not in st.session_state:
    st.session_state.history = []
else:
    for ele in st.session_state.history:
        with st.chat_message(ele["role"]):
            st.write(ele["content"])

# 1、构建数据库
db = SQLDatabase.from_uri("mysql+pymysql://root:root@localhost:3306/job")
# 2、构建大模型
model = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key="909d29c7f1e28c2d92c3f32b453d0b11.U2XRoY1Q7UVd55PV",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
#3、使用create_sql_query_chain把数据库和大模型组合起来
sql_chain = create_sql_query_chain(llm=model,db=db)
#4、创建一个带有提示词的LLMChain链，这个链美化查询结果
prompt = PromptTemplate.from_template("现在你是一个专业的数据库问答专家，你只能对数据库的这些问题做回答，用户的提问是{input},数据库对问题的回答是{answer},你需要对数据库的回答加以美化，以人的说话的口吻输出结果")
beau_chain=LLMChain(llm=model,prompt=prompt)


# 通过界面制作一个聊天输入框
problem = st.chat_input("请输入你的问题")
# 判断输入框有没有填写信息
if problem:
    with st.chat_message("user"):
        st.write(problem)
    st.session_state.history.append({"role":"user","content":problem})
    # 先通过sql_chain这个链生成SQL语句
    sql = sql_chain.invoke({"question":problem})
    # 为了把生成的SQL中的无用信息去除，如果不取出 SQL执行一定会报错
    sql = sql.replace("```sql","").replace("```","").replace("SQLResult:","")
    print(sql)
    # 执行SQL
    result = db.run(sql)
    # 使用beau_chain这个链美化查询回来的结果 输出
    beau_result = beau_chain.invoke({
        "input":problem,
        "answer":result,
    })
    with st.chat_message("assistant"):
        st.write(beau_result["text"])
    st.session_state.history.append({"role": "assistant", "content": beau_result["text"]})