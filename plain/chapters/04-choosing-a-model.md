# Chapter 4: A Model Choice Is Three Numbers You Were Not Given

**Summary**: *A ticket arrives naming what the feature must do and nothing about how well, how fast or how cheaply. Under a ticket like that every model is defensible. That is the sign the ticket is incomplete, not that the decision is hard. This chapter covers the three figures missing from it, what separates the tiers, and why a model you pinned still shifts underneath you.*

## The requirement arrived with no quality bar, no latency ceiling and no cost per unit

**First, the idea.** Choosing a model is like hiring a worker for a job. The job brief (the **ticket**) says what the work is. It does not say how good the work must be, how long you can wait, or how much you can pay. Without those three, you cannot pick anyone sensibly.

**The analogy for this chapter.** You are the manager hiring a worker (the **model**). The workers come in four levels of seniority (the **tiers**). Each charges a rate (the **price per token**). The job brief is the **ticket**. Each time the analogy comes up, the real term is in bold beside it.

**What the ticket has.** The **ticket is complete** on its own terms: what the feature does, the acceptance criteria, the edge cases, the owner, the date. At the bottom is **one line** asking you to use **whichever Claude model** gives the **best results**.

**The problem.** That line is a **hole with a sentence** in front of it. Best judged by whom? Inside what **wait**? At what **price**?

**The three missing figures.** Call them the **unstated triple**:
- the **quality bar** the output must clear (how good the finished work has to be)
- the **ceiling** on how long somebody will sit waiting (the deadline, or **latency ceiling**)
- the **spend** the business carries per unit of work (the budget, or **cost per unit**)

Nothing can be traded until somebody says what it is **traded against**. While all **three stay blank**, every tier is arguable. **Four defensible answers** mean the question is **underspecified**, not hard. People give you **functional requirements** (what the feature does) without being asked. The triple has to be **asked** for.

**Three ways to skip that conversation.** They all look like progress:
- The **borrowed leaderboard** scores work that is not yours and **sets no threshold**. It is like hiring on someone else's reviews.
- The **mid-tier hedge** guesses all three figures and **records none**. It is like always hiring the middle person.
- The **top of the range by default** spends everything on quality and leaves the **other two unbudgeted**. It is like always hiring the most senior person. This is the standard and most expensive mistake here.

**ELI5.** Imagine you ask a grown-up to hire someone to paint a room. You forgot to say how neat it must be, by when, and how much money you have. Now any painter could be right. So first you say those three things, then you pick.

## Four tiers, ordered the same way by price and by capability

**First, the idea.** Once you have the three numbers, the choice is short. There are four levels of worker. The more senior the worker, the more they can do and the more they charge.

**The ladder.** From **lowest cost and capability to highest**: Claude Haiku 4.5, Claude Sonnet 5, Claude Opus 5, then Claude Fable 5 at the frontier (the most capable).<sup>[1]</sup>

| Tier, cheapest first | Per million tokens, in then out | Documented for |
|---|---|---|
| Claude Haiku 4.5 (the junior) | $1 and $5 | Real-time work, high volume, subagents<sup>[2]</sup> |
| Claude Sonnet 5 (the regular) | $2 and $10 | Code, analysis, content, visual understanding, tool use<sup>[2]</sup> |
| Claude Opus 5 (the senior) | $5 and $25 | Multihour coding agents, refactors, vision-heavy work<sup>[2]</sup> |
| Claude Fable 5 (the expert) | $10 and $50 | Long-horizon agents, deep reasoning, research<sup>[2]</sup> |

"In then out" means **input tokens** (small chunks of text you send) first, then **output tokens** (chunks Claude writes back).

**Names and rates move**, so confirm the lineup when you build. The shape lasts longer than the list. Each step up roughly **doubles the per-token price**, and capability climbs with it.

**Size can decide it on its own.** Claude Opus 5 serves a **1M token context window** by default and up to **128k output tokens**<sup>[2]</sup>. Claude Haiku 4.5 **caps output at 64k**.<sup>[3]</sup> So if you need one very long answer, a tier is **ruled out** before quality even comes up.

**ELI5.** There are four helpers, from a junior to an expert. The better the helper, the more they charge. Sometimes the job is just too big for the junior, so you do not need to compare them at all.

## Price a model on cost per completed task, and price the hardest tenth

**First, the idea.** Do not compare workers by hourly rate. Compare them by what the whole finished job costs.

**Why per token is the wrong unit.** Per token, the frontier looks extravagant. But you are buying finished work. A more capable model finishes with **fewer turns**, less searching and less backtracking. That routinely **swallows the premium**.<sup>[1]</sup> A senior worker who needs one pass can cost less than a junior who needs five.

**The direction is not fixed.** On one research benchmark, Anthropic measured the frontier model at low effort as more accurate and about **10% cheaper per task** than the mid-tier model. On a coding subset it went the other way. Claude Opus 5 alone matched Claude Fable 5's accuracy at **roughly 60% of the cost**.<sup>[1]</sup>

**The trap: the median priced and the tail ignored.** On the typical request, every tier looks alike, so the cheapest looks best. But the bill is set by the requests that fail. A failed task **bills its tokens**. Then the retry bills again. Then there is the **downstream damage**. Here are two examples:
- In one twenty-problem run, two problems carried 43% of the spend.<sup>[1]</sup>
- At the floor, Claude Haiku 4.5 answered a graduate-level question set at a **tenth of Claude Opus 5's cost** per question. It scored 63% against 92%.<sup>[1]</sup>

The cheap tier is excellent where **output is checkable**. It is poor where a **wrong answer travels** (gets passed on and acted on).

**What to do.** An **eval** (a repeatable test of the model on your own cases) **promotes a model change**. An argument does not.
- **Step up** when a measurement shows the tier missing the bar on your hardest cases.
- **Step down** when a measurement shows a **cheaper tier holding** the bar.

Chapter 19 covers the eval.

**ELI5.** Do not ask how much each worker costs per hour. Ask how much it costs to get the job done right. And look at the hardest jobs, because that is where cheap workers fail and you pay twice.

## Reasoning depth and raw speed are bought separately from capability

**First, the idea.** A worker's seniority is one thing. How long they think before answering, and how fast they work, are separate dials.

**Settings are independent.** Chapter 1 showed that **model, thinking and effort** are separate settings. What matters for choosing is that the **tiers do not all offer** the same settings. So a reasoning requirement can decide the model before cost does.

**What each setting does:**
- **Effort** runs on all supported models with no beta header. It defaults to `high`. The levels are `low`, `medium`, `high`, `xhigh` and `max`. The **top levels are absent on some models**.<sup>[4]</sup>
- **Adaptive thinking** (the model decides how much to think) varies more. Claude Fable 5 and Claude Mythos 5 have it always on, and **disabling it errors**.<sup>[2]</sup> Claude Opus 5 runs it by default. It accepts `thinking: {"type": "disabled"}` only at **`high` effort or below**.<sup>[5]</sup>
- Claude Haiku 4.5 has **no interleaved thinking** (thinking between tool calls).<sup>[6]</sup>
- **Effort is a latency lever** too. Anthropic measured **`low` at 4.5 minutes per problem** against 7.9 at the default.<sup>[1]</sup>

**Fast mode (paying for a rush).** One lever changes latency and nothing else. **Fast mode** runs the same model on a **faster inference configuration**. Intelligence and capabilities do not change. It gives up to **2.5 times the output tokens per second** on Claude Opus 5 and Claude Opus 4.8. The price is $10 and $50 per million tokens, against the standard $5 and $25.<sup>[7]</sup> You pay money for speed. Quality stays the same.

**What to do when speed is the problem.** If quality is already fine, use **lower effort**, streaming, or **fast mode**. They leave the output alone. **Dropping a tier does not**, because a different tier produces different work.<sup>[8]</sup>

**ELI5.** You can ask the same worker to think less, or pay extra to have them work faster. Their skill stays the same. Swapping to a cheaper worker is different, because the work itself changes.

## A model ID is frozen and the system around it is not

**First, the idea.** The worker you hired keeps the same skills. But the office around them can change, and the worker can be retired.

**What a model ID is.** From the 4.6 generation onward, **model IDs are dateless**. Each names one **fixed snapshot**. **Weights are never updated** under an existing ID. An update ships as a new ID. The common mistake is to think a dateless ID points to whatever is newest.<sup>[9]</sup>

**Earlier models work the other way.** On earlier models the **short name is a pointer**. It resolves to the **most recent dated snapshot**. So you have two strings that look alike and **promise opposite things**.

**A pinned ID is not a frozen system.** The **serving layer** around the weights keeps changing. That means the router, the classifiers and the sampling logic. If behaviour shifts on an ID nobody moved, an infrastructure update is the likely cause.<sup>[9]</sup>

**You cannot stay put forever.** Models are deprecated, then retired, with at least **60 days' notice**. **Requests after that date fail**. Partner platforms keep their own schedules.<sup>[10]</sup>

**The trap: the drop-in that is only a string change.** The request shape survives a new generation. Several other things do not:
- On Claude Opus 4.7 and later, a non-default `temperature`, `top_p` or `top_k` **returns a `400`**. So do manual thinking budgets and assistant prefill.
- A request without a thinking field ran **without thinking** on Claude Opus 4.8. It thinks on Claude Opus 5. That puts **reasoning tokens** under a **`max_tokens` cap** that was sized without them.<sup>[5]</sup>

**The quietest failure raises nothing.** Over time you add instructions for the model that needed them. A **newer model obeys them literally**. Prompts tuned for Claude Opus 4.8 **cost 36% more per ticket** on Claude Opus 5, with no gain in accuracy. An **audit took 14% off** the cost while raising accuracy.<sup>[1]</sup> Nothing breaks. The bill just moves. So a model choice comes with a **maintenance schedule**. Chapter 18 covers pinning it.

**ELI5.** Your worker never changes their skills. But the building they work in can get new rules, and one day the worker retires. A new worker may follow your old notes too literally, and you pay for that quietly.

## How wrong answers are built on this material

**First, the idea.** Wrong answers here describe things a careful developer really does: benchmarking, picking a **mid-range model**, **upgrading to the newest release**. What makes one wrong is the **assumption underneath**.

**Three wrong assumptions:**
- **A target guessed instead of obtained.** The option names a tier, a model or a benchmark, but the **quality bar**, the **wait** and the **spend** are all blank. A **public score has the same flaw**. It **measures work that is not yours** and **sets no threshold**.
- **One axis optimised and two left unbudgeted.** Going for **maximum capability**, or **minimum price**, treats the decision as one-dimensional. Ask what an option silently does to the **other two numbers**.
- **A release treated as a string swap.** The **identifier is assumed to carry** the prompt, the settings and the token arithmetic along. Some of that **breaks loudly with a 400**. Some only **costs more**.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Functional requirements only, no figures for speed, spend or quality | Obtain all three targets, then choose against them | Naming a tier or a benchmark before the figures exist |
| Spend is the problem, output quality holds | Cost per completed task, priced on the hardest tenth | A per-token price judged on the typical request |
| Latency is the problem, output quality holds | A lever that leaves the output alone: effort, streaming, paid speed | A smaller tier, which changes what is produced |
| A working integration moves to a newer release | Re-baseline settings, prompts and token counts | Assuming a drop-in because the request shape held |
| A model in production has a retirement date | Migrate before it, because later requests fail | Treating deprecation as advisory, or trusting one platform's dates |

**A habit that works past the table.** For every option, say which of the **three numbers it moves** and which two it leaves unstated.

**ELI5.** Most wrong answers pick a worker without knowing the quality, the deadline and the budget. Or they fix only one of the three and forget the others. Or they swap in a new worker and assume nothing else changes.

## What to remember

- The **unstated triple** is the **quality bar**, the **latency ceiling** and the **cost per unit** of work. **No model is defensible** until all three exist, so obtain them before shortlisting.
- **Capability and price** rise together across **Claude Haiku 4.5**, **Claude Sonnet 5**, **Claude Opus 5**, **Claude Fable 5**. Each step roughly **doubles the per-token price**. Rosters go stale, so **confirm the lineup** when you build.
- Compare on **cost per completed task**, not per token, because a stronger model uses fewer turns. **Price the hardest tenth**: a **failed task bills** its **tokens**, the **retry**, and the **downstream damage**.
- An **eval promotes a model change**, both ways. **Step up** when a measurement shows the **bar missed** on your **hardest cases**. **Step down** when one shows a **cheaper tier holding** it.
- Reasoning modes vary by model. **`xhigh` and `max` are absent** on some. **Adaptive thinking** is always on at the frontier and **cannot be disabled** there. **Claude Haiku 4.5** has **no interleaved thinking**.
- **Fast mode buys latency alone**: the **same model**, **no capability change**, **2.5 times the output tokens** per second, at double the standard rate.
- A **dateless model ID** is a **fixed snapshot**, never a pointer to the newest. **Pre-4.6 short names point** at the latest dated snapshot. **Weights stay fixed** and the **serving layer does not**.
- A **release changes behaviour, not just an identifier**, and **retirement makes requests fail** after **60 days' notice**. Loud breaks are **400s** on **sampling parameters**, **thinking budgets** and **prefill**. The quiet cost is money, when **stale instructions** are obeyed literally.

**ELI5.** Before hiring, say how good, how fast and how cheap. Judge workers by the cost of the finished job, not the hourly rate. The worker keeps their skills, but the office and the rules around them change over time.

## Endnotes for this chapter

1. Cost and intelligence levers, including the ordering of the current models from lowest to highest cost and capability; the instruction to compare models on cost per completed task because a more capable model finishes with fewer turns and less backtracking; the DeepResearch Bench II result in which the frontier model at low effort was more accurate and about 10% cheaper per task than the mid-tier model; the SWE-bench Pro subset result in which Claude Opus 5 alone matched Claude Fable 5 within run-to-run noise at about 60% of the cost; the instruction to price the hardest tenth of a workload rather than the median, and the WideSearch run in which two of twenty problems carried 43% of the spend; the GPQA Diamond comparison in which Claude Haiku 4.5 answered at about a tenth of Claude Opus 5's cost per question at 63% against 92%; the effort latency figures of 4.5 minutes per problem at low effort against 7.9 at the default; and the support-desk audit in which prompts written for Claude Opus 4.8 cost 36% more per ticket on Claude Opus 5 for no change in accuracy, while running the audit made the same work 14% cheaper and raised accuracy from 92% to 97% of tickets. Anthropic, *Optimizing for cost and intelligence* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)

2. The documented starting points and example use cases for the four current tiers (Fable 5, Opus 5, Sonnet 5, Haiku 4.5); Claude Opus 5's 1M token context window by default and 128k maximum output tokens; the always-on adaptive thinking of Claude Fable 5 and Claude Mythos 5, on which no thinking configuration is required and a disabled setting returns an error; and per-tier list prices of $10 and $50, $5 and $25, $2 and $10, and $1 and $5 per million input and output tokens. Anthropic, *Choosing the right model* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/choosing-a-model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)

3. Output limits by model: the current frontier and Opus-class models, together with Sonnet 5, Opus 4.6 and Sonnet 4.6, support up to 128k output tokens per request, while Haiku 4.5, Sonnet 4.5 and Opus 4.5 support up to 64k. Anthropic, *Thinking* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)

4. The effort parameter is available on all supported models with no beta header, defaults to high, and offers the levels low, medium, high, xhigh and max, with xhigh a newer level that some models supporting max do not offer. Anthropic, *Effort* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/effort](https://platform.claude.com/docs/en/build-with-claude/effort)

5. Migration behaviour across recent releases: thinking runs by default on Claude Opus 5 where a request without a thinking field ran without thinking on Claude Opus 4.8, with `max_tokens` remaining a hard limit on thinking plus response text; disabling thinking is accepted only at effort high or below and is validated on each request; setting `temperature`, `top_p` or `top_k` to a non-default value returns a `400` error on Claude Opus 4.7 and later; manual extended thinking with `budget_tokens` returns a `400` error; and prefilling the assistant message returns a `400` error. Anthropic, *Migration guide* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/migration-guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)

6. Interleaved thinking is automatic on every model that supports adaptive thinking and requires no beta header, and Claude Haiku 4.5 does not support interleaved thinking. Anthropic, *Thinking* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)

7. Fast mode delivers up to 2.5 times higher output tokens per second from Claude Opus 5 and Claude Opus 4.8 at premium pricing, runs the same model on a faster inference configuration with no change to intelligence or capabilities, and is priced at $10 per million input tokens and $50 per million output tokens on the supported models. Anthropic, *Fast mode* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/fast-mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode)

8. Selecting an appropriate model is one of the most direct ways to reduce latency, with Claude Haiku 4.5 offering the fastest response times, alongside minimising input and output tokens and streaming to improve perceived responsiveness. Anthropic, *Reducing latency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency)

9. Model IDs identify a pinned version whose underlying model stays constant for the lifetime of that ID; from the 4.6 generation onward IDs are dateless and each is the canonical fixed snapshot rather than an evergreen pointer to the latest or best-performing version, with updates shipping under a new ID; models before that generation have short aliases on the Claude API that resolve to the most recent dated snapshot; and the serving infrastructure around a model, including the request router, safety classifiers and sampling logic, can change and occasionally produce minor differences in observable behaviour on an unchanged model ID. Anthropic, *Model IDs and versioning* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)

10. Anthropic provides at least 60 days' notice before retiring a publicly released model, requests to models past the retirement date will fail, and partner-operated platforms including Amazon Bedrock and Google Cloud set their own retirement schedules so a model's lifecycle status and dates can differ. Anthropic, *Model deprecations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/model-deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)
