# 目次

- [初めに](#初めに)
- [動作環境設定](#動作環境設定)
- [OPENAI APIキーの設定](#openai-apiキーの設定)
- [実行方法](#実行方法)
- [評価記録](#評価記録)

# 初めに

このアプリは南海放送もぎたてテレビナレーション原稿を愛媛新聞に掲載する文章へと要約するアプリとなっている。

その目的としては、同じ内容の文章であってもナレーション原稿や、新聞記事、Web記事やSNS投稿文章など、さまざまな場面に応じて書き換える必要があるため、一つの記事から他の場面に応じた記事内容へ変更できるようにすることが挙げられる。

今回は前述したようにナレーション原稿を新聞記事へ要約することに主に取り組んだ。

# 動作環境設定

Streamlit、Langchain、OpenAIの利用に必要なライブラリのインストールを行う。

### for windows
コマンドプロンプトを開き
```
pip install streamlit langchain openai
```
※利用できない場合は[こちら](https://qiita.com/celeron5576/items/9ba3588a97fea46c6946)

### for mac
ターミナルを開き
```
pip3 install streamlit langchain openai
```

# OPENAI APIキーの設定

## OPENAI APIキーの取得
- [OPENAIのサイト](https://openai.com/product)へアクセス

```Get started```をクリック。

アカウントの作成、またはサインインを行い、以下の画面左のリストにあるAPI keysをクリック。

![api_key](https://github.com/manabekota/nankai_pbl/blob/main/.image_dir/api_key.png)

```+Create new secret key``` をクリックし、APIキーを作成。

※このとき得られるKEYを"YOUR KEY"とする。

### for Windows
windowsの「設定」を開いて、検索窓から「環境変数」として出てくる「環境変数を編集」を開く。
![open_en_var](https://github.com/manabekota/nankai_pbl/blob/main/.image_dir/open_en_var.png)

環境変数のウィンドウが開いたら、上段の「ユーザー環境変数」の「新規」をクリック。
![en_var](https://github.com/manabekota/nankai_pbl/blob/main/.image_dir/en_var.png)

変数名として、「OPENAI_API_KEY」、変数値は入手したAPIキー「YOUR KEY」を貼り付ける。
![edit_en_var](https://github.com/manabekota/nankai_pbl/blob/main/.image_dir/edit_en_var.png)

### for Linux / MacOS
ターミナルで以下のコマンドを実行して、**yourkey**を取得したAPIキーに置き換える。
```
echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
```

その後、新しい変数でシェルを更新する。
```
source ~/.zshrc
```

その後、以下のコマンドで環境変数が設定されていることを確認する。
```
echo $OPENAI_API_KEY
```

表示されれば、先ほどまでの```.zshrc```を```.bash_profile```に置き換えて実行する。
```
echo "export OPENAI_API_KEY='yourkey'" >> ~/.bash_profile
source ~/.bash_profile
```

## APIキーの不正利用があったときは
OPENAIのサイトにログインすることで使用状況とその料金を監視することができる。
APIキーの漏洩等による不正利用があった場合には[APIkeys](https://platform.openai.com/account/api-keys)ページからすぐにキーを更新して再度設定し直すようにする。

## OPENAI APIキーの商用利用について
OPENAI社の利用規約には、出力に関する再販、販売、商品化の権利はユーザーに譲渡される旨が記載されている。
ChatGPTは利用規約上は商用利用できるが、以下のような点などには注意しなければならない。
- 法律の遵守
- 自分自身や他人に危害を加えるための使用を禁止
- 安全対策の尊重

ChatGPTの利用ポリシーについては[こちら](https://openai.com/policies/usage-policies)

# 実行方法

### リポジトリのクローン作成
保存したいディレクトリの場所で以下のコマンドを実行する。
初期設定時のみ行う。
```
git clone https://github.com/manabekota/nankai_pbl
```

### few-shot用データセットの準備
few-shotの例で使用するデータを、A列に原稿、B列に要約として3件用意し、カンマ区切りのcsvファイル(add_dataset.csv)として保存する。

このcsvファイルを、リポジトリをクローンしたディレクトリと同じディレクトリに置く。

app.pyとadd_dataset.csvが同じディレクトリ内に存在するようにする。

### リポジトリへ移動
```
cd nankai_pbl
```

### 実行
これによりサイトが開きます。
```
streamlit run app.py
```

### 利用方法について
サイト上にあるテキストボックスに要約したい文章を入力し、新聞用かSNS用を選択して要約ボタンを押す。

または要約したい文章が記述されたテキストファイルをアップロードして要約形式を選択して要約ボタンを押す。


# 評価記録

### 文字数やROUGEスコアについて記録しておく。
+p：プロンプト改良

+f-n：few-shot実装（n件）
||既存手法<br>(独自データ)|既存手法<br>(南海放送データ)|GPT|GPT<br>+p +f-2|
|:---|:---|:---|:---|:---|
|ROUGE-1|0.1698|0.2415|0.3598|0.3929|
|ROUGE-2|0.0060|0.0102|0.0890|0.0945|
|ROUGE-L|0.1128|0.1473|0.1986|0.2291|
|文字数平均(文字)<br>評価用：192.3|72.0|182.3|244.6|192.7|
