---
title: ASENA：Coding Agent 如何通过 Workspace 实现 Self-evolving
date: '2026-11-03'
lastmod: '2026-11-02'
draft: false
tags:
- Embodied AI
- Agents
- VLN
- Robotics
categories: []
summary: 梳理 ASENA 如何通过编码智能体、持久工作区与导航工具组织机器人任务，并记录对工具接口和自我演化的思考
math: true
showtoc: true
tocopen: true
---

## 概览

我觉得 ASENA 值得关注的地方，是它把 Self-evolving 拆成了 Worker 和 Improver 两个角色，以及它为了接入 Agent 系统，对 Navigation Policy 做了专门适配

- **Worker：执行任务并提供反馈** Worker 实际运行任务，留下执行轨迹和结果，作为后续修改 Workspace 的依据
- **Improver：根据反馈修改外部权重** Improver 是负责修改代码和 Workspace Context 的 Coding Agent，这里的 Self-evolving 由 LLM 修改代码、笔记和指导来实现，模型权重本身保持固定
- **Navigation Policy：为工具调用做适配** ASENA-VLN 使用结构化 JSON 表达目标和约束，输出可执行的 waypoint 轨迹，并配合 atomic-navigation 数据训练，我觉得这种为了接入 Agent Toolchain 而调整 Policy 接口和训练数据的方式，可以借鉴到 VLA 里

这篇文章将 agent 和 vln 结合了，并且设计了一个叫

* ASENA 的系统 - 一个用于传感器访问、代码执行、监督式机器人控制与持久经验的具身智能体系统
* ASENA-VLN 是一种可选的 4B 单目导航策略，可将指令与 RGB 历史映射为航点，该策略在仿真中评估，并可由 coding agent 作为导航工具调用

![Pasted image 20261102182021](/images/asena-self-evolving-agent-cc0655325863.png)

## Self-evolving

ASENA 研究的是“权重全部固定，只让工作区围绕一个预训练导航策略演化”

演化我理解为

他把“**能力增长”放在可以改写的代码和笔记里**，而不是放在模型权重里，学来的导航策略只是工具箱里的一件工具

### 外部权重

“外部权重”具体是什么？

具体对应的是**工作区里的文件**：

* **可执行技能：** 一个个 `.py`，比如 `onsurface.py`、`climb.py`
* **笔记、指导和心得：** EQA 部分说演化会加入新的例程、细化已有的指导
* **以前的动作序列：** 在 R2R/RxR 的重复任务里，worker 还可以保存之前的动作序列（Sec. 4.4）

它和真正的权重有两点不同

1. 第一，更新方式是 LLM 对文本和代码做离散编辑，不是梯度更新
2. 第二，它有版本号，人能看懂，能回滚，还能做“合并、测试、删减”这样的操作

### 能力怎么增长的？

能力增长的过程是什么？

improver 负责在两轮之间，根据 worker 留下的记录去修改共享工作区

1. improver 就是专门负责“改工作区”的那个 coding agent
2. worker 是 负责跑任务的 coding agent

论文的定义在 Sec. 3.2：

$$ W_{k+1} = I_\phi(W_k,\ \mathcal{T}_k,\ f_k) $$

* $W_k = (N_k, S_k)$ 是第 $k$ 版工作区，$N_k$ 是笔记，$S_k$ 是可执行技能
* $\mathcal{T}_k$ 是 worker 这一轮的执行轨迹
* $f_k$ 是反馈，仿真里是 ground-truth 的成败结果
* $I_\phi$ 就是 improver，$\phi$ 是它的模型权重，整个过程中一直不变

## Agent 在里面承担什么角色？

![Pasted image 20261102182426](/images/asena-self-evolving-agent-d72f61210cf4.png)

agent 是一个用写代码（编写工具）来规划、调度、调试的“大脑”，在任务中实时写程序，把感知、几何计算、ASENA-VLN、抓取和运动规划、手势、语音等工具组合起来（组合调用 tool chain）**工作区**是它跨任务积累下来的**外部记忆**（我现在知道已经什么），执行记录是它用来检查和修改程序的**证据**（我理解为根据过去和当下的状态记录去 self-evolving）

## 任务进度怎么管理的？

大致有几个层面

1. 单次调用的颗粒度 比如一次 vln 调用结束控制权交给 agent
2. 进度判断写成代码，是 agent 根据任务内容自己写下来脚本用来判断任务进度的
3. 空间记忆，真机上地图是边探索边重建的，agent 会维护空间记忆（Sec. 4.6），EQA 工具里也有 place memory（Sec. 4.5）
4. 任务超时检测

高层的任务进度主要靠 agent 自己的上下文，加上它写的检查代码

## 下层的 Tools 怎么给 Agent 适配的？

### 统一操作入口

把下层能力统一包装成 agent 可以在程序里直接调用的“原子技能”，再对少数工具专门设计接口，项目主页的给出的案例是里有 `find_floor_patch(views)`、`step_and_observe()` 这类 Python 风格的调用

因此大概率 agent **统一操作入口**应该是 python api，agent 负责自主组合这些 api

### 观测数据的处理

**原始数据直接交给 agent** 360° 相机、LiDAR、里程计、IMU、关节状态都是直接给 agent 的原始传感数据，然后让 agent 自己写代码来处理 这些数据再来调用统一操作入口，也就是 传感器的读取到处理到决策 是让 agent 自主完成的，再去组合下层的 操作入口

> 我觉得传感器的入口也应该更好的封装而不是从零写，但是从 0 写更能体现 rsi，但是我觉得更应该提前尝试好去把感知到调用下层这个 skills 的链路也提前选好吧，让 rsi 去调整具体感知处理策略里面的细节，而不是让他临时自己选型用什么算法处理传感器数据再去调用下面的 skills，这样很浪费时间

### Policy 为了被调用专门设计过

VLN 的

1. 输入是结构化 JSON：目标文本，加上可选的终点位姿、锚点物体、运动约束

作者明说这样设计就是为了**方便它作为工具被调用**（Sec. 3.3 “Policy inputs”）

> 为了方便被调用这个背景下，policy 被作为工具调用链路的一个环节，为了适配 toolchains，自然要对输入输出有所改动

理由是

* 对 agent 来说，好处是它可以用代码拼出精确的约束，比如 `{"target":"agent_start","relation":"forward","distance_m":1.0}`，不用只靠一句自然语言

因此 为了让训练数据对上这个接口，他们用 GPT-5.5 把原有的导航指令 **（自然语言）重写成这种 JSON 格式**（Sec. 3.3 “Training mixture”，附录 Table 10）

> 我觉得这个可以借鉴到 vla 里面去

2. 输出是**一小段机体坐标系 waypoint 轨迹** （Sec. 3.3 “Output representations”）

是可以直接执行，作用有点像 robot arm 里面把 action 换成 action chunk，性能上**减少 agent 反复决策**（这层用意是推断的，作者只报告了调用次数下降，离散输出 token 的 vln 是走 15cm 这种，可能会导致反复决策）

同时为了适配 让 agent 通过**JSON 输入能写出精确约束**，去做“往前 1 米”“穿过门”这类局部指令，因此造了 atomic 数据，专门教 policy 执行这些短而精确的指令，（Sec. 3.3 “Curated atomic-navigation data”）

## 链路的 Self-evolving

校验失败会把原因告诉 agent

抓取这条链路是 SAM 2 分割、深度测量、可选的 GraspGen-X、IK 和运动规划串起来的，执行前系统会根据实测的关节状态重建轨迹，检查关节限位、自碰撞和场景净空，手势会先在 MuJoCo 里校验，任何一项校验失败，系统都会把具体违反了哪条约束返回给 agent，让它修改（Sec. 3.1 “Manipulation”“Execution checks”）

> 我觉得可以这么做，能体现 self-evolving，但是效率比较低这样的 feedback 再修正很慢，但是确实算是运行时 agent 系统的 self-evolving，我觉得可以让失败模式尽可能能用固定的方式去优化？就像提前做好专门的失败的 skills 去处理这个异常，而不是让 agent 临时兴起 ideas
