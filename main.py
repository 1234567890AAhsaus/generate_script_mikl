import streamlit as st
#https://python.langchain.com/docs/integrations/llms/tongyi/  --- lanchain_tongyi
#https://help.aliyun.com/zh/dashscope/developer-reference/activate-dashscope-and-create-an-api-key  --- keyword
import streamlit as st
import pandas as pd

from langchain.prompts import ChatPromptTemplate
import os


from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage



def generate_script(subject, video_length, creativity):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             """
             )
        ]
    )
    os.environ["DASHSCOPE_API_KEY"] = "sk-c29e90529fb749f390f02be4693112a2"
    model = ChatTongyi(streaming=True, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content


    script = script_chain.invoke({"title": title, "duration": video_length}).content
    return title, script





st.title("🎬 视频脚本生成器")



subject = st.text_input("💡 请输入视频的主题")
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("生成脚本")


if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()
if submit:
    with st.spinner("AI正在思考中，请稍等..."):
        title, script = generate_script(subject, video_length, creativity)
    st.success("视频脚本已生成！")
    st.subheader("🔥 标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)

