import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def main():
    llm = ChatOpenAI(temperature=0,model_name="gpt-4")

    col1, col2 = st.columns([2, 1])  # カラムの幅を調整

    col1.markdown("# &#8203;``【番宣にすぐ利用可能！】``&#8203;")
    st.markdown("# もぎたてテレビを簡単にお伝え")
    col2.image("thum_mogitate.png", width=200)

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # テキスト入力またはファイルアップロードの選択
    st.markdown("\n\n")
    option = st.radio("テキスト入力またはファイルアップロード", ("テキスト入力", "ファイルアップロード"))

    output_format = None  # 初期の出力形式

    if option == "テキスト入力":
        # テキスト入力
        user_input = st.text_area("もぎたてテレビの原稿を入力してください", "")
        output_format = st.radio("出力形式を選択してください", ("SNS用", "新聞用"))
        if output_format in ("SNS用", "新聞用"):
            if st.button("要約する"):
                # 既存の要約指示をクリアして新しい要約指示を追加
                st.session_state.messages = []
                if output_format == "SNS用":
                    st.session_state.messages.append(
                        SystemMessage(content="入力された文章を180字程度に要約してください")
                    )
                elif output_format == "新聞用":
                    st.session_state.messages.append(
                        SystemMessage(content="入力された文章を、固有名詞を入れないで、”応募”に関する文章は除外して180字程度に要約してください")
                    )
                
                # ユーザーの入力をAIに送信して応答を取得
                st.session_state.messages.append(HumanMessage(content=user_input))
                with st.spinner("要約作成中..."):
                    response = llm(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))
    else:
        # ファイルアップロード
        uploaded_file = st.file_uploader("もぎたてテレビの原稿をアップロードしてください", type=["txt"])
        if uploaded_file is not None:
            file_contents = uploaded_file.read()
            input_text = file_contents.decode("utf-8")
            output_format = st.radio("要約の種類を選択してください", ("SNS用", "新聞用"))
            if output_format in ("SNS用", "新聞用"):
                if st.button("要約する"):
                    # 既存の要約指示をクリアして新しい要約指示を追加
                    st.session_state.messages = []
                    if output_format == "SNS用":
                        st.session_state.messages.append(
                            SystemMessage(content="入力された文章を200字程度に要約してください")
                        )
                    elif output_format == "新聞用":
                        st.session_state.messages.append(
                            SystemMessage(content="入力された文章を、固有名詞を入れないで、”応募”に関する文章は除外して180字程度に要約してください")
                        )

                    # ファイルからのテキストをAIに送信して応答を取得
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
        elif isinstance(message, SystemMessage):
            pass  # システムメッセージは表示しない

if __name__ == '__main__':
    main()
