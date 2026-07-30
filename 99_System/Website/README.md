# MaxQi 网站同步

## 核心原则

- Obsidian 是唯一内容源。
- 网站不会修改或写回 Obsidian。
- 未标记的笔记不会同步。
- 财务、合同、会议、尽调、银行和税务路径会被安全规则拦截。
- 网站后台只管理发布状态和平台访问。

## 日常使用

1. 在 Obsidian 正常完成文章、区域研究或项目记录。
2. 使用“网站发布模板”，或在现有笔记 Frontmatter 中加入网站字段。
3. 把 `website_sync` 改为 `true`。
4. 首次将 `website_visibility` 保持为 `candidate`。
5. 运行本目录中的 `同步到 MaxQi 网站.cmd`。
6. 打开 `https://maxqi.com/admin/sync`。
7. 检查内容来源与同步时间，然后点击“发布”。

## 可见范围

- `candidate`：同步到后台，保持草稿。
- `public_excerpt`：首次同步时直接发布公开版本。
- `public`：首次同步时直接公开。
- `members`：同步到后台，但当前保持草稿，预留给会员平台。
- `archived`：在后台归档。
- `private`：完全不传输。

## 内容类型

- `website_type: article`：进入“文章/精选思考”。
- `website_type: project`：进入“项目”。

## 修改已经发布的内容

直接在 Obsidian 修改正文并更新 `updated`，再次运行同步。网站会更新正文，但保留后台现有的发布或下架决定。
