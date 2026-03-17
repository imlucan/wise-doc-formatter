# punctuation-fix

## 目的

这是 `punctuation.py` 的 skill 实现层说明文件。

它负责接收一个 `.docx` 文件路径，执行中文标点修复，并返回是否处理成功以及输出文件地址。

## 对外定位

- 唯一入口：`fix_document_punctuation`
- 实现文件：`skills/punctuation_fix.py`
- 注入适配层：`src/doc_demo/skills/builtin.py`

## 输入

- `input_path`
  - 一个 `.docx` 文件路径

## 输出

返回一个结构化对象，核心字段为：

- `success`
- `output_path`

同时补充：

- `input_path`
- `message`

## 文件约定

- 原始文件不覆盖
- 输出文件写入 `output/artifacts/`

## 当前边界

- 当前不直接返回“改了多少段落”的精细统计
- 当前失败时只返回简单错误信息
- 更详细的修复统计后续可以再补
