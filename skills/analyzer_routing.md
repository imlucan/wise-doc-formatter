# analyzer-routing

## Purpose

分析一个 `.docx` 文件，返回可用于后续决策的结构化结果。

## Entry

- `inspect_document_for_routing`

## Inputs

- `input_path`
  - `.docx` 文件路径

## Outputs

返回一个结构化对象，包含：

- `summary`
- `issue_counts`
- `routing_hint`
- `recommended_tools`
- `samples`
- `raw_analysis`

## Side Effects

- 无输出文件
- 不修改原始文档

## Constraints

- 只接受 `.docx` 文件路径
