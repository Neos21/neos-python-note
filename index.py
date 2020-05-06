#!/usr/bin/python3


# ======================================================================
# Neo's Python Note
#
# Neo (@Neos21) http://neo.s21.xrea.com/
# ======================================================================


import cgi
import cgitb
import io
import json
import os
import pathlib
import sys

# 日本語文字を有効にする
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
# デバッグを有効にする
cgitb.enable()


# 定数
# ======================================================================

# Private ディレクトリのパス (末尾スラッシュなし) : この配下に「クレデンシャルファイル」と「ノートファイル」を配置する
PRIVATE_DIRECTORY_PATH = '../private'
# クレデンシャルファイル : 閲覧・保存用パスワードが記載されたファイル名
CREDENTIAL_FILE_NAME = 'credential.txt'
# ノートファイル : テキストを記録するファイル名
NOTE_FILE_NAME = 'note.txt'
# title 要素に指定するタイトル
PAGE_TITLE = '&#65279;'
# 見出しに指定するタイトル
HEADLINE_TITLE = "Neo's Python Note"
# 見出しに指定するリンク URL
HEADLINE_URL = 'http://neo.s21.xrea.com/'


# メイン処理
def main():
  # パラメータを取得する
  params = cgi.FieldStorage(keep_blank_values = True)
  
  # クレデンシャルパラメータの存在チェック
  if not 'credential' in params:
    response_error('Credential Is Null')
    return
  
  # ファイルからクレデンシャルを取得する
  try:
    credential_file = pathlib.Path(PRIVATE_DIRECTORY_PATH) / CREDENTIAL_FILE_NAME
    credential = credential_file.read_text(encoding = 'utf-8').strip()
    if params['credential'].value != credential:
      response_error('Invalid Credential')
      return
  except IOError:
    response_error('Failed To Open Credential File')
    return
  
  # リクエストメソッド別に処理して終了する
  if os.environ['REQUEST_METHOD'] == 'GET':
    on_get(params['credential'].value)
  elif os.environ['REQUEST_METHOD'] == 'POST':
    on_post(params)
  else:
    response_invalid_method()

# エラーレスポンス
def response_error(message):
  if os.environ['REQUEST_METHOD'] == 'GET':
    print_header()
    print(f'<h1><a href="{HEADLINE_URL}">{HEADLINE_TITLE}</a></h1>')
    print('<p><strong>Error : ' + message + '</strong></p>')
    print_footer()
  elif os.environ['REQUEST_METHOD'] == 'POST':
    print('Content-Type: application/json; charset=UTF-8\n')
    print(json.dumps({ 'error': message }))
  else:
    response_invalid_method()

# 意図しないリクエストメソッドはプレーンテキストでレスポンスする
def response_invalid_method():
  print('Content-Type: text/plain; charset=UTF-8\n')
  print('Invalid Method')

# HTML のヘッダ部分を出力する
def print_header():
  print('Content-Type: text/html; charset=UTF-8\n')
  # ヒアドキュメント中のブレースは2つずつ書くことでエスケープする : '{{' '}}'
  print('''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{page_title}</title>
    <style>

@font-face {{
  font-family: "Yu Gothic";
  src: local("Yu Gothic Medium"), local("YuGothic-Medium");
}}

@font-face {{
  font-family: "Yu Gothic";
  src: local("Yu Gothic Bold"), local("YuGothic-Bold");
  font-weight: bold;
}}

*,
::before,
::after {{
  box-sizing: border-box;
}}

html {{
  font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, YuGothic, "Yu Gothic", "Hiragino Sans", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  text-decoration-skip-ink: none;
  -webkit-text-size-adjust: 100%;
  -webkit-text-decoration-skip: objects;
  word-break: break-all;
  line-height: 1.5;
  background: #000;
  -webkit-overflow-scrolling: touch;
  cursor: default;
}}

html,
a {{
  color: #0d0;
}}

body {{
  margin: 0;
}}

h1 {{
  font-size: 1rem;
}}

h1 a {{
  text-decoration: none;
}}

h1 a:hover {{
  text-decoration: underline;
}}

#form {{
  display: grid;
  grid-template: "title message save" auto
                 "note  note    note" 1fr
                 / auto 1fr     auto;
  border: 1px solid #0c0;
}}

#title {{
  grid-area: title;
  margin: 0;
  padding: 0 1rem 0 .25rem;
  white-space: nowrap;
}}

#message {{
  grid-area: message;
  border-right: 1px solid #0c0;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}}

#save-btn,
#note {{
  margin: 0;
  border: 0;
  border-radius: 0;  /* For iOS */
  color: inherit;
  font-size: 1rem;
  font-family: inherit;
  background: transparent;
  outline: none;
}}

#save-btn {{
  grid-area: save;
}}

#save-btn:disabled {{
  color: #999;
}}

#note {{
  grid-area: note;
  border-top: 1px solid #0c0;
  padding: .25rem;
  min-height: 320px;  /* Optimized For iPhone */
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
  resize: vertical;
}}

/* Scrollbar Width */
#note::-webkit-scrollbar {{
  width: 10px;
}}

/* Scrollbar Colour */
#note::-webkit-scrollbar-thumb {{
  border-radius: 0;
  background: #090;
}}

/* Resizer */
#note::-webkit-resizer {{
  background: #060;
}}

#note::placeholder {{
  color: #090;
}}

.error {{
  color: #c00;
}}

.warning {{
  color: #990;
}}

    </style>
    <script>

document.addEventListener('DOMContentLoaded', () => {{
  const message = document.getElementById('message');
  const saveBtn = document.getElementById('save-btn');
  const note    = document.getElementById('note');
  if(!message || !saveBtn || !note) {{
    return;
  }};
  
  // Initial State
  saveBtn.disabled = true;
  let isEditted = false;
  let original  = note.value;
  
  // For PC
  window.addEventListener('beforeunload', (event) => {{
    if(isEditted) {{
      event.returnValue = '保存されていない内容があります';
      return '保存されていない内容があります';
    }}
  }});
  // FIXME : For iOS But Does Not Working On iOS 13
  window.addEventListener('pagehide', (event) => {{
    window.event.cancelBubble = true;
    if(isEditted) {{
      event.returnValue = '保存されていない内容があります';
      return '保存されていない内容があります';
    }}
  }});
  
  note.addEventListener('input', () => {{
    isEditted = note.value !== original;
    saveBtn.disabled = !isEditted;
    if(isEditted) {{
      message.innerHTML = '';
    }}
  }});
  
  saveBtn.addEventListener('click', () => {{
    saveBtn.disabled = true;
    message.innerHTML = '';
    const newOriginal = note.value;
    const form = document.getElementById('form');
    window.fetch(form.action, {{
      method: 'POST',
      body: new FormData(form) // Don't Set Content-Type Header
    }})
      .then((result) => {{
        console.log('Raw Result', result);
        return result.json();  // Get JSON Body
      }})
      .then((result) => {{
        console.log('JSON Result', result);
        if(result.error) {{
          message.innerHTML = `<span class="error">Error : ${{result.error}}</span>`;
          saveBtn.disabled = false;
          return;
        }}
        if(!result.result) {{
          message.innerHTML = '<span class="warning">OK (Unknown)</span>';
          saveBtn.disabled = false;
          return;  // Unexpected Success
        }}
        message.innerHTML = `${{result.result}}`;
        // Reset State
        saveBtn.disabled = true;
        isEditted = false;
        original = newOriginal;
      }})
      .catch((error) => {{
        console.error('Error', error);  // Unexpected Error
        message.innerHTML = `<strong class="error">Error : ${{error}}</strong>`;
        saveBtn.disabled = false;
      }})
  }});
}});

    </script>
  </head>
  <body>
'''.format(page_title = PAGE_TITLE).strip())

def print_footer():
  print('''
  </body>
</html>
'''.strip())

# GET 時の処理
def on_get(credential):
  note_file = pathlib.Path(PRIVATE_DIRECTORY_PATH) / NOTE_FILE_NAME
  
  # ファイルが存在しない場合は生成を試みる
  if not note_file.exists():
    try:
      with note_file.open(mode = 'w') as file:
        file.write('NOTE')
    except IOError:
      response_error('Cannot Create Note File')
      return
  
  # 取得する
  note = ''
  try:
    note = note_file.read_text(encoding = 'utf-8')
  except IOError:
    response_error('Cannot Read Note File')
    return
  
  print_header()
  print('''
<form action="{script_name}" id="form">
  <h1 id="title">{headline_title}</h1>
  <div id="message"></div>
  <input type="button" id="save-btn" value="Save" accesskey="s" tabindex="2">
  <textarea id="note" name="note" accesskey="n" tabindex="1" placeholder="Input Your Note">{note}</textarea>
  <input type="hidden" name="credential" value="{credential}">
</form>
'''.format(
  script_name = os.environ['SCRIPT_NAME'],
  headline_title = HEADLINE_TITLE,
  credential = credential,
  note = note
).strip())
  print_footer()

# POST 時の処理
def on_post(params):
  if not 'note' in params:
    response_error('Note Is Null')
    return
  
  try:
    note = params['note'].value.replace('\r', '')  # Force 'LF'
    note_file = pathlib.Path(PRIVATE_DIRECTORY_PATH) / NOTE_FILE_NAME
    with open(note_file, 'w', encoding = 'utf-8', newline = '\n') as file:
      file.write(note)
  except IOError:
    response_error('Cannot Write Note File')
    return
  
  print('Content-Type: application/json; charset=UTF-8\n')
  print(json.dumps({ 'result': 'Saved' }))


# メイン処理を実行する
main()
