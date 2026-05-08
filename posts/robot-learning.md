---
title: Robot Learning Tutorial 笔记 — RL 基础
date: '2026-05-08'
draft: false
showtoc: true
tocopen: true
tags:
- robot-learning
- reinforcement-learning
- mdp
- paper-notes
categories:
- paper-notes
math: true
summary: Lerobot Robot Learning Tutorial 的 RL 篇精读笔记：MDP 形式化、价值函数 V/Q、策略优化目标。
source: 00_inbox/Robot Learning.md
---
reading Robot Learning: A Tutorial[Robot Learning: A Tutorial - a Hugging Face Space by lerobot](https://huggingface.co/spaces/lerobot/robot-learning-tutorial)

rl 和 IL 的数据来源非常不同在, rl 是通过自身与环境交互产生的 interaction data.优化 policy

![[robot-learning-65a684e4791d.png]]

> Figure 12 | Agent-Environment interaction diagram (image credits to Sutton and Barto (2018)).

这个 agent-env 交互上图讲的很清楚

* 策略网络接受 $s_{t}$ 输出 $a_{t}$ , 与 env 交互, 自然得到下一个观测状态 $s_{t+1}$ 和新的奖励 $r_{t+1}$, 优化的循环中 $r_{t}$ 被用作优化器 优化 policy

> Formally, a lenght- $T$ Markov Decision Process (MDP) is a tuple $\mathcal { M } = \langle { \mathcal { S } } , \mathcal { A } , \mathcal { D } , r , \gamma , \rho , T \rangle$

更具体一点,robot learning rl 的 problem 被建模为一个轨迹长度为 T 的 **MDP**[^concept-mdp] 马尔可夫决策过程 $\mathcal { M } = \langle { \mathcal { S } } , \mathcal { A } , \mathcal { D } , r , \gamma , \rho , T \rangle$ , 本质上就是一个 tuple

rl 背景下的马尔可夫决策过程是一个元组 $\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{D}, r, \gamma, \rho, T \rangle$。

* **$\mathcal{S}$ (状态) / $\mathcal{A}$ (动作) / $r$ (奖励)**：分别是传感器的输入（`obs`）、机械臂的输出（`action`）、以及打分机制
* **$\mathcal{D}$ (Dynamics, 动力学,物理定律的 model free 的概率分布表示)**：$\begin{array} { r } { \mathcal { D } \left( s _ { t } , a _ { t } , s _ { t + 1 } \right) = } \end{array}\mathbb { P } ( s _ { t + 1 } | s _ { t } , a _ { t } )$ 就是状态转移方程,在状态 $s_{t}$ 下执行动作 $a_{t}$，结果**刚好**落在状态 $s_{t+1}$ 的概率是多少
	* 在你的代码里，这就是调用 `env.step(action)` 背后那个你无法掌控的真实物理世界（或者仿真器）。
* **$\gamma$ (Discount factor, 折扣因子)**：代码里通常设为 `0.99`。决定机器人是“目光短浅”（只看眼前得分）还是“高瞻远瞩”（考虑未来得分）。
* **$\rho$ (Initial distribution)**：初始化分布。代码里对应 `env.reset()` 时机器人和物体的随机初始摆放位置。$s_{0}$ 是在这个分布中采样的
* **$T$ (Horizon)**：一个回合（Episode）的最大步数，比如 500 步。

$$
\tau = (s_0, a_0, r_0, s_1, a_1, r_1, \dots, s_{T-1}, a_{T-1}, r_{T-1}, s_T)
$$

这就是“一条长度 $T$ 的轨迹（Trajectory）”，也就是机器人从开机（$s_0$）到关机/任务结束（$s_T$），所经历的完整录像。

 “健忘”的法则：马尔可夫假设

* $\mathbb{P}(s_{t+1}|s_t, a_t, s_{t-1}, a_{t-1}, \dots) = \mathbb{P}(s_{t+1}|s_t, a_t)$ 强调 未来只与现在有关
* $\mathbb{P}(a_t|s_t, a_{t-1}, s_{t-1}, \dots) = \mathbb{P}(a_t|s_t)$ 强调 机器 policy 的输出 $a_{t}$ 仅仅和 $s_{t}$ 有关

**物理意义**：**马尔可夫性（Markovian）**，大白话就是“**未来只与现在有关，与过去无关**”

> 这个特性负担很轻,没有很长的历史记录
> 后来的 ACT 用了 Chunking 技术引入了一小段历史，那是为了对抗现实世界中并不完美的马尔可夫性，即部分可观测问题 POMDP，但基础理论基石依然在此?

轨迹的概率分布定义

$$
\mathbb{P}_{\theta; \mathcal{D}}(\tau) = \rho \prod_{t=0}^{T-1} \mathcal{D}(s_t, a_t, s_{t+1}) \pi_\theta(a_t|s_t)
$$

* $\rho$ 省略了 参数 $s_{0}$ 初始 $s_{0}$ 发生的概率
* $\mathcal{D}$ 动力学决定状态转移成功的概率,
* $\pi$ 是 param 为 $\theta$ 策略网络决定 在 $s_{t}$ 下面取 $a_{t}$ 输出的概率
* Markovian 性导致的历史**条件独立**,自然的**连乘**形式

策略优化目标定义

 $$
G(\tau) = \sum_{t=0}^{T-1} \gamma^t r_t
$$

$$
J(\pi_\theta) = \mathbb{E}_{\tau \sim \mathbb{P}_{\theta; \mathcal{D}}}[G(\tau)]
$$

* $G(\tau)$ 是轨迹的 return ,总得分, 受到了 discount factor 的影响, $\gamma <1$ 时自然越往后占比越低
* $J(\pi_\theta)$ 是期望 return , 是衡量轨迹概率分布 $\mathbb{P}_{\theta; \mathcal{D}}(\tau)$ 的平均表现 也就是 结合了 $G(\tau)$ 的加权平均, 在 $\pi_{\theta}, \mathcal{D}$ 的作用下, 机器人跑无数条 $\tau$ 平均能拿多少分
* 优化目标自然是最大化期望了, RL 的训练过程 `optimizer.step()`，就是在解 $\max_\theta J(\pi_\theta)$

价值函数 V 和 Q

因为不能等每次跑完再去算分, 所以也有对 $s,a$ 的打分

$$
Q_\pi(s_t, a_t) = \mathbb{E}_{s_{t+1} \sim \mathbb{P}(\bullet|s_t, a_t)}[r_t + \gamma V_\pi(s_{t+1})]
$$

$$
V_\pi(s_t) = \mathbb{E}_{a_t \sim \pi(\bullet|s_t)}[Q_\pi(s_t, a_t)]
$$

* **$V_\pi(s_t)$ (状态价值函数, State-value)**：评估“**当前状态有多爽**”。比如机械臂已经悬停在待抓物体的正上方，哪怕还没抓，这个状态的 $V$ 值也很高，因为“闭着眼睛都能赢”。当前的 $V$ 等于 对所有可能动作的 $Q$ 值求期望, 就是对 **$Q$ 的加权平均版**
* **$Q_\pi(s_t, a_t)$ (动作价值函数, Action-value)**：评估“**在这个状态下，做这个特定动作有多爽**”。 当前的 $Q$ 值等于“即时奖励 $r_t$” 加上“下一步局面的 $V$ 值”(TD 时序差分) , 本质上也是评估 $s_{t+1}$ 有多好

> 这两个也叫,Bellman Equation

这就是所谓的 **Actor-Critic 架构**：Actor（策略网络 $\pi_\theta$）负责干活输出动作，Critic（Q 网络）负责当裁判，告诉 Actor 刚才那一步能得几分，从而用梯度引导 Actor 更新权重。

![[robot-learning-fe4bb220a2e8.png]]

> Popular RL algorithms. See Achiam (2018) for a complete list of citations.

前面那堆冗长的 MDP 公式定义了“我们要优化什么（Objective）”，而 PPO、TD3、SAC 这些算法是具体“怎么去优化（Optimizers）,既然是从交互数据中学习,他们对如何利用数据的策略自然是大不相同的

真机的试错成本比仿真要高很多, 所以 要很好的利用 少量的数据, off-policy 对数据的利用率更高更适合

* **PPO (On-policy)**：非常稳定，但它是“现学现卖”，收集一批数据更新完网络后，这批数据就**扔掉**了。它是个“数据黑洞”，只适合在仿真器（Simulation）里几千个并发环境一起跑
* **TD3 / SAC (Off-policy)**：它们维护了一个**经验回放池（Replay Buffer）**。不仅过去收集的数据可以反复拿来训练（样本高效 Sample-efficient），**还可以把人类遥控机器人的专家数据（Prior Data）塞进去**。因此，**真机 RL 必须使用 Off-policy 算法！**

对于仿真环境训练的强化学习,不可避免考虑 DR 域随机化的问题,是一种调参地域, sim2real 的难题, 人形机器人在 locomotion 和 模仿学习里面已经有很多研究

既然写物理仿真这么痛苦，而且软体和形变根本仿真不出来，那我们为什么不直接**在真实世界里用真机训练**呢？聊聊真机的 强化学习训练

对于实机整个 RL 引擎的进化本质上就是为了**在“连续动作空间”中寻找一个“既能稳定探索、又极其节省数据”的最优解**

**DQN 搞定了高维输入但只能做离散动作（上下左右）；DDPG 打通了连续动作的控制，但它输出的是死板的确定性动作，既不会探索也容易在真实物理世界中崩溃；这最终逼迫学术界进化出了目前的终极形态——SAC**

Soft Actor-Critic (SAC) (Haarnoja et al., 2018) 是在 积累 最大化 return 的情况下要 **动作尽可能多样**/ 随机, 这个随机性就是叫做熵, 这个算法是 在最大熵 rl 框架下对 DDPG 的派生

$$
J(\pi) = \sum_{t=0}^{T} \mathbb{E}_{(s_t,a_t)\sim \chi}\left[ r_t + \alpha \mathcal{H}(\pi(\bullet|s_t)) \right]
$$

* 策略的熵 $\mathcal{H}$**（用 $\alpha$ 控制比重）。熵越大，代表策略越不确定。分布不偏, 有很多可能的动作
* $\mathcal{H}(\pi(\bullet|s_t))$ 在状态  下，$s_{t}$ 策略  $\pi$ 输出的**动作概率分布**的熵, 这个 $\bullet$ 代表不是单一动作是动作分布, 这里的 $\pi$ 就是概率密度函数 (PDF)

> **分布=规则本身，PDF=连续规则的一种数学写法 (l 连续随机变量的概率分布)**, 算 PDF 的概率要**积分**, 适用于连续动作变量,这里自然是连续的动作.. 还有其他离散的随机变量的分布叫做 PMF 概率质量函数 $P(X=x)$

直观上来看, 模型学会的策略会更鲁棒, 对于真机 rl, 鲁棒是对 现实噪音的对抗,

> 比如在面对一个任务（比如抓杯子）时，如果有多条轨迹都能抓到，SAC 会倾向于“记住所有能成功的方法”，而不是像 DDPG 那样死磕一条路。如果执行时遇到了物理偏差，SAC 能立刻顺滑地切换到另一条成功路径上。这在充满噪音的真实物理世界是极其关键的保命技能。

这是 AC 算法, 知道了优化目标, 那怎么更新 actor 和 critic 网络呢?

critic 网络学习的是一个 soft TD-target 时序差分

$$
 y _ {i} = \mathbb {E} _ {s _ {t + 1} \sim \mathbb {P} (\bullet | s _ {t}, a _ {t})} \left[ r _ {t} + \gamma \left(Q _ {\theta_ {i - 1}} \left(s _ {t + 1}, a _ {t + 1}\right) - \alpha \log \pi_ {\phi} \left(a _ {t + 1} \mid s _ {t + 1}\right)\right) \right], \quad a _ {t + 1} \sim \pi_ {\phi} (\bullet | s _ {t}) \tag {16} 
$$

这是 Critic（Q 网络）更新时的目标值（Target）$y_{i}$ , 前面的优化目标 引入了最大熵, 这里自然加上 $-\alpha \log \pi_\phi(a_{t+1}|s_{t+1})$ 就是熵的样本形式 ($a _ {t + 1} \sim \pi_ {\phi} (\bullet | s _ {t}) \tag {16}$)

> 概率分布 $\pi$ 套一个 $-\log$ 就是在算 这个分布偏不偏, ,数字越小越偏, 越随机 (期望行为)

* $-\alpha \log \pi_\phi(a_{t+1}|s_{t+1})$ 让 Critic 在打分时，把“**探索的潜力**”也算作了分值的一部分。即便当前动作没拿到环境奖励，只要它能带来更多未知的探索价值，网络也会认为它是一个好动作。

> 这里的 期望 + 熵奖励 体现了是 soft 的 而不是选最大的的 $Q$ 去更新 critic 网络

Actor 的进化方向

$$
\pi_{k+1} \leftarrow \arg\min_{\pi' \in \Pi} \text{D}_{KL} \left( \pi'(\bullet|s_t) \left\| \frac{\exp(Q_{\pi_k}(s_t, \bullet))}{Z_{\pi_k}(s_t)} \right.\right)
$$

这是 Actor（策略网络）的更新规则

* 大白话就是，**“让输出动作的概率分布，紧紧贴合裁判 $Q$ 给出高分的区域”**

> **KL divergence**($D_{KL}$) — 衡量两个概率分布 " 有多像 " 的指标
> exp(f(x)) 就是把某个函数变成 $e^{f(x)}$ , 这样可以把任意函数变成正数, 并且把原来的差距拉大, 再除上 Partition Function $Z$ 确保积分是 1 是合法的概率密度函数
> 这个目标分布是数学和统计物理学中，如果你要求一个系统在保持一定能量（得分）的情况下，熵（混乱度）最大，这是带约束的优化问题, 算出来的**理论最优概率分布****Boltzmann Distribution**

有了 SAC 这个强大的引擎，我们依然没法**直接**把它放到硬件上跑，因为**“冷启动瞎探索（危险且慢）”**和**“奖励函数写不出来（工程灾难）”**。

Human-in-the-Loop, Sample Efficient Robot reinforcement Learning (HIL-SERL) (Luo et al., 2024) 是目前解决这两个痛点的 SOTA（State-of-the-Art）**工程方案**

就是想办法满足前面的 SAC 算法,落地

![[robot-learning-e86ec7423f89.png]]

Prior Data (RLPD) (Ball et al., 2023) 避免了从头开始学习, 将 replay buffer 分为一半自己试错 online data 一半是 人类演示数据, 避免了从头开始瞎探索, 又慢又危险

如果让未经训练的 SAC 直接在真机上跑，它会像帕金森一样乱挥机械臂，不仅学不到东西还容易损坏硬件。

* **核心机制**：HIL-SERL 维护了**两个独立的数据池**：
    1. offline_buffer：里面装着人类专家遥控机械臂录制的几十条完美视频轨迹（Prior Data）。
    2. online_buffer：机器人在真机上自己试错产生的新数据。

> Sim-Pretrain → Real-RL Fine-tune 这个和当前截然不同的做法也有两派
> **Locomotion 派 (最成熟)** 因为 locomotion 任务接触少、动力学相对干净，sim pretrain 的偏置可控，所以那条路走得通
> **Manipulation** 也有这么做的, 冻结 sim policy 做 base，真机只学一个**残差策略** ，安全性比直接微调主网络好很多
> 但是接触太丰富的不适合 用这种仿真预先训练 提供基础, 但是 [RLToken](https://www.pi.website/research/rlt) 用这种残差修正 vla 引导 是很好的 方法

Luo et al. (2025, SERL) 解决了 奖励函数打分的问题, 你没法用 xyz 坐标为 叠衣服 查插座 这类人物设计奖励函数, 而是训练一个极其轻量的视觉分类器 $c$（论文中推荐使用预训练的 ResNet-18）

定义奖励为：$r(s) = \log c(e^+|s)$。当分类器觉得当前摄像头画面越接近“成功”画面，得分就越高

在 rl 训练之前,打分的分类器就训练好了,训练的时候 机器人走一步，就把当前视角的图片传给分类器，分类器立刻吐出一个 0 到 1 之间的概率值作为 $r_t$ 喂给 SAC

## 即使有了辅助，仍然卡在瓶颈怎么办？

HIL (人在回路干预)

有时模型可能会钻牛角尖，反复在一个错误状态下死循环。

* **核心机制**：在机器人自主训练时，人拿着遥控器在旁边盯着。一旦发现机器人快要搞砸了（比如要碰倒杯子），人类立刻接管遥控器，手动把杯子抓起来。

在这段“人类接管”的时间里产生的数据，会被打上一个特殊的标记。在存入 Buffer 时，这些数据会被同时塞进 online_buffer 和 offline_buffer，从而获得极高的数据采样权重

> 我觉得 HIL-SERL 部分没必要写那么多, 这是具体的方法论, 基础理论可以稍微详细一点, 具体的方法论没必要那么详细, 因为这种知识复用率太低了

## Imitation Learning

> 如果说上一章的 RL（强化学习）是在教机器人**“如何自己试错考高分”**，那么这一章的 IL（模仿学习）就是在教机器人**“如何完美抄人类专家的满分作业”**

Prior Data (RLPD) (Ball et al., 2023) 其实已经尝试引入 人类示范数据来解决 rl 不能从 0 开始探索

模仿学习直接学习 与现实世界的交互的数据 - **人类专家示范数据 (human demonstrations)**, 而不是自己依赖试错产生的交互中的数据在奖励函数的引导下学习 , 所以自然相比 rl 学习的数据的模态会更高

对于如何从 human demonstrations 学习, 很早提出的 Behavioral Cloning (BC) (Pomerleau, 1988) 是 在人类示范数据的监督下 学习的是 $f : \mathcal { O } \mapsto A$ 确定性的映射,自然有一些问题

比如

1. **累积误差的问题** compounding errors (Ross et al., 2011) . 根因是**协变量偏移（Covariate Shift**), 模型自身的不完美导致预测的 $a$ 产生后续的观测 $o$ , 离开了训练数据 human demonstrations 的数据分布 (**Out-of-Distribution, OOD**), 自然没法 work
2. **多模态分布灾难（Multimodal）** poor fit to multimodal distributions (Florence et al., 2022; Ke et al., 2020)：抓一个杯子，人类可以左手抓，也可以右手抓（两种正确的模式）。单模态回归器 (Unimodal Regressor) 比如 MLP+ Mse_loss 会取这两种动作的**平均值**——结果就是机器人的手直挺挺地撞向杯子中间这种 unsafe command

> 在今天的机器学习和深度学习语境下，“协变量”基本上就是 **“输入特征（Feature）”** 或“自变量（Independent Variable，通常记作 $X$ ）”的学术化（或者说更老派的统计学）叫法
> 这里协变量偏移是说 **预测/部署/测试的输入分布 和 训练集的输入分布 shift 了**

### Generative Models

为了解决 multimodal 的问题，Florence et al. (2022) 提出：不要去学一个死板的预测函数，而去学 **产生 human demonstrations 数据的“底层概率分布”**

$$
p(o, a)
$$

本质上 GM 是根据 human demonstrations$\mathcal{D}$ 来找到 $o,a$ 构成的观测,动作极维度空间的潜在流形 $p(o,a)$ 也就是通过从 $\mathcal{D}$ 学习还原 潜在分布 $p(o,a)$

> 常见用最大化对数似然 max $\log_{\theta}p(o,a)$ 调节参数 $\theta$ 来拟合数据 $o,a$ 来解这个分布

> 推理阶段的是对 $p(o,a)$ 的采样, 就像是在模仿 human demonstrations 的数据,

> 相比较 rl, GM 学习的是联合概率分布,可以通过算边缘概率来得到 判断当前状态 $o$ 有没有 OOD

> **流形假设** manifold hypothesis 认为，现实世界中出现的许多 [高维](https://en.wikipedia.org/wiki/High-dimensional "High-dimensional") 数据集实际上位于该高维空间内的低维 [潜流形](https://en.wikipedia.org/wiki/Latent_manifold "Latent manifold") 上。[^1]

#### VAE

在处理机器人学中的**高维非结构化数据**时，直接对数据的真实联合分布 $p(o,a)$ 进行极大似然估计，或计算精确的后验分布 $q _ { \phi } ( z | o , a )$ 是不可解的（intractable）

所以提出的 VAE 提出可解的变分下界（ELBO）来近似求解极大似然估计，并使用 Encoder 和 decoder 拟合近似后验与似然。

##### Definition

1. 隐变量生成模型 $p(o, a)$
2. 近似后验分布 $q_\phi(z|o, a)$ (建立在模型 1 难以精确求解的基础上)
3. 证据下界 $\text{ELBO}$ (组合 1 和 2 形成最终目标)

[^2]

###### 隐变量生成模型

当引入一个不可观测的隐变量 $z \in Z$ ,作为看不见的高层决策意图,可以把 $p(o,a)$ 表示为 $p(o,a,z)$ 对 $z$ 的的边缘化

$$
 p (o, a) = \int_ {\operatorname {s u p p} (Z)} p (o, a | z) p (z) \tag {19} 
$$

  * $(o, a)$: 观测与动作对，数据集 $\mathcal{D} = \{(o, a)_i\}_{i=0}^N$ 中的采样样本。
  * $z$: 不可观测的隐变量（$z \in Z$），物理意义上代表人类演示者正在执行的底层任务的高层抽象表示
  * $p(z)$: 隐变量的先验分布
  * $p(o, a|z)$: 在给定隐变量条件下的生成似然

引入 $z$ 好处是可以自然的捕捉不同任务的影响 (可估计不同 $z$ 意图下的似然性 likelihood of observation-action pairs)

###### Encoder 和 Decoder

$$
q_\phi(z|o, a) \approx q_\theta(z|o, a)
$$

由于 $q_\theta(z|o, a)$ 理论上由贝叶斯定理推导出的真实后验分布，通常不可解

* 后验 $q _ { \phi } ( z | o , a )$ 用 Encoder 去近似真实的后验 $q_\phi(z|o, a)$
* 似然 $p _ { \theta } ( o , a | z )$ 用 Decoder / 参数化似然
* 先验 $p(z) \sim \mathcal{N}(0,\boldsymbol{I})$ 假设先验简单服从高斯分布 (因为有很多良好的数学特性)

###### 证据下界 (ELBO)

但是现在还不能算, 但是可以把问题用**Jensen 不等式**$\log \mathbb { E } [ \bullet ] \geq \mathbb { E } [ \log ( \bullet ) ]$ 转移到最大化证据下界问题 Evidence LOwer Bound, $E L B O$

$$
\log p _ {\theta} (\mathcal {D}) \geq\operatorname {E L B O} _ {\mathcal {D}} (\theta , \phi) = \sum_ {i = 0} ^ {N} \left(\mathbb {E} _ {z \sim q _ {\theta} (\bullet | (o, a) _ {i})} \left[ \log p _ {\theta} ((o, a) _ {i} | z) \right] - \mathrm {D} _ {\mathrm {K L}} \left[ q _ {\theta} (z | (o, a) _ {i}) \| p (z) \right]\right)
$$

优化目标就是 $E L B O$

##### Loss

写成损失的形式 由两部分构成

$$
\min _ {\theta , \phi} - \operatorname {E L B O} _ {(o, a) \sim \mathcal {D}} (\theta , \phi) = \min _ {\theta , \phi} \mathbf {L} ^ {\text {r e c}} (\theta) + \mathbf {L} ^ {\text {r e g}} (\phi), \tag {27}
$$

* **$\mathbf{L}^{\text{rec}}(\theta)$**：**重建损失（Reconstruction Loss）** 解码器拿到 $z$ 后的 $-$ 的对数似然, 数据的角度上, 是先对数据压缩在还原是在强迫它从高维特征提炼特征 $z$
* **$\mathbf{L}^{\text{reg}}(\phi)$**：**正则化损失（Regularization Loss）** 它强制要求编码器算出的后验分布 $q_\phi$，必须尽量长得像我们的出厂预设的 latent space $p(z)$（标准高斯分布）。

> KL 散度。一种衡量两个概率分布有多大差异的数学工具。

> **拟合观测数据** 最大似然估计（MLE）的核心目的就是通过调整参数，让模型生成的概率分布“紧贴”真实观测到的数据点。也就是学习分布的过程
> **似然（Likelihood）是我们用来衡量模型拟合好坏的**标尺

 本身一种 **高级的、非线性的降维技术**。

* **在训练时（Training）**：编码器（看到全貌）和解码器同时工作。我们拿着人类专家的真实数据 $(o, a)$，通过编码器生成意图 $z$，再通过解码器重构出动作 $\hat{a}$。我们优化公式 (27)，不断调整 $\theta$ 和 $\phi$。
* **在推理时（Inference / Deployment）**：编码器被**直接丢弃**！由于在训练时，KL 散度已经把编码器输出的意图空间 $Z$ 驯化成了标准正态分布 $\mathcal{N}(0, I)$。当机器人在真实物理世界中运行时，我们只需要凭空从 $\mathcal{N}(0, I)$ 中随机抽一个噪声向量 $z$（这就代表随机抽取了一个合理意图），连同当前的摄像机画面 $o$ 一起丢给解码器 $p_\theta$，解码器就会顺理成章地输出一个合理的、极具人类专家神韵的动作 $a$。

> **the underlying generative process reproduced by (1) sampling a latent variable and (2) learning to decode it into a high-likelihood sample under the (unknown) $p ( o , a )$

*VAE 它将一个无法穷举的多模态决策空间，压缩成了一个可以随意采样的连续数学空间。*

#### Diffusion Models

VAE 虽然能够处理多模态问题，但它试图用**一次映射**（从 $z$ 直接解码到 $a$）来完成所有工作，这对于机器人极其复杂的高维连续动作序列（Action Chunks）来说太吃力了。

所以提出将 VAE 的“单一隐变量”纵向拉长，演化为**层级马尔可夫隐变量模型（HMLV）** 并将其特殊化 (固定后验) 作为 DMs

##### Definition

***DMs are a particular instantiation of HMLV models for which the posterior is fixed***

引入了多个 latent variables $z_{0} \dots z_{T}$ 其中, 马尔可夫性让 latent variable 是仅仅和前面一项的状态有关系

DMs 也就是用**多步**的 variational inference 来 approximating the generative process

![[robot-learning-4cd8f1b730e6.jpg]]

DMs 把这个 VAE 一步还原 $p(o,a)$ 的过程 扩展为 $T$ 个 $z$ 一步一步边缘化得到 $p(o,a)$

$$
p \left(\underbrace {o , a} _ {= z _ {0}}\right) = \int* {\operatorname {s u p p} \left(Z _ {0}\right)} \int_ {\operatorname {s u p p} \left(Z _ {1}\right)} \dots \int_ {\operatorname {s u p p} \left(Z _ {T}\right)} p \left(z _ {0}, z _ {1}, \dots z _ {T}\right) \tag {30}
$$

$$
p \left(z _ {0}, z _ {1}, \dots z _ {T}\right) = p \left(z _ {T}\right) \prod_ {t = 1} ^ {T} p \left(z _ {t - 1} \mid z _ {t}\right), \tag {31}
$$

$p \left(z _ {0}, z _ {1}, \dots z _ {T}\right)$ 是根据联概率分布的条件概率公式 $p(\boldsymbol{x},\boldsymbol{y})=p(\boldsymbol{y}\mid\boldsymbol{x})p(\boldsymbol{x})$ 和 Markov property(消除了不相关的联合分布) 得到

* $z_{0}=(o,a)$ 是 无噪声的观测数据
* $z_t$ 是第 $t$ 步的隐变量

扩散模型的前向加噪过程本质是一个马尔可夫链，但借助高斯分布的叠加性质（重参数化技巧），我们跳过了中间所有的迭代步骤，用一个闭式解直接从无噪声的起点瞬间 " 穿越 " 到任意时刻 $t$ 的加噪状态

$$
q(z_t|z_0) = \mathcal{N}(\sqrt{\bar{\alpha}*t}z_0, (1-\bar{\alpha}*t)\mathbf{I})
$$

$$
z_t = \sqrt{\bar{\alpha}*t}z_0 + \sqrt{1-\bar{\alpha}*t}\epsilon
$$

##### 与 VAE 的比较

比如对于 $t$ 比较大的时候, 模型去噪实际上是在**做高层规划的任务**, 当 $t$ 接近 $0$ 的时候,是在**做精细的调整**, 这种由粗到细的调整, 就是不同层级的

虽然 DMs 也是类似 VAE 从简单的分布比如高斯分布采样,然后**还原**相对 $o,a$ 高似然的潜在分布 $p(o,a)$, 但是 VAE 的 $p(z)$ 本身是基于 encoder 构建的, 所以蕴含了 $o,a$ 相关的信息, 并且还原靠 decoder 就行了

* 但是 DMs 去噪的过程从 $z_{T}$ 出发本身, 因此不带 $o,a$, 是纯噪声, 所以有没有 $o,a$ 信息相关的起点.
* 那还原 $p(o,a)$ 分布的能力从何而来? 体现在 $p_{\theta}$ 的参数权重, **去噪的过程本身就编码了 $p(o,a)$ 的全部信息**

##### Loss

$$
\mathcal {L} (\theta) = \mathbb {E} _ {t, z _ {0}, \epsilon} \left[ \left\| \epsilon - \epsilon* {\theta} \left(\sqrt {\bar {\alpha} _ {t}} z _ {0} + \epsilon \sqrt {1 - \bar {\alpha} _ {t}}, t\right) \right\| ^ {2} \right] \tag {44}
$$

**【符号拆解】**：
* $t \sim \mathcal{U}(\{1, \dots, T\})$：从 $1$ 到 $T$ 中均匀随机抽取的一个时间步。
* $z_0 \sim \mathcal{D}$：从离线的人类示范数据集 $\mathcal{D}$ 中抽取的一个真实动作片段。
* $\epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$：我们故意生成的一个完美的标准高斯噪声。
* $\underbrace{\sqrt {\bar {\alpha} _ {t}} z _ {0} + \epsilon \sqrt {1 - \bar {\alpha} _ {t}}}_{= z_t}$：重参数化后的加噪公式。它的物理意义是：**时刻 $t$ 时，被破坏的模糊动作 $z_t$**。
* $\epsilon_\theta(\cdot, t)$：**我们的核心深度神经网络（如 U-Net 或 Transformer）**。输入模糊动作 $z_t$ 和时间 $t$，输出它猜测的噪声。
* $\| \epsilon - \epsilon_\theta \|^2$：均方误差（MSE Loss）。强迫神经网络去预测刚刚加进去的真实噪声 $\epsilon$。

损失函数引导模型学会 预测噪声, 这样才能用来去噪

逆向推理过程 (Denoising / Inference)

在机器人的实际部署阶段，我们从纯噪声 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 开始，利用训练好的网络 $\epsilon_\theta$ 迭代去噪，生成动作（公式 45）：

$$
z _ {t - 1} = \frac {1}{\sqrt {\alpha* {t}}} \left(z _ {t} - \frac {\beta* {t}}{\sqrt {1 - \bar {\alpha} _ {t}}} \epsilon* {\theta} (z _ {t}, t)\right) + \sigma_ {t} \epsilon \tag {45}
$$

**【符号拆解】**：
* $z_{t-1}$：比 $z_t$ 稍微干净一点点的动作轨迹。
* $\frac {\beta_ {t}}{\sqrt {1 - \bar {\alpha} _ {t}}} \epsilon_ {\theta} (z _ {t}, t)$：网络预测出的、在这一步应该被减去的“噪声残差”。
* $\sigma_t \epsilon$：**Langevin 动力学注入的随机噪声**。在去噪时再加一点点小噪声，防止模型陷入局部最优，保持生成动作的多样性。

想象一滴墨水（完美的专家动作）滴入清水中。前向加噪过程就是墨水分子的**布朗运动**，随着时间 $t$ 推进，墨水不断扩散，直到整杯水变成均匀的灰色（纯高斯噪声）。此时，关于原始动作的所有信息（Information）都消散了。

而我们的神经网络 $\epsilon_\theta$，就像是一个“时光倒流引擎”，它学会了看懂一杯灰水中的微小分子运动趋势，一帧一帧地把墨水重新聚合成最开始的那一滴。

相比于后面的 flow matching 去噪推理过程,直观上, 把布朗运动给逆过来, 效率听起来就是很低的

##### 几何直觉

![[robot-learning-1c611f2c815a.png]]

* left 是 观测的图像和 6dof 的电机角度位置, 某一帧, $t=1000$ 几乎都是噪音
* mid 是 q2 电机编码器读得 $o$ 还有 摇操臂发送的 $a$ 某个数据集 $\mathcal{D}$ 的联合概率密度分布图
	* 坐标轴显示都归一化到 $[-1,1]$ 亮度代表概率密度, 某处比较亮代表某个角度对在数据集里面出现比较多
	* 由于摇操命令和电机实际执行几乎是同步的, 所以图上表示概率密度的区域是一条类似 $y=x$ 的直线
	* $t=1000$ 时候, 呈现类似高斯分布
* right 是得分场 是 $z_{t}$ 的对数概率密度的梯度向量场
	* 中间的线条就是 数据流形
	* 模型学会的就是这个**score field**— 学好之后推理时就靠它走回流形

1. 机器人的合法动作在整个高维空间中只占极其微小的一条线或一个面（图 25 中的对角线 $a \simeq o$）。这被称为流形。
2. 加噪操作本质上是把数据点从安全的流形上“推开”，扔进了无意义的混乱空间。
3. 网络预测的“噪声” $\epsilon_\theta$，在数学上等价于对数概率密度的梯度（Score function, $\nabla_{z_t} \log p(z_t)$）。它的物理意义就是**向量场（Vector Field）中的箭头**（见图 24 右侧）。这些箭头永远指向数据密度最高的地方（即流形）。
4. 所谓的“迭代去噪”，其实就是小船（噪声向量）顺着网络预测的得分场（风向箭头），一步步**欧几里得投影（Euclidean projection）** 回安全的数据流形（合法的动作空间）的过程。

#### Flow Matching

DMs 工程上性能很差, 为了从目标分布中恢复一个样本，通常需要执行大量的迭代计算

具体来说 DMs 的加噪, 去噪过程是类比正逆向布朗运动, 这个过程是离散 ($t \sim \mathcal{U}(\{1, \dots, T\})$), 随机采样高斯分布的的 $z_{t}$, 每一步的去噪都是再预测一个 高斯噪声

> 在特定的高斯分布间进行概率的离散跳跃。

所以 引入流匹配 flow matching ，用**确定性**的、**连续**的常微分方程（ODE）完全泛化并替代**离散的扩散马尔可夫链**

##### Definition

flow-matching 建立在

1. 向量场 vector fields $v(t, z)$
2. 轨迹函数 $\psi(z, t)$
3. 常微分方程 OED $\frac{d}{dt} \psi(z_0, t) = v(t, \psi(z_0, t))$
4. 流 flow $\psi: \lfloor 0, 1 \rfloor \times Z \mapsto Z$
5. 条件流匹配 Conditional flow matching
	1. 最优传输 Optimal Transport 路径 $\psi(t, z_0)= z _ { t } = ( 1 - t ) z _ { 0 } + t z _ { 1 }$
	2. 条件目标向量场 $u(t, z_t) = z_1 - z_0$
这些数学工具上面

###### 向量场

 向量场 vector fields[^3]

> 这里都默认为速度场

* $v(t, z)$

在二维速度场中，坐标 $z=(x, y)$。向量场函数接收时间 $t$ 和坐标 $(x, y)$，吐出一个二维的速度向量（包含横向速度和纵向速度）：

$$
v(t, x, y) = \begin{pmatrix} v_x(t, x, y) \\ v_y(t, x, y) \end{pmatrix}
$$

直观上看，向量场中的“箭头”大小方向随时间变化而不是固定的

向量场本质上是一个查表公式：你告诉我现在的坐标 $(x,y)$ 和当前的时间 $t$，我立刻吐出一个瞬时受力/速度大小的向量

在 Flow Matching (FM) 的上下文中，向量场驱动的不是单一物理粒子，而是整个**概率质量 (Probability mass)** 的输运

向量场定义了如何将一个容易采样的简单先验分布（如标准高斯分布）的**概率密度**，在连续时间区间内，平滑且确定性地 " 搬运 " 并**塑造成复杂的未知数据分布**

###### 轨迹函数

粒子在向量场中的轨迹如何?

$\psi(z, t)$ 定义为 向量场 $v(t,z)$ 的 轨迹函数

给定任意时间 $t$ 和位置 $z$，带入进去就算出一个具体的坐标点

###### 常微分方程 (ODE)

把轨迹函数和向量场联系起来就是 ODE

$$
\frac{d}{dt} \psi(z_0, t) = v(t, \psi(z_0, t))
$$

* 等号左边 $\frac{d}{dt} \psi(z_0, t)$：对轨迹（位置函数）求时间的导数。位置的导数就是**粒子自身的实际瞬时速度**
* 等号右边 $v(t, \psi(z_0, t))$：
	* 内层 $\psi(z_0, t)$：粒子此时此刻在空间中的实际坐标。
	* 外层 $v(t, \dots)$：拿着粒子当前的坐标，去向向量场系统“查表”。所以这一项是**向量场在粒子当前位置规定的理论瞬时速度**。

###### Flow

FM 旨在学习一个确定性、连续且可微的流 (Flow) $\psi: \lfloor 0, 1 \rfloor \times Z \mapsto Z$，完全由一个常微分方程 (ODE) 表征：

$$
 \frac{d}{dt} \psi(z, t) = v(t, \psi(t, z))
$$

$$
 \psi(0, z) = z
$$

* $t \in [0, 1]$：**连续变化**的时间标量，$t=0$ 代表初始噪声状态，$t=1$ 代表最终生成的数据状态。
* $z$：状态空间变量，代表概率分布支持域上的**样本点**
* $v(t, \cdot)$: 神经网络需要去近似的真实的未知的向量场 $u(t,\cdot)$(underlying vector field)
* $\psi(t, z)$: 确定性、连续且可微的流 (flow) 或轨迹，表示初始状态 $z$ 在时间 $t$ 沿向量场移动后的绝对坐标,将**样本**从先验分布 $p_0$ 迁移到未知数据分布 $p_1$。

###### Conditional Flow Matching

DMs 的噪声预测器 $\epsilon_\theta$ 实际学习到的条件目标向量场实际上是一个**被高斯衰减系数 $\alpha(t)$ 严重非线性扭曲的向量场**

* **概率路径 (Probability Path)**：当无数个样本都顺着各自的轨迹移动时，**所有样本构成的宏观概率密度的变化过程**，就是概率路径

因此从概率路径的视角来看 DMs 在做随机游走, 所以 $v(t, \cdot)$ 可以被限制,让 $\psi(z, t)$ 是直线的

这就是 Optimal Transport Flow Matching (OT-CFM)

轨迹路径被约束为 $z _ { t } = ( 1 - t ) z _ { 0 } + t z _ { 1 }$

* $z_0$: 轨迹起点坐标，由先验分布（纯噪声）采样得出, 这里没有像 DMs 被约束为高斯分布
* $z_1$: 轨迹终点坐标，由目标数据分布（真实图像 / 动作）采样得出。
* $t \in [0, 1]$: 连续推进的时间标量。
* $z_t$: 在任意 $t$ 时刻，状态空间中的确切中间坐标。

> 这是轨迹方程的缩写 $\psi(t, z_0)= z _ { t }$ , 这也就是线性插值, 随着 $t$ 改变在一条线上面的位置

对 $t$ 求导自然可得, 最优传输路径约束后的向量场

$$
u ( t , z _ { t } ) = z _ { 1 } - z _ { 0 }
$$

只要起点 $z_0$ 和终点 $z_1$ 这对锚点被固定下来，由它们定义的这个**条件向量场**就是一个全局的常数:

* **方向**：从起点 $z_{0}$ 指向 $z_1$
* **大小（距离的模长）**：因为必须在 $t=0$ 到 $t=1$ 这个标准单位时间内走完全程，所以速度的绝对大小必须精确等于两点之间的总距离。距离越远，初始赋予的恒定流速就越大

> 保留 $t$ 变量是因为接口一致性吧

##### Loss

给定数据分布和简单的先验分布，使用线性插值定义样本间的简单路径 $z_t = (1-t)z_0 + t z_1$，CFM 模型的回归目标定义为：

$$
 \mathcal{L}(\theta) = \mathbb{E}*{t, z_0, z_1} \left[ \| v*\theta((1-t)z_0 + t z_1, t) - (z_1 - z_0) \|^2 \right]
$$

* $t \sim \mathcal{U}([0, 1])$：从 $[0,1]$ 连续均匀分布采样 (Continuous Uniform Sampling)
* $z_0 \sim p_0(\bullet)$：从易于采样的先验分布（如标准高斯分布）中采样的起点。
* $z_1 \sim p_1(\bullet)$：从真实数据分布中采样的终点。
* $(1-t)z_0 + t z_1$：定义在 $z_0$ 和 $z_1$ 之间的线性插值，表示时刻 $t$ 的状态 $z_t$。
* $v_\theta(\cdot, t)$：学习向量场的神经网络回归器。
* $(z_1 - z_0)$：真实的目标向量场 $u(t, z_t)$

这里理论上是 $v_\theta(\cdot, t)$ 学会了 Optimal Transport 最优传输路径下将 先验分布 $p_{0}$ 转移到真实数据分布 $p_{1}$ 的向量场

> 工程上一次 优化 step 就是一次 蒙特卡洛近似, 完整的训练是通过 完整的蒙特卡洛近似理论期望值

推理的时候就是生成样本, 在实践中等价于求解常微分方程

* 从 $z_0 \sim p_0$ 启动，在 $t \in [0, 1]$ 过程下, 对 $\frac{dz}{dt} = v_\theta(z_t, t)$ 进行数值积分
* 常使用标准的 ODE 求解器（如前向欧拉法 Forward-Euler），在数十个 (tens of) 去噪步数内迭代更新得到对真实采样的 $z_1 \sim p_1(\bullet)$ 近似

##### 几何直觉

###### 向量场

![[robot-learning-cf6d137c5919.jpg]]

概率密度分布在各自**非时变场 (Time-invariant)** 向量场随时间 $t=0\to t=1$ 变化

> time invariant 向量场的规则不随时间变化

* $u _ { 1 } ( x , y ) = ( x , 0 )$ 水平拉伸
* $u _ { 2 } ( x , y ) = ( x / \sqrt { 2 } , y / \sqrt { 2 } ) )$

flow-matching 的上下文, 向量场就是对 概率密度分布的重塑

![Site Unreachable](https://x.com/i/status/2041506844783612094)

flow-matching **没有直接**去还原这个 人类示范数据的的潜在分布 $p(o,a)$ 而是学习了向量场, 怎么把一个简单的先验分布 迁移到了 潜在目标分布 $p(o,a)$

#### ACT

建立在 VAE 的基础上, 是条件概率分布, 而不是直接用 $o,a$ 的联合分布 变成了 CVAE

在线连续预测中, 生成模型 (GMs) 仍然存在严重的误差积累问题, 受人类规划一连串动作而非单一动作的启发, ACT 把生成一个动作扩展为**一个动作序列 action chunk**$a_{t:t+k}$

##### Definition










[^1]: [Manifold hypothesis - Wikipedia](https://en.wikipedia.org/wiki/Manifold_hypothesis)
[^2]: [Variational autoencoder - Wikipedia](https://en.wikipedia.org/wiki/Variational_autoencoder)
[^3]: [Vector field - Wikipedia](https://en.wikipedia.org/wiki/Vector_field)

[^concept-mdp]: 概念详见 `30_wiki/MDP`（暂未发布为博客文章）。
