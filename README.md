# Antigravity CLI Agent Skill

一个用于集成 Antigravity AI 编码助手的插件/技能仓库，包含两个主要组件：

- `hermes-antigravity/`: 为 Hermes Agent 提供的工具插件，用于让 Hermes 调用 Antigravity AI 进行高级软件开发任务。
- `openclaw-antigravity/`: 为 OpenClaw Agent 提供的技能定义，允许 OpenClaw 使用 `agy` 命令执行复杂的代码修改、分析、调试和文件生成。

## 目录结构

- `hermes-antigravity/plugin.yaml`
  - 描述 Hermes Agent 侧的自定义工具插件元数据。
- `openclaw-antigravity/SKILL.md`
  - 定义 OpenClaw Agent 使用 `agy` 的技能说明、执行方式和示例命令。

## 功能说明

### Hermes Antigravity

`hermes-antigravity` 是一个工具插件，旨在让 Hermes Agent 能够调用 Antigravity AI 编码助手（`agy`）来完成高级开发任务。

### OpenClaw Antigravity

`openclaw-antigravity` 是一个 OpenClaw 技能，它将 `agy` 命令集成到代理工作流中，用于：

- 代码重构
- 调试复杂错误
- 生成新文件或模块
- 审计代码库

## 使用方式

### 1. 准备 `agy` 可执行文件

确保本地环境能够访问 `agy`，并且在需要时将包含 `agy` 的目录添加到 `PATH`。示例：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 2. 运行 Antigravity 命令

在 OpenClaw 方案中，可以使用以下示例命令：

```bash
agy --dangerously-skip-permissions --add-dir "/Users/scien/dev/my-project" --print "Analyze the codebase for potential memory leaks or performance bottlenecks."
```

或者：

```bash
agy --dangerously-skip-permissions --add-dir "/Users/scien/dev/my-project" --print "Refactor src/utils/helper.js to use async/await instead of promises."
```

## 贡献

如果你希望扩展本仓库，请将新的 Agent 插件或技能添加到相应目录，并更新 `README.md` 以描述新增能力。

## 许可证

请根据项目实际需求补充许可证信息。
