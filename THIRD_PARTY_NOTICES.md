# 第三方内容声明

本仓库的 `LICENSE`（MIT）只覆盖**自有部分**：
`lecture-notes/SKILL.md`、`lecture-notes/references/figure-extraction.md`、
`lecture-notes/scripts/`、`README.md`、本文件。

下面列出打包进来的第三方内容，以及**有意没有**打包的东西。

---

## 1. 已打包：obsidian-markdown（MIT）

- **位置**：`lecture-notes/references/obsidian-markdown/`
- **上游**：obsidian-skills —— <https://github.com/kepano/obsidian-skills>
- **作者**：Steph Ango（[@kepano](https://github.com/kepano)）
- **许可**：MIT

该目录是上游 `skills/obsidian-markdown/` 的**原样副本**（未做修改），
包含 `SKILL.md`、`references/CALLOUTS.md`、`references/EMBEDS.md`、
`references/PROPERTIES.md`，并保留了上游的 `LICENSE` 文件。

MIT 许可允许再分发，条件是**保留版权声明与许可原文**——见
[`lecture-notes/references/obsidian-markdown/LICENSE`](lecture-notes/references/obsidian-markdown/LICENSE)，
全文亦抄录如下：

```
MIT License

Copyright (c) 2026 Steph Ango (@kepano)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. 有意**未**打包：Anthropic document-skills（专有许可）

`ppt` / `docx` / `pdf` 三个技能来自 Anthropic 的
[document-skills](https://github.com/anthropics/skills) 插件，
其许可为 **"© 2025 Anthropic, PBC. All rights reserved."**，并附有明确限制：

> **ADDITIONAL RESTRICTIONS:** Notwithstanding anything in the Agreement to the
> contrary, users may not:
> - Extract these materials from the Services or retain copies of these
>   materials outside the Services
> - Reproduce or copy these materials, except for temporary copies created
>   automatically during authorized use of the Services
> - Create derivative works based on these materials
> - Distribute, sublicense, or transfer these materials to any third party
> - …

**该许可禁止复制与再分发**，因此这些技能**不在本仓库内**。
使用者需要自行安装：

```
/plugin marketplace add anthropics/skills
/plugin install document-skills
```

本技能对它们只做**调用**（`.pptx` / `.docx` 的读取），不包含其任何内容。
`lecture-notes/scripts/pptx_dump.py` 与 `pptx_media.py` 是**独立编写的替代实现**
（只用 Python 标准库 `zipfile` + `xml.etree`），与本仓库同一许可，不依赖上述插件。
