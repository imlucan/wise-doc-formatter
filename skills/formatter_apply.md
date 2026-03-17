# formatter-apply

## 目的

这是 `formatter.py` 的第一阶段 skill 实现层说明文件。

当前按黑盒格式化能力处理，不拆内部页面、段落、表格、页码等子步骤。

## 对外定位

- 唯一入口：`format_document_with_preset`
- 实现文件：`skills/formatter_apply.py`
- 注入适配层：`src/doc_demo/skills/builtin.py`

## 输入

- `input_path`
  - 一个 `.docx` 文件路径
- `preset_name`
  - 当前仅支持：
    - `official`
    - `academic`
    - `legal`

## 输出

返回一个结构化对象，核心字段为：

- `success`
- `output_path`

并补充：

- `input_path`
- `preset_name`
- `message`

## 当前边界

- 先不支持 `custom`
- 先不处理本地字体检测逻辑精简
- 先不把结构识别改为 LLM 注入
- 先不拆成多段格式化子 skill

## 文件约定

- 原始文件不覆盖
- 输出文件写入 `output/artifacts/`
