# nankai_pbl

- ここには成果物を再現するための説明を書くこと
- 例えばファイルの配置場所の関係や実行環境の確認なども含める。

- [目的](#setup)
- [動作環境設定](#-run-this-app)
- [実行方法](#-score)

## setup

### Streamlit、Langchain、OpenAIの利用に必要なライブラリのインストール

#### for windows
※Pythonをインストールし、pipコマンドが利用できることを確認してください。
- 利用できない場合は[こちら]()

```
pip install streamlit langchain openai
```
#### for mac
```
pip3 install streamlit langchain openai
```

### 環境変数にAPIキーを設定
```
export OPENAI_API_KEY="YOUR KEY"
```

### リポジトリのクローン作成
```
git clone https://github.com/manabekota/nankai_pbl
```

## run this app

### リポジトリへ移動
```
cd nankai_pbl
```

### 実行
これによりサイトが開きます。
'''
streamlit run app.py
'''

## score

