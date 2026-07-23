---
name: vic-land-site-research
description: 以一个维多利亚州完整地址为唯一必需输入，自动研究地块、城镇、开发区、法定规划、战略规划、环境和基础设施，创建或更新 Obsidian 地块项目，并生成“地块分析报告”HTML与互动规划地图HTML。用户说“分析地块”“研究这个地址”“生成地块报告/规划地图”，或当前笔记只有地址并要求自动调查时使用。
---

# Victorian Land Site Research

## 核心原则

- 只要求一个完整地址；除非地址无法唯一定位，否则不要把资料搜集工作推回给用户。
- 先研究，后写结论。优先使用维州政府、Council、公用事业机构和法定文件等一手来源。
- 严格区分：`已确认事实`、`合理推断`、`待核实`。不得把销售广告、地址点或示意范围写成产权事实。
- 没有 Title Plan、Vicmap Property polygon 或其他可靠地籍边界时，只显示地址定位点，并明确写“不是法定产权边界”。
- 报告名称固定为“地块分析报告”，不要命名为“完整 Rezoning 分析报告”。
- 不要预设住宅 Rezoning 是唯一或最佳路径；分别判断住宅、低密度、工业/商业、农业持有、资源/采掘、分拆或长期等待等路径。
- 所有外部事实记录来源链接、文件日期、访问日期和证据等级。
- 某个官方接口失败时继续使用其他一手来源；无法确认的项目保持“待核实”，不得补造数据。

## 输入解析

从用户消息或当前笔记读取：

1. 完整地址（唯一必需项）
2. Lot/Plan、面积、目标用途或附件（如已有则使用，不要求重复提供）

如地址有多个政府候选点，列出候选并先用 Council、道路关系和出售资料交叉判断；仍无法唯一确定时只问一个选择题。

## 项目目录

在 Vault 内查找现有 `买地` 或 `Land Research` 根目录；优先沿用。两者都不存在时创建 `买地/`。

每个地址使用一个项目目录：

```text
买地/<标准化地址>/
├── 00 地块主页.md
├── 01 地块分析报告.html
├── 02 互动规划地图.html
├── 03 证据与来源.md
├── 04 待核实资料.md
├── 05 研究更新记录.md
├── data/
│   └── site-data.json
└── attachments/

如同一地址的项目已存在，更新原文件，不新建重复项目。更新前读取现有结论和附件；保留 05 研究更新记录.md 的历史，不静默删除旧判断。

自动研究流程

1. 定位与法权

标准化地址并记录经纬度、Council、locality、postcode。

查找可公开取得的 Lot/Plan、面积、产权数量和 Vicmap Property 地籍 polygon。

地籍 polygon 与 Title/Section 32 不一致或无法对应时，以 Title 文件为最高优先级并标注差异。

销售广告只能作为线索；面积、Title 数量等若只来自广告，标为“待产权文件核实”。

2. 法定规划

逐地块/逐 Title 核查：

Planning Scheme 与 Council

Zone、schedule 和关键用途/最小面积要求

全部相关 Overlays

Urban Growth Boundary、settlement boundary 或其他法定边界

Incorporated/Reference Documents

已实施或在审 Planning Scheme Amendments

不要用一个门牌点的查询结果代表跨越多个地块、道路两侧或多个 Zone 的全部土地。

3. 城镇与开发方向

查找并阅读与地址相关的：

Township / Structure / Growth Area / Precinct Structure Plan

Housing、Industrial、Rural Land、Economic Development 策略

Council Plan 和 Infrastructure Plan

邻近既有开发区、规划开发区、未来调查区

城镇连续性、与现有服务的距离、跨越高速公路/铁路/河流等物理阻隔

近年的 Amendments、Panel Reports 和类似地块先例

明确区分“法定开发边界”“Council 战略调查范围”“长期意向”“仅地图示意”。

4. 约束与基础设施

核查：

flood、LSIO/FO、drainage、waterway

bushfire、BMO/BPA

biodiversity、vegetation、environmental、heritage、landscape

contamination、landfill/quarry/resource buffers、SERA/SRO

road access、arterial road permit、rail、easements

potable water、sewer、stormwater、electricity 和 servicing authority

农业保护、土壤、资源或现状经营价值

区分“可工程解决的成本项”和“政策/法定硬门槛”。

5. 路径判断

至少评估：

普通住宅

低密度/乡村住宅

工业/商业/就业

保持农业或现状用途

资源、采掘或其他特殊机会

多 Title 分拆、独立退出或长期等待

对每条路径给出：

结论：推进 / 条件推进 / 长期观察 / 不建议 / 资料不足

0–100 初步机会分

硬性 Gate

支持因素

反对因素

下一项最能改变判断的证据

分数不能掩盖硬性 Gate；存在决定性 Gate Fail 时，结论必须反映。

输出

读取 references/output-contract.md 并严格遵守。完成后简要告诉用户：

创建或更新了哪个项目目录

一句话核心判断

最重要的三个不确定项

报告和地图的相对路径

更新模式

用户加入 Title、Section 32、Planning Property Report、顾问意见或新规划文件后说“更新这个地块”时：

读取新增文件及既有项目；

重新核验受影响的事实、Gate 和路径评分；

更新主页、报告、地图、数据和待核实清单；

在研究更新记录追加日期、来源和结论变化；

不删除历史记录。
