# punctuation-fix

## Purpose

修复 `.docx` 文件中的中文标点问题，并输出新的文档文件。

## Entry

- `fix_document_punctuation`

## Inputs

- `input_path`
  - `.docx` 文件路径

## Outputs

返回一个结构化对象，包含：

- `success`
- `output_path`
- `input_path`
- `message`

## Side Effects

- 不覆盖原始文件
- 输出文件写入 `output/artifacts/`

## Constraints

- 只接受 `.docx` 文件路径
- 当前返回值不包含精细修复统计
