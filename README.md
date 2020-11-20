# Neo's Python Note

Python 製のオレオレノート。


## 機能

- パスワード認証により、管理者だけが管理・閲覧できる、オリジナルのノート。単一ファイルの Google Keep 的な使い方を想定
- ノートはテキストファイルに保存する


## 設定

`index.py` の `定数` 部分を自環境に合わせて変更する。

- `PRIVATE_DIRECTORY_PATH`
    - クレデンシャルファイルやノートファイルを格納する「プライベートディレクトリ」のパス。Python の配置先から見た相対パスで記載できる
    - ex. Apache サーバの `/var/www/html/` に `index.py` を配置した場合、`'../private'` と指定すれば、`/var/www/private/` ディレクトリ配下を参照するようになる
- `CREDENTIAL_FILE_PATH`
    - アクセスパスワードを書いた「クレデンシャルファイル」の名前を記す
    - `PRIVATE_DIRECTORY_PATH` と結合して参照するので、デフォルトの記述のままでいけば `/var/www/private/credential.txt` を参照することになる
- `NOTE_FILE_NAME`
    - ノートを保存する「ノートファイル」の名前を記す
    - `PRIVATE_DIRECTORY_PATH` と結合するので、デフォルトの記述のままでいけば `/var/www/private/note.txt` といったファイルが生成される
    - ファイルが存在しなかった場合は `NOTE` を記入したファイルを生成する
- `PAGE_TITLE`
    - `title` 要素で示されるページタイトル
- `HEADLINE_TITLE`
    - 見出し (`h1` 要素) に指定するタイトル
- `HEADLINE_URL`
    - エラー画面の `h1` 要素に適用するリンク URL


## 導入方法

1. Apache サーバで Python を CGI として利用できるように設定する
2. Apache サーバの `/var/www/html/` 配下などに `index.py` を配置する
3. 変数 `PRIVATE_DIRECTORY_PATH` + `CREDENTIAL_FILE_PATH` のパスに、アクセスパスワードを記した1行のテキストファイル (クレデンシャルファイル) を作る
4. `index.py`、プライベートディレクトリ、クレデンシャルファイル、ノートファイルのパーミッションを適宜設定する
5. `index.py` にアクセスする


## 管理者閲覧の方法

URL に `credential` パラメータを指定してアクセスすると、ノートが表示できる。

- ex. `http://example.com/index.py?credential=MY_CREDENTIAL`

`credential` パラメータで指定したパスワードの整合性は、「クレデンシャルファイル」と突合して確認する。

管理者用画面では、ノートの参照・編集・保存が行える。


## Links

- [Neo's World](https://neos21.net/)
