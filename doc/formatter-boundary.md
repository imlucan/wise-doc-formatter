# Formatter 边界约定

## 当前结论

`formatter.py` 现阶段仍按一个黑盒格式化能力看待，不急着拆成多个 skill。

原因：

- 它内部耦合了页面、段落、表格、页码、预设、平台兼容等多层逻辑
- 当前阶段更需要稳定的“文件输入 -> 文件输出”能力
- 过早拆分会让 LLM 需要理解过多内部细节，反而不利于调度

## 已确认的边界

### 1. 本地字体检测

当前 `formatter.py` 中存在 macOS 字体检测与回退逻辑，但你已经确认：

- 目标运行环境是 Linux Docker
- 服务器会预装格式化需要的字体
- 即使字体不存在，也不应该阻塞文档修改

结论：

- 这部分暂时不作为当前 skill 改造重点
- 后续真正改造 formatter 时，可优先弱化或移除“本地字体检测”逻辑

### 2. 预设加载

当前存在：

- 内置 `PRESETS`
- 外部 `custom_settings.json`

结论：

- 先做简单版本
- 后续 formatter skill 改造时，将 `custom_settings.json` 的内容内嵌为代码内置项
- 暂不继续扩展外部自定义配置加载

这个方向当前仅记录在文档与 skill 实现层中，不再改动参考用的 `scripts/formatter.py`。

### 3. 文档结构识别

你希望未来把“结构识别类型”变成函数入参，由大模型从 prompts 中给出。

结论：

- 这是后续设计方向
- 但与当前 formatter 的第一阶段 skill 化改造无关
- 当前先不调整 `detect_para_type(...)` 的实现

### 4. 格式化能力边界

当前仍建议保留为一个黑盒 skill，输出保持简单稳定：

- `success`
- `output_path`
- 可选补充：`preset_name`、`message`

## 当前推荐的 formatter skill 形态

第一阶段建议：

- skill 名称：`format_document_with_preset`
- 输入：
  - `input_path`
  - `preset_name`
- 输出：
  - `success`
  - `output_path`
  - `preset_name`
  - `message`

## 预设参数来源建议

对于 `format_document_with_preset` 的 `preset_name`，当前更推荐：

1. 由界面或上层调用方明确传入
2. LLM 只负责推荐或在缺失时提示用户选择
3. 不让 LLM 在无确认的情况下静默决定最终格式

原因：

- 格式预设属于高影响参数，一旦选错会导致整篇文档风格跑偏
- 这类参数比普通工具路由更适合由显式输入控制
- 当前项目还没有足够稳定的文档类型识别体系，直接交给 LLM 自行决定风险较高

因此第一阶段建议：

- 默认用界面参数作为最终真值
- 如果未来要支持自然语言输入，可让 LLM 先输出推荐 preset
- 最终仍由界面参数或显式确认结果驱动 skill 调用

## 暂不处理的内容

- 本地字体检测精简
- 结构识别由 LLM 注入
- formatter 内部细粒度拆分
- 自定义 preset 外部配置体系
