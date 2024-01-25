import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
import base64
import pandas as pd

def summarize(output_format, llm, user_input):
    # 既存の要約指示をクリアして新しい要約指示を追加
    st.session_state.messages = []

    if output_format == "SNS用":
        st.session_state.messages.append(
            SystemMessage(content="入力された文章を200字程度に要約してください。人の名前は入れないでください。また、最初の一文に魅力的な文章を入れてください。")
        )
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)

    elif output_format == "新聞用":
        prefix, prompt_text, user_input = few_shot_prompt(user_input)
        st.session_state.messages.append(
            SystemMessage(content=prefix)
        )
        # ユーザーの入力をAIに送信して応答を取得
        with st.spinner("ChatGPT is typing ..."):
            response = llm([HumanMessage(content=prompt_text)])
        st.session_state.messages.append(HumanMessage(content=user_input))


    st.session_state.messages.append(AIMessage(content=response.content))


    # ファイル出力ボタン
    output_filename = "summary.txt"
    download_link = create_download_link(response.content, output_filename)
    st.markdown(download_link, unsafe_allow_html=True)

    return response

def few_shot_prompt(input):
    csv_exfile_path = 'add_dataset.csv'
    ex_df = pd.read_csv(csv_exfile_path, delimiter=',', names=['main', 'summarize'])

    examples = [
        {"text": ex_df['main'][0], "summarize": ex_df['summarize'][0]},
        {"text": ex_df['main'][1], "summarize": ex_df['summarize'][1]},
    ]
    example_formatter_template = "原稿: {text}\n要約: {summarize}"
    example_prompt = PromptTemplate(
        template=example_formatter_template,
        input_variables=["text", "summarize"]
    )

    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="入力された文章を、固有名詞を入れないで、”応募”に関する文章は除外して180字程度に要約してください。人の名前は入れないでください。また、最初の一文に魅力的な文章を入れてください。",
        suffix="原稿: {input}\n要約:",
        input_variables=["input"],
        example_separator="\n",
    )
    
    prompt_text = few_shot_prompt.format(input=input)

    return few_shot_prompt.prefix, prompt_text, input

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
                response = summarize(output_format, llm, user_input)
    else:
        # ファイルアップロード
        uploaded_file = st.file_uploader("もぎたてテレビの原稿をアップロードしてください", type=["txt"])
        if uploaded_file is not None:
            file_contents = uploaded_file.read()
            input_text = file_contents.decode("utf-8")
            output_format = st.radio("要約の種類を選択してください", ("SNS用", "新聞用"))
            if output_format in ("SNS用", "新聞用"):
                if st.button("要約する"):
                    response = summarize(output_format, llm, user_input)

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
                # 文字数を表示
                st.write(f"文字数：{len(response.content)}")
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        elif isinstance(message, SystemMessage):
            pass  # システムメッセージは表示しない

def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">要約結果をダウンロード</a>'
    return href

if __name__ == '__main__':
    main()
