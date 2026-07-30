# 请帮我整理 maxqi.com / Obsidian / GitHub / Vercel 系统信息清单

我需要你把当前这套系统完整梳理出来，尽量基于真实配置，不要猜测，不确定的地方请明确写“不确定”。

目标是让我能把这份信息交给另一个 Codex，让它快速理解整个系统，并帮我做下一步规划。

## 1. 网站对应的 GitHub 仓库

请告诉我：

- `maxqi.com` 当前在 Vercel 绑定的是哪个 GitHub 仓库
- 仓库完整地址
- 如果不是 `maxstillwell/obsidian`，请明确说明
- 当前绑定的分支是什么

## 2. Vercel 项目信息

请整理：

- Vercel 项目名
- Production domain
- Preview domain（如果有）
- 连接的 GitHub repo
- 连接的 branch
- Framework preset
- Build command
- Install command
- Output directory
- Node version
- 是否配置了 environment variables
- 如果有，请只说明变量名，不要泄露敏感值

## 3. 网站源码结构

请给我网站仓库的简要结构，至少包括：

- 根目录主要文件列表
- `package.json`
- 主要配置文件
  - 例如 `next.config.*`
  - `astro.config.*`
  - `vite.config.*`
  - `tsconfig.json`
  - `vercel.json`
- 主要源码目录
  - `app/`
  - `pages/`
  - `src/`
  - `content/`
  - `public/`
  - 其它关键目录

请说明网站使用的技术栈，例如：

- Next.js
- Astro
- React
- Tailwind
- MDX
- 静态生成 / SSR / ISR 等

## 4. 页面结构与源码映射

请列出当前网站主要页面，并说明它们对应哪个源码文件。

至少包括：

- Home
- About
- Projects
- Insights
- Contact
- 项目详情页（如果有）
- 中文页（如果有）

请尽量用这种格式：

- `Home` -> `src/app/page.tsx`
- `Projects` -> `src/app/projects/page.tsx`

## 5. 内容来源说明

请明确说明网站内容是怎么来的，分清楚下面几类：

- 哪些内容直接来自 Obsidian
- 哪些内容是从 Obsidian 手工整理后复制到网站仓库
- 哪些内容只是参考 Obsidian，并不是同步
- 有没有自动化同步
- 有没有中间转换脚本

如果有脚本、导出流程、内容清洗流程，请说明文件位置和作用。

## 6. Obsidian 与网站的关系

请明确回答：

- `maxstillwell/obsidian` 这个仓库在整个系统里扮演什么角色
- 它是不是网站的直接源码仓库
- 如果不是，它和网站仓库的关系是什么
- 网站内容现在和 Obsidian 的关系是：
  - 直接发布
  - 手工搬运
  - 半自动整理
  - 仅参考

## 7. 发布流程

请把当前真实发布流程写清楚，不要理想化。

我需要知道：

1. 在 Obsidian 里改了内容之后会发生什么
2. 是否先提交到 `obsidian` 仓库
3. 是否还要同步到另一个网站仓库
4. Vercel 是自动部署还是手动部署
5. 生产环境更新的真实步骤是什么

请尽量写成步骤列表。

## 8. 当前已知问题

请顺手检查并列出当前系统里已经存在的问题或风险，特别是：

- 首页是否有重复内容
- 页面是否有空白页
- 导航是否正常
- 项目页是否有占位内容
- 中英文切换是否完整
- 网站内容是否和 Obsidian 已有正式材料不一致
- 是否有过期内容
- 是否有未文档化的关键发布步骤
- 是否依赖某个人工记忆才能发布

如果你发现问题，请直接列出来。

## 9. 如果网站仓库是私有的

如果网站仓库不能直接完整展示，请至少整理这些信息：

- 仓库名
- 技术栈
- 目录结构摘要
- 关键页面文件
- 部署分支
- 最近一次上线方式
- 和 Obsidian 的关系

## 10. 系统关系总图

最后请给我一份文字版系统关系图，用最直接的方式表达，例如：

`Obsidian -> GitHub(obsidian repo) -> 手工整理/脚本转换 -> GitHub(site repo) -> Vercel -> maxqi.com`

如果有多条路径，也请写出来。

## 11. 输出格式要求

请按下面结构输出：

### A. 一页摘要
用简短文字总结整个系统。

### B. 详细清单
按上面 1-10 项逐条写。

### C. 风险与下一步建议
最后给一个简短建议：
- 现在最需要先补什么
- 哪些地方最容易出错
- 下一步最值得做什么

要求：
- 尽量基于真实文件和真实配置
- 不要脑补
- 不确定就明确写“不确定”
- 如果能给文件路径，就尽量给文件路径