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

## 🎯 Overview
**pulldoc** is a tool for communicating repository history to LLM!
It analyzes GitHub pull request history and automatically generates modification patterns and issue templates, so you can leverage LLM to improve your team's development efficiency!

## 🌟 Key Features

<details>
<summary><b>📊 Pull Request Collection & Analysis</b></summary>

- Automatic collection of PR history through GitHub API
- Efficient retrieval of PRs within specified ranges
- Structured information for merged and unmerged PRs
</details>

<details>
<summary><b>🤖 AI-Driven Summary Generation</b></summary>

- Support for multiple LLM models including [Bedrock, Huggingface, VertexAI, TogetherAI, Azure, OpenAI, Groq etc.]
- Flexible summary generation with custom prompts
- Multilingual support
- Efficient batch processing for large data volumes
</details>

<details>
<summary><b>📈 Intelligent Analysis</b></summary>

- Automatic identification of code fix patterns
- Classification and organization of common issues
- Team development trend analysis
- Generation of reusable templates
</details>



## 🚀 Quick Start

```bash
# Set LLM API Key
export OPENAI_API_KEY="your_openai_api_key" or other LLM provider settings

# Set Github Token (Private Only)
export GITHUB_TOKEN="your_github_token"
```

Using uvx
```bash
uvx pulldoc run {owner/repo-name}
```

### 💻 Installation

```bash

# Install dependencies (uv recommended)
uv add pulldoc

# or use pip
pip install pulldoc
```

### 🎯 Basic Usage

```bash
pulldoc run {owner/repo-name}
```
```
# Options
--start INTEGER # starting point of PR number
--end INTEGER # end point of PR number
--model TEXT # LLM model (default: gpt-4o-mini)
--custom-prompt TEXT # custom prompt
--lang TEXT # language (default: en)
--only-total # generate final summary only.

```

- Execute individually.
```
# 1. collect PR data
pulldoc collect owner/repo-name --start 100 --end 200

# 2. summarize collected data
pulldoc summarize owner/repo-name --model us.anthropic.claude-sonnet-4-20250514-v1:0 --lang ja
```


## 📁 Output Structure

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


## 🤝 Contributing

We welcome contributions to pulldoc!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request


## 🐛 Bug Reports & Feature Requests

If you discover issues or have ideas for new features, please let us know through [Issues](https://github.com/ppspps824/pulldoc/issues).

When reporting bugs, please include the following information:
- Python version
- Command executed
- Error message
- Expected behavior

## 📄 License

This project is released under the [MIT License](LICENSE).

## 🙏 Acknowledgments

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/GitHub_API-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub API" />
  <img src="https://img.shields.io/badge/Typer-009639?style=for-the-badge&logoColor=white" alt="Typer" />
  <img src="https://img.shields.io/badge/litellm-4B275F?style=for-the-badge&logoColor=white" alt="litellm" />
</p>

---

<div align="center">

**⭐ If this project was helpful, [please give it a star!](https://github.com/ppspps824/pulldoc/stargazers) ⭐**


</div>
