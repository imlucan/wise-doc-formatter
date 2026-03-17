# formatter-apply

## Purpose

按指定预设对 `.docx` 文件执行全文格式化，并输出新的文档文件。

## Entry

- `format_document_with_preset`

## Inputs

- `input_path`
  - `.docx` 文件路径
- `preset_name`
  - 当前支持：
    - `official`
    - `academic`
    - `legal`

## Outputs

返回一个结构化对象，包含：

- `success`
- `output_path`
- `input_path`
- `preset_name`
- `message`

## Side Effects

- 不覆盖原始文件
- 输出文件写入 `output/artifacts/`

## Constraints

- 只接受 `.docx` 文件路径
- 当前只支持 `official`、`academic`、`legal`
