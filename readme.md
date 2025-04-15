# RAG Search Accuracy Evaluator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/github/license/iwaitu/rag-accuracy-evaluator)
![Eval Mode](https://img.shields.io/badge/Mode-model--vs--model%20%7C%20rag--vs--rag-yellow)
![Status](https://img.shields.io/badge/Ready%20To%20Use-green)

这是一个用于评估 RAG 系统检索准确率的工具。通过对指定文档自动生成问题和标准答案，并调用 RAG 系统进行查询，评估返回结果是否匹配预期。

## 🔍 评测思路

本项目旨在精准评估 RAG（Retrieval-Augmented Generation）系统的**搜索准确率**，而非语言生成质量。系统通过构造问答样本集，对每条问题从 RAG 系统中获取检索内容，并结合大模型的判断与语义相似度分析，量化其准确性。

项目支持两种横向对比模式：

### 模式一：`model-vs-model` —— 比较不同模型在相同 RAG 返回内容下的判断能力
- 所有系统使用相同的 RAG 接口进行检索；
- 指定一个“标准模型”生成问题与标准答案；
- 其他模型使用自身能力判断 RAG 的返回内容是否符合答案标准。
- 应用于评估 **不同大模型对检索结果的理解和判断能力差异**。

### 模式二：`rag-vs-rag` —— 比较不同 RAG 系统在相同模型评判下的检索效果
- 所有系统使用相同的评判模型（如 GPT-4o）；
- 每个系统使用不同的 RAG 接口进行搜索；
- 统一使用模型进行摘要、判定与打分。
- 应用于评估 **不同向量库/切片策略/检索方法的效果优劣**。

评估指标包括：
- LLM 判断是否“语义匹配”
- 向量相似度（embedding cosine similarity）
- 综合得分（结合二者）

---

## ✅ 功能特性
- 自动生成每篇文档的多个问题与标准答案（基于 OpenAI GPT）
- 上传文档至 RAG 系统
- 调用 RAG 搜索接口获取结果
- 利用大模型判断答案是否匹配 + 向量相似度评估
- 输出包含图表和评分详情的深色 HTML 报告
- 支持两种横向对比模式（不同模型 vs 不同 RAG）

---

## 📦 安装依赖
```bash
pip install -e .
```

---

## ⚙️ 配置
参考以下两个配置文件：
- `config.model_vs_model.yaml`：不同模型评估同一 RAG
- `config.rag_vs_rag.yaml`：相同模型评估不同 RAG

---

## 🚀 使用方法
```bash
rag-eval --config config.model_vs_model.yaml
rag-eval --config config.rag_vs_rag.yaml
```

---

## 🧪 示例文本文件夹结构
```
texts/
├── doc1.txt
├── doc2.txt
```

---

## 📄 开源协议
MIT License - 欢迎社区贡献改进
