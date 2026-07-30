# MaxQi 系统交接与团队协作说明

> 更新时间：2026-07-30  
> 适用对象：Max Qi、团队内容研究成员、接手本项目的 Codex  
> 本文根据当前本地仓库、Obsidian Vault、同步程序与已部署网站源码整理。无法从本地配置独立确认的 Vercel Dashboard 设置均明确标注为“不确定”。

---

# A. 一页摘要

MaxQi 当前不是一个仓库，而是由三套核心系统组成：

1. **Obsidian 私人知识库**
   - GitHub：`https://github.com/maxstillwell/obsidian.git`
   - 角色：研究、2DD、项目记录、投资理念和正式文章的唯一内容源。
   - 它不是网站源码仓库。

2. **MaxQi 网站源码**
   - GitHub：`https://github.com/maxstillwell/maxqi.com.git`
   - 角色：主网站、文章与项目展示、后台、MQ Land Intelligence、Obsidian 同步接口。
   - 技术：Next.js 15、React 19、TypeScript、Tailwind、Supabase、Leaflet。

3. **Vercel + Supabase 运行环境**
   - Vercel 项目：`maxqi-com`
   - 生产域名：`https://maxqi.com`
   - 土地研究入口：`https://land.maxqi.com`，源码中会将该域名根路径重写到 `/land`。
   - Supabase：保存网站文章、项目、联系表单、研究地块及后台数据。

当前内容发布采用**单向、半自动流程**：

`Obsidian 本地笔记 -> 本地同步脚本 -> maxqi.com 同步接口 -> Supabase 草稿/已发布记录 -> 网站后台审核 -> 网站前台`

Obsidian 的 GitHub 同步与网站内容同步是两条不同路径：

- Obsidian GitHub 负责知识库版本备份和团队协作；
- 网站同步脚本直接读取本地 Vault，再调用网站接口；
- 内容更新不需要每次重新部署 Vercel；
- 网站代码发生变化时，才需要推送 `maxqi.com` 仓库并由 Vercel 部署。

团队成员目前最合适的分工是：

- 在 Obsidian 更新 2DD、区域研究和可发布稿件；
- 通过 Git 与 Max 同步 Obsidian；
- 不直接编辑网站源码、Supabase 或 Vercel；
- 由 Max 或 Codex执行网站同步与后台发布；
- 待流程稳定后，再把同步改成独立的自动化服务账号。

---

# B. 详细清单

## 1. 网站对应的 GitHub 仓库

### maxqi.com 网站仓库

- 仓库名：`maxstillwell/maxqi.com`
- 完整地址：`https://github.com/maxstillwell/maxqi.com.git`
- 本地仓库路径：
  - `C:\Users\MaxQ\.codex\.chatgpt-projects\g-p-68ad3b897c4881918fe538a8a5e598c7\maxqi-site`
- 当前本地工作分支：
  - `codex/land-parcel-registry`
- 当前生产代码对应 commit：
  - `5543be626ad36b3b334944183d8f4fa7ea7fcd47`
- `origin/main` 当前也指向上述 commit。
- 实际上线方式是从工作分支执行：
  - `git push origin HEAD:main`
- 因此当前实际生产分支是 `main`。

### 与 Obsidian 仓库的区别

`maxqi.com` **不是** `maxstillwell/obsidian`。

- `maxstillwell/maxqi.com`：网站源码。
- `maxstillwell/obsidian`：私人知识库、研究资料和内容源。

---

## 2. Vercel 项目信息

### 已确认

- Vercel 项目名：`maxqi-com`
- Vercel Project ID：
  - `prj_UdBtUrqKUPqe1ybs4PODXZktVvbt`
- Production domain：
  - `https://maxqi.com`
- 另有土地研究子域名：
  - `https://land.maxqi.com`
- 连接的网站仓库：
  - `maxstillwell/maxqi.com`
- 实际生产分支：
  - `main`
- 网站框架：
  - Next.js 15 App Router

上述项目名和 ID 来自：

- `.vercel/project.json`

### 源码层可以确认的构建设置

- `package.json` 中的 Build command：
  - `next build`
- Install command：
  - 仓库没有自定义 Vercel install command。
  - GitHub CI 使用 `npm ci`。
  - Vercel Dashboard 的实际 install command：**不确定**。
- Output directory：
  - 仓库没有 `vercel.json`，也没有自定义 output directory。
  - Next.js 默认输出为 `.next`。
  - Vercel Dashboard 是否人工覆盖：**不确定**。
- Framework preset：
  - 源码明确是 Next.js。
  - Vercel Dashboard 显示的 preset 未被独立读取，因此精确设置：**不确定**。
- Node version：
  - `package.json` 没有 `engines.node`。
  - GitHub Actions 使用 Node 22。
  - Vercel Production 的实际 Node version：**不确定**。
- Preview domain：
  - 历史上存在 Vercel preview deployment。
  - 当前固定 preview alias：**不确定**。

### Environment variables

源码和 `.env.example` 中确认的应用变量名：

- `NEXT_PUBLIC_SITE_URL`
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `LAND_MAP_PASSWORD`
- `ADMIN_SHARED_PASSWORD`

说明：

- `SUPABASE_SERVICE_ROLE_KEY` 属于高敏感值，不应进入 Obsidian、Git 或聊天记录。
- `ADMIN_SHARED_PASSWORD` 当前同时参与后台保护和 Obsidian 同步鉴权，长期应拆分。
- Vercel 会自动注入若干 `VERCEL_*` 系统变量，这些不是项目成员需要手工维护的内容。

---

## 3. 网站源码结构

### 根目录主要内容

```text
maxqi-site/
├─ .github/
├─ .vercel/
├─ app/
├─ components/
├─ content/
├─ data/
├─ docs/
├─ lib/
├─ prompts/
├─ public/
├─ scripts/
├─ supabase/
├─ middleware.ts
├─ next.config.ts
├─ package.json
├─ package-lock.json
├─ postcss.config.js
├─ tailwind.config.ts
└─ tsconfig.json
```

### 关键目录

- `app/`
  - Next.js App Router 页面、后台、API。
- `components/`
  - 首页、公共页面、后台和 Land Intelligence 组件。
- `content/`
  - 静态文案、旧 Obsidian fallback、同步快照。
- `data/`
  - 研究地块的 JSON 数据。
- `lib/`
  - Supabase 查询、认证、地图数据、Obsidian 内容转换。
- `scripts/`
  - Obsidian 同步和地块 geocoding。
- `supabase/migrations/`
  - 数据库迁移。
- `public/`
  - 图片、OG 图、Land Intelligence 截图和插图。
- `docs/`
  - 架构和数据库说明；部分文件已经落后于当前系统。

### 技术栈

- Next.js `15.2.9`
- React `19`
- TypeScript
- Tailwind CSS `3.4`
- Leaflet + OpenStreetMap / 官方 ArcGIS 图层
- Supabase Postgres + REST API
- React Markdown
- Vercel
- GitHub Actions

### 页面生成方式

- 首页、项目、Insights、Writing 等内容页使用动态服务器渲染：
  - `export const dynamic = "force-dynamic"`
- About、Contact、Life 等部分页面可静态生成。
- Land Intelligence 是以客户端交互地图为核心的页面。
- 后台与 API 由 Next.js Route Handlers 和 Server Actions 提供。

---

## 4. 页面结构与源码映射

### 主网站

- `Home /`  
  -> `app/page.tsx`  
  -> `components/home-page.tsx`

- `About /about`  
  -> `app/about/page.tsx`

- `Projects /projects`  
  -> `app/projects/page.tsx`

- `Project Detail /projects/[slug]`  
  -> `app/projects/[slug]/page.tsx`

- `Insights /insights`  
  -> `app/insights/page.tsx`

- `Insight Detail /insights/[slug]`  
  -> `app/insights/[slug]/page.tsx`

- `Selected Writing /writing`  
  -> `app/writing/page.tsx`

- `Obsidian Writing Detail /writing/[slug]`  
  -> `app/writing/[slug]/page.tsx`

- `Contact /contact`  
  -> `app/contact/page.tsx`

- `Life /life`  
  -> `app/life/page.tsx`

### 中文路由

- `/cn`  
  -> `app/cn/page.tsx`  
  -> 当前直接 redirect 到 `/`

- `/cn/about`  
  -> `app/cn/about/page.tsx`

- `/cn/projects`  
  -> `app/cn/projects/page.tsx`

- `/cn/projects/[slug]`  
  -> `app/cn/projects/[slug]/page.tsx`

- `/cn/insights`  
  -> `app/cn/insights/page.tsx`

- `/cn/insights/[slug]`  
  -> `app/cn/insights/[slug]/page.tsx`

- `/cn/contact`  
  -> `app/cn/contact/page.tsx`

### Land Intelligence

- `/land`  
  -> `app/land/page.tsx`  
  -> `components/land/land-workspace-loader.tsx`  
  -> `components/land/land-workspace.tsx`

- `land.maxqi.com/`  
  -> `middleware.ts` 重写到 `/land`

### 后台

- `/admin`  
  -> `app/admin/page.tsx`

- `/admin/sync`  
  -> `app/admin/(protected)/sync/page.tsx`

- `/admin/projects`  
  -> `app/admin/(protected)/projects/page.tsx`

- `/admin/insights`  
  -> `app/admin/(protected)/insights/page.tsx`

- `/admin/regions`  
  -> `app/admin/(protected)/regions/page.tsx`

- `/admin/research`  
  -> `app/admin/(protected)/research/page.tsx`

### API

- Obsidian 同步：
  - `app/api/admin/obsidian-sync/route.ts`
- 联系表单：
  - `app/api/contact/route.ts`
- 订阅：
  - `app/api/subscribe/route.ts`
- 地块：
  - `app/api/land/parcels/route.ts`
- 地址定位：
  - `app/api/land/geocode/route.ts`
- 规划查询：
  - `app/api/land/planning/statewide/route.ts`

---

## 5. 内容来源说明

当前网站并不是所有内容都来自同一来源。

### 直接从 Obsidian 同步的内容

目前有四篇笔记设置了 `website_sync: true`：

1. `20_Knowledge/1.1｜前言与投资愿景.md`
2. `20_Knowledge/1.2 战略匹配原则：以农地为核心的系统性选择.md`
3. `20_Knowledge/打造时间杠杆下的农业资产循环体系.md`
4. `20_Knowledge/发展研究/维州未来发展研究.md`

同步后：

- 文章进入 Supabase `writing` 表；
- 网站后台在 `/admin/sync` 显示；
- 发布后由 `/writing` 和首页精选文章读取；
- 正文仍只能在 Obsidian 修改。

### 从 Supabase 读取的内容

- 项目：
  - `lib/queries/projects.ts`
  - Supabase `projects`
- 通用 Insights：
  - `lib/queries/articles.ts`
  - Supabase `writing`
- Obsidian Writing：
  - `lib/obsidian/content.ts`
  - 同样读取 Supabase `writing`，但会识别嵌入正文中的 Obsidian metadata。

### 静态源码内容

- `content/data.ts`
  - About、页面介绍、旧项目和旧 Insights 示例文案。
- `content/obsidian-public.ts`
  - Obsidian 公开文章的 fallback。
- `content/obsidian-sync-snapshot.json`
  - 最近一次本地同步快照。

### 同步脚本

- `scripts/sync-obsidian.mjs`

作用：

1. 扫描本地 `C:\OB\obsidian`；
2. 只读取 `website_sync: true` 的 Markdown；
3. 执行目录白名单和敏感路径过滤；
4. 解析 Frontmatter；
5. 生成同步快照；
6. POST 到：
   - `https://maxqi.com/api/admin/obsidian-sync`
7. 网站接口 upsert 到 Supabase。

### 当前属于哪种同步

准确描述是：

> **一键触发的单向半自动同步。**

它不是实时监听，也不是 GitHub push 后自动同步。

---

## 6. Obsidian 与网站的关系

### `maxstillwell/obsidian` 的角色

- 私人知识库；
- 2DD 和区域研究底稿；
- 项目研究；
- 投资理念和正式文章；
- 团队知识协作；
- 网站可发布内容的源文件。

### 它是不是网站源码仓库

不是。

### 两个仓库如何连接

连接发生在本地同步脚本，而不是 GitHub 仓库之间：

```text
C:\OB\obsidian
  -> scripts/sync-obsidian.mjs
  -> maxqi.com/api/admin/obsidian-sync
  -> Supabase
  -> 网站前台
```

### 重要区别

Obsidian 的 Git commit/push：

- 只把知识库更新到 `maxstillwell/obsidian`；
- 不会自动更新网站。

运行“同步到 MaxQi 网站”：

- 直接读取本地 Vault；
- 不要求先将 Obsidian push 到 GitHub；
- 将被标记的内容发到 Supabase；
- 也不会修改网站源码仓库。

---

## 7. 当前真实发布流程

### 内容更新流程

1. 在 Obsidian 写作或修改研究。
2. 如果只是内部研究：
   - 保持 `website_sync: false`，或不加入网站字段。
3. 如果准备进入网站后台：
   - 使用网站模板；
   - 设置 `website_sync: true`；
   - 初次建议设置 `website_visibility: candidate`。
4. Obsidian Git 插件将 Vault 提交并 push 到：
   - `maxstillwell/obsidian`
5. 在 Max 的电脑运行：
   - `99_System/Website/同步到 MaxQi 网站.cmd`
6. 脚本将内容发送到网站同步接口。
7. 内容进入 Supabase：
   - `candidate` 通常成为 `draft`
   - `public` / `public_excerpt` 首次同步可成为 `published`
8. 打开：
   - `https://maxqi.com/admin/sync`
9. 检查来源、同步时间、摘要和正文。
10. 点击“发布”或“下架”。
11. 网站前台动态读取 Supabase，因此内容发布不需要 Vercel 重新部署。

### 已发布内容修改

1. 回到 Obsidian 修改；
2. 更新 `updated`；
3. 再次运行同步；
4. 正文更新；
5. 后台原有 `published` / `draft` 决定会保留。

### 网站代码更新流程

只有修改页面、地图功能、后台或 API 时才走：

```text
本地 maxqi-site
  -> Git commit
  -> push 到 maxstillwell/maxqi.com 的 main
  -> Vercel 自动部署
  -> maxqi.com
```

Vercel 是否设置了额外的人工 approval：**不确定**。当前实际操作结果表现为 push `main` 后自动部署。

---

## 8. 当前已知问题和风险

### 8.1 两套文章入口并存

目前同时存在：

- `/writing`：Obsidian 精选公开文章；
- `/insights`：Supabase 通用文章系统。

它们都可能读取 `writing` 表，但页面定位和筛选逻辑不同，长期容易让团队不确定文章应该发布到哪里。

建议：

- 将 `/writing` 定为个人精选思考；
- 将 `/insights` 定为正式区域研究或机构化 Research；
- 或将两者合并，避免双重内容体系。

### 8.2 中英文系统不完整

- `/cn` 当前直接跳回 `/`；
- 中文子页面仍存在；
- 新首页已经是中英混合；
- 旧 About / Projects / Insights 仍保留独立中英文结构。

因此目前不是完整双语网站，而是：

> **一个中英混合主网站 + 一组遗留的中英文子页面。**

### 8.3 视觉和信息架构仍有两代页面

- 首页、Writing、Contact 使用深色 Land Intelligence 风格；
- About、Projects、Insights、Life 仍大量使用旧的浅色 editorial 风格。

这不是功能错误，但会造成品牌体验不完全一致。

### 8.4 旧占位内容仍在源码

`content/data.ts` 中仍有：

- Grey Stone Farm
- Project 700
- Investment Notes Platform
- 多篇旧英文和中文示例文章

部分只是遗留数据，部分页面仍引用其标题或介绍。团队成员不能把这里的内容全部当成已核准的正式资料。

### 8.5 项目重复数据需要核查

生产网站抓取曾出现两条同名 `Yaloak Estate`。源码首页本身没有重复循环，因此更可能是 Supabase 中存在两条已发布项目记录。

该问题需要在后台 `/admin/projects` 核查，不应只通过修改前端隐藏。

### 8.6 旧文档已经过期

以下文件仍描述“没有 CMS”或“自动同步尚未实施”，与当前系统不一致：

- `README.md`
- `docs/architecture.md`
- `docs/obsidian-publishing.md`

接手项目的 Codex如果只读这些文件，会形成错误判断。

### 8.7 同步脚本写死本机路径

当前：

- `99_System/Website/同步到 MaxQi 网站.cmd`

写死了 Max 电脑上的：

- 网站仓库路径；
- Node.js 路径。

团队成员在另一台电脑双击不会正常工作。

现阶段正确方式：

- 团队成员只更新并 push Obsidian；
- Max 或 Max 的 Codex在主电脑执行网站同步。

### 8.8 同步鉴权权限过大

`ADMIN_SHARED_PASSWORD` 当前同时承担：

- 网站后台共享密码；
- Obsidian 同步 API key。

建议增加独立的：

- `OBSIDIAN_SYNC_KEY`

并停止让团队成员共享后台主密码。

### 8.9 同步快照可能包含完整正文

`content/obsidian-sync-snapshot.json` 会保存参与同步的完整正文。

虽然网站仓库目前是私有的，但仍建议：

- 快照只保存 slug、hash、状态和来源路径；
- 不在 Git 中保留完整候选稿正文。

### 8.10 安全过滤只检查目录名称

同步脚本会拦截含有以下关键词的路径：

- 财务
- transaction
- ownership
- meeting / 会议
- 尽调 / due diligence
- 合同
- bank
- tax

但是它不会对正文做完整的隐私或机密信息识别。

因此：

> `website_sync: true` 必须由人工明确决定，不能批量添加。

### 8.11 `00_Research` 当前不能同步

同步白名单只有：

- `10_Projects`
- `20_Knowledge`
- `30_Reports`

`00_Research` 不在白名单中。

这对 2DD 很重要：

- 2DD 底稿可以继续留在 `00_Research`；
- 需要发布时，应在 `30_Reports` 或 `20_Knowledge` 制作经过整理的发布版；
- 不建议直接把整个 `00_Research` 放进同步白名单。

### 8.12 Git 并发编辑风险

团队成员与 Max 同时编辑同一篇 Markdown 时，可能产生 Git conflict。

基本规则：

1. 开始工作前先 pull；
2. 一次只由一个人负责同一篇核心研究；
3. 完成一个小阶段就 commit；
4. 不要同时修改 `.obsidian/` 配置；
5. 合并冲突时保留双方正文，不要直接覆盖整个文件。

### 8.13 空白页和导航

- 最近一次生产构建成功生成所有主要路由；
- 当前源码未发现首页重复 section；
- 未发现明确的空白路由实现；
- 管理后台需要登录，不能用公开抓取完整验证；
- `land.maxqi.com` 的根路径依赖 Host rewrite；
- 中文语言切换属于不完整状态，见 8.2。

---

## 9. 私有仓库情况下的必要信息

网站仓库是私有仓库时，新成员至少需要知道：

- 网站仓库：`maxstillwell/maxqi.com`
- Obsidian 仓库：`maxstillwell/obsidian`
- 技术栈：Next.js / React / TypeScript / Tailwind / Supabase / Leaflet / Vercel
- 部署分支：`main`
- 网站内容源：Obsidian + Supabase + 少量静态源码
- Obsidian 不是网站源码
- 内容同步脚本：`scripts/sync-obsidian.mjs`
- 后台审核入口：`https://maxqi.com/admin/sync`
- 网站生产地址：`https://maxqi.com`
- Land Intelligence：`https://land.maxqi.com`

团队内容成员不需要获得：

- Supabase Service Role Key；
- Vercel 全部权限；
- 主网站管理员共享密码；
- 生产 `.env.local`。

---

## 10. 系统关系总图

### 知识库协作路径

```text
团队成员 Obsidian
  -> Git commit / push
  -> GitHub: maxstillwell/obsidian
  -> Max 的 Obsidian pull / Obsidian Git 自动同步
```

### 网站内容发布路径

```text
Max 本地 Obsidian Vault
  -> website_sync: true
  -> scripts/sync-obsidian.mjs
  -> maxqi.com/api/admin/obsidian-sync
  -> Supabase writing / projects
  -> maxqi.com/admin/sync 审核
  -> /writing、/projects、首页
```

### 网站代码发布路径

```text
本地 maxqi-site
  -> GitHub: maxstillwell/maxqi.com
  -> main
  -> Vercel: maxqi-com
  -> maxqi.com / land.maxqi.com
```

### Land Intelligence 数据路径

```text
官方规划 / ArcGIS / 研究地块 / Google Sheet 等来源
  -> Next.js API / JSON / Supabase
  -> components/land
  -> /land
  -> land.maxqi.com
```

---

# C. 风险与下一步建议

## 现在最需要先补什么

### 1. 先建立团队 Obsidian 工作规范

建议将内容明确分为三层：

```text
00_Research = 原始研究和 2DD 底稿，不同步网站
10_Projects = 正式项目主档
30_Reports = 经过审核、可进入前端的区域/2DD 报告
```

`20_Knowledge` 用于长期方法论、投资理念和可公开文章。

### 2. 给团队成员独立身份，而不是共享所有密码

短期：

- 团队成员获得 Obsidian GitHub 仓库权限；
- 不获得生产 Service Role Key；
- Max 负责最终网站同步和发布。

中期：

- 独立 `OBSIDIAN_SYNC_KEY`；
- Supabase / 网站后台改成成员登录和角色权限；
- 研究成员可提交，只有 Max 可以发布。

### 3. 统一 Writing 和 Insights

需要明确：

- 什么叫“精选思考”；
- 什么叫“区域研究”；
- 什么叫“项目”；
- 什么内容只在 VIP Land Intelligence 展示。

不先统一内容类型，前端会继续出现两个文章入口和重复资料。

### 4. 让 2DD 使用标准模板

建议下一步新增：

- `2DD 区域研究模板`
- `Town / Corridor 研究模板`
- `Shire 规划政策模板`
- `前端发布摘要模板`

每份 2DD 至少包含：

- 研究区域；
- 结论；
- 证据来源；
- 规划状态；
- 5–10 年催化剂；
- 发展方向；
- 风险与否决条件；
- 地图坐标或 GeoJSON；
- 数据更新时间；
- 研究负责人；
- 是否允许进入前端。

### 5. 修正文档与脚本

优先处理：

1. 更新网站 `README.md`；
2. 更新 `docs/architecture.md`；
3. 更新 `docs/obsidian-publishing.md`；
4. 把同步脚本的本机路径改成可配置；
5. 同步快照停止保存完整正文；
6. 将后台密码与同步密钥拆分。

---

# D. 团队成员的实际工作方式

## 你可以做什么

- 更新 Obsidian 内的区域研究；
- 完成 2DD 底稿；
- 整理 Shire / PSP / Structure Plan / Zoning 政策；
- 为 Land Intelligence 准备结构化前端内容；
- 在 `30_Reports` 制作可审核的发布版；
- 提交 Git 更新；
- 在交接说明中记录数据来源和更新时间。

## 你暂时不要做什么

- 不直接修改 maxqi.com 前端代码；
- 不直接修改 Supabase；
- 不直接操作 Vercel；
- 不把 `00_Research` 整个目录标记为同步；
- 不在 Obsidian 保存网站生产密钥；
- 不将未审核的 2DD 设置为 `public`；
- 不与另一位成员同时编辑同一篇核心报告。

## 推荐的首次任务

选择一个区域，例如 `Ballarat East Corridor`：

1. 在 `00_Research` 完成原始资料收集；
2. 按 Town、Shire、规划、基础设施和风险整理证据；
3. 在 `30_Reports` 制作一份前端可用的区域报告；
4. 标明：
   - 数据时间；
   - 官方来源；
   - 规划状态；
   - 未来 5–10 年方向；
   - 发展方向；
   - 地图要素；
   - 风险；
5. 提交到 Obsidian Git；
6. 由 Max 审核；
7. 通过后再决定：
   - 公开文章；
   - 项目页；
   - VIP Land Intelligence 内容；
   - 仅保留内部。

---

# E. 给另一个 Codex 的最短上下文

如果把本项目交给另一个 Codex，可直接提供以下说明：

> Obsidian `C:\OB\obsidian` 是唯一研究内容源，GitHub 仓库是 `maxstillwell/obsidian`。网站源码是另一个私有仓库 `maxstillwell/maxqi.com`，本地路径为 `...\maxqi-site`，使用 Next.js 15、React 19、TypeScript、Tailwind、Supabase 和 Leaflet，生产部署在 Vercel 项目 `maxqi-com`，域名为 `maxqi.com` 和 `land.maxqi.com`。Obsidian 内容通过 `scripts/sync-obsidian.mjs` 单向同步到 `maxqi.com/api/admin/obsidian-sync`，进入 Supabase 后在 `/admin/sync` 审核发布。同步只允许 `10_Projects`、`20_Knowledge`、`30_Reports`，不允许 `00_Research`。正文只在 Obsidian 修改，后台只控制发布状态。网站代码 push 到 `main` 后由 Vercel 部署；内容同步不需要重新部署。

