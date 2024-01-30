# nankai_pbl

- ここには成果物を再現するための説明を書くこと
- 例えばファイルの配置場所の関係や実行環境の確認なども含める。

- [初めに](https://github.com/manabekota/nankai_pbl/blob/main/README.md#初めに)
- [動作環境設定](https://github.com/manabekota/nankai_pbl/blob/main/README.md#動作環境設定)
- [実行方法](https://github.com/manabekota/nankai_pbl/blob/main/README.md#実行方法)
- [評価記録](https://github.com/manabekota/nankai_pbl/blob/main/README.md#評価記録)

## 初めに

このアプリは南海放送もぎたてテレビナレーション原稿を愛媛新聞に掲載する文章へと要約するアプリとなっている。

その目的としては、同じ内容の文章であってもナレーション原稿や、新聞記事、Web記事やSNS投稿文章など、さまざまな場面に応じて書き換える必要があるため、一つの記事から他の場面に応じた記事内容へ変更できるようにすることが挙げられる。

今回は前述したようにナレーション原稿を新聞記事へ要約することに主に取り組んだ。

## 動作環境設定

### Streamlit、Langchain、OpenAIの利用に必要なライブラリのインストール

#### for windows
※Pythonをインストールし、pipコマンドが利用できることを確認してください。
- 利用できない場合は[こちら](https://qiita.com/celeron5576/items/9ba3588a97fea46c6946)

```pip install streamlit langchain openai```
#### for mac
```pip3 install streamlit langchain openai```

### 環境変数にAPIキーを設定
```export OPENAI_API_KEY="YOUR KEY"```

### リポジトリのクローン作成
```git clone https://github.com/manabekota/nankai_pbl```

## 実行方法

### リポジトリへ移動
```cd nankai_pbl```

### 実行
これによりサイトが開きます。
```streamlit run app.py```

## 評価記録

### 文字数やROUGEスコアについて記録しておく。


