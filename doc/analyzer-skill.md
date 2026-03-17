# Analyzer Skill 设计

## 目标

`analyzer.py` 在后续 skill 体系中的主要职责，不是直接修复文档，而是作为“前置分析入口”帮助模型决定下一步该调用哪个工具。

因此这里不再把它暴露成多个零散分析接口，而是收敛为一个高信息密度的唯一 skill 接口。

当前采用的目录策略是：

- 业务实现统一放在独立 `skills/` 目录
- 注入逻辑单独放在 `src/doc_demo/skills/`
- Markdown 说明尽量与 skill 实现放在一起

## 当前唯一接口

- skill 名称：`inspect_document_for_routing`
- 实现位置：`skills/analyzer_routing.py`
- 同目录说明：`skills/analyzer_routing.md`
- 注入适配层：`src/doc_demo/skills/builtin.py`

## 返回信息

该 skill 返回一个结构化对象，包含：

- `summary`
  - 人类可读摘要
- `issue_counts`
  - 标点、序号、段落、字体及总问题数
- `routing_hint`
  - 建议的下一步动作，例如 `fix_punctuation`、`format_document`
- `recommended_tools`
  - 推荐调用的后续工具及原因
- `samples`
  - 每类问题的少量样例，避免 token 过载
- `raw_analysis`
  - 完整分析结果

## 为什么只暴露一个接口

对于 LLM/skill 调度来说，`analyzer.py` 的价值是“决策前置”，不是让模型逐个拼装：

- `analyze_punctuation`
- `analyze_numbering`
- `analyze_paragraph_format`
- `analyze_font`

如果全部直接暴露给模型，会带来：

- 工具选择变复杂
- 模型需要自己汇总和路由
- token 开销增大
- 更难形成稳定工作流

因此当前默认策略是：

1. 由唯一 analyzer skill 统一分析
2. 根据返回的 `recommended_tools` 和 `routing_hint`
3. 再决定是否调用标点修复或全文格式化

## 当前路由规则

- 仅有标点问题：优先建议 `fix_document_punctuation`
- 有段落或字体问题：优先建议 `format_document_with_preset`
- 无明显问题：返回 `no_action_needed`
- 只有序号等无法直接自动修复的问题：返回 `review_manually`

## 后续演进

后续如果 analyzer 逻辑继续增强，可以在不改变 skill 名称的前提下继续扩展返回内容，例如：

- 风险等级
- 文档类型判断
- 推荐 preset
- 是否需要人工复核
