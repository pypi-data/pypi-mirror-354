# playground_common_utils

Pythonで汎用的な**ファイル操作・ディレクトリ操作・ログ出力**を支援するライブラリです。

---

## 🚀 インストール

インストールするには：

```bash
pip install playground-common-utils
```

## 📦 主な機能

### 確認系
- `is_exist(path)` : パスの存在確認
- `is_file(path)` : ファイルか確認
- `is_dir(path)` : ディレクトリか確認
- `is_match_first_keyword(target, first_keyword)` : 文字列の最初のキーワードが一致しているか
- `is_match_last_keyword(target, last_keyword)` : 文字列の最後のキーワードが一致しているか

### 作成系
- `create_file(path)` : 空ファイル作成
- `create_dir(path)` : ディレクトリ作成

### 取得系
- `read_current_dir()` : カレントディレクトリ取得
- `read_file(path)` : ファイル内容取得
- `read_list_dir(path)` : ディレクトリ内一覧取得

### 更新系
- `overwrite_file(path, content)` : ファイルに上書き
- `append_file(path, content)` : ファイルに追記

### 削除系
- `delete_file(path)` : ファイル削除
- `delete_dir(path)` : ディレクトリ削除

### 操作系
- `copy_file(src_path, dst_path)` : ファイルコピー
- `move_file(src_path, dst_path)` : ファイル移動

### ログ出力系
`logger.debug("Debug test")` : デバッグ ログ出力
`logger.info("Debug test")` : インフォ ログ出力
`logger.worning("Debug test")` : ワーニング ログ出力
`logger.error("Debug test")` : エラー ログ出力
`logger.critical("Debug test")` : クリティカル ログ出力

logger.set_level(WARNING)　: Warning以上のログ出力可能 / DEBUG,INFOログは出力しない 
---

## 🛠️ 使用例

``` python
ファイル作成・書き込み・削除
from playground_common_utils.files import *

# ファイル作成
create_file('sample.txt')

# ファイル上書き
overwrite_file('sample.txt', 'Hello World')

# ファイル削除
delete_file('sample.txt')
```

## ディレクトリ操作
``` python
from playground_common_utils.files import *

# ディレクトリ作成
create_dir('new_folder')

# ディレクトリ内一覧取得
items = read_list_dir('new_folder')

# ディレクトリ削除
delete_dir('new_folder')
```

## ログ出力
```python
from playground_common_utils.logger import logger
logger.debug("Debug test")
# 🐞 2025-05-20 21:45:19 [DEBUG] | <stdin> / <module>  [1] | Debug test

logger.info("Info test")
# ℹ️  2025-05-20 21:45:33 [INFO] | <stdin> / <module>  [2] | Info test

logger.warning("Warning test")
# ⚠️  2025-05-20 21:45:40 [WARNING] | <stdin> / <module>  [3] | Warning test

logger.error("Error test")
# 🚨 2025-05-20 21:45:51 [ERROR] | <stdin> / <module>  [4] | Error test

logger.critical("Critical test")
# 🔥 2025-05-20 21:45:58 [CRITICAL] | <stdin> / <module>  [5] | Critical test
```

## HTTP通信
```python
from playground_common_utils.logger import http, HTTP_Method

response = fetch(url="http://example.com", # Endpoint URL
      method=HTTP_Method.GET, # GET / POST / PUT / DELETE
      request_headers={"Content-Type": "application/json"}, # Default = {"Content-Type": "application/json"}
      request_dict={}) # python dict型 ⚠️ 内部的にjsonに変換しリクエスト送信します
```

## ⚙️ 対応バージョン

* Python 3.7以上

## 📄 ライセンス

MITライセンス

## 👤 作者情報

Author: Hiroki Umatani
Project URL: [Github](https://github.com/HirokiUmatani/playground_common_utils)

playground-common-utilsは、実業務に直結するファイル管理作業の効率化を目指して開発されました。
営業・開発・レポート作成などのプロジェクトを圧倒的スピードで推進するための基盤ライブラリです。