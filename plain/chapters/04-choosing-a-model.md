# Chapter 4: A Model Choice Is Three Numbers You Were Not Given

**Summary**: *Some tickets list what a feature does and skip the quality, the speed and the cost. Every model fits such a ticket, so the ticket is unfinished. This chapter covers the three missing numbers, the tiers, and why a pinned model still shifts.*

## The Requirement Arrived With No Quality Bar, No Latency Ceiling and No Cost Per Unit

Say you run a courier firm. The job sheet ends with "use the best vehicle". Best at what? The vehicle is this chapter's analogy. It stands for the model.

A feature ticket has the same hole. Best judged by whom? Inside what wait? At what price? Those are three missing numbers, the **unstated triple**:

- the quality bar the output must clear (how well the parcel must arrive),
- the ceiling on how long someone will wait (the delivery window),
- the spend per unit of work (what each parcel may cost).

Until they exist, nothing can be traded off. With all three blank, four tiers can each be defended. So the question is underspecified, not hard.

Three shortcuts skip that talk.

- The borrowed leaderboard scores someone else's work and sets no threshold for yours.
- The mid-tier hedge quietly assumes values for all three and writes none down.
- The top tier by default spends everything on quality. It is the most common and most expensive mistake.

**ELI5.** "Bring the best vehicle" means nothing until you know how far, how soon and how much money. Ask first.

## Four Tiers, Ordered the Same Way by Price and by Capability

The yard holds four vehicles. From cheapest and weakest to dearest and strongest: Claude Haiku 4.5 (the bike), Claude Sonnet 5 (the car), Claude Opus 5 (the van), then Claude Fable 5 at the frontier (the lorry).<sup>[1]</sup>

| Tier, cheapest first | Per million tokens, in then out | Documented for |
|---|---|---|
| Claude Haiku 4.5 | $1 and $5 | Real-time work, high volume, subagents<sup>[2]</sup> |
| Claude Sonnet 5 | $2 and $10 | Code, analysis, content, visual understanding, tool use<sup>[2]</sup> |
| Claude Opus 5 | $5 and $25 | Multihour coding agents, refactors, vision-heavy work<sup>[2]</sup> |
| Claude Fable 5 | $10 and $50 | Long-horizon agents, deep reasoning, research<sup>[2]</sup> |

Names and prices drift. Check the lineup when you build. The pattern lasts. Each step up roughly doubles the per-token price.

Size can decide it. Claude Opus 5 gives a 1M token context window by default and up to 128k output tokens.<sup>[2]</sup> Claude Haiku 4.5 stops at 64k.<sup>[3]</sup> For one huge answer, the bike is out at once.

**ELI5.** Bigger vehicles carry more and cost about twice as much. Some loads will not fit on a bike.

## Price a Model on Cost Per Completed Task, and Price the Hardest Tenth

A lorry looks silly per mile. But you pay for parcels delivered, not per token. A stronger model needs fewer turns and less backtracking, so it often wins back the higher price.<sup>[1]</sup>

It can go either way. On one research benchmark, the frontier model at low effort beat the mid-tier model on accuracy and was about 10% cheaper per task. On a coding subset it flipped. Claude Opus 5 alone matched Claude Fable 5's accuracy at roughly 60% of the cost.<sup>[1]</sup>

Now the trap behind cheap-tier picks. On easy jobs every vehicle looks alike, so the bike wins. But failures set the bill. A failed task bills its tokens, then the retry, then the downstream damage. In a twenty-problem run, two problems ate 43% of the spend.<sup>[1]</sup>

Take the bike to its limit. On a graduate-level question set, Claude Haiku 4.5 cost a tenth of Claude Opus 5 per question. It scored 63% against 92%.<sup>[1]</sup> That suits output you can check. It hurts when a wrong answer travels on.

So price the hardest tenth. Switch tiers on evidence: an **eval**, a measured test on your own cases, promotes a model change. An argument does not. Step up when the bar is missed on your hardest cases. Step down when a cheaper tier holds. Chapter 19 covers evals.

**ELI5.** A bike suits letters. A broken fragile parcel costs a resend. Count the hard parcels.

## Reasoning Depth and Raw Speed Are Bought Separately From Capability

Model, thinking and effort are separate settings (chapter 1). Not every vehicle offers every setting, so a reasoning need can pick the model before cost does.

Effort needs no beta header and works on all supported models. It defaults to `high`. Levels are `low`, `medium`, `high`, `xhigh` and `max`, but some models lack the top ones.<sup>[4]</sup>

Adaptive thinking varies more.

- Claude Fable 5 and Claude Mythos 5 always have it on. Turning it off gives an error.<sup>[2]</sup>
- Claude Opus 5 starts with it on. It takes `thinking: {"type": "disabled"}` only at `high` effort or below.<sup>[5]</sup>
- Claude Haiku 4.5 lacks interleaved thinking.<sup>[6]</sup>

Effort moves speed too. `low` took 4.5 minutes per problem in Anthropic's test, against 7.9 at the default.<sup>[1]</sup>

One setting changes speed alone. **Fast mode** runs the same model on a faster inference setup, with the same intelligence and capabilities. On Claude Opus 5 and Claude Opus 4.8 it gives up to 2.5 times the output tokens per second. It costs $10 and $50 per million tokens, against the standard $5 and $25.<sup>[7]</sup> Picture an express lane: same vehicle, sooner, for a fee.

If speed is the problem, use lower effort, streaming or fast mode. A smaller tier changes the output. These do not.<sup>[8]</sup>

**ELI5.** An express lane gets the same truck there sooner for a fee. A smaller truck may do the job worse.

## A Model ID Is Frozen and the System Around It Is Not

A model ID is the name in your request. Since the 4.6 generation, IDs carry no date. Each is one fixed snapshot. Weights never change under an ID. A change ships as a new ID. Dateless does not mean "newest".<sup>[9]</sup>

Earlier models are the reverse. Their short name points to the most recent dated snapshot.

Pinning the ID does not pin everything. A bus number stays while the streets are rerouted. The serving layer (router, classifiers, sampling logic) keeps changing. If behaviour shifts on an ID nobody moved, suspect an infrastructure update.<sup>[9]</sup>

You cannot stay still forever. Models are deprecated, then retired, with at least 60 days' notice. Partner platforms set their own dates.<sup>[10]</sup>

Next, the "drop-in" myth: a new release is just a string change. The request shape survives. Other things do not.

- On Claude Opus 4.7 and later, a non-default `temperature`, `top_p` or `top_k` returns a `400`. So do manual thinking budgets and assistant prefill.
- A request with no thinking field ran without thinking on Claude Opus 4.8. On Claude Opus 5 it thinks. Those reasoning tokens now sit under a `max_tokens` cap sized without them.<sup>[5]</sup>

The quietest failure raises no error. Old instructions pile up, and a newer model obeys them literally. Prompts tuned for Claude Opus 4.8 cost 36% more per ticket on Claude Opus 5, with no gain in accuracy. An audit took 14% off while raising it.<sup>[1]</sup> Only the bill moved. So a model choice carries upkeep. Chapter 18 covers pinning.

**ELI5.** The bus number stays while the roads change. One day the line closes. A new bus may read your old note too literally.

## How Wrong Answers Are Built on This Material

Wrong answers describe what careful developers do: benchmark, pick mid-range, upgrade. The flaw is the hidden assumption.

- A target guessed, not obtained. A public score is no better: it tests work that is not yours and sets no threshold.
- One axis chosen, two unbudgeted. "Maximum capability" or "minimum price" ignores the other two numbers.
- A release treated as a string swap. Some damage is a loud 400. Some just costs more.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| No figures for speed, spend or quality | Get all three targets, then choose | Naming a tier or benchmark first |
| Spend is the problem, output quality holds | Cost per completed task, priced on the hardest tenth | Per-token price on the typical request |
| Latency is the problem, output quality holds | Effort, streaming, paid speed | A smaller tier, which changes the output |
| A working integration moves to a newer release | Re-test settings, prompts and token counts | Assuming a drop-in |
| A model in production has a retirement date | Migrate first, since later requests fail | Treating deprecation as optional, or trusting one platform's dates |

Ask of every option: which number does it move, and which two does it ignore?

**ELI5.** Wrong quiz answers fix one thing and ignore the other two. Ask what each does to quality, speed and cost.

## What to Remember

- Get the quality bar, latency ceiling and cost per unit before you shortlist.
- Capability and price rise together across the four tiers, roughly doubling per step.
- Compare on cost per completed task. Price the hardest tenth. A failure costs tokens, a retry and downstream damage.
- Evals decide model changes, up or down.
- `xhigh` and `max` are missing on some models. Adaptive thinking cannot be disabled at the frontier. Claude Haiku 4.5 lacks interleaved thinking.
- Fast mode is the same model, 2.5 times the output tokens per second, at double the standard rate.
- A dateless ID is a fixed snapshot. Pre-4.6 short names point to the latest dated snapshot. The serving layer still changes.
- Retirement makes requests fail after 60 days' notice. Loud breaks are 400s. The quiet cost is stale instructions followed literally.

**ELI5.** Ask how good, how fast and how cheap first. Count the costly failures.

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
