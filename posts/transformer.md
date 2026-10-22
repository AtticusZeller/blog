---
title: Transformer：从注意力到 ViT
date: '2026-10-22'
draft: false
tags:
- transformer
- attention
- deep-learning
- vit
categories:
- learning-notes
summary: 从 attention pooling、缩放点积与多头注意力出发，梳理 Transformer 的编码器-解码器结构、位置编码与 ViT，并记录它在机器人学习中的用法。
math: true
showtoc: true
tocopen: true
---

# Transformer


## Attention Pooling

![qkv](/images/transformer-8394449e7ce2.svg)

> [^1] The attention mechanism computes a **linear combination** over values $\boldsymbol{v}_{i}$ via **attention pooling**, where weights are derived according to the compatibility between a query $\boldsymbol{q}$ and keys $\boldsymbol{k}_{i}$.

attention pooling 输出的**attention output vector**，它是所有 $\boldsymbol{v}_{i}$ 向量的加权汇聚结果,**也叫 attended representation**

score → softmax → weight → weighted sum

查询对象 定义为 $D \overset{\mathrm{def}}{=}\{(\mathbf{k}_1,\mathbf{v}_1),\ldots,(\mathbf{k}_m,\mathbf{v}_m)\}$ 得到的定义:

$$
\operatorname{Attention}(\mathbf{q},D)
\overset{\mathrm{def}}{=}
\sum_{i=1}^{m}
\alpha(\mathbf{q},\mathbf{k}_i)\mathbf{v}_i
$$

## Attention Weight

前面的图 是 attention pooling 的过程, 输出是 对 $\boldsymbol{v}$ 的线性组合,而且是凸组合, 计算过程是 depend 这个 attention weight 怎么计算 ?

![attention-output](/images/transformer-b688f2891b59.svg)

1. 先要算 attention score, 这里采用 dot product 来衡量 $\boldsymbol{q}$ 和 $\boldsymbol{k}_{i}$ 的相似度, 除 $\sqrt{ d }$ 是为了让 $s_{i}$ 的典型大小随维度 $d$ 增长的问题

只不过这里 假设了 $\mathbf{q}\in\mathbb{R}^{d},\mathbf{k}_i\in\mathbb{R}^{d}$, 所有元素都是独立同分布的随机变量，均值为零，方差为一。两个向量之间的点积均值为零，方差为 $d$

> 如果把 dot product 看成随机变量 $X$, 减去均值除上 标准差来做标准化 ,这里就是 除根号 d

$$
a(\mathbf{q},\mathbf{k}_i)
=
\frac{\mathbf{q}^{\top}\mathbf{k}_i}{\sqrt{d}}
$$

[^2]

如果不消除维度 $d$ 带来的影响,方差大了会导致后面 一些列问题 比如 softmax 退化成 one-hot 的情况不利于参数学习

2. 套 softmax 算 attention weight
对权重计算函数 $\alpha$ 需要满足 凸组合 ( convex combination) 的性质:
每个 $\boldsymbol{v}_{i}$ 乘上的权重系数之和 $=1$ 且每项权重 $\alpha_{i}\geq{0}$

$$
\sum_{i=1}^{m}
\alpha(\mathbf{q},\mathbf{k}_i)=1,
\qquad
\alpha(\mathbf{q},\mathbf{k}_i)\ge 0
$$

因此要套一层 *softmax* 得到 attention weight 的函数:

$$
\alpha(\mathbf{q},\mathbf{k}_i)
=
\operatorname{softmax}\!\left(a(\mathbf{q},\mathbf{k}_i)\right)
=
\frac{
\exp\!\left(\mathbf{q}^{\top}\mathbf{k}_i/\sqrt{d}\right)
}{
\sum_{j=1}^{n}
\exp\!\left(\mathbf{q}^{\top}\mathbf{k}_j/\sqrt{d}\right)
}
$$

[^1]

> exp 就是指数函数 $e^{x}$

## Scaled Dot Product Attention

这是相对前面的单次 attention pool 的过程

前面定义 $\alpha(\mathbf{q},\mathbf{k}_i)$ 是一次 查询 $q$ 对 一个 $\boldsymbol{k}_{i}$ 算 一项 attention weight $\alpha_{i}$ 算 $m$ 次得到 attention output

实践中有时需要对 $\boldsymbol{q},\boldsymbol{k}_{i}$ 进行批量计算, 比如同时算 $n$ 次 attention pooling 即

* 同时计算 $n$ 个查询和 $m$ 个 $\boldsymbol{k}_{i},\boldsymbol{v}_{i}$ 对的 attention

所以给出矩阵形式的定义

$$
\mathbf{Q}\in\mathbb{R}^{n\times d},
\qquad
\mathbf{K}\in\mathbb{R}^{m\times d},
\qquad
\mathbf{V}\in\mathbb{R}^{m\times v}
\qquad
\boldsymbol{S} \in \mathbb{R}^{n\times m}
$$

$$
\boldsymbol{S} = \frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}
$$

计算时间复杂度是 $O(mnd)$ 理解为最终产出 $mn$ 个元素,并且每个元素的产生有 $d$ 项加起来得到的

$$
\operatorname{softmax}\!\left(
\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}
\right)
\mathbf{V}
\in
\mathbb{R}^{n\times v}
$$

在实际计算中加入 batch 维度

| 张量        | PyTorch shape | 含义                      |
| --------- | ------------- | ----------------------- |
| `queries` | $(B,n,d)$    | B 个 $n\times d$ 的 $Q$ |
| `keys`    | $(B,m,d)$    | B 个 $m\times d$ 的 $K$|
| `values`  | $(B,m,v)$    | B 个 $m\times v$ 的 $V$ |

`bmm` 是批量矩阵乘法

算 attention score

shape= (b,n,m)

> [!example]- 代码：计算 attention score
>
> ```python
> scores = torch.bmm(
>     queries,
>     keys.transpose(1, 2) # 交换 axis 1,2 方便匹配 矩阵运算
> ) / math.sqrt(d)
> ```

算 最终的 attention

> [!example]- 代码：计算最终的 attention
>
> ```python
> torch.bmm(attention_weights, values)
> ```

### Masked Softmax Operation

本质上是 Attention 本身是要算一组

$$
\mathbf S=[s_{ij}]_{n\times m},
\qquad
s_{ij}=a(\mathbf q_i,\mathbf k_j)
$$

表示所有 query 与 key 之间的匹配程度, 但有些 query-key 位置按照**任务规则**不允许被关注


$$
\widetilde{\mathbf S}_{ij}
=
\begin{cases}
\mathbf S_{ij}, & M_{ij}=1\quad (\mathbf q_i\text{ 可以关注 }\mathbf k_j),\\
-\infty, & M_{ij}=0\quad (\mathbf q_i\text{ 不允许关注 }\mathbf k_j),
\end{cases}
\qquad
\mathbf M\in\{0,1\}^{n\times m}
$$

实现思路就是送入 softmax 操作之前被 set 成 $-\infty$ 最终输出的 attention weight 自然变成 $0$

> [!example]- 代码：Masked Softmax
>
> ```python
> # 布尔 mask
> scores = scores.masked_fill(~keep_mask, float("-inf")) # shape=(b,m,n)
> weights = torch.softmax(scores, dim=-1)
> ```

常见的 mask 类型有

1. Padding Mask 比如一个 batch 里面 有一些 序列长度不一样,是占位符, 屏蔽补齐的 `<pad>` token, 这些位置就应该被 屏蔽
2. Causal Mask 当前位置不能看到未来 token。通常是一个下三角矩阵, 用于 GPT 等自回归模型。

## Additive Attention

这是相对于 scaled dot product 的 attention score 方法, 适用于 $\mathbf{q}\in\mathbb{R}^{q},\mathbf{k}\in\mathbb{R}^{k}$ 维度不匹配不能 dot product 的时候

$$
a(\mathbf{q},\mathbf{k})
=
\mathbf{w}_v^{\top}
\operatorname{tanh}\!\left(
\mathbf{W}_q\mathbf{q}
+
\mathbf{W}_k\mathbf{k}
\right)
\in
\mathbb{R}
$$

* 本质上是将 $\boldsymbol{q}$ 和 $\boldsymbol{k}$ 拼接起来，并输入到具有单个隐藏层的 MLP 中
其中 $\mathbf{W}_q\in\mathbb{R}^{h\times q}, \mathbf{W}_k\in\mathbb{R}^{h\times k}, \mathbf{w}_v\in\mathbb{R}^{h}$

```text
q ──W_q──┐
          ├─ 相加 ─ tanh ─ w_v ─ score
k ──W_k──┘
```

也就是 $\mathbf x= \begin{bmatrix} \mathbf q\\ \mathbf k_i \end{bmatrix} \in\mathbb R^{d_q+d_k}$

再使用普通 MLP：

$$
\mathbf h_i = \tanh \left( \underbrace{ \begin{bmatrix} \mathbf W_q&\mathbf W_k \end{bmatrix} }_{h\times(d_q+d_k)} \begin{bmatrix} \mathbf q\\ \mathbf k_i \end{bmatrix} \right)
$$

$$
s_i = \underbrace{\mathbf w_v^\top}_{1\times h} \mathbf h_i
$$

层宽可以写成：

$$
 (d_q+d_k)\rightarrow h\rightarrow1 
$$

> `tanh` 是激活函数它把任意实数压缩到 $(-1,1)$[nn](../nn-basics/)

## Multi-Head Attention

[^3]

在实践中，对于**同一组查询、键和值**，我们可能希望模型能够融合来自同一注意力机制不同行为的知识，例如捕捉序列中不同范围（例如，短范围与长范围）之间的依赖关系

![multi-head-attention](/images/transformer-28cd949c5c8c.svg)

> FC 是全连接层

假设共有 $n$ 个查询、$m$ 个 key-value 对：

$$
\mathbf{Q}\in\mathbb{R}^{n\times d_q},
\qquad
\mathbf{K}\in\mathbb{R}^{m\times d_k},
\qquad
\mathbf{V}\in\mathbb{R}^{m\times d_v}
$$

第 $i$ 个头的投影矩阵 (统一到 $d_{h}$ 维度)

> Transformer 通常设置：$d_h=\frac{d_{\mathrm{model}}}{h}$ 并且 $\boxed{d_q=d_k=d_v=d_o=d_{\mathrm{model}}=h\,d_h}$ 输入与最终输出的模型维度保持不变，便于后续执行残差连接
> PyTorch 的 `MultiheadAttention` 默认 $d_q=d_k=d_v$

对于第 $i$ 个注意力头，其中 $i=1,\ldots,h$，定义：

$$
\mathbf{W}_i^Q\in\mathbb{R}^{d_q\times d_h},
\qquad
\mathbf{W}_i^K\in\mathbb{R}^{d_k\times d_h},
\qquad
\mathbf{W}_i^V\in\mathbb{R}^{d_v\times d_h}
$$

第 $i$ 个头的 $Q/K/V$ 表示

同一组原始 $\mathbf Q,\mathbf K,\mathbf V$ 经过第 $i$ 套投影矩阵：

$$
\mathbf{Q}_i
=
\mathbf{Q}\mathbf{W}_i^Q
\in\mathbb{R}^{n\times d_h},
\qquad
\mathbf{K}_i
=
\mathbf{K}\mathbf{W}_i^K
\in\mathbb{R}^{m\times d_h},
\qquad
\mathbf{V}_i
=
\mathbf{V}\mathbf{W}_i^V
\in\mathbb{R}^{m\times d_h}
$$

第 $i$ 个头的 attention 表示

$$
\operatorname{head}_i = \operatorname{Attention} (QW_i^Q,KW_i^K,VW_i^V) \in\mathbb{R}^{n\times d_h}
$$

多头拼接

将 $h$ 个头沿特征维度拼接：

$$
\mathbf{H}
=
\operatorname{Concat}
\left(
\operatorname{head}_1,\ldots,\operatorname{head}_h
\right)
\in\mathbb{R}^{n\times hd_h}
$$

定义输出投影矩阵

$$
\mathbf{W}^O\in\mathbb{R}^{hd_h\times d_o}
$$

多头注意力的最终输出为：

$$
\operatorname{MultiHead}(\mathbf{Q},\mathbf{K},\mathbf{V})
=
\operatorname{Concat}
\left(
\operatorname{head}_1,\ldots,\operatorname{head}_h
\right)
\mathbf{W}^O
\in\mathbb{R}^{n\times d_o}
$$

### Self-Attention and Cross-Attention

二者使用相同的多头注意力计算，区别在于输入来源：

* **Self-attention**：query、key、value 的输入都来自同一个序列 `x`。
* **Cross-attention**：query 来自当前序列，key、value 来自另一个序列 `memory`。

> [!example]- 代码：Self-Attention 与 Cross-Attention
>
> ```python
> import torch
> from torch import nn
>
> # B=2：两个样本
> # L=4：query 序列长度
> # S=6：memory 序列长度
> # E=8：每个位置的特征维度
> B, L, S, E = 2, 4, 6, 8
>
> x = torch.randn(B, L, E)
> memory = torch.randn(B, S, E)
>
> attention = nn.MultiheadAttention(
>     embed_dim=E,      # 输入、输出特征维度
>     num_heads=2,      # 两个注意力头
>     batch_first=True  # (batch, sequence, feature)
> )
>
> # Self-attention：
> # query、key、value 都来自同一个输入 x
> self_output, self_weights = attention(
>     query=x,
>     key=x,
>     value=x,
>     need_weights=True,
>     average_attn_weights=False
> )
>
> print("Self-attention")
> print(self_output.shape)   # torch.Size([2, 4, 8])
> print(self_weights.shape)  # torch.Size([2, 2, 4, 4]) 
> # `self_weights[b, h, i, j]` 对 第h个head中第i次q对同一个j的权重
>
> # Cross-attention：
> # query 来自 x，key、value 来自另一个输入 memory
> cross_output, cross_weights = attention(
>     query=x,
>     key=memory,
>     value=memory,
>     need_weights=True,
>     average_attn_weights=False
> )
>
> print("Cross-attention")
> print(cross_output.shape)   # torch.Size([2, 4, 8])
> print(cross_weights.shape)  # torch.Size([2, 2, 4, 6])
> ```

其中

$$
\text{head output}=\text{self\_weights}\times V_{heads}
$$

> [!example]- 代码：各个 head 的输出
>
> ```python
> # weights: (B, H, L, S)
> # V_heads: (B, H, S, d_h)
>
> head_output = torch.matmul(weights, V_heads)
> # shape: (B, H, L, d_h)
> ```

[^3]

## Positional Encoding

![cnn-rnn-self-attention](/images/transformer-17e926522ec5.svg)

* self-attention 的计算复杂度 $O(n^2d)$ 来自 Attention 的两次核心矩阵乘法
* $O(1)$ 路径表示一层即可让任意位置直接交互

裸自注意力只根据 token 内容计算彼此关系，对输入顺序具有置换等变性

`nn.MultiheadAttention` 和 `nn.TransformerEncoderLayer` 本身不注入位置信息，使用者需要在模型结构中另外处理。

经典实现方式是:

$\text{固定正余弦绝对位置编码：}\quad src=X+P$

假设输入表示 $\mathbf{X}\in\mathbb{R}^{n\times d}$ 包含序列符号的  $dn$- 维嵌入。位置编码 $\mathbf{X}+\mathbf{P},$ 使用  $\mathbf{P}\in\mathbb{R}^{n\times d}$ 相同形状的位置嵌入矩阵输出，其在 $i^{th}$ 行和 $(2j)^{th}$ 或 $(2j+1)^{th}$  列上的元素为

$$
\begin{split}\begin{aligned} p_{i, 2j} &= \sin\left(\frac{i}{10000^{2j/d}}\right),\\p_{i, 2j+1} &= \cos\left(\frac{i}{10000^{2j/d}}\right).\end{aligned}\end{split}
$$

只在最开始送入 encoder`TransformerEncoderLayer`(或者 decoder) 堆叠或者 `MultiheadAttention` 的时候编码位置信息

* [?] 现代 Transformer 还可能使用可学习位置嵌入、RoPE、相对位置偏置、ALiBi 等，具体原理等实际遇到再补充即可。

## The Transformer Architecture

![transformer](/images/transformer-da7f1eaec4b1.svg)

Transformer 先用 Attention 根据 $QK$ 相关性对 $V$ 加权聚合，让每个 token 获得上下文信息；再让所有 token 共用同一个 FFN，对各自的上下文化表示进行非线性特征提炼。两部分都在最终损失函数监督下通过反向传播共同学习。

在 Transformer 中，对于序列任一位置的任意输入 $\mathbf{x} \in \mathbb{R}^d$  ，我们都要求 $\textrm{sublayer}(\mathbf{x}) \in \mathbb{R}^d$，  以确保残差连接 $\mathbf{x} + \textrm{sublayer}(\mathbf{x}) \in \mathbb{R}^d$  是可行的

> 回看到 multi-head attention, 每个 head 的 input, QKV 的维度是 $d_{h}=\frac{d}{h}$

### FFN

注意 被多个向量 $\boldsymbol{x}$ 共享的 mlp, `nn.linear` 只变换最后一维，前面的维度全部自动保留并批量处理

> [!example]- 代码：Position-wise FFN
>
> ```python
> def make_ffn(d_model: int, d_ff: int, dropout: float) -> nn.Sequential:
>     """The position-wise FFN is just the same MLP applied to every token."""
>     return nn.Sequential(
>         nn.Linear(d_model, d_ff),
>         nn.ReLU(),
>         nn.Dropout(dropout),
>         nn.Linear(d_ff, d_model),
>     )
> ```

### Add & Norm

残差连接在这里体现为 Add & Norm 中 Add 的操作, residual connection 比较紧贴 功能模块比如 FFN 和 multi-head attention 的裸露输出

`Y` 这里可能是 `attn_out` 或者 `ffn_out`

> [!example]- 代码：Add & Norm
>
> ```python
> class AddNorm(nn.Module):  #@save
>     """The residual connection followed by layer normalization."""
>     def __init__(self, norm_shape, dropout):
>         super().__init__()
>         self.dropout = nn.Dropout(dropout)
>         self.ln = nn.LayerNorm(norm_shape)
>     def forward(self, X, Y):
>         return self.ln(self.dropout(Y) + X)
> ```

### Encoder

单一的 encoder 里面两个 sublayer, self_att 和 ffn, 并且两个子层之间采用 residual connection 和 layernorm

> [!example]- 代码：Encoder Block
>
> ```python
>
> class EncoderBlock(nn.Module):
>     """Original Transformer encoder block (post-norm, matching D2L)."""
>
>     def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float):
>         super().__init__()
>         self.self_attn = nn.MultiheadAttention(
>             d_model, num_heads, dropout=dropout, batch_first=True
>         )
>         self.ffn = make_ffn(d_model, d_ff, dropout)
>         self.norm1 = nn.LayerNorm(d_model)
>         self.norm2 = nn.LayerNorm(d_model)
>         self.dropout1 = nn.Dropout(dropout)
>         self.dropout2 = nn.Dropout(dropout)
>     def forward(
>         self, x: torch.Tensor, src_padding_mask: torch.Tensor | None = None
>     ) -> torch.Tensor:
>         attn_out, _ = self.self_attn(
>             x,
>             x,
>             x,
>             key_padding_mask=src_padding_mask,
>             need_weights=False,
>         )
>         x = self.norm1(x + self.dropout1(attn_out))
>         x = self.norm2(x + self.dropout2(self.ffn(x)))
>         return x
> ```

encoder 中两层 sublayer 都没有改变其输入的形状。

### Decoder

decoder 有 3 个 sublayer `Masked self-attention + encoder-decoder cross-attention + FFN.`

encoder 最终输出整条源序列的上下文化表示，一般记作 `memory`。它不是压缩成单个向量的 context，而是由每个源 token 对应的 contextualized hidden state 组成的序列，batch 形式的 shape 通常是 $(B,S,d_{\mathrm{model}})$。

#### Masked Self-attention

这个 mask 就是 causal mask 因果 mask

causal mask = 用矩阵并行实现“每个位置只能根据过去预测下一个 token

mask 本质就是让串行的把它扩展成了矩阵形式一次性计算所以如果再考虑 mask 应该长什么样，你就要去思考，你想一次性算什么相当于从上到下，你一次性就算完了一个连续过程。这个连续过程中，每一次计算，你希望谁能看到谁，谁不能看到谁，这个就是对 mask 的设计思路

#### Encoder-decoder Cross-attention

Transformer 的经典应用背景之一是机器翻译。例如，源句 `I love apples` 经过 tokenization、embedding 和 positional encoding 后进入 encoder；encoder 内部的 self-attention 让每个源 token 按需聚合其他源 token 的信息，输出源序列的上下文化表示 (contextualized representations)`memory`。

> 这个 encoders 最终输出的 `memory` 被每一层的 decoder 共享做 cross-attention

decoder 根据已经给出的目标端 token 和源句 `memory` 预测目标语言中的下一个 token。训练时输入右移后的目标序列，通过 causal mask 并行计算各位置的 next-token prediction；推理时才逐 token 自回归生成，直到输出 `<eos>`。

在 encoder-decoder cross-attention 中，query 的输入来自 masked self-attention 子层之后的 decoder hidden states；key 和 value 的输入来自 encoder `memory`。

cross-attention 的作用更准确地说是：让每个目标位置根据当前 decoder state，从源序列 `memory` 中检索并聚合与当前预测相关的信息。

> [!example]- 代码：Decoder Block
>
> ```python
>
> class DecoderBlock(nn.Module):
>     """Masked self-attention + encoder-decoder cross-attention + FFN."""
>
>     def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float):
>         super().__init__()
>         self.self_attn = nn.MultiheadAttention(
>             d_model, num_heads, dropout=dropout, batch_first=True
>         )
>         self.cross_attn = nn.MultiheadAttention(
>             d_model, num_heads, dropout=dropout, batch_first=True
>         )
>         self.ffn = make_ffn(d_model, d_ff, dropout)
>         self.norm1 = nn.LayerNorm(d_model)
>         self.norm2 = nn.LayerNorm(d_model)
>         self.norm3 = nn.LayerNorm(d_model)
>         self.dropout1 = nn.Dropout(dropout)
>         self.dropout2 = nn.Dropout(dropout)
>         self.dropout3 = nn.Dropout(dropout)
>
>     def forward(
>         self,
>         x: torch.Tensor,
>         memory: torch.Tensor,
>         causal_mask: torch.Tensor,
>         tgt_padding_mask: torch.Tensor | None = None,
>         memory_padding_mask: torch.Tensor | None = None,
>     ) -> torch.Tensor:
>         self_attn_out, _ = self.self_attn(
>             x,
>             x,
>             x,
>             attn_mask=causal_mask,
>             key_padding_mask=tgt_padding_mask,
>             need_weights=False,
>         )
>         x = self.norm1(x + self.dropout1(self_attn_out))
>
>         cross_attn_out, _ = self.cross_attn(
>             x,
>             memory,
>             memory,
>             key_padding_mask=memory_padding_mask,
>             need_weights=False,
>         )
>         x = self.norm2(x + self.dropout2(cross_attn_out))
>         x = self.norm3(x + self.dropout3(self.ffn(x)))
>         return x
>
>
> ```

### Transformer Classical and Modern

- [ ] 现代 transformer 变体?

## Transformers for Vision

Transformer 架构最初是为序列到序列学习提出的，重点应用于机器翻译

ViT 尝试将 Transformer 用于图像分类

Transformer 是处理序列的, 图像在送入之前得切块才能变成 token 序列

是 encoder-only Transformer ,Pre-Norm（Norm → Attention/FNN → Residual 的

![vit](/images/transformer-4af3b559c575.svg)

上图示例，一幅图像被划分为九个图像块。一个特殊的 `cls` 标记和九个展平后的图像块分别经过图像块嵌入和  $n$ 个 Transformer encoder 模块的变换，得到十个表示。`cls` 表示进一步被变换为输出标签

展示了视觉 Transformer 的模型架构。该架构由以下部分组成：

* 用于将图像划分为图像块的 stem
* 基于多层 Transformer 编码器的 body
* 以及将全局表示转换为输出标签的 head

> `cls` 就相当于是空的答案 token 然后经过多层信息融合交互查看其他 token 得到最终 的分类结果

### Patch Embedding

考虑批量输入图像：

$$
 \mathbf{X}\in\mathbb{R}^{B\times c\times h\times w} 
$$

将 patch 的高度和宽度均设为 $p$

`nn.Conv2d` 使用大小为 $p\times p$ 的卷积核和步幅 $p$，直接将图像划分为互不重叠的图像块：

```text
┌────────┬────────┬────────┐
│ 16×16  │ 16×16  │ 16×16  │
├────────┼────────┼────────┤
│ 16×16  │ 16×16  │ 16×16  │
├────────┼────────┼────────┤
│  ...   │  ...   │  ...   │
└────────┴────────┴────────┘
```

图像块的数量为：

$$
 m=\frac{h}{p}\frac{w}{p}=\frac{hw}{p^2} 
$$

每个 patch 包含 $cp^2$ 个元素。`nn.Conv2d` 一次完成“划分 patch + 将每个 patch 线性投影到 $d$ 维”，得到二维 patch 网格。随后，`flatten(2)` 将二维网格合并为长度为 $m$ 的 patch 序列，`transpose(1, 2)` 再将维度排列为 Transformer 使用的 $(B,m,d)$：

$$
 (B,c,h,w) \xrightarrow{\mathrm{Conv2d}} \left(B,d,\frac{h}{p},\frac{w}{p}\right) \xrightarrow{\mathrm{flatten}(2)} (B,d,m) \xrightarrow{\mathrm{transpose}(1,2)} (B,m,d) 
$$

其中 $d=\texttt{embed\_dim}$，最终得到由 $m$ 个 $d$ 维视觉 token 组成的序列。[^4]

> [!example]- 代码：Patch Embedding
>
> ```python
> import torch
> from torch import nn
>
>
> class PatchEmbedding(nn.Module):
>     def __init__(
>         self,
>         image_size: int = 96,
>         patch_size: int = 16,
>         in_channels: int = 3,
>         embed_dim: int = 512,
>     ):
>         super().__init__()
>
>         if image_size % patch_size != 0:
>             raise ValueError(
>                 "image_size must be divisible by patch_size"
>             )
>
>         self.image_size = image_size
>         self.patch_size = patch_size
>         self.num_patches = (image_size // patch_size) ** 2
>
>         self.projection = nn.Conv2d(
>             in_channels=in_channels,
>             out_channels=embed_dim,
>             kernel_size=patch_size,
>             stride=patch_size,
>         )
>
>     def forward(self, x: torch.Tensor) -> torch.Tensor:
>         _, _, height, width = x.shape
>
>         if height != self.image_size or width != self.image_size:
>             raise ValueError(
>                 f"Expected image size "
>                 f"{self.image_size}×{self.image_size}, "
>                 f"but received {height}×{width}"
>             )
>
>         # (B, c, h, w) -> (B, d, h/p, w/p)
>         x = self.projection(x)
>
>         # (B, d, h/p, w/p) -> (B, d, m)
>         x = x.flatten(start_dim=2)
>
>         # (B, d, m) -> (B, m, d)
>         x = x.transpose(1, 2)
>
>         return x
> ```

### ViT

> [!example]- 代码：ViT MLP
>
> ```python
> class ViTMLP(nn.Module):
>     def __init__(
>         self,
>         embed_dim: int,
>         mlp_dim: int,
>         dropout: float = 0.1,
>     ):
>         super().__init__()
>
>         self.layers = nn.Sequential(
>             nn.Linear(embed_dim, mlp_dim),
>             nn.GELU(),
>             nn.Dropout(dropout),
>             nn.Linear(mlp_dim, embed_dim),
>             nn.Dropout(dropout),
>         )
>
>     def forward(self, x: torch.Tensor) -> torch.Tensor:
>         # (B, m + 1, d) -> (B, m + 1, d)
>         return self.layers(x)
> ```

ViT 使用 Pre-LayerNorm，即先进行归一化，再进入多头自注意力或 MLP：

> [!example]- 代码：ViT Block
>
> ```python
> class ViTBlock(nn.Module):
>     def __init__(
>         self,
>         embed_dim: int,
>         mlp_dim: int,
>         num_heads: int,
>         dropout: float = 0.1,
>         attention_bias: bool = False,
>     ):
>         super().__init__()
>
>         self.norm1 = nn.LayerNorm(embed_dim)
>
>         self.attention = nn.MultiheadAttention(
>             embed_dim=embed_dim,
>             num_heads=num_heads,
>             dropout=dropout,
>             bias=attention_bias,
>             batch_first=True,
>         )
>
>         self.norm2 = nn.LayerNorm(embed_dim)
>
>         self.mlp = ViTMLP(
>             embed_dim=embed_dim,
>             mlp_dim=mlp_dim,
>             dropout=dropout,
>         )
>
>     def forward(self, x: torch.Tensor) -> torch.Tensor:
>         # Pre-LN + Multi-Head Self-Attention + Residual
>         normalized_x = self.norm1(x)
>
>         attention_output, _ = self.attention(
>             query=normalized_x,
>             key=normalized_x,
>             value=normalized_x,
>             need_weights=False,
>         )
>
>         x = x + attention_output
>
>         # Pre-LN + MLP + Residual
>         x = x + self.mlp(self.norm2(x))
>
>         # (B, m + 1, d) -> (B, m + 1, d)
>         return x
> ```

> [!example]- 代码：完整 ViT
>
> ```python
> class ViT(nn.Module):
>     def __init__(
>         self,
>         image_size: int = 96,
>         patch_size: int = 16,
>         in_channels: int = 3,
>         embed_dim: int = 512,
>         mlp_dim: int = 2048,
>         num_heads: int = 8,
>         num_blocks: int = 2,
>         num_classes: int = 10,
>         embedding_dropout: float = 0.1,
>         block_dropout: float = 0.1,
>         attention_bias: bool = False,
>     ):
>         super().__init__()
>
>         self.patch_embedding = PatchEmbedding(
>             image_size=image_size,
>             patch_size=patch_size,
>             in_channels=in_channels,
>             embed_dim=embed_dim,
>         )
>
>         num_patches = self.patch_embedding.num_patches
>
>         # 可学习的分类 token，形状为 (1, 1, d)
>         self.cls_token = nn.Parameter(
>             torch.zeros(1, 1, embed_dim)
>         )
>
>         # m 个 patch token + 1 个 cls token
>         self.position_embedding = nn.Parameter(
>             torch.randn(1, num_patches + 1, embed_dim)
>         )
>
>         self.embedding_dropout = nn.Dropout(
>             embedding_dropout
>         )
>
>         self.blocks = nn.Sequential(
>             *[
>                 ViTBlock(
>                     embed_dim=embed_dim,
>                     mlp_dim=mlp_dim,
>                     num_heads=num_heads,
>                     dropout=block_dropout,
>                     attention_bias=attention_bias,
>                 )
>                 for _ in range(num_blocks)
>             ]
>         )
>
>         self.head = nn.Sequential(
>             nn.LayerNorm(embed_dim),
>             nn.Linear(embed_dim, num_classes),
>         )
>
>     def forward(self, images: torch.Tensor) -> torch.Tensor:
>         # images: (B, c, h, w)
>         x = self.patch_embedding(images)
>
>         # x: (B, m, d)
>         batch_size = x.shape[0]
>
>         # (1, 1, d) -> (B, 1, d)
>         cls_tokens = self.cls_token.expand(
>             batch_size, -1, -1
>         )
>
>         # (B, m, d) -> (B, m + 1, d)
>         x = torch.cat(
>             (cls_tokens, x),
>             dim=1,
>         )
>
>         # 加入可学习的位置嵌入
>         x = self.embedding_dropout(
>             x + self.position_embedding
>         )
>
>         # (B, m + 1, d) -> (B, m + 1, d)
>         x = self.blocks(x)
>
>         # 只取 cls token 的最终表示
>         cls_output = x[:, 0]
>
>         # (B, d) -> (B, num_classes)
>         logits = self.head(cls_output)
>
>         return logits
> ```

> [!example]- 代码：ViT 前向计算示例
>
> ```python
> model = ViT(
>     image_size=96,
>     patch_size=16,
>     in_channels=3,
>     embed_dim=512,
>     mlp_dim=2048,
>     num_heads=8,
>     num_blocks=2,
>     num_classes=10,
>     embedding_dropout=0.1,
>     block_dropout=0.1,
> )
>
> images = torch.randn(4, 3, 96, 96)
> logits = model(images)
>
> print(logits.shape)
> # torch.Size([4, 10])
> ```

## 图解补充：整体结构与信息流

简单的结构长这样 [^5]

![Pasted image 20260606163249](/images/transformer-8777a4995b55.png)

![](https://jalammar.github.io/images/t/The_transformer_encoder_decoder_stack.png)

编码器在结构上完全相同（但它们不共享权重）。每个编码器都分解为两个子层

![Pasted image 20260606163606](/images/transformer-40b81982cd5f.png)

编码器的输入首先流经一个自注意力层——一个帮助编码器在编码特定单词时查看输入句子中其他单词的层

自注意力层的输出被输入到前馈神经网络。完全相同的前馈网络被独立地应用于每个位置。

![Pasted image 20260606164541](/images/transformer-e13098c77626.png)

**最后一个 encoder 的输出会送到每一层 decoder 的 Encoder-Decoder Attention**。

encoder 最终输出作为 memory，被 decoder 每一层的 encoder-decoder attention 使用。

![Pasted image 20260606165223](/images/transformer-562e6b63fe92.png)

不同的领域有不同的方法转成 token，这里每个词被嵌入到一个大小为 512 的向量中。我们将用这些简单的方框来表示这些向量。

![Pasted image 20260606165655](/images/transformer-048b776e11c1.png)

从这里我们可以看到 Transformer 的一个关键特性，即每个位置的词在编码器中通过自己的路径流动（output 的路径是保持的）。在这些路径之间存在自注意力层中的依赖关系（自注意力层可以相互参考）。然而，前馈层没有这些依赖关系，因此各种路径可以在通过前馈层时并行执行。

![Pasted image 20260606165909](/images/transformer-c6564965b57f.png)

编码器以一系列向量作为输入。它通过将这些向量输入到“自注意力”层，然后输入到前馈神经网络，然后将输出向上发送到下一个编码器。

### Self-Attention 图解：直觉

Self-attention is the method the Transformer uses to bake the “understanding” of other relevant words into the one we’re currently processing.

请将以下句子作为我们想要翻译的输入句子：

”`The animal didn't cross the street because it was too tired`”

这句话中的“it”指的是什么？是指街道还是指动物？对人类来说这是一个简单的问题，但对算法来说就不那么简单了。

当模型处理单词“it”时，自注意力机制使其能够将“it”与“animal”关联起来。

![Pasted image 20260606170327](/images/transformer-2e07a9484fc2.png)

> 当我们对堆栈中最上层的编码器#5 中的单词 "it" 进行编码时，注意力机制的一部分专注于 "The Animal"，并将其部分表示嵌入到 "it" 的编码中。

self-attention 就是在更新某个 token 表示时，让它参考同一句子里其他 token 的信息，把相关信息按权重混进来

这里的案例说明 it 更依赖 the animal 的信息

### Self-Attention 图解：逐步计算

解释 Self-Attention 具体怎么算的？从 token embedding$x_{1},x_{2},\dots$ 的输入到 输出给 FFN 的 $z_{1},z_{2}\dots$

计算自注意力机制的第一步是从编码器的每个输入向量（在此情况下，每个单词的嵌入）中**创建三个向量**。每个单词，我们创建一个查询向量 $q$、一个键向量 $k$ 和一个值向量 $v$。在**训练过程中**这些向量是通过将嵌入乘以训练的三个矩阵 $Q,K,V$ 来创建的。

这些新向量的维度比嵌入向量小。**它们的维度为 64**，而嵌入向量和编码器输入/输出向量的维度为 512。它们不必一定更小，这是一种架构选择，目的是使多头注意力（主要是）的计算保持恒定。

![Pasted image 20260606171909](/images/transformer-d04bbb398cc0.png)

每个 token 的对应 qkv 向量是用一个 $Q,K,V$ 矩阵乘出来了的

那 $q,k,v$ 是什么？

![Pasted image 20260607093304](/images/transformer-7d8ec3936460.png)

计算自注意力机制的第二步是计算一个分数。

假设我们正在计算这个例子中第一个词“Thinking”的自注意力。我们需要将输入句子的每个词与这个词进行评分。**这个分数决定了在编码某个位置的词时，应该将多少注意力放在输入句子的其他部分上。**

> 也就是这个 token 会多少程度上关注 token 序列的其他 token

该分数是通过将 查询向量 与我们正在评分的相应单词的 键向量 进行点积计算得出的。因此，如果我们正在处理位置 #1 的单词的自注意力机制，第一个分数将是 q1 和 k1 的点积。第二个分数将是 q1 和 k2 的点积。

![Pasted image 20260607094020](/images/transformer-3fafc2cf5116.png)

第三步和第四步是将分数除以 8（论文中使用的键向量 $k$ 的维度的平方根——64。这会导致梯度更加稳定。这里可能有其他可能的值，但这是默认值），然后将结果通过 softmax 操作。Softmax 将分数标准化，使它们都是正数并且总和为 1。

这个 softmax 分数决定了每个词在这个位置上表达的程度。显然，这个位置上的词将具有最高的 softmax 分数，但有时关注与当前词相关的另一个词也是有用的。

![Pasted image 20260607101035](/images/transformer-0fa71a554c46.png)

第五步是将每个值向量 $v$ 乘以 softmax 分数（为将它们相加做准备）。这里的直观理解是**保持我们想要关注的单词的值不变，通过乘以很小的数字（例如 0.001）来淹没无关的单词**。

第六步是求加权值向量的和。这产生了自注意力层在**此位置（对于第一个词）**的输出 $z_{1}$。

这完成了自注意力计算。所得向量可以传递给前馈神经网络。然而，在实际实现中，该计算以矩阵形式进行以加快处理速度。现在我们已经了解了单词层面的计算直觉，让我们来看看这一点。

### Self-Attention 图解：矩阵形式

把前面的拆分换成矩阵的形式

**第一步**是计算查询（Query）、键（Key）和值（Value）矩阵。我们通过将嵌入（embeddings）打包到矩阵 $X$ 中，并将其与训练好的权重矩阵（WQ、WK、WV）相乘来完成这一步。

![Pasted image 20260607101345](/images/transformer-4a68511322f8.png)

矩阵 $X$ 中的每一行对应输入句子中的一个词。我们再次看到嵌入向量（512 维，或图中 4 个方框）与 q/k/v 向量（64 维，或图中 3 个方框）在大小上的差异。

![Pasted image 20260607101753](/images/transformer-6b95d6e3e6ca.png)

最后，由于我们处理的是矩阵，可以将步骤二至步骤六合并为一个公式来计算自注意力层的输出。

1. $QK^T$ 是每个 query 与每个 key 的相似度打分 (点积),计算得到的矩阵中每个都是 对应 $q_{i},k_{j}$ 的 raw score
2. 然后除以 $\sqrt{d_k}$ 是为了防止维度大时点积过大 (dot-product sum 的次数和维度成正比) 导致 softmax 梯度消失，梯度更稳定
3. softmax 把分数归一成权重
4. 再对 $V$ 加权求和 得到 $Z$

Scaled Dot-Product Attention

```python
import torch, math
import torch.nn as nn
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    # Q: (B, h, Lq, d_k)  K,V: (B, h, Lk, d_k)
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)   # (B, h, Lq, Lk)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))  # 屏蔽位置
    attn = F.softmax(scores, dim=-1)                    # 权重,行和为 1
    out  = attn @ V                                     # (B, h, Lq, d_v)
    return out, attn
```

### Multi-Head Attention 图解

**一个注意力头只能学一种“看关系”的方式，多头可以同时从多个角度看同一句话。**

对于同一个 token 相对其他 token 的关系可能是多个角度的

相当于对前面的 Self-Attention 初始化互不相关然后并行计算最终把多头的输出拼接乘上权重矩阵 $W^O$，然后再送给 FFN

该论文通过添加一种称为“多头”注意力的机制，进一步精炼了自注意力层。这通过两种方式提高了注意力层的性能：

1. **它扩展了模型关注不同位置的能力**。是的，在上面的例子中，z1 包含了其他编码的一点点信息，但它可能被实际单词本身所主导。如果我们正在翻译一个像“动物没有过马路，因为它太累了”这样的句子，知道“it”指的是哪个词将非常有用。
2. 它为注意力层提供了多个“表示子空间”。正如接下来我们将看到的，通过多头注意力机制，我们不仅有一个，而是多个 Query/Key/Value 权重矩阵的集合（Transformer 使用八个注意力头，因此**每个编码器/解码器最终都会有八个集合**）。这些集合中的每一个都是**随机初始化**的。然后，在训练之后，每个集合都被用来将输入嵌入（或来自较低编码器/解码器的向量）投影到不同的表示子空间中。

![Pasted image 20260607111314](/images/transformer-3c561d9c4f03.png)

如果我们按照上述概述进行同样的自注意力计算，只是用不同的权重矩阵重复八次，最终我们会得到八个不同的 Z 矩阵

![Pasted image 20260607111539](/images/transformer-3c3a95ffa42b.png)

前馈层不是期望八个矩阵——它期望一个单一的矩阵（每个词一个向量）。因此，我们需要一种方法将这些八个压缩成一个单一的矩阵。

我们将矩阵连接起来，然后乘以一个额外的权重矩阵 $W^O$。

![Pasted image 20260607111603](/images/transformer-ec8eef4de890.png)

![Pasted image 20260607111838](/images/transformer-d805dba1e819.png)

Self-Attention 输入 $X$ 输出 $R=Z$

### Positional Encoding 图解

到目前为止，我们所描述的模型中缺少的一个方面是解释输入序列中单词顺序的方法。

也就是说，至少得让相同的 token 在 transformer 里面是不一样的吧，因此 token 被送入 transformer 之前都要加上位置编码

$$
X = X_{\text{token}} + P
$$

加完之后，每个 token 的向量已经不只是内容向量，而是“内容 + 位置”的混合表示

为了解决这个问题，Transformer 为每个输入嵌入添加了一个向量。这些向量遵循模型学习的特定模式，这有助于它确定每个单词的位置，或序列中不同单词之间的距离。这里的直观理解是，将这些值添加到嵌入中，一旦它们被投影到 Q/K/V 向量中，并且在点积注意力期间，就会在嵌入向量之间提供有意义的距离。

![Pasted image 20260607142533](/images/transformer-4efab37dbd0a.png)

如果我们假设嵌入的维度为 4，实际的位置编码将如下所示：每个值介于 1 和 -1 之间，颜色对应热力图

![Pasted image 20260607143757](/images/transformer-e0a45553f257.png)

原始的 位置编码 Transformer 使用正弦函数和余弦函数交替生成，很多现代模型的做法是**可学习位置编码** $P$，随机初始化，然后训练过程中被优化

![Pasted image 20260607143707](/images/transformer-c5b03a4c161d.png)

### Residual 与 LayerNorm 图解

在继续之前，我们需要提及编码器架构中的一个细节：每个编码器中的每个子层（自注意力机制、前馈神经网络）都有一个残差连接，随后是一个 [层归一化](https://arxiv.org/abs/1607.06450) 步骤。

![Pasted image 20260607144552](/images/transformer-285a1a9a2a70.png)

这同样适用于解码器的子层。如果我们考虑一个由 2 个堆叠的编码器和解码器组成的 Transformer，它看起来会像这样：

![Pasted image 20260607144726](/images/transformer-28344ab0fe89.png)

encoder 的最后一层输出会送到 每一个的 decoder 的 cross-attention

### Decoder 侧的信息流

现在我们已经涵盖了编码器的大部分概念，基本上也知道了解码器组件的工作原理。但让我们看看它们是如何**协同**工作的。

编码器首先处理输入序列。然后，顶层编码器的输出被转换为一组注意力向量 K 和 V。这些向量将被每个解码器在其“编码器 - 解码器注意力”层中使用，以帮助解码器专注于输入序列中的适当位置：

![](https://jalammar.github.io/images/t/transformer_decoding_1.gif)

解码器一开始 是没有输入的，然后 output 都会作为 decoder 自己的输入

以下步骤将重复执行，直到出现特殊符号，表明 Transformer 解码器已完成其输出。每一步的输出将输入到下一个时间步的底部解码器中，解码器像编码器一样逐层传递其解码结果。与我们对编码器输入所做的那样，我们也对解码器输入进行嵌入并添加位置编码，以指示每个单词的位置。

![](https://jalammar.github.io/images/t/transformer_decoding_2.gif)

在解码器中，自注意力层**仅被允许关注输出序列中较早的位置**。这是通过在自注意力计算中的 softmax 步骤之前，将未来位置掩码化（将其设置为 `-inf`）来实现的。也就是 masked multi-head attention

“编码器 - 解码器注意力”层的工作方式与多头自注意力类似，只是它从下层创建其查询矩阵，并从编码器堆栈的输出中获取键和值矩阵。

> [!question]
> Self-Attention 和 Cross-Attention 的区别？

### Final Linear 与 Softmax

解码器堆栈输出一个浮点数向量。我们如何将这个转换为单词？这是最终线性层的任务，该层后面跟着一个 Softmax 层。

线性层是一个简单的全连接神经网络，它将解码器堆栈产生的向量投影到一个远、远更大的向量，称为 logits 向量。

假设我们的模型知道 10,000 个独特的英语单词（模型“输出词汇表”），这些单词是从其训练数据集中学习到的。这将使 logits 向量有 10,000 个单元格宽——每个单元格对应一个独特单词的得分。这就是我们如何解释模型经过线性层后的输出。

然后 softmax 层将这些得分转换为概率（所有正数，总和为 1.0）。概率最高的单元格被选中，与之关联的单词作为该时间步的输出产生。

![Pasted image 20260607152410](/images/transformer-01b523d084eb.png)

## 和 Robot Learning 的关系

Transformer 很适合做这种 token 间关系建模，所以 ACT 这类方法里可以把图像 embedding、机器人状态、视觉、latent 这些都作为 token。

**Transformer 在 robot learning 里很常见，但不是所有 encoder 都必须用 Transformer**。它常见于两类场景：
* 一类是 **模仿学习 / 动作序列建模**，比如 ACT、Diffusion Policy Transformer 变体、VQ-BeT
* 另一类是 **VLA / robotic foundation model**，比如 RT-1、RT-2、OpenVLA、π0 系列

[^1]: [11.1. Queries, Keys, and Values — Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html)
[^2]: [11.3. Attention Scoring Functions — Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html)
[^3]: [11.5. Multi-Head Attention — Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/multihead-attention.html)
[^4]: [11.8. Transformers for Vision — Dive into Deep Learning](https://d2l.ai/chapter_attention-mechanisms-and-transformers/vision-transformer.html)
[^5]: [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
