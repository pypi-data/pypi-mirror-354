# Pulldoc テストスイート

このディレクトリには、pulldocプロジェクトの包括的なテストスイートが含まれています。

## テスト構造

```
test/
├── __init__.py                 # テストパッケージ
├── conftest.py                 # pytest設定とフィクスチャ
├── test_collector.py           # collector.pyのテスト
├── test_summarizer.py          # summarizer.pyのテスト
├── test_settings.py            # settings.pyのテスト
├── test_integration.py         # 統合テスト
└── README.md                   # このファイル
```

## テストの種類

### 1. ユニットテスト
各モジュールの個別機能をテストします：
- **test_collector.py**: GitHub PR収集機能のテスト
- **test_summarizer.py**: LLMを使用した要約機能のテスト
- **test_settings.py**: 設定管理機能のテスト

### 2. 統合テスト
- **test_integration.py**: モジュール間の連携とエンドツーエンドワークフローのテスト

## テスト実行方法

### 基本的な実行

```bash
# 全てのテストを実行
make test

# 詳細出力でテストを実行
make test-verbose

# カバレッジレポート付きでテストを実行
make test-coverage
```

### 特定のテストカテゴリを実行

```bash
# ユニットテストのみ実行
make test-unit

# 統合テストのみ実行
make test-integration
```

### 特定のテストファイルを実行

```bash
# collector機能のテストのみ
make test-collector

# summarizer機能のテストのみ
make test-summarizer

# settings機能のテストのみ
make test-settings
```

### pytestを直接使用

```bash
# 全てのテストを実行
pytest test/

# 特定のテストファイルを実行
pytest test/test_collector.py -v

# 特定のテストクラスを実行
pytest test/test_collector.py::TestFetchPRs -v

# 特定のテストメソッドを実行
pytest test/test_collector.py::TestFetchPRs::test_fetch_prs_success -v

# キーワードでフィルタ
pytest test/ -k "github" -v
```

## テスト環境の設定

### 開発依存関係のインストール

```bash
# 開発用の依存関係をインストール
make install-dev

# または直接pipを使用
pip install -e ".[dev]"
```

### 環境変数

テストは実際のAPIキーを必要としません。モック機能を使用してAPIコールをシミュレートします。

## カバレッジレポート

カバレッジレポートを生成するには：

```bash
make test-coverage
```

このコマンドは以下を生成します：
- ターミナルでのカバレッジサマリー
- `htmlcov/`ディレクトリ内のHTML形式の詳細レポート

## テストのベストプラクティス

### 1. テストの命名規則
- テストファイル: `test_<module_name>.py`
- テストクラス: `Test<ClassName>`
- テストメソッド: `test_<function_name>_<scenario>`

### 2. フィクスチャの使用
`conftest.py`で定義されたフィクスチャを活用：
- `temp_dir`: 一時ディレクトリ
- `sample_pr_data`: サンプルPRデータ
- `mock_github_client`: GitHub APIのモック

### 3. モックの使用
外部依存関係（GitHub API、LLM API）はモックを使用してテストします。

### 4. アサーション
明確で読みやすいアサーションを書きます：
```python
assert result.status == "success"
assert len(result.items) == 3
assert "error" not in result.message
```

## トラブルシューティング

### よくある問題

1. **ImportError**: `PYTHONPATH`が正しく設定されていることを確認
2. **ModuleNotFoundError**: 開発依存関係がインストールされていることを確認（`make install-dev`）
3. **テストファイルが見つからない**: プロジェクトルートディレクトリからコマンドを実行していることを確認

### デバッグ

テストのデバッグには以下のオプションが便利です：

```bash
# 最初の失敗で停止
pytest test/ -x

# 詳細な出力とlocal変数の表示
pytest test/ -vvv --tb=long

# 特定のテストをデバッグモードで実行
pytest test/test_collector.py::TestFetchPRs::test_fetch_prs_success -vvv --pdb
```

## CI/CD

継続的インテグレーション用のコマンド：

```bash
# 全てのチェック（リント + テスト + カバレッジ）
make test-ci
```

このコマンドは以下を実行します：
1. コードフォーマットのチェック（black、isort）
2. 全テストの実行
3. カバレッジレポートの生成

## 貢献

新しいテストを追加する際は：

1. 適切なテストファイルに追加（新機能の場合は新しいファイルを作成）
2. 明確なdocstringを記述
3. 必要に応じて新しいフィクスチャを`conftest.py`に追加
4. テストが成功することを確認（`make test`）
5. カバレッジが維持されることを確認（`make test-coverage`）
