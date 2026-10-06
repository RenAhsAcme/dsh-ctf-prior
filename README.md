# dsh-ctf-prior
适用于 DeepSeek Harness (Powered By DeepSeek-V4.1-Flash) 的 CTF 解题 SKILL，它是代号 pt 项目的前期灵感。

我希望教会 AI 如何更加高效地全自动地完成 CTF 比赛，由此推广，我希望能够打造一个专为网络空间安全从业者设计的 Harness。它也是我推动代号 pt 项目开发的前期灵感。

假设一场 CTF 比赛存在简单、中等和困难类型的题目，使用该 SKILL 并基于 DeepSeek-V4.1-Flash (High) 模型，基于 2026-10-05 的测试结果，你可以实现：
- 执行简单类型题目时，2-5 min 即可得到 Flag 与 WP；
- 执行中等类型题目时，极大概率可在 5-30 min 得到 Flag 与 WP；
- 执行困难类型题目时，极大概率无法解出。

根据实验结果来看，在简单题目上采取 Medium 的思考强度，可在保持相对持平的正确率上，提高模型解题效率，并进一步抑制异常幻觉、异常 Token 重复的问题。

不建议使用 Max 思考强度。因为我们已经使用了一些定向 Skill 来指导模型从事 CTF 工作。仍然使用 Max 思考强度将导致思考链大幅延长，异常 Token 重复出现、循环推理、异常幻觉出现概率增大，降低解题效率，且对解题正确率（指退回 Explore 阶段重试的概率）无较大帮助。

> Forge a sharp sword, slay my old self, create a brand-new paradigm, and then bury the self of the old era—for I shall become the architect of the new age.
