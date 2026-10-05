# {{CHALLENGE_NAME}}

<!--
CTF Writeup 通用模板。

目标：
1. 让具备相应基础知识的读者可以理解完整解题逻辑。
2. 让读者能够根据本文独立复现解题过程。
3. 重点解释“为什么”，而不仅仅记录“执行了什么命令”。
4. 保留真正影响解题的尝试、失败原因和关键判断，删除无价值流水账。
5. Writeup 应当尽可能形成完整的因果链：

题目条件
→ 信息收集
→ 关键观察
→ 漏洞 / 弱点
→ 可利用原语
→ 利用方案
→ Payload / Solver
→ Flag
→ 总结

使用本模板时：
- 删除不适用于当前题目的章节。
- 可以根据题型增加子章节。
- 不要为了套模板而保留空章节。
-->

## 0. Challenge Information

| Item | Value |
|---|---|
| Competition | {{COMPETITION_NAME}} |
| Challenge | {{CHALLENGE_NAME}} |
| Category | {{Web / Pwn / Reverse / Crypto / Misc / Forensics / Hardware / ...}} |
| Difficulty | {{Easy / Medium / Hard / Insane}} |
| Points | {{POINTS}} |
| Author | {{CHALLENGE_AUTHOR}} |
| Solver | {{SOLVER_NAME}} |
| Date | {{YYYY-MM-DD}} |

<!--
基本信息只保留有价值的内容。

如果比赛采用动态分值，可填写最终解题时分值。
如果未知出题人，可以删除 Author。
-->

---

## 1. TL;DR

<!--
用 1～5 句话概括整道题的完整解题链。

要求：
- 不写背景废话。
- 不展开细节。
- 尽可能包含“漏洞/弱点 + 核心利用方法 + 最终目标”。

示例：

> The application contains an SSRF vulnerability in `/fetch`.
> By bypassing the URL filter with an IPv6 loopback address, the internal
> `/admin` service can be accessed, from which the flag is obtained.

或者：

> Stack overflow → leak libc through `puts@GOT`
> → calculate libc base → ret2libc → `system("/bin/sh")`.
-->

> {{ONE_PARAGRAPH_SOLUTION_SUMMARY}}

---

## 2. Challenge Description

<!--
尽可能保留原始题目描述。

如果题目描述很长，只保留与解题相关的部分。
不要修改原题文字而导致语义变化。
-->

> {{ORIGINAL_CHALLENGE_DESCRIPTION}}

### Provided Files

<!--
列出题目提供的附件。
没有附件时删除本节。
-->

```text
{{FILE_TREE}}
```

例如：

```text
challenge/
├── chall
├── libc.so.6
├── ld-linux-x86-64.so.2
└── Dockerfile
```

### Target

<!--
存在远程服务时填写。
公开发布 Writeup 时，应避免暴露已经失效但包含敏感信息的个人基础设施。
-->

```text
{{TARGET}}
```

---

## 3. Initial Analysis

<!--
描述“拿到题目后的第一轮判断”。

这一部分应该回答：

1. 题目给了什么？
2. 最明显的攻击面 / 分析入口是什么？
3. 初步怀疑考察什么知识点？
4. 哪些信息值得进一步验证？

避免：

“先打开题目看看。”
“然后我随便试了一下。”
“感觉这里有问题。”

应该说明判断依据。
-->

{{INITIAL_ANALYSIS}}

### Initial Hypothesis

<!--
如果存在明确假设，可以记录下来。

示例：

- 用户输入直接进入 SQL 查询，可能存在 SQL Injection。
- Binary 未启用 PIE 且存在 `gets()`，可能考虑 ROP。
- RSA 使用较小的 `e`，需要检查是否满足 low exponent attack 条件。
-->

- {{HYPOTHESIS_1}}
- {{HYPOTHESIS_2}}

---

## 4. Reconnaissance / Information Gathering

<!--
记录真正影响后续分析的信息收集过程。

不要把所有执行过的命令全部贴出来。

每一个命令最好都能回答：
“为什么执行？”
“结果说明什么？”

推荐格式：

目的
→ 命令
→ 关键输出
→ 结论
-->

### 4.1 {{RECON_ITEM}}

{{WHY_THIS_CHECK_IS_NEEDED}}

```bash
{{COMMAND}}
```

关键输出：

```text
{{IMPORTANT_OUTPUT}}
```

由此可以确定：

- {{CONCLUSION_1}}
- {{CONCLUSION_2}}

### 4.2 {{RECON_ITEM}}

{{CONTENT}}

---

## 5. Root Cause / Vulnerability Analysis

<!--
这是 Writeup 最重要的章节之一。

必须回答：

1. 弱点具体位于哪里？
2. 为什么这是一个漏洞 / 可利用缺陷？
3. 攻击者可以控制什么？
4. 最终能够获得什么能力？

尽量区分：

Vulnerability（漏洞）
Primitive（利用原语）
Exploit（最终利用）

例如：

Use-After-Free
    ↓
Heap address leak
    ↓
Arbitrary write
    ↓
Overwrite function pointer
    ↓
Code execution
-->

### 5.1 Vulnerable Code / Logic

<!--
仅摘录必要代码。

不要无意义粘贴整个源码文件。
-->

```{{LANGUAGE}}
{{RELEVANT_CODE}}
```

关键问题位于：

```text
{{VULNERABLE_LOCATION}}
```

原因：

{{ROOT_CAUSE_EXPLANATION}}

---

### 5.2 Attacker-Controlled Input

<!--
明确攻击者能控制哪些数据。

例如：
- HTTP 参数
- Cookie
- 文件内容
- 栈上的输入
- Heap chunk 内容
- RSA 参数
- 加密明文
-->

攻击者可以控制：

- {{CONTROLLED_VALUE_1}}
- {{CONTROLLED_VALUE_2}}

这些数据最终流向：

```text
{{DATA_FLOW}}
```

---

### 5.3 Exploitation Primitive

<!--
如果题目存在明确的利用原语，应单独说明。

常见 Primitive：

- Arbitrary Read
- Arbitrary Write
- Relative Write
- OOB Read
- OOB Write
- RIP Control
- PC Control
- Stack Pivot
- Heap Address Leak
- libc Leak
- Authentication Bypass
- File Read
- SSRF
- Command Injection
- SQL Injection
- Padding Oracle
- Known Plaintext
-->

当前漏洞能够构造：

> **{{PRIMITIVE}}**

具体原因：

{{PRIMITIVE_EXPLANATION}}

---

## 6. Exploitation Strategy

<!--
先讲完整思路，再讲具体操作。

这一节应该让读者在不看 exploit 代码的情况下，
已经理解“如何从漏洞走到 Flag”。

推荐使用攻击链表达。
-->

完整攻击链：

```text
{{STEP_1}}
    ↓
{{STEP_2}}
    ↓
{{STEP_3}}
    ↓
{{STEP_4}}
    ↓
{{FLAG_OR_FINAL_GOAL}}
```

其中关键步骤是：

1. {{KEY_STEP_1}}
2. {{KEY_STEP_2}}
3. {{KEY_STEP_3}}

---

## 7. Exploitation / Solution

<!--
逐步展开真正的利用过程。

建议：
- 一个重要阶段一个三级标题。
- 每一阶段说明目标。
- Payload 前说明为什么这样构造。
- 输出后说明结果意味着什么。
-->

### 7.1 {{STAGE_1_NAME}}

目标：

> {{STAGE_1_GOAL}}

{{STAGE_1_EXPLANATION}}

```{{LANGUAGE}}
{{STAGE_1_CODE_OR_PAYLOAD}}
```

结果：

```text
{{STAGE_1_RESULT}}
```

因此：

{{STAGE_1_CONCLUSION}}

---

### 7.2 {{STAGE_2_NAME}}

目标：

> {{STAGE_2_GOAL}}

{{STAGE_2_EXPLANATION}}

```{{LANGUAGE}}
{{STAGE_2_CODE_OR_PAYLOAD}}
```

结果：

```text
{{STAGE_2_RESULT}}
```

---

### 7.3 {{STAGE_3_NAME}}

{{CONTENT}}

---

## 8. Final Solver / Exploit

<!--
这里放可以独立运行的最终版本。

要求尽可能满足：

1. 删除调试阶段无关代码。
2. 保留必要注释。
3. 避免硬编码可以自动计算的数据，除非题目本身要求。
4. 明确本地 / 远程切换方式。
5. 如依赖特殊环境，注明版本。
6. Solver 应与正文描述一致。

如果代码非常长，可以单独保存：

exp.py
solve.py
solver.sage
exploit.js

然后这里只展示核心代码或链接。
-->

```{{LANGUAGE}}
{{FINAL_EXPLOIT_OR_SOLVER}}
```

运行：

```bash
{{RUN_COMMAND}}
```

输出：

```text
{{FINAL_OUTPUT}}
```

---

## 9. Flag

<!--
如果比赛规则禁止公开 Flag，则删除本节或写：

Flag omitted.

公开 Writeup 时根据比赛要求决定是否保留。
-->

```text
{{FLAG}}
```

---

## 10. Key Takeaways

<!--
用较短内容总结真正值得记住的知识。

不要重复整个解题过程。

重点回答：

- 这题真正考什么？
- 哪一个观察最关键？
- 哪个技巧可以迁移到其他题？
-->

本题核心知识点：

- {{KNOWLEDGE_POINT_1}}
- {{KNOWLEDGE_POINT_2}}
- {{KNOWLEDGE_POINT_3}}

最关键的突破点：

> {{MOST_IMPORTANT_INSIGHT}}

---

## 11. Pitfalls / Failed Attempts

<!--
可选章节。

只记录有分析价值的失败。

值得记录：
- 为什么一种看起来可行的方法实际上不成立；
- 某个保护机制导致利用失败；
- 本地与远程环境不同；
- 某个边界条件容易忽略；
- 某种算法不能使用的数学原因。

不值得记录：
- 拼错命令；
- 忘记保存文件；
- 无意义随机尝试；
- 与题目本身无关的环境问题。
-->

### 11.1 {{FAILED_ATTEMPT}}

最初尝试：

```text
{{ATTEMPT}}
```

该方法失败的原因是：

{{FAILURE_REASON}}

最终改为：

{{FINAL_FIX}}

---

## 12. Further Analysis

<!--
可选。

用于补充不是完成题目所必需，但具有学习价值的内容。

例如：

- 是否存在第二种解法？
- 漏洞如何修复？
- 出题人为什么设置某个保护？
- 某个绕过技术的原理是什么？
- 是否能够进一步扩展利用？
-->

### 12.1 Alternative Solution

{{ALTERNATIVE_SOLUTION}}

### 12.2 Mitigation

<!--
如果分析漏洞修复方式，不能只写“过滤输入”。

应该尽量说明根本修复方案。

例如：

SQL Injection：
使用参数化查询，而不是黑名单过滤。

Buffer Overflow：
使用长度安全 API，并进行边界检查。

Path Traversal：
规范化路径后验证其仍位于允许目录。
-->

{{MITIGATION}}

---

## 13. References

<!--
只放真正使用过或值得进一步阅读的资料。

优先：
- 官方文档
- RFC
- CVE / CWE
- 源码
- 官方手册
- 原始论文
- 高质量技术文章

避免为了显得完整而堆大量无关链接。
-->

- {{REFERENCE_1}}
- {{REFERENCE_2}}
- {{REFERENCE_3}}

---

# Appendix A — Web-Specific Structure

<!--
以下内容是 Web 题可选模块。

使用时可以将相关内容移动到正文，
不需要全部保留。
-->

## A.1 Application Surface

```text
{{APPLICATION_STRUCTURE}}
```

关注入口：

| Endpoint | Method | Parameters | Notes |
|---|---|---|---|
| `{{PATH}}` | `{{METHOD}}` | `{{PARAMETERS}}` | {{NOTES}} |

## A.2 Request

```http
{{HTTP_REQUEST}}
```

## A.3 Response

```http
{{HTTP_RESPONSE}}
```

## A.4 Data Flow

```text
User Input
    ↓
{{COMPONENT}}
    ↓
{{COMPONENT}}
    ↓
{{VULNERABLE_SINK}}
```

## A.5 Payload

```text
{{PAYLOAD}}
```

## A.6 Why the Payload Works

{{PAYLOAD_EXPLANATION}}

<!--
Web Writeup 尤其需要解释：

- 输入如何到达危险 Sink；
- Sanitization / Validation 在哪里失效；
- Payload 中特殊字符分别发挥什么作用；
- 如果存在绕过，绕过的是哪条规则；
- 服务端最终实际执行了什么。
-->

---

# Appendix B — Pwn-Specific Structure

<!--
Pwn 推荐遵循：

Binary Information
→ Protections
→ Static Analysis
→ Dynamic Analysis
→ Vulnerability
→ Primitive
→ Leak
→ Address Calculation
→ Control Flow Hijack
→ Final Exploit
-->

## B.1 Binary Information

```bash
file {{BINARY}}
checksec --file={{BINARY}}
```

输出：

```text
{{CHECKSEC_OUTPUT}}
```

保护机制：

| Protection | Status | Impact |
|---|---|---|
| RELRO | {{STATUS}} | {{IMPACT}} |
| Canary | {{STATUS}} | {{IMPACT}} |
| NX | {{STATUS}} | {{IMPACT}} |
| PIE | {{STATUS}} | {{IMPACT}} |

## B.2 Vulnerable Function

```c
{{DECOMPILED_CODE}}
```

## B.3 Memory Layout

```text
High Address
┌─────────────────────┐
│ {{ITEM}}            │
├─────────────────────┤
│ {{ITEM}}            │
├─────────────────────┤
│ {{ITEM}}            │
└─────────────────────┘
Low Address
```

## B.4 Offset

```text
offset = {{OFFSET}}
```

确定方法：

```bash
{{OFFSET_COMMAND}}
```

## B.5 Address Leak

泄露：

```text
{{LEAK_TARGET}}
```

计算：

```text
{{ADDRESS_CALCULATION}}
```

## B.6 ROP / Heap / Exploitation Chain

```text
{{CHAIN}}
```

<!--
Pwn 中应尽可能区分：

Vulnerability:
    Stack Buffer Overflow

Primitive:
    RIP Control

Technique:
    ROP

Stage 1:
    Leak libc

Stage 2:
    ret2libc

Final:
    system("/bin/sh")
-->

---

# Appendix C — Reverse-Specific Structure

<!--
Reverse 推荐强调程序语义恢复过程。

不要仅仅大量粘贴反编译代码。
-->

## C.1 Program Entry

入口：

```text
{{ENTRY}}
```

## C.2 Important Functions

| Original Name | Renamed | Purpose |
|---|---|---|
| `sub_{{ADDR}}` | `{{NAME}}` | {{PURPOSE}} |

<!--
强烈建议在分析过程中对 IDA / Ghidra 默认函数名重命名。
-->

## C.3 Control Flow

```text
main
 ↓
{{FUNCTION}}
 ↓
{{FUNCTION}}
 ↓
{{VERIFY_FUNCTION}}
```

## C.4 Verification Logic

```c
{{PSEUDOCODE}}
```

等价逻辑：

```text
{{SIMPLIFIED_LOGIC}}
```

## C.5 Algorithm Reconstruction

原算法：

```text
{{FORWARD_ALGORITHM}}
```

逆过程：

```text
{{REVERSE_ALGORITHM}}
```

## C.6 Solver

```python
{{SOLVER}}
```

---

# Appendix D — Crypto-Specific Structure

<!--
Crypto Writeup 应优先展示数学关系，而不是先放 Solver。
-->

## D.1 Given

已知：

\[
{{KNOWN_VALUES}}
\]

目标：

\[
{{TARGET_VALUE}}
\]

## D.2 Cryptosystem

使用的密码系统：

> {{CRYPTOSYSTEM}}

核心关系：

\[
{{CORE_EQUATION}}
\]

## D.3 Weakness

题目满足：

\[
{{WEAK_CONDITION}}
\]

因此：

\[
{{DERIVATION}}
\]

这意味着：

{{CRYPTO_WEAKNESS_EXPLANATION}}

## D.4 Attack

攻击方法：

> **{{ATTACK_NAME}}**

适用条件：

- {{CONDITION_1}}
- {{CONDITION_2}}

本题满足这些条件，因为：

{{WHY_ATTACK_APPLIES}}

## D.5 Solver

```python
{{CRYPTO_SOLVER}}
```

<!--
禁止只写：

“发现是 RSA，直接套脚本。”

应该明确：
- 为什么识别为某种攻击；
- 攻击要求哪些数学条件；
- 本题为什么满足这些条件；
- Solver 中每个核心计算对应什么数学步骤。
-->

---

# Appendix E — Forensics / Misc-Specific Structure

## E.1 Evidence Overview

```text
{{FILES_OR_EVIDENCE}}
```

## E.2 Timeline

| Time | Event |
|---|---|
| {{TIME}} | {{EVENT}} |

## E.3 Artifact Analysis

### {{ARTIFACT}}

来源：

```text
{{SOURCE}}
```

发现：

```text
{{FINDING}}
```

意义：

{{WHY_FINDING_MATTERS}}

## E.4 Extraction / Decoding Chain

```text
{{INPUT}}
    ↓
{{FORMAT_OR_ENCODING}}
    ↓
{{TRANSFORMATION}}
    ↓
{{RESULT}}
```

---

# Appendix F — Quality Checklist

<!--
完成 Writeup 后逐项检查。

这些内容通常不需要保留在最终公开版本中。
-->

- [ ] TL;DR 能否在一分钟内说明完整解题链？
- [ ] 是否解释了漏洞 / 弱点为什么存在？
- [ ] 是否区分了漏洞、利用原语和最终利用？
- [ ] 是否说明了关键 Payload 为什么有效？
- [ ] 是否删除了无意义的命令流水账？
- [ ] 是否只保留了与分析有关的关键输出？
- [ ] 是否能够根据本文从零复现？
- [ ] 最终 Solver / Exploit 是否与正文一致？
- [ ] 是否记录了真正有价值的失败尝试？
- [ ] 是否说明了题目的核心知识点？
- [ ] 是否避免大量无解释的截图？
- [ ] 是否避免直接贴大段源码而不分析？
- [ ] 是否避免“套脚本即可”之类缺乏原理的描述？
- [ ] 一年后重新阅读时，是否仍然可以理解完整攻击链？

<!--
最终质量标准：

一个优秀的 CTF Writeup 不应该只是证明：

“我做出了这道题。”

而应该完整回答：

“题目为什么可以这样解？”
“攻击链为什么成立？”
“别人如何复现？”
“这道题有什么值得迁移到其他题目的知识？”
-->