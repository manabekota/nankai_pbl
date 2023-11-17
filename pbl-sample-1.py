import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage
from langchain.schema import AIMessage

import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain

# OpenAIのモデルのインスタンスを作成
# chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# プロンプトのテンプレート文章を定義
template = """
次の文章に誤字がないか調べて。誤字があれば訂正してください。
{sentences_before_check}
"""

# テンプレート文章にあるチェック対象の単語を変数化
prompt = PromptTemplate(
    input_variables=["sentences_before_check"],
    template=template,
)

# OpenAIのAPIにこのプロンプトを送信するためのチェーンを作成
chain = LLMChain(llm=chat, prompt=prompt,verbose=True)

# チェーンを実行し、結果を表示
print(chain("こんんんちわ、真純です。")['text'])
