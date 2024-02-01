import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
import base64
import pandas as pd
import re

def summarize(output_format, llm, user_input):
    st.session_state.messages = []
    user_input = remove_strings(user_input)

    if output_format == "SNS用":
        content_message = '''
入力された文章はテレビ番組のナレーションに当たる文章です。私はこの文章を要約したのち、公式アカウントを利用してSNSにアップロードしたいと考えています。
しかし、この文章には本来必要のないプレゼントキャンペーンに関する文章が含まれています。あなたには入力された文章を、見た人が内容を知りたくなるような興味の惹かれる要約文にしてください。
ただし、SNSにアップロードするため不適切な表現をさけ、文字数制限にかからないように4行分程度の要約にしてください。
'''
        st.session_state.messages.append(
            SystemMessage(content=content_message)
        )
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            response = llm(st.session_state.messages)

    elif output_format == "新聞用":
        prefix, prompt_text, user_input = few_shot_prompt(user_input)
        st.session_state.messages.append(
            SystemMessage(content=prefix)
        )
        # get response
        with st.spinner("ChatGPT is typing ..."):
            response = llm([HumanMessage(content=prompt_text)])
        st.session_state.messages.append(HumanMessage(content=user_input))


    st.session_state.messages.append(AIMessage(content=response.content))


    # make output file link
    output_filename = "summary.txt"
    download_link = create_download_link(response.content, output_filename)
    st.markdown(download_link, unsafe_allow_html=True)

    return response

def remove_strings(cell_value):
    pattern_to_remove = re.compile(r'【.*?】|[ＲR][ー-]\d+|\n|\t|\s+|■|＊')
    
    cell_value = pattern_to_remove.sub('', cell_value)
    return cell_value

def few_shot_prompt(input):
    csv_exfile_path = 'add_dataset.csv'
    ex_df = pd.read_csv(csv_exfile_path, delimiter=',', names=['main', 'summarize'])

    ex_df['main'] = ex_df['main'].fillna('').astype(str)
    # preprocess few-shot data
    ex_df['main'] = ex_df['main'].apply(remove_strings)

    examples = [
        {"text": ex_df['main'][0], "summarize": ex_df['summarize'][0]},
        {"text": ex_df['main'][1], "summarize": ex_df['summarize'][1]},
    ]
    example_formatter_template = "原稿: {text}\n要約: {summarize}"
    example_prompt = PromptTemplate(
        template=example_formatter_template,
        input_variables=["text", "summarize"]
    )

    prefix="入力された文章はテレビ番組のナレーションに当たる文章です。私はこの文章を、要約して新聞に掲載したいと考えています。しかし、新聞では固有名詞を入れることが出来ないのです。さらにこの文章には本来必要のないプレゼントキャンペーンに関する文章が含まれています。あなたには入力された文章を、固有名詞を使わずに、かつ必要のない内容を含まない、4行以上5行未満の文章に要約してほしいです。要約した文章を出力する前に一度その文章の文字数が4行以上5行未満になっているか数え、超えている場合は出力する文章を変更してください。出力する文章が4行以上5行未満になるまで文章は出力せず、文字数確認の作業を繰り返し行ってください。"
    suffix="原稿: {input}\n要約:"
    
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input"],
        example_separator="\n",
    )
    
    prompt_text = few_shot_prompt.format(input=input)

    return few_shot_prompt.prefix, prompt_text, input

def main():
    llm = ChatOpenAI(temperature=0,model_name="gpt-4-0125-preview")

    col1, col2 = st.columns([2, 1])

    col1.markdown("# &#8203;``【番宣にすぐ利用可能！】``&#8203;")
    st.markdown("# もぎたてテレビを簡単にお伝え")
    col2.image("thum_mogitate.png", width=200)

    # reset chatlog
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown("\n\n")
    # text or file
    option = st.radio("テキスト入力またはファイルアップロード", ("テキスト入力", "ファイルアップロード"))

    output_format = None

    if option == "テキスト入力":
        # text
        user_input = st.text_area("もぎたてテレビの原稿を入力してください", "")
        output_format = st.radio("出力形式を選択してください", ("SNS用", "新聞用"))
        if output_format in ("SNS用", "新聞用"):
            if st.button("要約する"):
                response = summarize(output_format, llm, user_input)
    else:
        # file upload
        uploaded_file = st.file_uploader("もぎたてテレビの原稿をアップロードしてください", type=["txt"])
        if uploaded_file is not None:
            file_contents = uploaded_file.read()
            user_input = file_contents.decode("utf-8")
            output_format = st.radio("要約の種類を選択してください", ("SNS用", "新聞用"))
            if output_format in ("SNS用", "新聞用"):
                if st.button("要約する"):
                    response = summarize(output_format, llm, user_input)
    
    # show chatlog  
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
                st.write(f"文字数：{len(message.content) }")
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        elif isinstance(message, SystemMessage):
            pass  # pass system message

def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">要約結果をダウンロード</a>'
    return href

if __name__ == '__main__':
    main()
