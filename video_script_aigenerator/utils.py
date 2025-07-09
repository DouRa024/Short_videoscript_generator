from re import search

from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

#from langchain_community.chat_models.deepseek import ChatDeepSeek

def generate_script(subject,video_length,creativity,api_key):

    title_template = ChatPromptTemplate.from_messages(

        [
            ('human','请为{subject}这个主题的视频想一个吸引人的标题')

         ]

    )
    script_template = ChatPromptTemplate.from_messages(
      [  ("human",
         """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
         视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
         要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
         整体内容的表达方式要尽量轻松有趣，吸引年轻人。""")
         ]
    )

    model = ChatOpenAI(
        api_key=api_key,  # Replace with your DeepSeek API key
        base_url="https://api.deepseek.com/v1",  # DeepSeek endpoint
        model="deepseek-chat",  # or "deepseek-coder"
        temperature=creativity
    )
    #model=ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=creativity) # 替换为实际API密钥
              #ChatOpenAI(openai_api_key=api_key,temperature=creativity)

    title_chain= title_template | model
    script_chain=script_template | model

    title =title_chain.invoke({'subject':subject}).content

   # search=WikipediaAPIWrapper(lang='zh')

    #search_result=search.run(subject)

    script=script_chain.invoke({'title':title,'duration':video_length}).content

    return title,script

#print(generate_script('openai',1,0.7,'sk-d5ecfe9df3e34c1e9d2452b6e2841850'))