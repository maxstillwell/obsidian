# Output Contract

## 00 地块主页.md

使用 YAML Properties，至少包括：

```yaml
---
project_type: Land Acquisition
address:
council:
locality:
area_ha:
titles:
current_zones: []
urban_growth_boundary:
primary_opportunity:
overall_recommendation:
evidence_completeness:
status: Initial Review
date_updated:
---
```

正文保持简洁，包含：

当前投资判断

各路径结论表

两个 HTML 文件入口

三项最关键不确定因素

下一步行动

01 地块分析报告.html

生成一个单文件、中文、响应式 HTML。标题必须是：

<地址> — 地块分析报告

不得使用“完整 Rezoning 分析报告”作为文件名或标题。

报告至少包括：

执行摘要

地块与产权概况

法定 Zone / Overlay / 边界

城镇、开发区及战略规划关系

环境、道路和基础设施约束

六类开发/持有路径比较

Gate Tests 与机会评分

已确认事实、推断和待核实事项

买前尽调清单

证据来源（可点击链接、文件日期、访问日期）

顶部显示“资料截至日期”和证据完整度。提供打印/另存 PDF 按钮。不要把未经确认的数据包装成确定结论。

02 互动规划地图.html

生成一个可独立打开的 Leaflet 单文件 HTML，中文界面，布局和配色可参考 Vault 中现有的 4980_Lang_Lang_Planning_Map.html，但不要覆盖参考文件。

地图必须有：

街道图 / 卫星图切换

地块定位点

可靠取得时显示地籍/Title 边界；否则明确标示“地址点，不是法定边界”

周边城镇及名称

现有镇区、法定开发范围、规划开发/调查范围

Planning Zones

Urban Growth Boundary 或对应 settlement boundary

关键 Overlays

主要道路、铁路或其他重要阻隔（如相关）

图层开关、图例、来源和边界免责声明

“返回地块”“查看城镇/区域”“打印/PDF”按钮

优先将关键 GeoJSON 数据嵌入 HTML，确保研究时看到的边界不会因接口以后变化而悄悄改变；如同时连接实时政府图层，清楚标注“实时图层”。任何示意范围必须使用不同样式并标注“示意/待核实”。

地图左侧摘要显示：

Council

面积/Title 数量及证据状态

Zone

UGB/settlement boundary

最近城镇

当前主要机会

03 证据与来源.md

用表格记录：

| 主题 | 结论/数据 | 证据等级 | 来源机构 | 文件/图层 | 文件日期 | 访问日期 | 链接 |

证据等级仅使用：

A：法定文件、官方 GIS、Title/Section 32

B：官方策略、主管机构正式回复

C：销售资料或可靠二手资料

D：空间推断/尚待核实

04 待核实资料.md

用复选框列出缺口，并按以下顺序排序：

会改变 Gate 或投资结论

会改变估值或可分拆性

会改变成本/时间

一般补充资料

每项说明“为什么重要”和“向谁索取”。

05 研究更新记录.md

每次运行追加：

日期时间

新增/更新来源

结论或评分变化

仍未解决的问题

data/site-data.json

保存结构化数据，至少包括：

address、coordinates、council、lot_plan、titles、area

zones、overlays、boundaries

towns、strategic_plans、infrastructure、constraints

opportunity_paths、gate_tests、scores

sources、evidence_status、generated_at

HTML 内展示的数据必须与此 JSON 一致。JSON 使用 UTF-8、合法语法，不写注释。
