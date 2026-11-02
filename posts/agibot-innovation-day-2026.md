---
title: 智元 2026 创新大会笔记：三智一体、Worken 与数据驱动的作业智能
date: '2026-10-31'
lastmod: '2026-11-01'
draft: false
tags:
- embodied-ai
- humanoid-robot
- agibot
- robot-learning
- industry-notes
categories:
- event-notes
summary: 记录智元 2026 创新大会的业绩、五次跃迁路线，以及运动、作业、交互三类智能的发布，并附上我对订单数字、数据驱动落地和 RSI 叙事的看法。
math: false
showtoc: true
tocopen: true
---

## 概览

智元把这次大会的发布归成“三智一体”：运动智能、作业智能、交互智能。贯穿全文的几个看法：

* **业绩与 Worken**：公布的订单数我估计偏高，可能有出货给子公司的成分；新提出的 Worken（有效智能工时）想做物理 AI 的 KPI，但更直观的指标是一台机器人能替代多少人力、省下多少成本。
* **运动智能最成熟**：AGILE 2.0 感控一体模型加仿真 infra，agent 能发现腿部故障、重新训练并恢复行走。
* **作业智能讲得最多，落地最少**：数据（AGIBOT WORLD 2026、MEgo Glove、觅蜂派众包、MEgo Engine）和模型（GO-3、CEL、Genie Master）占了大部分篇幅，已部署的项目却主要靠轮式双臂的运控加 CV。数据驱动的卖点是交付一个部署后还能持续变强的产品。
* **RSI 是最有吸引力的叙事**：Genie Master 目前更接近 Harness RSI，改进的是 agent 怎么调用已有能力，还没改到 policy 本身。
* **交互智能已经能用**，主要用在导览。我的一个猜想是，把它放到小型机器人或卡通 IP 机器人上，商业价值可能比放在全尺寸人形上更大。

## 业绩

![img_v3_0216v_cae80c8c-ac4d-4942-a288-3fa1b725c40g](/images/agibot-innovation-day-2026-5ad8983b5dac.png)

我估计实际订单没有这么多。根据他们已经商业化落地的客户倒推，真实订单量应该低于这个数字。一种可能是出货给子公司觅蜂科技和擎天租，在体系内流转把订单量做上去。订单肯定是有的，数字是否有水分只是我的推测。

![Pasted image 20261030112027](/images/agibot-innovation-day-2026-51ef1cca1325.png)

这是智元自己估计的状态，部署成长期

比较值得关注的是提出了一个新概念，Worken

![Pasted image 20261030112159](/images/agibot-innovation-day-2026-728f3b01039b.png)

![Pasted image 20261030112211](/images/agibot-innovation-day-2026-808dfbf8c689.png)

![Pasted image 20261030112225](/images/agibot-innovation-day-2026-8f742be04117.png)

含义是有效智能工时

定义为**多少台设备运行了多少时间乘上人工替代率**，比如 100 台机器全天 24 小时能够干 0.5 个人的产出速度 Worken 就是 1200

被设计为作为物理 AI 的 KPI，其实这个也复杂了，更直观和简单的形式

***一个机器人能够替代一个员工多少产能和节约用工多少成本***

![Pasted image 20261030131029](/images/agibot-innovation-day-2026-b9714a51e905.png)

展示了智元几个落地的项目

1. 成都宽窄巷子游客服务
2. 龙旗产线上下料
3. 广州地铁安检引导
4. 珠海长隆文娱表演
5. 爱仕达零售导购
6. 香格里拉酒店服务

导览/跳舞/工业上下料

对应到智元的三智一体：运动智能、作业智能、交互智能

显然运动智能以及很成熟，作业智能还在发展，交互智能已经发布了新的多模态交互能力

## 技术路线

**总览：物理 AI 从可用到通用会经历五次关键跃迁**

![Pasted image 20261030151229](/images/agibot-innovation-day-2026-0236b69e86ef.png)

不准确，为讲故事画的图，不是递进的关系

**第二次跃迁：在垂域细分场景进入部署态**

![Pasted image 20261030151745](/images/agibot-innovation-day-2026-8275d54e2a8a.png)

体现的内容是，做本体，做完本体用专业化细分的场景用运控加 CV 落地

**第三次跃迁：形成泛化的具身基座模型**

![Pasted image 20261030151821](/images/agibot-innovation-day-2026-5410c57eb037.png)

同时也在发展具有泛化的基座模型去进军更复杂一点的场景

**第四次跃迁：从单机到群体，机器人的群体自主进化**

![Pasted image 20261030151837](/images/agibot-innovation-day-2026-f35f84201caa.png)

群体进化更多的是后面提到的**真机 RL**：用整个机器人集群在真实部署中积累的经验做后训练，对应后文的 CEL（Collective Experience Learning，96 台机器人）

**第五次跃迁：智能系统自我举升**

![Pasted image 20261030151908](/images/agibot-innovation-day-2026-8cb329474361.png)

自举是最近的 RSI 概念

同时我也觉得是非常有吸引力的技术突破，有点奥创的味道，AI 自己为自己造身体，并且自我优化自己的物理世界的能力

接下来是智元的战略方向

![Pasted image 20261030152050](/images/agibot-innovation-day-2026-1550bad7493b.png)

两智是**运动智能**和**交互智能**

这俩都是**腿式**人形为主

一智能是**作业智能**

以**轮式双臂**为主

## 硬件

产品发布速览

![Pasted image 20261031214428](/images/agibot-innovation-day-2026-0ba37dacc4de.png)

> 机器人所有的智能，最终都需要通过可靠的硬件载体，才能在物理世界兑现价值。

![img_v3_02170_99037928-05ca-420a-96fc-5adcc9cff68g](/images/agibot-innovation-day-2026-94c87931e95d.png)

智元针对**工业作业**、**商业服务**以及**不同复杂度的操作任务**等不同场景设计了多种形态的本体：腿式双臂、轮式双臂、四足机器狗，和对应的夹具、灵巧手和夹爪

驱动控制装置重点强调了**自研液冷电机**和 **AHA3 控制器**

### 自研液冷电机

机器人进入持续工作场景后，关节散热会成为限制性能的重要因素。

![img_v3_02170_0c6266ec-a86b-47bc-8e20-f66fe4a357fg](/images/agibot-innovation-day-2026-3df19ff6bbcc.png)

### AHA3：第三代三智一体硬件架构

![img_v3_02170_618092ff-ebd2-4e63-b58d-00ee92f9d56g](/images/agibot-innovation-day-2026-cefdfa2ff34c.png)

传统大脑、小脑分离架构的主要问题，是不同计算模块之间需要额外的数据传输。智元把他们合并到一起了

原先分散的计算和控制需求整合到统一 SoC 平台，减少跨板通信，提高系统集成度和响应能力。很自然的设计

### 灵巧手

![img_v3_02170_cf38c70f-1a81-4a44-9589-3226c7fc897g](/images/agibot-innovation-day-2026-fc9354a9ecea.png)

灵巧手分成 3 档，根据使用复杂度递增灵巧度

## 运动智能

一句话总结为：弱视觉感知与成熟的全身控制融合，加上 agent，是智元目前能用来展示的运动智能

为何用弱？因为我觉得依赖仿真训练的感知策略，并且是为了运动控制适配的感知策略，并不是通用的感知策略，类似 VLA 的

SONIC 那条 VLA 控制下面的 policy 看起来没很成熟用在这里

![Pasted image 20261030153843](/images/agibot-innovation-day-2026-0319ef669337.png)

彭志辉首先回顾了机器人运动智能的**发展历程**。

早期机器人运动控制主要依赖 MPC（模型预测控制）、轨迹规划和稳定性控制，重点解决机器人能否站稳、行走以及维持动态平衡的问题。

随后，随着动力学控制、强化学习和模仿学习的发展，机器人开始掌握跑步、跳跃、后空翻等更加复杂的运动技能。

但这些能力仍有局限：机器人即使学会了大量动作，这些动作**不是基于感知发生的**。

目前运动智能还是几乎收敛了的状态

* **动作泛化**主要指通过大规模、多样化运动数据训练，使模型能执行或组合未见过的动作，能否跟踪训练时没见过的参考动作，例如 ExBody2。具体体现为复杂的舞蹈动作
* **环境泛化**就是感知运控模型了，感知驱动的运动控制，在不同地形、障碍物和环境扰动下保持有效运动 [Humanoid Parkour Learning](https://humanoid4parkour.github.io)，具体体现为上楼梯

![d905d2dc313eee0e6c49b20e3c7fc8a4](/images/agibot-innovation-day-2026-4e4865c8df92.jpg)

![7365fc95e4577093caa71850f6b51744](/images/agibot-innovation-day-2026-420260a90d3b.mp4)

### AGILE 2.0 感控一体模型

自进化用了一个案例展示了 AGILE 2.0 感控一体模型

展示了好几个核心能力，最直接的是 locomotion-manipulation，并且加上了 agent 自行发现腿部故障，重新调用仿真环境训练行走策略，然后恢复运动能力

![3884851240f439a850978f047ac6f529](/images/agibot-innovation-day-2026-6bf87699331b.mp4)

视频显示看起来**不是 SONIC 那条路线**

从发展历程引出自己的模型

发布的 AGILE 2.0 算是智元目前的王牌运动智能模型了，机器人运动会能拿第一这确实够强

![img_v3_02170_df029222-cf54-4578-a6cb-ebf0e861194g](/images/agibot-innovation-day-2026-98b1e17ebea7.png)

![img_v3_02170_5ac2e38b-0a0e-4123-a414-3e013ffb597g](/images/agibot-innovation-day-2026-8de026468ac8.png)

我不是做这个方向的，我理解为有了自研腿式本体之后，有好的仿真 infra 以及感控一体模型配合起来构成运动智能

## 作业智能

除了娱乐导览，机器人还得干活

但是值得注意的是，主要宣讲的**强调数据驱动的作业智能**，还**没有很好的落地**，已经落地的智元方案主要是轮式双臂构型运控算法和 CV 类型完成的任务

但是大部分篇幅都关注做好数据、做好模型

前面运动智能是彭志辉主讲，这边是姚卯青

主要介绍了 AGIBOT WORLD 2026 开源数据集、MEgo 无本体数据采集体系、新发布的 MEgo Glove 触觉手套、觅蜂派众包平台和 MEgo Engine 数据治理引擎

姚卯青首先回应了一个行业关注的问题：随着 GPT-6 等通用大模型能力快速进步，机器人专用模型是否会被通用 AI 取代？他觉得要不做那个被击穿的，做那个 AI

> 对于 GPT-6 我觉得用于具身，肯定不是端侧模型，没法那么高频控制，这个就像用法拉利拉货一样的问题，你问他能不能拉，可以，但是没必要拉。因此 GPT-6 存在对于具身应该是积极的，更多是为具身领域**分担一部分困难的问题**，而**不是完全取代**现有的具身模型

![c766d4e79f79f8f6e73bff3ac17f427a](/images/agibot-innovation-day-2026-a87f6f1ba98b.jpg)

姚卯青强调，衡量机器人能力的标准，已经从能否完成一次精彩演示，转向能否在真实环境中长期可靠地完成工作。

机器人能否进入真实工作流程，大会将其归纳为四个相互关联的组成部分：

数据、模型、本体、场景。

![Pasted image 20261031210816](/images/agibot-innovation-day-2026-9f86a6689452.png)

### 数据

和前面的运动智能技术路线相比就很不一样了，运动智能的模仿数据学习数据可以来源于仿真器精确建模的试错经验、人类视频提取的或者动捕动作轨迹

作业智能主要是面向操作的，数据得来源于在真实物理世界数据采集

机器人开发标准流程往往先采集示范数据，训练模型，然后进行部署。

但真实部署过程中，机器人还会不断遇到新的物体、环境、任务变化和失败情况。

这些**真实交互经验同样具有训练价值**。

因此，智元希望建立一套能够持续生产、处理和转化高质量数据的系统。

**两面性**

这是虽然说是和传统机器的交付不一样，传统做一台自动化流水线设备，设计好了调试调试交付，正常运行，再售后售后就行了

具身数据驱动的能力可以在部署场景学习的更强，交付的是一个能力持续提升的产品。

* 批评可以被理解为：你们的机器人能力比较弱，来到我们部署现场还需要自己尝试运行一个月才能满足甲方的需求
* 优势可以理解为：模型的能力可以持续积累，对于下一家甲方可以能可以直接上线，或者很快适应，长期来看大大减少了不同复杂场景的适配需求，这是数据驱动方案的优势

#### AGIBOT WORLD

![ca6529015fb9a11c0de0faf2a9008d5d](/images/agibot-innovation-day-2026-82c0181a2268.jpg)

姚卯青首先介绍了智元此前发布的 AGIBOT WORLD 数据体系。

* 2024 年，智元发布了 AGIBOT WORLD 百万真机数据集，希望为具身智能研究建立更大规模的数据基础。
* 2026 年，智元进一步推出 AGIBOT WORLD 2026，计划围绕五类研究主题分阶段开放数据。

| 发布阶段 | 数据主题                         | 重点解决的问题            |
| ---- | ---------------------------- | ------------------ |
| 第一期  | 模仿学习（Imitation Learning）     | 从专家示范中学习基础操作技能     |
| 第二期  | 多样交互（Diverse Interaction）    | 覆盖更多样的交互状态与行为      |
| 第三期  | 强化学习（Reinforcement Learning） | 利用成功、失败和人工纠正经验学习   |
| 第四期  | 具身推理（Physical Reasoning）     | 根据任务状态和条件，判断应该如何行动 |
| 第五期  | 待后续发布                        | 本段演讲未明确公布主题        |

第一期是算是传统 VLA 模仿学习短时 pick and place 的任务

第二期算是为了世界模型的训练构建的数据

第三期是为了让模型可靠能力提升的数据，这部分数据估计不好用，这类自主 rollout 数据局限于具体 robot 和具体场景的自我优化

第四期我理解为 agent 的方案，agent + VLA 原子动作的数据集

重点培养机器人对任务条件、过程记忆和行动选择的理解能力

**传统操作数据**

* 给定物体和目标，学习如何抓取、放置或完成一段操作。

**具身推理数据**

* 给定任务目标与当前环境状态，先判断哪些操作必要、应该按什么顺序执行，再完成实际动作。

AGIBOT WORLD 主要还是真机本体的采集

还有一大类是无本体采集

#### MEgo Glove：从手部运动采集到力觉、触觉采集

![edf3e36d1584bef04e563335990c4ff1](/images/agibot-innovation-day-2026-4e910f3e6273.jpg)

之前就发布了 ego、UMI 数采设备了，当天发布了灵巧手触觉数据采集

![2d8691a65356a613be8e50915e71a5cb](/images/agibot-innovation-day-2026-3770aaa890d5.jpg)

* MEgo Glove 首先强调免工具快拆快装方便清洗，因为采集者手汗很多。
* 手部位姿使用 EMF 惯性测量，没用 CV 的人手提取算法，这个我很赞同，本来 CV 数据都在人手上面训练的，没必要识别手套，以及人手提取算法更适用于人手 ego 数据
* MEgo Glove Air 与 Ultra 两个版本，Ultra 版本才有触觉，目前官方只明确了三维触觉测量能力，没有披露采用压阻式、电容式、磁感应式还是光学视触觉传感器

记录触觉数据采集从“人类做了什么动作”，进一步走向记录“人类如何与物体产生接触”。

![wx_camera_1793247624553](/images/agibot-innovation-day-2026-f8bf6c41f08c.jpg)

#### 觅蜂派 App

数采接单 App

数采厂的数据多样性是有限的，因此，将数据采集从少量集中式数据工厂，扩展为连接不同场景和采集人员的分布式平台。

![e2ac15f1b3ddacb6a248b4e860c44280](/images/agibot-innovation-day-2026-88a38645635a.jpg)

姚卯青在演讲中使用了外卖平台作为类比。

外卖平台连接商家、订单需求和骑手，组织分布式的线下履约网络。

觅蜂派希望建立类似的数据采集组织方式。

#### MEgo Engine：把原始采集数据转化为可训练的数据

我理解为智元内部的数据处理管道

![65d8c8b1e958ee33b39cc2126408c5f1](/images/agibot-innovation-day-2026-9dfeb32861e3.jpg)

硬件上面我觉得难的地方是，多源数据对齐，对齐视觉、运动和其他传感数据，非常对齐，数据精度 OK，硬件这块应该都 OK 了

主要是更难的是软件这块

觅蜂科技还介绍了将连续操作拆解为 120 多种标准原子动作的处理体系，并使用 ManiEval 开展多维质量评估

自动化将长时任务拆分为子任务和原子动作和语义标注，我觉得挺难的

还有异常数据数据质检与分级，最终到能够用来训练的数据，这个非常重要

### 模型

姚卯青首先提出，具身智能模型的持续提升，需要覆盖多个学习阶段。

整个体系分为三个阶段：

![Pasted image 20261031045240](/images/agibot-innovation-day-2026-efa41bd005ae.png)

GO-3 和 Genie Master 年底会开源

#### GO-3 Preview：智元第三代具身基座模型

现场展示 GO-3 Preview 在 RoboTwin、RoboColiseum 等三个榜单上排第一。我觉得成绩主要来源于数据预训练 + 模型 + agent

**WRAM：统一任务理解、未来预测与动作生成**

WRAM 的整体作用由三个模块形成了不同的分工。

| 模块   | 核心功能       | 主要解决的问题            |
| ---- | ---------- | ------------------ |
| CoAE | 控制向视觉特征压缩  | 如何高效表示与机器人操作有关的信息  |
| SVP  | 未来状态预测     | 如何从任务条件推断物理世界的后续变化 |
| IDM  | 根据状态变化生成动作 | 如何把预测目标转换为机器人执行动作  |
| KASO | 训练时的选择性优化  | 如何让未来预测与动作监督更加一致   |

#### Collective Experience Learning，CEL

![a835d71b8c77ee39acd70318f42a63aa](/images/agibot-innovation-day-2026-a6a2a567d3e5.jpg)

智元与清华大学、无问芯穹合作研发的群体经验学习（Collective Experience Learning，CEL）。

群体经验学习的基本闭环

![Pasted image 20261031051319](/images/agibot-innovation-day-2026-9e77ee1f5c46.png)

CEL 使用的核心算法之一是 FERT（Failure-guided Experience Retrieval Fine-Tuning），即失败引导的经验检索微调。

姚卯青强调，机器人失败后，不应仅把这次执行当成无效数据，也不能简单地重复训练所有成功示范。

这里最重要的技术思想是：

成功轨迹提供动作监督，失败轨迹提供学习重点。

论文：[Learning from Fleet Experience: Collective Experience Learning across 96 Robots](https://cel-robot-learning.github.io/)，副标题是 The fleet becomes a source of experience（机器人集群成为经验的来源）。作者来自清华大学、智元和无问芯穹，这部分的工作是于超老师（THU）参加的。

RLinf 百机实验的技术报告已经上线，共 50 页，总结了过去大半年对大规模真机后训练的探索。

介绍完 FERT 之后，姚卯青进一步强调：即使算法能够从群体经验中学习，也必须解决真实机器人集群的工程稳定性问题。

因此，团队开发了 FATS（Fault-tolerant Asynchronous Training System），即容错异步训练系统。

#### 世界模型后训练：利用经验回溯探索不同的未来

![6840efc8b0eeb85ef7ca09ab3ba65eb3](/images/agibot-innovation-day-2026-69c4d183ab50.jpg)

世界模型我觉得水分还是比较大

#### Genie Master：从后训练 Scaling 走向部署后 Physical RSI

![a507c8ba84f47e78313613af95cab1eb](/images/agibot-innovation-day-2026-a69def61763e.jpg)

![645ae0003e284349898055612f8aa10c](/images/agibot-innovation-day-2026-bd50f017252f.jpg)

根据智元 2026 年 10 月 27 日的 Genie Master 发布资料，框架提出 EEP 具身执行协议，包含能力、引导、反馈和连续性四类接口

智元提出 EEP（Embodied Execution Protocol）具身执行协议，统一以下四类接口：

| 接口 | 作用 |
| --- | --- |
| 能力接口 | Agent 了解机器人有哪些可调用技能 |
| 引导接口 | Agent 向下层 Policy 提供执行指导 |
| 反馈接口 | 机器人返回执行结果和异常信息 |
| 连续性接口 | 任务中断后保留进度并继续执行 |

姚卯青介绍了一个具体案例。

机器人需要把零食袋挂到便利店货架的挂钩上。

但由于挂钩尺寸较小，且受到标签牌遮挡，机器人使用头部相机时难以准确观察目标，导致挂货频繁失败。

Genie Master 通过回溯失败记录定位问题，然后调整执行过程。

官方技术资料进一步说明，Genie Master 将经验积累分成 Harness RSI 和 Policy RSI 两条路线。

| 对比             | Harness RSI         | Policy RSI        |
| -------------- | ------------------- | ----------------- |
| 改进对象           | Agent 执行系统           | 底层动作 Policy        |
| 主要方式           | 记忆、Prompt、执行规则与策略调整 | 使用执行与恢复数据继续训练     |
| 是否需要更新 Policy 权重 | 不需要                 | 需要                |
| 典型案例           | 挂货失败后改用腕部相机辅助定位     | 利用打包异常与恢复轨迹训练动作策略 |
| 核心价值           | 让 Agent 记住更有效的执行方法    | 让经验转化为参数化动作能力     |

这里最重要的区别是：

Harness RSI 改善的是如何组织和调用已有能力；Policy RSI 改善的是动作策略本身。

RSI 的故事可以再讲讲，还没有很收敛，我觉得 Genie Master 应该是 Harness RSI

**11 月 2 日的连续 24 小时验证**

大会最后预告：

![Pasted image 20261031052354](/images/agibot-innovation-day-2026-8cb86d0b8b6c.png)

#### GO-3 与 Genie Master Demo

![bff6370140a26a529a9e3ba7ddfff0e9 1](/images/agibot-innovation-day-2026-a93ca6cc39be.mp4)

![d59e98f21c12176f2a36797baecdd3d7](/images/agibot-innovation-day-2026-96e90e437e12.jpg)

这个 demo 可能是 GO-3 模型和 Genie Master 的体现，模型原子动作 + agent

关键在于 而是利用少量数据微调，**再通过 Agent 编排多个动作步骤**

agent 与模型的结合也值得研究

### 本体

![ce9f2974b4fb50e3e72490ec679080c4](/images/agibot-innovation-day-2026-7ef401323feb.jpg)

发布高负载工业作业本体

### 场景

![9bb0442c8ebb818b5356212c16a87272](/images/agibot-innovation-day-2026-b6074f63c476.jpg)

![9fb6fc6fc190cee2313bd74db71145a9](/images/agibot-innovation-day-2026-dd4a9f61b025.jpg)

我觉得 11 月 2 号直播的场景才和前面数据、模型、后训练有关系

现在落地的场景和前面展示的数据、模型、后训练关系不大，不能说明重点研发的技术已经很好地落地了，更像是在为周期很长的数据驱动方案争取缓冲

#### 落地场景 Demo

![wx_camera_1793242774731](/images/agibot-innovation-day-2026-abf1107fe301.mp4)

![aaf9953b06c3b83e48d15fde990b061c](/images/agibot-innovation-day-2026-d7b906535989.mp4)

双机协同

![7363cf2fcd7de4c56d9873fe06ac7009](/images/agibot-innovation-day-2026-05b2c7886251.mp4)

运控 + CV 校准

## 交互智能

![Pasted image 20261031211904](/images/agibot-innovation-day-2026-f92c0d52ace3.png)

交互智能与 WITA-OMNI

它是人形的本体，要维持基本的交互动作，以及下半身的稳定平衡和基本的运动

上半身要负责拾音、视觉输入，然后模型推理，再到 React 输出语音、面部动画，并且输出对应的上半身的动作

官方提到的是在 think talk 的范式上做了扩展，具体怎么实现的我不熟悉这块音频多模态生成模型，不好去推测

但是我觉得比较难处理的几个地方就是：首先，我觉得动作可能没有那么复杂，但是如果在嘈杂的环境下拾音，并且要在多个人交流的情况下选对交流的目标，以及非常快的端侧响应，我觉得这是比较难的一点。但他们这方面做得挺好。

![Pasted image 20261031220712](/images/agibot-innovation-day-2026-a786a08e0abd.png)

交互数据那肯定是部署时候的数据非常重要了

![Pasted image 20261031220704](/images/agibot-innovation-day-2026-8bb93392c900.png)

他们的交互模型架构

![Pasted image 20261031220728](/images/agibot-innovation-day-2026-b0d36773cddf.png)

能力还是非常强的

已经研发落地

![Pasted image 20261031224033](/images/agibot-innovation-day-2026-0eada7c12e87.png)

![Pasted image 20261031224047](/images/agibot-innovation-day-2026-07a2f22154c5.png)

主要还是导览才有交互

**一个猜想：交互智能放到 IP 机器人上**

现在交互智能是放在远征 A3 这样的全尺寸人形上。但交互的价值主要在对话、表情和陪伴，对本体运动能力的要求不高。如果把这套能力放到特定的小型机器人或者卡通 IP 机器人身上，成本更低，也更容易进商场、景区和家庭。一旦某个 IP 火起来，商业价值可能比放在人形导览上更大。
