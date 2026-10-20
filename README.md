# lecture-notes

把英文课件、讲义、论文和长文本，整理成**中文 Obsidian 复习笔记**的 Claude Code 技能。

## 有啥用

- **翻译课件**：全文翻译，不跳页、不省略；术语首次出现中英并列。
- **提炼知识点**：每条按「问题 → 是什么 → 怎么理解」组织，全文件连续编号。
- **一个定义一行**：多个术语、函数、步骤、标准分开写，解释逐条对应，不挤成一整段。
- **配原图**：只裁课件里的图本身，放到对应知识点下面，不贴整页截图。
- **整理论文**：按「原文 → 翻译 → 讲解 + 小例子」梳理，适合案例题。
- **维护索引**：同步更新课程索引，笔记直接在 Obsidian 里复习。
- **复习资料**：可继续整理成按周组织的简答复习笔记。

适合英文 PDF 课件、讲义、论文和长文本。PPTX / DOCX 建议先导出 PDF；扫描件需要先 OCR。

## 怎么用

### 1. 安装 Claude Code（终端）

macOS 13+ / Windows 10+，不需要预装 Node.js。

**macOS：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

装完新开一个终端，验证：

```bash
claude --version
```

也可以用 Homebrew：`brew install --cask claude-code`。Homebrew 不会自动更新，需要手动 `brew upgrade claude-code`。

**Windows（PowerShell）：**

```powershell
irm https://claude.ai/install.ps1 | iex
```

验证同上。

### 2. 接入模型

两种常用方式，选一种。

**方式 A：Claude 账号登录（订阅）**

需要 Pro / Max / Team / Enterprise 账号，免费版不支持 Claude Code。

```bash
claude
```

首次启动按提示在浏览器登录，成功后终端显示 `Login successful`。之后可用 `/login` 重新登录，`/status` 查看当前账号、模型和凭据来源。

**方式 B：Anthropic API Key**

在 https://platform.claude.com 创建 key，然后任选一种配置：

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

或写入 `~/.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-..."
  }
}
```

API key 按 token 计费，并且会覆盖订阅登录；想切回订阅先 `unset ANTHROPIC_API_KEY`。

**可选：第三方网关**

```bash
export ANTHROPIC_BASE_URL="https://你的网关地址"
export ANTHROPIC_AUTH_TOKEN="你的网关密钥"
```

官方只支持转发到 Claude 的网关；把 Claude Code 接到非 Claude 模型属于社区做法，不受官方支持，升级后可能失效。

### 3. 安装本技能

需要先装 Git：macOS 运行 `xcode-select --install`；Windows 安装 [Git for Windows](https://git-scm.com/download/win)。

**macOS / Linux：**

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/2392496291/lecture-notes-skill.git
cp -r lecture-notes-skill/lecture-notes ~/.claude/skills/
```

**Windows（PowerShell）：**

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
git clone https://github.com/2392496291/lecture-notes-skill.git
Copy-Item -Recurse lecture-notes-skill\lecture-notes "$env:USERPROFILE\.claude\skills\"
```

不需要改配置。

可选依赖（只有拆页、渲染图片时用到）：

```bash
pip3 install --user pypdf
# 渲染器二选一：macOS 自带 sips；或 brew install poppler
```

### 4. 使用

在 Claude Code 里直接把课件丢进去：

```text
~/Downloads/Week3.pdf 帮我整理这节课的知识点
```

或者点名技能：

```text
用 lecture-notes 整理 ~/课件/week4
```

笔记默认写到 `课程/<课程名>/weekN/`，图片放 `课程/<课程名>/附件/`；告诉它你的 Obsidian 库路径即可。

## 效果怎么样

- 一份课件 → 一份连续编号的中文笔记，每条一个知识点。
- 定义和解释分开，多个定义不再挤成一段。
- 图在对应知识点下，课程索引同步更新。
- 已用于  Agent 课程：第 4 讲产出 27 条知识点（BDI 16 条 + 规划 11 条）、8 张配图。

产出格式示例：

```markdown
### 1. BDI 三个字母分别对应控制循环里的什么？

**是什么**：
- **B = Beliefs（信念）**：智能体当前认为世界是什么样。
- **D = Desires / options（愿望、候选）**：这一轮的候选愿望。
- **I = Intentions（意图）**：已经承诺要做什么。

**怎么理解**：
- **B**：世界观。
- **D**：草稿，可以有很多条。
- **I**：承诺，`filter` 把草稿变成承诺。
```

## 遇到的困难

| 问题 | 状态 | 怎么处理 |
|---|---|---|
| 知识点展示不简洁 | ✅ 已解决 | 固定「问题 + 是什么 + 怎么理解」简答格式 |
| 期末复习爱用 1.1、1.2 编号，不像知识点 | ✅ 已解决 | 全文件连续编号，标题写成问题 |
| 课件图片整页贴，不聚焦 | ✅ 已解决 | 只裁图本身，按知识点嵌入 |
| 长篇论文没有简洁梳理 | ✅ 已解决 | 原文 → 翻译 → 讲解 + 小案例 |
| 文件命名混乱 | ✅ 已解决 | 主题命名，不加「第N讲 - 」前缀；图片带讲次和页码 |
| 一个知识点里的几个定义挤成一整段 | ✅ 已解决 | 一个定义一行，解释逐条对应 |

还没完全解决：纯扫描 PDF 需要先 OCR；旧格式 `.ppt` / `.key` 需要先导出 PDF。

## 许可

本仓库自有部分采用 MIT 许可，见 [LICENSE](LICENSE)。打包的第三方内容见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
