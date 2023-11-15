import streamlit as st
from summarizer import summarize

def main():
    st.title("Text Summarizer App")

    # テキスト入力
    input_text = st.text_area("入力テキストを入力してください", "")

    # 要約ボタンがクリックされたときの処理
    if st.button("要約する"):
        # テキスト要約
        summary = summarize(input_text)

        # 要約結果の表示
        st.subheader("要約結果")
        st.write(summary)

if __name__ == "__main__":
    main()
