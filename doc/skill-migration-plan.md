# Skill 迁移计划

## 背景

当前 `scripts/` 仍是 Python 脚本集合，后续计划逐步演进为可由 Cursor 持续调用的 skill 或 tool 说明。

## 迁移原则

- 先稳定 Python 可调用接口，再抽象为 skill。
- 先迁移“边界清晰、风险较低”的能力。
- skill 负责描述工作流和调用条件，复杂文档操作继续保留在代码中。

## 分阶段路线

### 阶段一

- 保留 `scripts/` 原样能力
- 在 `skills/` 建立稳定实现层
- 在 `doc/` 中记录规则、输入输出和边界条件

### 阶段二

- 为 `analyzer`、`punctuation` 输出 skill 使用说明
- 把常见工作流写成结构化 playbook
- 建立标准输入输出示例
- 优先通过 `src/doc_demo/skills/` 维护 LangChain tool 适配层，再逐步沉淀为真正的项目 skill

### 阶段三

- 将稳定规则沉淀为项目级 skill
- 把复杂格式规则与回归案例抽离为参考文档
- 根据实际使用频率决定是否淘汰旧 CLI 调用方式

## 优先迁移顺序

1. `analyzer.py`
2. `punctuation.py`
3. `formatter.py`

## 当前进展

`analyzer.py` 已开始按“唯一前置分析入口”迁移，当前默认 skill 为 `inspect_document_for_routing`，目标是服务后续工具路由，而不是暴露多个细粒度分析函数给模型自行拼装。

`punctuation.py` 也已开始按“文件输入 -> 文件输出”的单一 skill 入口迁移，当前默认 skill 为 `fix_document_punctuation`，重点返回处理是否成功和输出文件路径。

`formatter.py` 当前已按黑盒文件处理能力进入第一阶段 skill 化，默认 skill 为 `format_document_with_preset`，重点返回处理是否成功、输出文件路径、预设名和消息。

`fix_spacing.py` 与 `fix_spacing_simple.py` 当前已明确标记为暂缓迁移、候选废弃，不纳入现阶段 skill 体系。

当前迁移结构已调整为：

- skill 实现层：`skills/`
- 注入适配层：`src/doc_demo/skills/`
- 项目级补充文档：`doc/`

## 讨论结论沉淀

### skill 文档边界

`skills/*.md` 只保留与 skill 本身直接相关的内容：

- 目的
- 输入
- 输出
- 文件副作用
- 参数约束

以下内容不再放进 `skills/*.md`，统一收口到本文件或其他 `doc/` 文档：

- 第一阶段/后续阶段讨论
- 是否以后交给 LLM 决定
- 是否以后支持更多 preset
- 注入适配层细节
- 工作流如何路由其他 skill

### analyzer 结论

- 继续保持单一高信息入口：`inspect_document_for_routing`
- 不暴露多个细粒度分析函数给模型自由拼装
- 其价值是“前置分析 + 后续工具推荐”，而不是直接修复文档

### punctuation 结论

- 保持为单一文件处理入口：`fix_document_punctuation`
- 返回值以 `success` 和 `output_path` 为核心
- 不在 skill 文档中扩展过多 roadmap 或统计细节说明

### formatter 结论

- 第一阶段继续按黑盒 skill 处理：`format_document_with_preset`
- 返回值以 `success`、`output_path`、`preset_name`、`message` 为主
- `preset_name` 第一阶段由界面或上层参数显式传入
- LLM 可以推荐 preset，但不应静默决定最终格式
- 本地字体检测、结构识别由 LLM 注入、细粒度拆分等话题，保留在项目级文档中讨论

### fix_spacing 脚本结论

- `fix_spacing.py`：暂缓迁移，候选废弃
- `fix_spacing_simple.py`：暂缓迁移，候选废弃
- 当前不纳入 skill 体系

## 需要持续维护的内容

- 每个 tool 的输入输出约定
- 常见失败原因
- 回归样例
- 新旧调用方式映射
