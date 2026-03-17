# Tool Catalog

## 首批公开工具

### `analyze_document`

- 来源：`scripts/analyzer.py`
- 角色：LangGraph 首个前置节点
- 输入：`input_path`
- 输出：结构化分析字典
- 说明：聚合标点、序号、段落、字体四类问题，适合 UI 直接展示

### `run_punctuation_fix`

- 来源：`scripts/punctuation.py`
- 角色：低风险修复工具
- 输入：`input_path`
- 输出：修复后的 `.docx` 文件路径
- 说明：保留现有脚本的 URL、邮箱、时间等保护规则

### `run_formatter`

- 来源：`scripts/formatter.py`
- 角色：黑盒全文格式化工具
- 输入：`input_path`、`preset_name`
- 输出：格式化后的 `.docx` 文件路径
- 说明：首版保留大一统调用，后续再拆成更细粒度节点

## 非首批公开工具

### `fix_spacing.py`

- 暂不单独暴露
- 原因：与 `formatter.py` 职责重叠，长期应并入格式化服务

### `fix_spacing_simple.py`

- 暂不单独暴露
- 原因：策略过于粗放，不适合作为默认公开能力

## 当前包装层位置

首批包装代码位于 `src/doc_demo/tools/document_tools.py`。

输出文件默认落在 `output/artifacts/`。
中间临时文件默认落在 `output/temp/`。

## 与 LangChain skill 的关系

当前项目已新增一层 `src/doc_demo/skills/builtin.py`，将现有文档能力包装为可注入的 LangChain tool：

- `inspect_document_for_routing`
- `fix_document_punctuation`
- `format_document_with_preset`

这层主要服务于后续 OpenAI 聊天入口和 skill 实验，不替代现有 LangGraph 工作流。

其中 `inspect_document_for_routing` 是当前推荐的唯一 analyzer skill 入口。
实现层位于 `skills/analyzer_routing.py`，详见 `doc/analyzer-skill.md`。

`fix_document_punctuation` 当前也已迁移为独立 skill 实现。
实现层位于 `skills/punctuation_fix.py`，说明位于 `skills/punctuation_fix.md`。

`format_document_with_preset` 当前也已迁移为独立 skill 实现。
实现层位于 `skills/formatter_apply.py`，说明位于 `skills/formatter_apply.md`。

## 后续拆分建议

下一阶段可以补充以下更细粒度工具：

- `classify_document_structure`
- `compare_analysis_reports`
- `format_tables_only`
- `apply_page_numbers_only`
- `validate_custom_preset`
