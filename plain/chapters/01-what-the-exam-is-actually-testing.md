# Chapter 1: What This Exam Tests That an Interview Does Not

**Summary**: *An interview asks whether you can build the thing. This exam asks whether you reached for the right mechanism (the right part of the system to act on). Almost every wrong answer it offers is a mechanism that works perfectly well somewhere else. That is the difficulty, and you cannot read past it. This chapter sets the idea up on the smallest material in the syllabus. It covers what a token is, what the window is, why one request run twice returns two different answers, and which dial does which job. That is four facts. A surprising number of later questions fall apart once you hold them straight.*

## The Same Request Twice Returns Two Different Answers, and Nothing Is Broken

**First, the idea.** Claude does not look up an answer. It picks one piece at a time. So the same request can come back worded differently, and that is normal.

**The analogy for this chapter: a kitchen.** Your **request** is the order ticket. **Claude** is the chef. The chef builds the dish one scoop at a time. Each scoop is a **token** (a small chunk of text). Every dial in this chapter is a different knob in that kitchen. Keep asking one question: which knob does this option turn?

**What happens.** Send a request. Send it again, **byte for byte identical** (exactly the same). The two responses will often **differ in wording**. Sometimes they differ in structure. Occasionally one has a caveat and the other does not.

**The reflex.** The reflex is to **open a ticket**. You assume something **upstream must be varying**. Maybe a stray timestamp is in the prompt. Maybe a config got redeployed. Maybe two versions of the code are running behind a load balancer.

**What is really going on.** Usually **nothing is varying**. **Generation proceeds one token at a time** (the chef adds one scoop at a time). Every one of those choices is **sampled rather than looked up** (picked from a shortlist, not read from a recipe card). So two runs can differ at any single position and stay different for the rest of the response. Anthropic says the strong form of this plainly. **Identical inputs can produce different outputs** even with **temperature set to 0**. That is true on Anthropic's own inference service and on third-party providers.<sup>[1]</sup> Temperature 0 is not a **determinism switch**. It narrows the shortlist. It does not shrink it to a single choice.

**Why it matters in code.** **Humans absorb the rewording** without noticing it. A **parser** does not. Neither does a **downstream step** that expected a field where a sentence now sits.

**Where the exam differs from an interview.** An interviewer watching you debug would accept "it varies, that is expected" and move on. A scenario here will **describe the variation**, put a **plausible defect** beside it, and ask what you tell the teammate who found it. The **scored answer** does two things. It **names the mechanism**, and then it says what the **application** does about it. A developer who stops at "that is expected" has **explained the behaviour** and **shipped nothing**.

**What the application does.**
- **Validation** (check the output has the shape you need).
- A **retry on failure**.
- **Sampling settings** where **consistency** matters more than **variety**.

None of these make the model repeat itself. They make the **surrounding system tolerant** of the fact that it will not. In kitchen terms, you cannot make the chef plate every dish identically. You add a check at the pass before the plate leaves.

**The shape to remember.** This answer comes up again and again: a **property of the technology**, then the **component that absorbs** it. An option with only the first half is **describing the world**. An option with only the second half treats a **permanent property as a bug** that has a fix.

**ELI5.** A chef making soup never makes it exactly the same twice. That is not a broken kitchen. So when it matters, you taste the soup before it goes out. You do not shout at the chef.

## A Token Is the Unit You Are Billed In, Limited By, and Debugging Against

**First, the idea.** A **token** is the scoop Claude works in. Three different things in this syllabus are counted in scoops.

**What a token is.** A **token** is the **smallest unit** the model works in. It maps to **words, subwords, characters or bytes**. It is not as tidy as one word each. For Claude, a token is **roughly 3.5 English characters**, and the ratio moves with the language.<sup>[2]</sup>

**Why it matters.** The definition is worth more than it looks. **Three separate things** in this syllabus are **measured in tokens**. People who have not absorbed the unit treat them as **three unrelated topics**.

| What is counted in tokens | Where it bites |
|---|---|
| Everything you send, on every request (the ingredients you hand the chef) | The bill, and how much of the window (the counter) is left |
| Everything the model generates (the dish that comes out) | The bill again, at a different rate, and the output cap |
| Everything the model spends reasoning before it answers (the chef thinking before plating) | The bill a third time, on work no human ever reads |

**The row that surprises people.** The **third row** is the one people miss. It is why the **effort setting** exists at all.

**ELI5.** Everything in the kitchen is counted in scoops. The scoops you hand over, the scoops that come out, and the scoops the chef spends thinking. You pay for all three.

## The Window Is Capacity, and Temperature Is Selection

**First, the idea.** The **context window** is how much fits on the counter. **Temperature** is how adventurous the chef is when picking the next scoop. These are two different things.

**The window (the counter).** The **context window bounds** how much material one request may carry. It is finite. It behaves as **working memory rather than storage**. **Accuracy and recall degrade** as it fills. Anthropic calls this **context rot**.<sup>[3]</sup>

**The confusion to clear up.** This is the most **productive confusion** in the chapter. It appears in **scenarios repeatedly**. It is always offered by a **colleague who sounds confident**.

**Temperature (how adventurous the chef is).** **Temperature** does not **affect capacity**. It **decides which candidate wins** at each step. It has no bearing on how much **text a request can carry**. So imagine a **transcript will not fit** and a colleague proposes **raising the temperature**. They have not proposed a weaker fix. They have proposed acting on a part of the request that has nothing to do with the problem. Turn it up or down and the wording of the failure changes, but the **failure stands**. A more adventurous chef does not make the counter bigger.

| Dial | What it changes | What it cannot change |
|---|---|---|
| Temperature and sampling settings (how adventurous the chef is) | Which token gets chosen from the candidates | How much input fits, and what the response costs |
| Context window (the counter) | How much material one request can hold and cross-reference | How varied or repeatable the wording is |
| `max_tokens` (the size of the plate) | How long the response may run | How much input fits |
| Effort (how long the chef thinks) | How many tokens are spent reasoning before answering | How much input fits |

**How to read the table.** Read it as **four separate machines** that happen to sit on the same request. The **capacity-versus-selection confusion** is the **named anti-pattern** here. It also runs the other way. If output wording is **inconsistent**, **trimming the input** does not repair it.

**A consequence that settles a whole class of question.** Say a scenario needs a **long document held together**. A reference in section nine has to resolve against something in section two. Both sections must be in the **same request**. That is **capacity**. No **sampling setting**, no **latency improvement** and no **output cap** has anything to say about it.

**ELI5.** The counter decides how much food you can lay out. The chef's mood decides which scoop comes next. Changing the chef's mood never makes the counter bigger.

## Reasoning Depth Is a Separate Setting From Model Choice

**First, the idea.** There is no single "how good do you want it" dial. There are **three settings**, they are **independent**, and the exam pulls them apart on purpose.

**The wrong assumption.** Developers arriving at this material tend to assume one **dial** called "how good do you want it", and that the dial is the **model name**.

**The three settings, plus one.**
- The **model** decides the **capability tier** (which chef you hired).
- **Thinking** decides whether the model **reasons visibly before answering** (the chef plans out loud before cooking). **Adaptive thinking** lets the model judge how much of that a given request needs.
- **Effort** controls how many tokens Claude spends when responding. It trades **thoroughness against token efficiency** on a single model. It is available on all supported models with no beta header.<sup>[4]</sup>
- **Fast mode** is different again. It buys up to **2.5 times higher** output **tokens per second** on supported Opus models, at **premium pricing**.<sup>[5]</sup>

**Quality or speed.** Two of these are **quality dials**. One is a **speed dial**. They are **priced differently**. That is the distinction a scenario tests.

| Setting | Buys you | Costs you |
|---|---|---|
| A larger model (a better chef) | Capability on genuinely harder work | Money per token, and usually latency |
| Thinking, or adaptive thinking (planning before cooking) | Reasoning before the answer, on work that needs it | Tokens the user never reads |
| Effort (how much planning happens) | Control over how much of that reasoning happens | Thoroughness, when turned down |
| Fast mode (a faster stove) | Output tokens per second | Premium pricing, on supported models only |

**A practical trap.** There is a **mechanical trap** under this. **Toggling thinking modes invalidates prompt caching**.<sup>[6]</sup> Prompt caching means reusing a part of the prompt you already sent, like prepped ingredients you do not have to buy again. Say a team turns thinking on for only a **subset of requests**, against a **large stable prefix** (the start of the prompt that stays the same) they had been paying to reuse. They have quietly **given up the reuse**. An interview never asks how two features interact like this. This exam does.

**ELI5.** Hiring a better chef, asking the chef to plan first, and buying a faster stove are three different choices. They are not one dial. And if you keep changing how the chef plans, the prepped ingredients can no longer be reused.

## Three Prompting Modes, Priced in Tokens

**First, the idea.** The cheapest technique in the book is showing Claude examples. People skip it because it feels too simple to be the answer.

**The three modes.**
- **Zero-shot** describes the task and **supplies no examples**.
- **One-shot** supplies a **single worked example**.
- **Multi-shot** supplies **several**.

**The trade.** Moving up that list **trades tokens for adherence** (how closely the output follows the shape you want). A description states a rule and leaves its edges to interpretation. A worked example shows one edge already decided. Say prose keeps producing the wrong capitalisation, or the wrong treatment of an awkward input. One decided case settles what another paragraph of instruction has not. In kitchen terms, a photo of the finished dish beats another paragraph describing it. The **cost recurs**, because the **examples ride along** with every request.<sup>[7]</sup>

**The scenario shape to recognise.** A team holds a **small set of labelled examples** that show exactly the output they want. The options offered are:
- **put them in the prompt**
- **store them in a database**
- **train a custom model**
- **warn users away** from the hard cases

Those examples are already what the technique runs on. Putting them in the prompt is the **shortest route** from what the team holds to the output it wants. Nothing has to be built before anyone can try it.

**The anti-pattern.** **Reaching past the cheap mechanism** is the **anti-pattern**, and it will be **dressed as rigour**. Training a custom model on a handful of labelled cases is not more serious than showing the model those cases. It is the **same information**, sent through a far more **expensive channel**, with a **deployment** to maintain afterwards.

**ELI5.** If you want the dish to look a certain way, show the chef a photo. Do not build a new kitchen to teach the chef one recipe.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here are **rarely absurd**. They describe **mechanisms that exist**, that work, and that a competent developer uses weekly. What makes one wrong is a **single assumption** underneath it. **Three assumptions** are worth memorising.

**The three wrong assumptions:**
- **A generation setting offered against a capacity problem.** **Temperature, `max_tokens` and sampling** all act on how the **response is produced** (what the chef does). None of them changes how much **input a request can carry** (what fits on the counter). Say a scenario is about **material that does not fit**. Then every option naming a sampling parameter is **wrong on mechanism**, not on **degree**.
- **Expected behaviour diagnosed as a defect.** **Run-to-run variation in wording**, with the **request unchanged**, is how **generation works**. An option that **confirms a bug**, **tickets** it, or **proposes pinning something** to remove it has **accepted a false premise**. The **corollary** matters too. An option that **explains the mechanism and stops** has not answered a question that asked what to do.
- **A heavier mechanism preferred to the one the material already fits.** **Training, retrieval infrastructure and separate applications** all turn up as answers to problems that a few **examples in the prompt** would settle. **Cost is the tell**. Ask what the **option needs built** before it can be **tried** at all.

**The table.** The table below is the **compressed form**. **Match** on what the **scenario** is doing, not on the **industry** it is set in.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Identical requests return differently worded responses | Name sampling as the mechanism, then say how the application validates, retries or constrains | Confirming a bug in request construction, or blaming the model version |
| A document is too long to process, or references across it are being lost | Capacity: fit it in one request, or split and carry state deliberately | A sampling parameter, a latency improvement, or a larger output cap |
| A small set of labelled examples of the desired output already exists | Put them in the prompt as examples | Training a custom model, or storing them somewhere the model never reads |
| Output quality is uneven on work that needs reasoning | Thinking or effort, chosen against what the tokens buy | A larger model offered as the only quality dial |
| Response speed is the stated problem, and quality is fine | The speed mechanism, priced accordingly | Anything that changes what the model produces rather than how fast |
| A stable prefix is being reused across many requests | Preserve the conditions the reuse depends on | Toggling a setting that silently invalidates it |

**A habit that works past the table.** When two options both **look reasonable**, ask which **mechanism** each one **acts** on. Then check which **mechanism the scenario named**. On this material the wrong option is almost always acting on a **real mechanism** that the **scenario never mentioned**.

**ELI5.** A wrong answer is usually a real kitchen tool used for the wrong job. Ask which knob it turns. Then ask whether that is the knob the problem is about.

## What to Remember

- A **token is the unit** of **billing**, of the **window**, and of **reasoning spend**. It is worth roughly **3.5 English characters** in Claude. **Input, output and thinking** are all counted in it, at **different rates**.
- Each **token is chosen by sampling**. So one **request run twice** can **return different text**, and that holds **even at temperature 0**. It is a **property of how generation works**, not a **defect** in how the request was built.
- **Temperature selects; the window holds**. A **capacity problem never responds** to a **sampling parameter**. **Inconsistent wording** never responds to **trimming the input**.
- The **context window is working memory, not storage**. It is **finite**, and **recall degrades** as it fills. Anthropic calls this **context rot**. **Anything that must be cross-referenced** has to be in the **same request**.
- **Model, thinking and effort** are **three independent settings**, not one **quality dial**. **Fast mode** is a **speed setting**. It buys output tokens per second at **premium pricing**, not capability.
- **Toggling thinking modes invalidates prompt caching**. So a **per-request thinking decision** can **silently cancel the reuse** a large stable prefix was earning.
- **Zero-shot, one-shot and multi-shot** trade **tokens for adherence**. Say a team already **holds labelled examples** of the output they want. Then **showing the model those examples** is the **cheapest mechanism that fits**. Reaching past it is the **standard wrong answer**.

**ELI5.** Claude is a chef who picks one scoop at a time, so no two plates match exactly. The counter is only so big, and the chef's mood does not change that. Hiring, planning and speed are separate choices. When you want a certain look, show a photo first.

## Endnotes for this chapter

1. Identical inputs can produce different outputs even with temperature set to 0, on Anthropic's own inference service and on third-party providers. Anthropic, *Glossary* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/glossary](https://platform.claude.com/docs/en/about-claude/glossary)

2. Tokens are the smallest individual units of a language model and can correspond to words, subwords, characters or bytes; for Claude a token approximately represents 3.5 English characters, varying by language. Anthropic, *Glossary* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/glossary](https://platform.claude.com/docs/en/about-claude/glossary)

3. The context window functions as working memory rather than storage, and accuracy and recall degrade as the token count grows, a phenomenon Anthropic names context rot. Anthropic, *Context windows* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/context-windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)

4. The effort parameter controls how many tokens Claude spends when responding, trading response thoroughness against token efficiency on a single model, and is available on all supported models with no beta header required. Anthropic, *Effort* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/effort](https://platform.claude.com/docs/en/build-with-claude/effort)

5. Fast mode delivers up to 2.5 times higher output tokens per second from supported Claude Opus models, at premium pricing. Anthropic, *Fast mode* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/fast-mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode)

6. Toggling thinking modes invalidates prompt caching. Anthropic, *Thinking* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)

7. Prompting techniques including the use of worked examples are documented as a means of improving adherence to a required output shape. Anthropic, *Prompt engineering overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
