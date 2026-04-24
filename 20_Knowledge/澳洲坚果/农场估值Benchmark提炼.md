---
tags:
  - knowledge
  - agriculture
  - valuation
  - benchmark
created: 2026-04-24
source_notes:
  - "[[10_Projects/夏威夷果农场/NSW老农场]]"
  - "[[10_Projects/夏威夷果农场/Qld新农场]]"
  - "[[30_Reports/Yaloak Estate 资产价值报告 2026-04-21]]"
  - "[[20_Knowledge/澳洲坚果/澳洲夏威夷果行业分析（2026）]]"
---

# 农场估值 Benchmark 提炼

> 目的：把专业评估机构常用的估值逻辑拆成可复用的投资模型字段，避免只看“总价”或“每公顷单价”。

## 1. 估值机构最常用的三层框架

### 1.1 资产层：先定“是什么资产”

估值机构通常先区分资产类型，再决定比较口径：

- **成熟经营性农场**：重点看现金流、产量、土地生产力、可比成交。
- **新建果园 / 成长期果园**：重点看已投入 CAPEX、园龄、成活率、灌溉、未来放量路径。
- **问题资产 / 弱经营资产**：重点看处置价值、替代用途、折价因素、流动性。
- **集团合并口径**：重点看组合协同，但不等于单宗资产价值。

### 1.2 土地层：先算“地值”

常见基准：

- **Site Value**：土地本身价值，通常不含或弱化经营性改良贡献。
- **CIV / Capital Improved Value**：土地 + 改良 + 附属设施后的价值。
- **Alternative Use**：如果农业用途不是最高最佳用途，会给出替代用途价值。

### 1.3 经营层：再看“能赚多少”

常见基准：

- 单产（t/ha、kg/ha）
- 产果面积 / bearing area
- 核仁回收率 / 出仁率
- 水权或灌溉强度（ML/ha）
- 品种结构、树龄、健康状况
- 现金成本 / ha
- 毛利 / ha
- 可比销售（comparable sales）

---

## 2. 从你现有几份报告里能抽出的 benchmark

### 2.1 [[10_Projects/夏威夷果农场/Qld新农场]]

这份报告最像标准的 rural mortgage security valuation。

**机构关注点：**

- As Is market value
- 已建果园面积 vs balance land
- 树龄是否进入成熟放量期
- 水资源是否足以支撑未来成熟产量
- orchard plan、道路、设施、病害风险
- 可比果园 / 灌溉农场成交

**可直接复用的 benchmark 字段：**

- 总土地面积
- 已种植面积
- 未开发 / balance land 面积
- 水权 / 储水 / 灌溉配置
- 树龄结构
- 首次采收时间
- 预计商业化产量释放时间
- 现阶段健康状况
- 可比销售价格
- 估值日期的 Market Value (As Is)

**这类资产最关键的 benchmark：**

- `已种植面积 / 总面积`
- `ML/ha`
- `树龄是否接近稳产`
- `未来 3-5 年放量路径`
- `单宗估值 / ha`

---

### 2.2 [[30_Reports/Yaloak Estate 资产价值报告 2026-04-21]]

这份更像 council / rates valuation 口径，核心是 **Site Value vs CIV**。

**机构关注点：**

- Site Value
- CIV
- 同一资产在不同年度的 revaluation
- 分公司 / 分地块拆分
- 每个资产单元的价值变动

**可直接复用的 benchmark 字段：**

- `Site Value`
- `CIV`
- `CIV - Site Value`（改良贡献）
- `年度变化率`
- `单地块价值`
- `每公顷 site value`
- `每公顷 CIV`

**这类资产最关键的 benchmark：**

- `site value per ha`
- `CIV per ha`
- `年度重估幅度`
- `哪一块地驱动总价值变化`

---

### 2.3 [[10_Projects/夏威夷果农场/NSW老农场]]

这份更接近“经营下行 + 资产重组”的估值/处置逻辑。

**机构关注点：**

- 资产是不是还能继续作为经营资产
- 哪些地块是核心资产，哪些可以卖
- 经营是否接近盈亏平衡
- 债务压力是否影响可持续经营
- 有无 alternate use / salvage value

**可直接复用的 benchmark 字段：**

- 单位产量
- 每公顷收入
- 每公顷管护成本
- 利息前盈亏
- 负债水平
- 可处分非核心资产数量
- 处置后核心资产剩余质量

**这类资产最关键的 benchmark：**

- `收入/ha`
- `成本/ha`
- `EBITDA / 经营现金流`
- `debt burden`
- `core vs non-core asset split`

---

## 3. 专业评估机构真正看重的“benchmark 清单”

下面这些最值得放进你的投资模型：

| 维度 | Benchmark | 作用 |
| --- | --- | --- |
| 土地 | Site Value / ha | 看纯土地价值 |
| 改良 | CIV / ha | 看土地+改良后的总值 |
| 经营 | Revenue / ha | 看产出能力 |
| 经营 | Cash Cost / ha | 看经营效率 |
| 经营 | Gross Margin / ha | 看单产兑现能力 |
| 生产 | Yield / ha | 看产量水平 |
| 生产 | Bearing area % | 看有效产能 |
| 水利 | ML / ha | 看灌溉安全边际 |
| 果园 | Tree age / maturity | 看未来放量节奏 |
| 果园 | Survival / health score | 看成园质量 |
| 市场 | Comparable sale $/ha | 看市场定价锚 |
| 风险 | Discount for scale / illiquidity | 看大额资产流动性折价 |
| 风险 | Alternate use value | 看下行保护 |

---

## 4. 建议你在投资模型里统一的字段

如果你以后要做多个农场横向比较，建议统一成下面这组字段：

### 4.1 资产基础字段

- 总面积 ha
- 已种植面积 ha
- 可扩种面积 ha
- 可灌溉面积 ha
- Water entitlement / 储水量
- 树龄结构
- 资产类型（成熟园 / 新园 / 混合 / 问题资产）

### 4.2 经营字段

- 产量 t/ha
- 单位收入 AUD/ha
- 单位成本 AUD/ha
- 毛利 AUD/ha
- 出仁率 / 回收率
- 成熟期预计到达年份

### 4.3 估值字段

- Site Value
- CIV
- Market Value (As Is)
- Alternative Use Value
- Value / ha
- Value / planted ha

### 4.4 风险字段

- 水缺口
- 病虫害风险
- 地形 / 交通 / 进入性
- 流动性折价
- 资本开支缺口

---

## 5. 你这个项目里最实用的判断方式

如果要把这些报告变成投资决策工具，我建议以后每个农场都做四个 benchmark：

1. **地值 benchmark**：Site Value / ha
2. **经营 benchmark**：Revenue / ha、Cost / ha、Gross Margin / ha
3. **产能 benchmark**：Yield / ha、Bearing %、ML / ha
4. **交易 benchmark**：Comparable sale $/ha、Alternative Use Value

这样你就不会只看到“总价多少”，而是能同时回答：

- 这个农场值不值这个价？
- 这块地是不是靠经营才能值钱？
- 未来放量是否可信？
- 下行时大概还能保住多少价值？

## 6. 一句话总结

**专业评估机构不是只看土地单价，而是把“土地价值、改良价值、产能价值、流动性折价”一起算。**

