# Antigravity CLI Agent Skill

一个用于集成 **Antigravity CLI (`agy`)** 的插件与技能仓库。它提供了两个主要组件，使用户和智能体（Agent）能够以完全自动化的方式利用 Antigravity CLI 的超强能力执行复杂的代码生成、修改、调试和分析任务：

- 🤖 **`openclaw-antigravity/`**: 为 **OpenClaw Agent** 深度定制的技能定义，让 Agent 能够使用 `agy` 命令行工具安全、顺畅地操作文件。
- ⚙️ **`hermes-antigravity/`**: 为 **Hermes Agent** 提供的自定义工具插件，利用 Python 子进程封装与注册 `invoke_antigravity` 工具。

---

## 📐 架构与工作流

Antigravity CLI (简称 `agy`) 作为底层强大的 AI 编码引擎，可以通过命令行（CLI）非交互式地接收任务。以下是 Agent 侧集成该工具的工作流：

```text
               ┌──────────────────────┐
               │    用户请求 Task     │
               └──────────┬───────────┘
                          │
                  ┌───────┴───────┐
                  ▼               ▼
            【OpenClaw】       【Hermes】
                  │               │
            调用技能        使用自定义工具
       call-antigravity   invoke_antigravity
                  │               │
                  ▼               ▼
            Shell 执行       Python 执行
             agy 命令      subprocess.run
                  │               │
                  └───────┬───────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │   Antigravity CLI (agy)   │
            │                           │
            │  携带以下关键参数标志：  │
            │  • --dangerously-skip...  │
            │  • --print "提示词"       │
            └─────────────┬─────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │   执行代码修改/分析/生成   │
            └─────────────┬─────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │    返回标准 Markdown 结果   │
            └─────────────┬─────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │   Agent 自动同步并理解变更 │
            └───────────────────────────┘
```


---

## 🛠️ 前置准备工作

无论是使用 OpenClaw 还是 Hermes，底层都必须能够访问 `agy` 命令行工具。

1. **安装并确保 `agy` 可用**：
   确保你的本地环境中已配置好 `agy` 命令行。
2. **环境变量配置 (`PATH`)**：
   `agy` 默认安装在用户本地二进制目录（例如 `/Users/scien/.local/bin`）。请确保此路径在 Agent 的环境变量中。
   ```bash
   export PATH="/Users/scien/.local/bin:$PATH"
   ```

---

## 📁 1. OpenClaw Skill 使用指南 (`openclaw-antigravity`)

在 OpenClaw 中，该技能被定义为 **`call-antigravity`**。它允许 Agent 通过在 Terminal 中运行 CLI 命令直接调用 Antigravity。

### 📥 启用与集成步骤

要在 OpenClaw Agent 中集成并加载此技能，请按照以下步骤操作：

1. **放置技能目录**：
   将整个 `openclaw-antigravity/` 文件夹复制或通过软链接（symlink）方式放入 OpenClaw 的本地技能搜索目录中。通常该目录为：
   * 全局目录：`~/.openclaw/skills/openclaw-antigravity/`
   * 项目内目录：`/path/to/openclaw/skills/openclaw-antigravity/`
2. **在配置文件中声明**（若有配置限制）：
   在 OpenClaw 的主配置文件 `openclaw.yaml` 中，确保技能搜索路径包含该目录：
   ```yaml
   skills:
     paths:
       - ~/.openclaw/skills
   ```
3. **加载与自动注册**：
   当 OpenClaw 启动时，它会自动扫描技能路径下的所有 `SKILL.md` 文件。解析到 `openclaw-antigravity/SKILL.md` 的 YAML Frontmatter 元数据时，智能体会执行以下操作：
   * 注册名为 `call-antigravity` 的技能。
   * 检查本地环境中是否存在所需的可执行文件 `agy`（由 `metadata.openclaw.requires.bins` 声明）。
   * 识别其为 `user-invocable: true`，使其进入规划决策器（Planner）的动作库。

### ⚙️ 核心参数与标志

为了使智能体在后台或非交互式会话中能够顺利执行，必须传入以下**关键标志**：
- `-d` / `--dangerously-skip-permissions`：**至关重要**。跳过交互式权限确认，防止后台执行挂起。
- `-p` / `--print "<prompt>"`：直接以非交互方式接收提示词并在标准输出中打印 Markdown 结果。
- `--add-dir "<path>"`：指定项目工作区目录，让 Antigravity 拥有整个代码库 of 上下文。
- `-c` / `--continue`：在同一个会话中继续上一次的对话。
- `--conversation "<id>"`：恢复特定的历史对话会话。

### 📝 示例命令

#### 🔍 场景 A：对整个项目进行静态分析与瓶颈审计
```bash
agy --dangerously-skip-permissions --add-dir "/Users/scien/dev/my-project" --print "分析此代码库中潜在的内存泄漏或性能瓶颈。"
```

#### 🛠️ 场景 B：重构或修改特定代码文件
```bash
agy --dangerously-skip-permissions --add-dir "/Users/scien/dev/my-project" --print "将 src/utils/helper.js 重构为使用 async/await，替代原有的 Promise 链。"
```

#### 🔄 场景 C：延续上一轮对话（如为重构的代码补充单元测试）
```bash
agy --dangerously-skip-permissions --continue --print "为刚才修改的代码编写完整的单元测试。"
```

---

## 🔌 2. Hermes Tool Plugin 使用指南 (`hermes-antigravity`)

在 Hermes 中，该插件将注册一个名为 **`invoke_antigravity`** 的自定义工具。Hermes Agent 可以通过结构化的 JSON 载荷调用它，而无需自己手动拼接复杂的命令行字符串。

### 📥 启用与注册步骤

要在 Hermes Agent 中激活该工具，请按如下方式进行部署：

1. **导入插件目录**：
   将整个 `hermes-antigravity/` 文件夹放置或软链接到 Hermes 系统的插件存放目录中。例如：
   * `~/.hermes/plugins/hermes-antigravity/`
2. **在配置文件中声明插件**：
   打开 Hermes 的核心配置文件（如 `hermes.yaml`），在 `plugins` 列表中添加该插件的相对或绝对路径：
   ```yaml
   plugins:
     - path: ~/.hermes/plugins/hermes-antigravity
   ```
3. **初始化与工具注册**：
   Hermes 在启动时会加载指定的插件文件夹：
   * 读取 `plugin.yaml` 以确认元数据，识别该插件是一个 `kind: tool` 类型的集成。
   * 加载 `__init__.py`，并在系统初始化阶段执行其中导出的 `register(ctx)` 入口函数。
   * 该函数调用 `ctx.register_tool`，把位于 `tools.py` 的 Python 执行逻辑 `invoke_antigravity` 以及在 `schemas.py` 里通过 Pydantic 编写的 `AntigravityToolInput` 参数描述，注入到 Hermes Agent 的可用 LLM 工具库中。

### 🧩 接口定义与 Schema

该工具通过 Pydantic 定义输入参数（见 `schemas.py` 中的 `AntigravityToolInput`）：

| 参数名 | 类型 | 必填 | 默认值 | 描述说明 |
| :--- | :--- | :--- | :--- | :--- |
| **`prompt`** | `str` | **是** | - | 发送给 Antigravity 的具体任务或提示词（例如重构、除错或代码生成的指令）。 |
| **`workspace_dir`** | `str` | 否 | `None` | 项目或工作区文件夹的绝对路径（传入后会自动添加 `--add-dir` 标志）。 |
| **`continue_session`**| `bool` | 否 | `False`| 是否继续上一次会话（传入 `True` 会自动添加 `--continue` 标志）。 |
| **`conversation_id`**| `str` | 否 | `None` | 指定需要恢复的历史会话 ID（传入后会自动添加 `--conversation` 标志）。 |

### 📥 Tool Call 调用示例（JSON 载荷）

Hermes 在决策执行该工具时，会输出如下的参数 JSON：

```json
{
  "prompt": "在 src/components 目录下生成一个高阶 Button 组件，支持多种主题色（Primary, Secondary）和 Loading 状态，要求使用纯 CSS 样式并带有丝滑的微交互动画。",
  "workspace_dir": "/Users/scien/dev/my-web-app",
  "continue_session": false
}
```

### 📤 工具返回结果格式

工具执行完成后，会返回一个 JSON 格式的字符串：

* **成功时返回**：
  ```json
  {
    "status": "success",
    "output": "... [Antigravity 返回的 Markdown 格式的代码和分析内容] ..."
  }
  ```
* **失败时返回**：
  ```json
  {
    "status": "error",
    "code": 1,
    "stderr": "错误信息...",
    "stdout": "部分输出..."
  }
  ```

---

## 💡 最佳实践与注意事项

> [!IMPORTANT]
> **绝对的非交互式执行**：Agent 在调用 `agy` 时，**必须**携带 `--dangerously-skip-permissions`（或短标志 `-d`）。如果不带此标志，`agy` 在试图读取/修改敏感文件时会提示用户交互输入 `y/n`，这会导致 Agent 进程永久挂起。

> [!TIP]
> **代码同步与理解**：`agy` 会直接在本地工作区修改文件。在工具执行完毕后，Agent 应当使用其自带的文件读取或目录树扫描工具重新检查工作区，以感知由 `agy` 自动做出的代码变更。
