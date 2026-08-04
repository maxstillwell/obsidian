---
tags:
  - workflow
  - research
  - land
  - obsidian
  - google-sheets
  - website
updated: 04-08-2026
---
# OB 到 Google Sheet 资料库同步流程

## 目标

建立一套稳定的三层工作流：

1. `Obsidian` 作为主工作台
2. `Google Sheet` 作为结构化资料库中间层
3. `maxqi.com / land` 作为展示层

核心原则：

> 研究和判断在 `OB` 完成。  
> 结构化市场资料进 `Google Sheet`。  
> 网站只读取你愿意展示的内容。

## 一、三层系统怎么分工

## 1. Obsidian

负责：

- 周度找地扫描
- 单地块初筛
- A / B / C 判断
- 问询记录
- deeper research
- 股东周报草稿

不负责：

- 长期承载数百条结构化表格记录
- 直接作为网站地图的主要数据源

## 2. Google Sheet

负责：

- 维州市场地块总表
- 结构化字段管理
- 状态更新
- 降价 / sold / off market 跟踪
- 网站后续读取

不负责：

- 深研究正文
- IM / Section 32 / 规划分析长笔记

## 3. 网站 / 地图

负责：

- 展示总表
- 展示地图
- 展示你愿意给股东或相关方看的结果

不负责：

- 承担你的日常研究主流程

## 二、这套系统的工作顺序

## Step 1：先在 OB 里工作

每周先在 OB 完成：

1. 周度扫描
2. shortlist
3. 单地块初筛
4. 本周变化判断

这一层仍然是主工作流。

## Step 2：把需要进入总表的内容写成结构化条目

不是所有笔记都进表。

只有满足以下条件的地块才进入 `Google Sheet` 总表：

1. 命中监控池
2. 值得进入市场资料库
3. 有足够基础字段

记录时使用模板：

- [[99_System/Templates/Research/地块资料库条目模板]]

## Step 3：同步到 Google Sheet

同步对象不是整篇笔记，而是**结构化字段**。

也就是说：

- `OB` 保留分析和注释
- `Google Sheet` 只保留表格字段

## Step 4：网站读取 Google Sheet

网站以后不直接读取 `OB` 笔记，而是优先读取：

- `Google Sheet`
- 或由 `Google Sheet` 整理出来的结构化数据

这样地图和总表都更稳定。

## 三、第一轮测试版监控池

当前先只跑这三类池子：

### Pool 1

- `Victoria-wide`
- 所有 `1000ha+`

### Pool 2

- `Melbourne CBD 100km`
- 所有 `100ha+`

### Pool 3

- `Ballarat - 20km`
- `Wonthaggi - 10km`
- `Warragul - 20km`

同一个地块可以同时命中多个池子。

## 四、Google Sheet 总表的角色

这张总表不是研究笔记，而是：

> **市场资料库主表**

它要长期累积：

- 60 个地块
- 100 个地块
- 1000 个地块

所以它最重要的任务不是写长分析，而是：

1. 记录
2. 分类
3. 更新状态
4. 给网站读

## 五、建议的字段分组

Google Sheet 里的字段建议分成五组：

### 1. 基础识别

- record_id
- property_name
- address
- suburb_locality
- lga
- region
- state
- postcode

### 2. 市场字段

- source_platform
- listing_url
- agent
- agency
- listing_type
- asking_price
- price_display
- price_per_ha
- land_size_ha
- property_type

### 3. 距离字段

- distance_to_melbourne_cbd_km
- distance_to_ballarat_km
- distance_to_wonthaggi_km
- distance_to_warragul_km
- nearest_township
- distance_to_nearest_township_km

### 4. 规则命中

- hit_pool_statewide_1000ha
- hit_pool_melbourne_100km_100ha
- hit_pool_ballarat_20km
- hit_pool_wonthaggi_10km
- hit_pool_warragul_20km
- hit_count
- priority_bucket

### 5. 状态跟踪

- first_seen_date
- last_checked_date
- listing_status
- status_note
- previous_price
- price_changed_date

## 六、OB 里哪些内容进表，哪些不进表

## 可以进 Google Sheet 的

- 地址
- 面积
- 价格
- 每公顷价格
- 距离
- 命中池子
- 平台来源
- 状态变化

## 不建议直接进 Google Sheet 的

- 长段 thesis
- IM 摘要
- Section 32 细节
- 规划判断全文
- 中介往来细节
- 深研究结论正文

这些继续留在 `OB`。

## 七、每周工作节奏

## 周一 / 周二

1. 跑一轮全量或增量扫描
2. 在 OB 完成本周 shortlist
3. 更新总表中的：
   - 新地块
   - 新状态
   - 新价格

## 周四 / 周五

1. 补扫描
2. 检查：
   - 降价
   - sold
   - off market
   - withdrawn
3. 更新 OB 周报摘要

## 八、周报怎么和总表配合

周报只写变化，不重复整张大表。

周报建议包含：

1. 本周新增地块
2. 本周降价地块
3. 本周 sold / off market
4. 本周高优先级变化

而完整总表作为：

- 数据库底表
- 网站展示源
- 地图读取源

## 九、为什么不让网站直接读 OB

因为未来总量一大：

- `OB` 适合研究
- `Google Sheet` 更适合结构化表格
- 网站更适合读结构化中间层

所以这不是多一层麻烦，而是为了让：

1. 你的主工作方式不变
2. 网站展示更轻
3. 以后更容易维护

## 十、当前阶段的最小可用版本

如果先只做第一版，不做自动化，最小可用流程如下：

1. 在 `OB` 完成周度扫描
2. 用模板登记进入资料库的地块
3. 手工写入或整理进 `Google Sheet`
4. 网站读取 `Google Sheet`
5. 周报继续在 `OB` 写

等这套流程跑顺，再考虑：

- 半自动同步
- API 写入
- Google Sheet -> Supabase

## 十一、当前建议

> 第一阶段不要急着做双向同步。  
> 保持 `OB -> Google Sheet` 单向结构最稳。

因为你的主工作台很明确是 `OB`，所以中间层应当服务于它，而不是反过来改造你的工作方式。

## Related Links

- [[99_System/Workflows/大地块找地流程（Victoria）]]
- [[99_System/Workflows/找地邮件与Alert流程]]
- [[99_System/Templates/Research/地块资料库条目模板]]
- [[99_System/Templates/Research/周度找地扫描模板]]
- [[99_System/Templates/Research/地块初筛模板]]

