# 文件存储约定

## 背景

当前项目的 agent/skill 流程主要处理的是文件，而不是把完整文档内容直接作为 prompt 上下文传递给模型。

因此，文件存储策略需要先于单个 skill 的实现方式确定。

## 当前简化方案

本地统一使用 `output/` 目录管理运行产物：

- `output/artifacts/`
  - 存放最终结果或可交付的阶段性文件
- `output/temp/`
  - 存放处理中间态和临时文件

## 当前原则

1. 用户原始文件不直接覆盖。
2. skill 默认返回新文件路径，而不是原地修改。
3. 中间处理链尽量使用 `output/temp/`。
4. 对用户有意义的结果写入 `output/artifacts/`。
5. 后续如果接多步 agent 流程，再引入会话级子目录或任务 ID。

## 当前实现位置

- 路径工具：`src/doc_demo/utils/paths.py`

当前已提供：

- `build_output_path(...)`
- `build_temp_path(...)`

## 为什么先做简单版

目前仍处于单机原型阶段，先不引入数据库、对象存储或复杂会话管理。

优先目标是：

- 让 skill 迁移时有统一的文件路径约定
- 避免后续再从 `.runtime` 或零散输出位置迁移一遍
- 让后续压缩包上传或独立分发时结构更稳定

## 后续演进

未来如果 agent 流程变长，可以继续扩展为：

- `output/temp/<session-id>/`
- `output/artifacts/<session-id>/`
- 增加清理策略和过期删除机制
