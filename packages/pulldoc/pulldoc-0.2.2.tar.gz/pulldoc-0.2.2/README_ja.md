<div align="center">
<img width="200" alt="pulldoc Logo" src="https://github.com/user-attachments/assets/8ee1b6e9-03c0-4448-8f4f-55295474b549">

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version"></a>
  <a href="https://pypi.org/project/pulldoc/"><img src="https://img.shields.io/pypi/v/pulldoc.svg?color=orange&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

<p align="center">
  <a href="./README.md">English</a>
  <a href="./README_ja.md">日本語</a>
</p>

</div>

---

## 🎯 概要

**pulldoc**はリポジトリの歴史をLLMに伝えるためのツールです！
GitHubのプルリクエスト履歴を解析し、修正パターンと課題テンプレートを自動生成します。LLMを活用してチームの開発効率を向上させましょう！


## 🌟 主な機能

<details>
<summary><b>📊 プルリクエスト収集・分析</b></summary>

- GitHub APIを通じたPR履歴の自動収集
- 指定した範囲のPRを効率的に取得
- マージ済み・未マージPRの詳細情報を構造化
</details>

<details>
<summary><b>🤖 AI駆動の要約生成</b></summary>

- Bedrock, Huggingface, VertexAI, TogetherAI, Azure, OpenAI, Groq など、複数LLMモデルに対応
- カスタムプロンプトによる柔軟な要約生成
- 多言語対応
- バッチ処理による効率的な大量データ処理
</details>

<details>
<summary><b>📈 インテリジェントな分析</b></summary>

- コードの修正パターンの自動識別
- よくある課題の分類と整理
- チーム開発における傾向分析
- 再利用可能なテンプレートの自動生成
</details>



## 🚀 クイックスタート

```bash
# LLMプロバイダーのAPIキー設定
export OPENAI_API_KEY="your_openai_api_key" or その他のLLMプロバイダー設定

# Github Tokenの設定（プライベートリポジトリのみ）
export GITHUB_TOKEN="your_github_token"
```

Using uvx
```bash
uvx pulldoc run {owner/repo-name}
```

### 💻 インストール

```bash

# 依存関係をインストール（uvを推奨）
uv add pulldoc

# または pip を使用
pip install pulldoc
```

### 🎯 基本的な使用方法

```bash
pulldoc run {owner/repo-name}

# オプション
--start INTEGER # PR番号の始点
--end INTEGER # PR番号の終点
--model TEXT  # LLMモデル (デフォルト: gpt-4o-mini)
--custom-prompt TEXT  # カスタムプロンプト
--lang TEXT # 言語 (デフォルト: en)
--only-total  # 最終要約のみ生成

```

- 個別実行
```
# 1. PRデータを収集
pulldoc collect owner/repo-name --start 100 --end 200

# 2. 収集したデータを要約
pulldoc summarize owner/repo-name --model us.anthropic.claude-sonnet-4-20250514-v1:0 --lang ja

```

## 📁 出力構造

```
.pulldoc_result/
└── owner/
    └── repo-name/
        ├── raws/
        │   ├── pr_001.json
        │   └── pr_002.json
        ├── summaries/
        |   ├── batch_001_summary.md
        |   ├── batch_002_summary.md
        ├── RULES_FOR_AI.md
        └── ISSUE_TEMPLATES.md

```


## 🤝 コントリビューション

pulldocへのコントリビューションを歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成


## 🐛 バグ報告・機能要望

問題を発見した場合や新機能のアイデアがある場合は、[Issues](https://github.com/ppspps824/pulldoc/issues)でお知らせください。

バグ報告の際は以下の情報を含めてください：
- Python バージョン
- 実行したコマンド
- エラーメッセージ
- 期待される動作

## 📄 ライセンス

このプロジェクトは[MIT License](LICENSE)の下で公開されています。

## 🙏 謝辞

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/GitHub_API-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub API" />
  <img src="https://img.shields.io/badge/Typer-009639?style=for-the-badge&logoColor=white" alt="Typer" />
  <img src="https://img.shields.io/badge/litellm-4B275F?style=for-the-badge&logoColor=white" alt="litellm" />
</p>

---

<div align="center">

**⭐ このプロジェクトが役に立ったら、　[スター](https://github.com/ppspps824/pulldoc/stargazers)をお願いします！ ⭐**

</div>
