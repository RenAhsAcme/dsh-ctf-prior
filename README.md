# dsh-ctf-prior
适用于 DeepSeek Harness (Powered By DeepSeek-V4.1-Flash) 的 CTF 解题 SKILL 以及相关插件，它是代号 pt 项目的前期灵感。

我希望教会 AI 如何更加高效地全自动地完成 CTF 比赛，由此推广，我希望能够打造一个专为网络空间安全从业者设计的 Harness。它也是我推动代号 pt 项目开发的前期灵感。

假设一场 CTF 比赛存在简单、中等和困难类型的题目，使用该 SKILL 并使用 SKILL 调用的插件，并基于 DeepSeek-V4.1-Flash (High) 模型，基于 2026-10-05 的测试结果，你可以实现：
- 执行简单类型题目时，2-5 min 即可得到 Flag 与 WP；
- 执行中等类型题目时，极大概率可在 5-30 min 得到 Flag 与 WP；
- 执行困难类型题目时，极大概率无法解出。

根据实验结果来看，在简单题目上采取 Medium 的思考强度，可在保持相对持平的正确率上，提高模型解题效率，并进一步抑制异常幻觉、异常 Token 重复的问题。

不建议使用 Max 思考强度。因为我们已经使用了一些定向 Skill 来指导模型从事 CTF 工作。仍然使用 Max 思考强度将导致思考链大幅延长，异常 Token 重复出现、循环推理、异常幻觉出现概率增大，降低解题效率，且对解题正确率（指退回 Explore 阶段重试的概率）无较大帮助。

为了进一步提升模型执行能力，一些新插件被引入，高级化开发初见雏形。

2026-10-09 更新：

一个巨大的灵感出现了：[ARTEX](https://github.com/RenAhsAcme/ARTEX)。

第一次看到这个仓库的时候，心里其实有点难过的，其实这个项目完全符合我对那些网络安全 Harness 的一切幻想。在 AI 的全力加速下，这一产物也抢先在我懈怠的生活节奏之中发布并在野利用了。

我可能需要考虑另外的创新点了。比如原项目已经停更（准确来说是中止开源，因为为了阻止更广泛的在野滥用，虽然已经收效甚微），我希望把这个利器延续下去，并延伸至 DeepSeek Harness 的原生环境中，并为学习者提供一个全新的理解范式。

心里其实有些矛盾，一方面是已有人做出甚至可以武器化的东西（这该死的嫉妒心，人性的劣根），但另一方面我更乐见这样的进步，我对技术的一切进步都持有极大的热情，即使我知道他将以不同的方式化为利刃刺向我。

通过写一个 `README.md` 来水今日的 Commit 打卡吗？我真的会很有罪恶感。

> Forge a sharp sword, slay my old self, create a brand-new paradigm, and then bury the self of the old era—for I shall become the architect of the new age.
