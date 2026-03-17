# analyzer-routing

## 目的

这是 `analyzer.py` 的 skill 实现层说明文件。

它的核心职责不是直接修复文档，而是先给出一份足够让 LLM 做下一步决策的分析结果，用于触发后续工具调用。

## 对外定位

- 唯一入口：`inspect_document_for_routing`
- 实现文件：`skills/analyzer_routing.py`
- 注入适配层：`src/doc_demo/skills/builtin.py`

## 输入

- `input_path`
  - 一个 `.docx` 文件路径

## 输出

返回一个结构化对象，包含：

- `summary`
- `issue_counts`
- `routing_hint`
- `recommended_tools`
- `samples`
- `raw_analysis`

## 路由目标

默认用于决定是否调用：

- `fix_document_punctuation`
- `format_document_with_preset`
- 或转入人工复核
