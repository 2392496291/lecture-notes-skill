# current problem目前遇到的问题
1.skill没有简洁的展示出知识点（已解决，后续上传）

2.对于期末复习的整理，总是喜欢用1.1之类的符号来代替知识点（已解决，后续上传）

3.对于课堂的PDF等材料图片，总是展示出一整张图片没有聚焦到具体（已解决，后续上传）

4.对于长篇论文或者阅读材料没有简洁的梳理出知识点（已解决，后续会上传）

5.文件命名有问题

# lecture-notes — 课件翻译与知识点整理技能

> A [Claude Code](https://claude.com/claude-code) / Agent Skill that turns English lecture
> slides (PDF / PPTX / DOCX) into **study-ready Chinese notes in Obsidian** — full
> translation, distilled knowledge points, the original figures embedded inline, plus a
> glossary and a course index. Works for any subject; it was built and battle-tested on
> university CS handouts.

把英文课件（PDF / PPTX / DOCX、讲义、课堂照片）变成**中文的、能拿来复习的** Obsidian 笔记。

不是「翻译一遍」就完事，而是**译完就能直接学**——翻译、提炼、归档、把课件里的图表截出来嵌进去，是一件事。

---

## 这个技能解决什么

手动整理一节课的课件，通常要来回做这几件事，而且很容易做漏：

| 步骤 | 技能里对应的能力 |
|---|---|
| 通读课件、抽全文和讲师备注 | `.pptx` / `.pdf` / `.docx` 三种源文件，配 `scripts/` 里的抽取脚本 |
| 全文翻译，不跳页 | 硬性要求：不许省略、不许编造、不确定就标 `⚠️ 原文存疑` |
| 提炼考点、公式、自测题 | 固定的笔记模板（frontmatter / callout / Mermaid / LaTeX） |
| **把课件里的图配进笔记** | 渲染 PDF 页、导出 pptx 内嵌图，按出处命名后就地嵌入 |
| 维护术语表和课程索引 | `术语表.md` + `<课程名>.md` 自动追加 |
| 检查有没有漏图、有没有孤儿图 | `scripts/check_embeds.py` 一键校验 |

## 目录结构

```
lecture-notes-skill/
├── README.md                  ← 你正在看的这个
├── LICENSE                    ← 本仓库自有部分的许可（MIT）
├── THIRD_PARTY_NOTICES.md     ← 打包进来的第三方内容及其许可
└── lecture-notes/             ← 技能本体，整个目录拷进 ~/.claude/skills/ 即可
    ├── SKILL.md               ← 主入口：完整工作流
    ├── references/
    │   ├── figure-extraction.md        ← 配原图的详细做法与踩坑记录
    │   └── obsidian-markdown/          ← Obsidian 语法参考（第三方，MIT，见声明）
    │       ├── SKILL.md
    │       └── references/{CALLOUTS,EMBEDS,PROPERTIES}.md
    └── scripts/
        ├── pdf_extract_text.py   ← 抽 PDF 文字层，找出「无文字层 = 整页截图」的页
        ├── pdf_render_pages.py   ← 把指定 PDF 页渲染成 JPEG（sips 或 pdftoppm）
        ├── pptx_dump.py          ← 抽 pptx 每页文字 + 讲师备注 + 媒体清单
        ├── pptx_media.py         ← 列出/导出每页引用的配图
        └── check_embeds.py       ← 校验 Obsidian 嵌入全部有效、无孤儿附件
```

## 安装

**1. 装技能**

```bash
git clone https://github.com/<你的用户名>/lecture-notes-skill.git
cp -r lecture-notes-skill/lecture-notes ~/.claude/skills/
```

Windows 上把 `lecture-notes` 目录放到 `%USERPROFILE%\.claude\skills\`。

**2. 装前置依赖**

- **读 `.pptx` / `.docx`**：需要 Anthropic 的 `document-skills` 插件（`pptx`、`docx`、`pdf` 三个技能）。
  在 Claude Code 里：

  ```
  /plugin marketplace add anthropics/skills
  /plugin install document-skills
  ```

  > 这三个技能是 Anthropic 的**专有许可**（All rights reserved），明确禁止再分发，
  > 所以**没有**打进本仓库。没有它们时，`scripts/pptx_dump.py` + `scripts/pptx_media.py`
  > 可以兜底把文字、备注和配图抽出来。

- **配原图（可选）**：

  ```bash
  pip3 install --user pypdf
  ```

  再加一个渲染器：macOS 自带的 `sips` 就行；Linux 上装 poppler（`brew install poppler` /
  `apt install poppler-utils`）。脚本会自动挑能用的那个。

**3. 改配置**

打开 `~/.claude/skills/lecture-notes/SKILL.md`，把「配置」表格里的
**Obsidian 库根目录**换成你自己的路径。其余几项是约定，不动也行。

## 用法

装好之后，直接把课件丢给 Claude：

```
/Users/你/下载/Week 3 - Structural Testing.pdf 帮我整理这节课的知识点
```

或者

```
把这些 pptx 整理成笔记放进 Obsidian，记得把里面的图也配上
```

技能会被自动触发。也可以显式点名：`用 lecture-notes 技能整理 ~/kcl文件/w4`。

## 脚本单独用

这些脚本不依赖 Claude，命令行直接跑：

```bash
# 1. 先侦察：哪几页是整页截图（通常就是历年真题页）
python3 -I scripts/pdf_extract_text.py slides.pdf /tmp/text.txt

# 2. 渲染指定页，文件名自带出处
python3 -I scripts/pdf_render_pages.py slides.pdf ./附件 \
    4:第1讲-p04-边界值测试 22:第1讲-p22-技术比较图

# 3. pptx：先看每页有哪些图，再导出指定页
python3 -I scripts/pptx_media.py deck.pptx -
python3 -I scripts/pptx_media.py deck.pptx ./附件 8,10,11

# 4. 整理完校验：嵌入是否都指得到文件、有没有孤儿图
python3 -I scripts/check_embeds.py ~/obsidian-knowledge/你的库
```

> `python3 -I` 是有意加的：课件解压出来的东西按不可信数据处理，
> 隔离解释器以免当前目录里被人埋了同名模块。

## 设计上的几个取舍

- **整页渲染，而不是抽 PDF 内嵌位图。** beamer 式讲义的图多是**矢量画的**，抽出来的位图是碎的；
  整页渲染还能顺带拿到**动画揭晓后的内容**。
- **不嵌纯文字页面。** 笔记本来就逐句译了，再贴一张满是字的截图只是噪音。哪些页嵌、哪些页不嵌，
  判断标准写在 `references/figure-extraction.md`。
- **附件平铺、文件名全局唯一。** Obsidian 的 `![[文件名]]` 是按 basename 在**整个库**里解析的，
  所以文件名里带讲次和页码（`第3讲二-p14-素路径练习图.jpg`）最省事。
- **只嵌能确认的东西。** 图上没图例、靠自己看颜色区分的，说明里必须写明「这是我的解读」；
  导不出来的图（比如用形状画的曲线）就直说导不出来，不拿低清截图充数。

## 已知限制

- 只处理文字层可抽的 PDF；纯扫描件需要先做 OCR（本技能不含 OCR）。
- 旧格式 `.key` / `.odp` / `.ppt` 需要你先导出成 PDF。
- 渲染质量参数（长边 1400 px、JPEG 质量 82）写死在 `pdf_render_pages.py` 顶部，可以自己调。
- Obsidian 语法参考打包的是上游 `obsidian-markdown` 技能的副本，**不会自动跟进上游更新**；
  上游更新了可以重新拷一份覆盖 `references/obsidian-markdown/`。

## 许可

本仓库自有的部分（`SKILL.md`、`references/figure-extraction.md`、`scripts/`、本 README）
采用 **MIT 许可**，见 [LICENSE](LICENSE)。

打包进来的第三方内容见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)：
`references/obsidian-markdown/` 来自 Steph Ango（@kepano）的
[obsidian-skills](https://github.com/kepano/obsidian-skills)，同样是 MIT 许可。
