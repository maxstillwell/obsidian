---
tags:
  - workflow
  - land
  - email
  - alert
  - sourcing
updated: 01-08-2026
---
# 找地邮件与 Alert 流程

## 目标

把 `maxqi.com@gmail.com` 变成找地系统的统一外部联系入口，用来完成三件事：

1. 接收各平台的 `email alert`
2. 统一向 agent 发 `地块问询`
3. 把收到的重要信息登记回 Obsidian，形成可追踪的 deal flow

## 一、这个邮箱在系统里的角色

建议把 `maxqi.com@gmail.com` 定义为：

> **土地发现、市场提醒、外部问询的统一邮箱**

它不只是收邮件，而是整个找地系统的外部收口点。

建议它专门承担：

1. Realestate / Domain / Real Commercial 的 alert
2. agent brochure、IM、报价补充资料
3. 地块问询往来
4. 订阅更新、价格变化、open inspection / EOI 截止提醒

不建议它承担：

1. 内部财务沟通
2. 法律合同往来
3. 生产环境账号恢复类高敏感用途

## 二、这套系统怎么运作

建议把流程拆成三条线：

### 1. Alert 线

平台自动发邮件到：

- `maxqi.com@gmail.com`

你要做的是：

- 看新盘
- 看降价
- 看状态变化
- 看 EOI / Deadline 提醒

然后把值得看的内容登记到 Obsidian 的周度找地扫描里。

### 2. Inquiry 线

当某个地块值得进一步了解时：

- 统一从 `maxqi.com@gmail.com` 发问询
- 目标是拿到 brochure、price guide、water、title、lease、planning 方向等基础资料

然后把问询动作和回复结果登记到地块初筛或项目研究笔记里。

### 3. Logging 线

所有关键邮件都不应该只留在邮箱里。

要回到 Obsidian 形成记录：

1. 本周收到了什么 alert
2. 哪个地块发过问询
3. 哪个 agent 回复了
4. 哪些资料已拿到
5. 哪些还在等

## 三、邮箱里的建议标签体系

建议 Gmail 里先用最简单的标签，不要一开始太复杂。

### 平台类

- `Alert/Realestate`
- `Alert/Domain`
- `Alert/RealCommercial`

### 动作类

- `Inquiry/Sent`
- `Inquiry/Reply`
- `Inquiry/Waiting`

### 状态类

- `Dealflow/A`
- `Dealflow/B`
- `Dealflow/C`
- `Need-Log`
- `Need-Followup`

### 资料类

- `Docs/Brochure`
- `Docs/IM`
- `Docs/Pricing`

## 四、建议的自动化规则

当前最实用的自动化，不是复杂脚本，而是 Gmail 自己的 filter。

建议先做三类 filter：

### 1. 平台 Alert 自动归类

例如：

- 来自 Realestate 的 alert 自动打 `Alert/Realestate`
- 来自 Domain 的 alert 自动打 `Alert/Domain`
- 来自 Real Commercial 的 alert 自动打 `Alert/RealCommercial`

### 2. 代理回复自动归类

如果主题或正文里包含：

- `brochure`
- `information memorandum`
- `price guide`
- `EOI`

可以自动加：

- `Inquiry/Reply`
- `Need-Log`

### 3. 等待跟进自动归类

自己发出去的问询，建议自动加：

- `Inquiry/Sent`
- `Need-Followup`

如果 3-5 天后还没回，可以人工追踪。

## 五、建议的操作节奏

### 每周两次处理邮箱

建议固定：

1. 周一或周二：处理上周末和本周初的 alert
2. 周四或周五：处理本周新增和 agent 回复

### 每次只做三件事

1. 把新 alert 过一遍
2. 决定哪些地块要发问询
3. 把关键回复登记回 Obsidian

## 六、建议的落地记录方式

### 1. Alert 进入周度扫描

如果某封邮件只是“发现了一个值得看地块”，就登记到：

- [[00_Research/找地扫描/2026-08-01 Victoria 周度找地扫描]]

### 2. 问询进入单地块笔记

如果已经对某个地块发了邮件，建议在对应地块笔记里加：

- 发件日期
- 问询内容
- 回复状态
- 已收到资料
- 下一步

### 3. 邮件台账单独记录

为了避免漏跟进，建议单独建：

- `邮件问询记录`
- `Alert 登记`

分别使用模板：

- [[99_System/Templates/Research/地块问询记录模板]]
- [[99_System/Templates/Research/邮件Alert登记模板]]

## 七、你怎么用这个邮箱帮我自动问询

如果以后让 Codex 真正接入这个邮箱，建议分三步：

### 第一阶段：半自动

1. 你本人注册各平台 alert
2. 邮件进 Gmail
3. Codex 帮你整理 Obsidian 记录
4. Codex 帮你生成问询邮件草稿
5. 你确认后发送

这是当前最稳的阶段。

### 第二阶段：接入 Gmail 工具

如果后面安装并连接 Gmail 插件，Codex 就可以进一步帮你：

1. 读取 alert 邮件
2. 提取地块信息
3. 生成 shortlist
4. 生成并发送标准化问询
5. 记录哪些 agent 已回复

### 第三阶段：自动台账

成熟以后可以做到：

1. 新 alert 自动进待处理列表
2. 问询邮件自动登记
3. 回复邮件自动更新状态
4. 每周自动生成“本周找地摘要”

## 八、最值得先做的事

如果只做最小可用版本，建议先做这 4 件事：

1. 用 `maxqi.com@gmail.com` 注册三大平台 alert
2. 在 Gmail 里建基础标签和 filters
3. 用 Obsidian 建立问询记录和 alert 登记模板
4. 每周固定两次清理邮箱并更新周度扫描

## 九、当前最好的原则

> 邮箱不是终点，Obsidian 才是系统记忆。

也就是说：

- 邮件负责进件
- 决策在 Obsidian
- 跟进也在 Obsidian

## Related Links

- [[99_System/Workflows/大地块找地流程（Victoria）]]
- [[99_System/Templates/Research/周度找地扫描模板]]
- [[99_System/Templates/Research/地块初筛模板]]
- [[99_System/Templates/Research/地块问询记录模板]]
- [[99_System/Templates/Research/邮件Alert登记模板]]
