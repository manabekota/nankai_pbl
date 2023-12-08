import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)


def main():
    llm = ChatOpenAI(temperature=0)

    SystemMessage(content="入力された文章を300字程度に要約してください")

    st.set_page_config(
        page_title="ChatGPT",
        # page_icon="🤗"
    )
    st.header("ChatGPT")

    st.markdown("# &#8203;``【忙しい方必見！】``&#8203;\n# もぎたてテレビを簡単まとめ")

    st.image("thum_mogitate.png", width=500)

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [  ]

      # テキスト入力またはファイルアップロードの選択
    option = st.radio("テキスト入力またはファイルアップロード", ("テキスト入力", "ファイルアップロード"))

    if option == "テキスト入力":
        # テキスト入力
        user_input = st.text_area("もぎたてテレビの原稿を入力してください", "")
        if st.button("要約する"):
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("ChatGPT is typing ..."):
                response = llm(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
    else:
        # ファイルアップロード
        uploaded_file = st.file_uploader("もぎたてテレビの原稿をアップロードしてください", type=["txt"])
        if uploaded_file is not None:
            file_contents = uploaded_file.read()
            input_text = file_contents.decode("utf-8")
            if st.button("要約する"):
                st.session_state.messages.append(HumanMessage(content=input_text))
                with st.spinner("ChatGPT is typing ..."):
                    response = llm(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))


    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else: # isinstance(message, SystemMessage):
            st.write(f" ")
    
    


if __name__ == '__main__':
    main()
