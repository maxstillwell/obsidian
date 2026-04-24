# Skills 安装建议

## 推荐优先级

### P1

- `obsidian-cli`
- `obsidian-markdown`
- `obsidian-bases`
- `defuddle`

### P2

- `mermaid-visualizer`
- `obsidian-canvas-creator`

### 暂不优先

- `json-canvas`
- `scholar-skill`
- 任何直接暴力文件 I/O 的旧式 Obsidian skill

## 推荐理由

### `obsidian-cli`

- 这是后续操作 Obsidian 的基础设施。
- 适合创建笔记、打开指定页面、调用 Obsidian CLI 能力。
- 你已经明确要求以后优先使用 Obsidian CLI，这个必须优先保证可用。

### `obsidian-markdown`

- 适合约束 Obsidian Markdown 的格式一致性。
- 能减少双链、标题、属性区块和结构化内容的格式漂移。

### `obsidian-bases`

- 适合为研究、项目、报告做数据库视图。
- 你的 vault 很适合后续用 `.base` 做研究看板、项目清单、报告清单。

### `defuddle`

- 适合抓取网页正文并转成干净 Markdown。
- 可用于 AI 研究、政策研究、项目外部资料整理。
- 你已经安装完成。

### `mermaid-visualizer`

- 适合把框架、流程、政策关系、产业链逻辑转成 Mermaid 图。
- 对投研和知识沉淀有价值，但不是最先要装的。

### `obsidian-canvas-creator`

- 适合把结构化研究内容变成 Canvas 白板。
- 更偏可视化整理，不是当前第一阶段刚需。

## 不建议优先安装

### `json-canvas`

- 太底层，直接收益不高。

### `scholar-skill`

- 依赖重，成本高，维护复杂。
- 更适合成熟的学术工作流，不适合当前先把 vault 主流程跑顺。

### 旧式文件 I/O 类 skill

- 既然决定优先用 `obsidian-cli`，就不应优先依赖直接读写文件的旧方案。

## 在当前系统里的具体用途

### AI研究

- `defuddle`: 抓取 AI 文章、博客、文档正文
- `obsidian-markdown`: 统一研究笔记格式
- `mermaid-visualizer`: 画技术框架图、产业链图

### 政策研究

- `defuddle`: 抓取政策原文、新闻、解读文章
- `obsidian-markdown`: 统一政策研究结构
- `obsidian-bases`: 管理政策主题、结论、参考资料

### 项目研究

- `obsidian-cli`: 创建和组织项目型笔记
- `obsidian-markdown`: 保持项目页、会议记录、决策记录一致
- `obsidian-bases`: 管理在研究、推进中、不买状态

### Dashboard 与系统层

- `obsidian-bases`: 做研究、项目、报告总览
- `obsidian-cli`: 快速打开、创建和跳转

## 下一步建议

1. 先确认 `obsidian-cli` 在你的日常终端里能正常使用。
2. 再补 `obsidian-markdown` 和 `obsidian-bases`。
3. 继续使用 `defuddle` 做网页资料清洗。
4. 等主流程稳定后，再考虑 `mermaid-visualizer` 和 `obsidian-canvas-creator`。
