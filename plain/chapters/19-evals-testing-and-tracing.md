# Chapter 19: A Test Says It Broke; a Trace Says Where

**Summary**: *Four questions run this chapter and each one asks where. First, where an error's cause sits. That decides whether waiting is a remedy. Second, where in the run a failure happened. Only a step-by-step record answers that. Third, where in the stack it started: your integration layer or the model's output. Most scenarios turn on this one. Fourth, where in a population a measurement holds. That decides what an average may tell you. Get the location wrong and every fix after it is aimed at the wrong thing.*

## A Green Suite Is a Claim About Parts, Not About the Product

**First, the idea.** A test suite can pass while the product is wrong. This section is about why, and the analogy for the whole chapter comes from here. Think of a **restaurant kitchen**. Each cook at a station is a **component** (one function or one step). A **check** is a taste of one thing at one point. The **pass** (the hatch where plates are handed over) is a **seam** (the join between two components).

**What happened?** The **retrieval function passes** its unit tests. So does the **prompt builder**, and a check confirms the model call returns the fields the parser wants. Run your flow end to end and it answers a policy question from **general knowledge** instead of from the **retrieved policy**, with **nothing raised anywhere**. In the kitchen: the sauce cook (retrieval) makes a perfect sauce and the plating cook (prompt builder) plates perfectly. But the sauce goes onto the plate in a form the plating cook does not recognise, so the dish goes out plain. Each cook passed their own taste test.

**The join broke.** Retrieval hands back a **list of records**, the builder expects text, and the assembled prompt carries something the model reads as noise. Both components are correct. **Nobody wrote the contract** between them (the agreement on what gets handed over and in what shape), so nothing exercised it.

**Field of view.** Every check observes a **bounded field of view** (the part of the run it can see): one function, one call, one flow, one number. A failure is findable only by a check whose field of view contains it. A **seam belongs to neither component** beside it. So it sits inside nobody's field of view until you build a check whose **field of view is the seam**. In the kitchen, that means tasting the plate at the hatch, not tasting each cook's work at their station.

**The anti-pattern.** **Coverage counted in components** is the anti-pattern, and the count is what makes it convincing. Every part is covered. The **joins are not parts**.

**ELI5.** Every cook can pass their own taste test and the meal can still come out wrong. That happens when nobody checks the handover from one cook to the next. So you need a check that looks at the handover itself.

## An Error's Bucket Is Where Its Cause Lives, Not Which Status Code Carried It

**First, the idea.** When your application throws an error, you sort it into one of two buckets. The sorting question is about the cause, not about the number in the status code.

**The one question.** One question sorts every failure your application throws. Could the **clock alone change the outcome**? In the kitchen, ask: if the customer just waited ten minutes, would the dish arrive?

**Yes: the cause is the state of the world.** The cause sits in the **state of the world**. Capacity, load, a per-minute limit, a dropped connection. This is the **busy kitchen**: too many orders at once, so wait your turn. The documented shapes are **`429` rate limits**, **`529` overloads**, **5xx server faults** and **timeouts**.<sup>[1]</sup> Waiting is a **real remedy** for those alone.

**No: the cause is the request.** If no, the **cause sits in the request**. This is the **wrong order ticket**: no amount of waiting fixes a ticket for a dish that is not on the menu. Examples are a malformed body, a revoked key, a permission the credential lacks, a resource that is not there: **`400`**, **`401`**, **`403`**, **404**.<sup>[1]</sup> Every later send returns the **identical error**. **Repair** it or **reject** it. Neither of those is a retry.

**The mapping is only a hypothesis.** Two documented cases break it in opposite directions.
- A **spend-cap `429` carries no `retry-after`** and keeps failing until access resumes.<sup>[1]</sup> It is the same status in the other bucket, with the **missing header as the tell**.
- A request too large for the context runs the other way. Claude Code **lowers `max_tokens`** and sends a different request, rather than repeating one that **fails identically**.<sup>[2]</sup>

**The anti-pattern.** The **status code read as the diagnosis** is the anti-pattern. The code proposes a cause. The header, the message and the request ID settle it.<sup>[1]</sup>

**ELI5.** Ask one thing: if we just waited, would it work? If yes, wait. If no, the order itself is wrong, so fix it or send it back. The number on the error is only a hint about which one it is.

## Misclassifying Costs Silence in One Direction and Noise in the Other

**First, the idea.** You will sometimes put an error in the wrong bucket. The two mistakes do not cost the same, so it helps to know which one to prefer when you are unsure.

**Terminal treated as retriable (silence).** Call a **terminal failure retriable** (one that can never succeed, treated as one worth trying again) and every attempt is **guaranteed to fail**. Your **budget drains**. The real error surfaces late, wearing the shape of slowness. On a rate limit, each attempt **deepens the limit** that caused it. In the kitchen, it is like sending the same wrong ticket back again and again while the cooks waste time on it.

**Retriable treated as terminal (noise).** Call a **retriable failure terminal** and a condition that would have cleared in seconds reaches a person as a **broken feature**. That one gets **reported the same day**. The first looks like latency and runs for months. So terminal is the **cheaper guess** when the cause is unclear.

**A second, separate question.** A second question sits underneath and it is not the same one. Has **anything already happened**? **Retriability** is a **property of the cause**. **Safety** is a property of what a **first attempt committed**. Claude Code will not re-issue a request that failed after Claude had completed a tool call, because the retry would **run those calls twice**.<sup>[2]</sup> In the kitchen, if the first attempt already cooked and served a dish, sending the order again means a second dish. Any retry crossing a **boundary that writes** is a second write unless the write is **idempotent** (doing it twice has the same effect as doing it once).

**Routing.** Where recovery stops is a routing decision. Retry mechanics themselves belong to chapter 2. **Impact and recoverability predict** whether a person must act now. **One severity predicts nothing**.

**ELI5.** If you wrongly keep retrying something that can never work, you waste money and nobody notices for months. If you wrongly give up on something that would have worked in a minute, someone complains today. So when you are not sure, treat it as one that will not work. Also, never redo something that already happened unless doing it twice is harmless.

## A Trace Records Each Step, and It Gets Built Before the Failure

**First, the idea.** A test tells you that something broke. A **trace** tells you where. In the kitchen, a test is the customer saying "this dish is wrong". The trace is the **ticket log** that shows every station the order passed through, what each cook received, what they sent on and how long it took. It has to be switched on before the bad dish, because you cannot add a log afterwards.

**What a trace is.** A **test reports** that a failure exists. Nothing in a pass or a fail says which step produced it. A **trace is that missing record**: every step of the run with its **prompt**, its **tool calls**, its **intermediate output** and its **timing**. So the **failing step** is visible instead of reconstructed.

**The shape worth copying.** The Agent SDK shows the shape worth copying.
- Each **turn of the loop** is a span (one timed step in the record).
- Each API call is a child span carrying **model name, latency and token counts**.
- Each tool invocation is a child span with the **permission wait separated** from the execution.
- A **subagent's spans nest** under the parent's tool span, so a delegation chain reads as one trace.<sup>[3]</sup>

**Two properties that decide what the record is good for.**
- **Telemetry is structural by default.** It carries **durations, model names and tool names** but not the **content** the agent reads and writes. Content is **opt-in**.<sup>[3]</sup> So the default trace says which step and how long, and never what was said.
- **Export fails quietly.** An **unreachable collector** (the place telemetry is sent) leaves the agent running and the **telemetry dropped**, with no error raised in your application.<sup>[3]</sup> The instrument has the same failure mode as the thing it watches.

**ELI5.** A test is a customer saying the food is wrong. A trace is the ticket that shows every cook the order passed through. You have to start keeping that ticket before anything goes wrong. By default it records who and how long, not what was said. And if the ticket box is unplugged, nobody gets told.

## The Model's Output Is the Line, and You Read It Before Blaming Either Side

**First, the idea.** When a run gives a wrong result, the fault is either in the **model's output** or in your **integration layer** (the code around the model). To tell which, you look at what the model returned, before anything downstream touched it. In the kitchen, this is looking at the dish as it left the chef, before the waiter touched it.

**The check.** Go to the trace and **read what the model returned**, before anything downstream touched it. Three readings exhaust the cases.

| What the trace shows | Where the fault is | What changes |
|---|---|---|
| Returned content is what was wanted, and the system did the wrong thing with it | Below the model | The parser, the handoff, the tool wrapper, the dispatcher |
| Returned content is wrong, and the input was truncated, malformed or missing its retrieved context | Still below the model | The step that built the input |
| Returned content is wrong, and the input arrived complete and well formed | The model's output | Examples, constraint, prompt, model choice |

**The middle row costs teams weeks.** It presents as a model failure, and every remedy aimed at the model leaves it standing. Hence the rule: a **model failure** is a model failure only after you have **read the input the model received**. **Read what was sent**, never the template meant to produce it. Configuration debugging runs the same two steps. First confirm the **instruction reached the context window**. Once it has, the problem is how it is written.<sup>[4]</sup>

**Identity across a boundary.** A failure crossing a boundary **carries its identity or loses it**. Chapter 6 covers the tool-result half, where **`is_error`** lets the model react to a failure it would otherwise read as data.<sup>[5]</sup> The general point belongs here. Take one message standing for an **invalid identifier**, an **expired token**, a **timeout** and a **policy refusal**. It has discarded the distinctions recovery runs on. **Recovery can be no more specific** than the error reaching it.

**ELI5.** Before you blame the chef, look at the dish as it left the kitchen pass. If it was good and went wrong later, the fault is in the serving. If the chef was handed the wrong ingredients, the fault is still upstream of the chef. Only a bad dish made from good ingredients is the chef's fault. And if every problem is reported as "something went wrong", nobody can tell what to fix.

## An Average Is Only a Fact About the Population It Averaged

**First, the idea.** An **eval** (a repeatable test of the model's output on a fixed set of cases) tells you whether a change helped overall. It cannot tell you where anything broke, and an average can hide who it helped and who it hurt. In the kitchen, an eval is a **taste test across a fixed menu of dishes** after you change the recipe.

**What an eval is for.** An **eval** is the check whose field of view is the **whole run's output**. It cannot say where **anything broke**. What it answers is narrower and nothing else answers it: did your **change help**, on a **fixed set of cases**.

**Build for coverage before rubric.** A rubric is the scoring guide. Coverage is how many of the right dishes are on the test menu.
- Anthropic's guidance is that **20 to 50 tasks** drawn from **real failures** make a good start. Cases where a behaviour should occur and cases where it should not both belong.<sup>[6]</sup>
- A **judge** (a model that scores the output) returns a confident-looking number. It means nothing until its **agreement with expert human judgement** has been measured and recalibrated as things move.<sup>[6]</sup>
- Ambiguity in a task specification becomes **noise in the metric**. So the standard for a case is that **two domain experts** reach the same verdict independently.<sup>[6]</sup>

**Then granularity.** An **overall figure licenses nothing** about any segment inside it. Slicing by category requires the **record to carry the category**, because nothing can be measured along an **axis the data does not hold**. So adding that field is your first move whenever performance differs by group. A flat average is also consistent with a change that **repaired one group and broke another**. That is why you read the per-case results rather than the mean alone. In the kitchen, "customers rate us 4 out of 5" can hide that the pasta got better and the fish got worse.

**ELI5.** A taste test over a fixed menu tells you if the new recipe is better overall. But the overall score can hide that one dish got better and another got worse. So write down which kind of dish each one is, and look at each dish, not only the average.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here are **competent engineering** aimed one step **too early** or one level **too coarse**. **Four assumptions** produce most of them.

**The four wrong assumptions:**
- **A remedy applied before the cause is located.** Examples are **lowering a sampling setting**, **swapping the model**, **raising a threshold** and **adding a validator**. Each is a real fix offered while the **failing step is unknown**. Each is correct only once the scenario has isolated the break. This is changing the recipe before you know which cook caused the problem.
- **A distinction collapsed rather than restored.** Examples are **one severity for every error**, **one message for every backend fault**, **one confidence cut** for every outcome, and an **empty result** standing in for a failure. The scenario usually names the collapse as the symptom. The option offering more of it reads as **tidying**.
- **An aggregate offered where a segment was named.** Examples are a **global threshold**, one **overall accuracy figure** and **review spread evenly across categories**. All are right when the **population is uniform**, which the scenario has usually just denied.
- **Repetition where the request itself has to change.** Examples are **retrying a rejection**, **duplicating requests** against a rate limit, **retrying unbounded** and adding a **fresh credential** to a throttle. These are correct only where **time was the variable** that could move.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| A status names a temporary pacing or capacity condition | Back off with a cap, honouring the wait the service supplies | A fresh credential, a duplicated request, or dropping the failing check |
| The same request sometimes succeeds and sometimes fails | Capture full input and output on both sides, then compare | Changing a parameter, counting the frequency, or filing it as expected |
| Every component passes its tests and the flow is wrong | Exercise the handoff with real output from the producing step | More component tests, or the model blamed for the result |
| One overall figure is quoted and errors are known to cluster by category | Record the category on each item, measure per category, sample inside the clusters | A global threshold, acting on the aggregate, or reviewing only low-confidence items |
| Part of a job failed and the rest succeeded | Report the failed part: what was attempted, the failure type, any partial result | Returning empty, aborting everything, or retrying unbounded |

**A habit that works past the table.** One **habit transfers**. For any option offered as a fix, ask what it would have to **observe** to be right. Then check whether **anybody in the scenario is observing** it.

**ELI5.** Most wrong answers fix something before anyone knows what broke. Or they squash different problems into one, or trust one average for everyone, or just try again when the order itself is wrong. Before you pick a fix, ask who has actually looked at the thing that fix depends on.

## What to Remember

- Every check has a **field of view**, the **bounded span of the run** it can see: one function, one call, one flow, one number. A **seam sits inside neither component**, so a suite where **every part passes** claims something about **parts, not about the product**.
- One **question sorts** an error: could the **clock alone change the outcome**. Yes is a **transient cause** where **waiting** is the remedy, as in **`429`, `529`, 5xx and timeouts**. No puts the cause in the **request**, leaving **repair or rejection**, as in **`400`, `401`, `403` and `404`**. The status only **proposes a cause**. A **spend-cap `429` carries no `retry-after`** and **never clears** on its own.
- The two misclassifications **cost differently**. **Terminal treated as retriable drains the budget**, **delays** the real error and **deepens a rate limit**. **Retriable treated as terminal** shows a **broken feature** and gets **fixed the same day**, so raise it as **terminal when unsure**. Separately, **retriability** is a property of the **cause** and **safety** is a property of what **already happened**. A retry across a **boundary that writes** is a **second write** unless it is **idempotent**.
- A **trace records each step** with its **prompt, tool calls, intermediate output and timing**. It turns "a **case failed**" into "**step four failed**, and here is what it received". Default telemetry is **structural**, holding **durations, model and tool names** but **no content** until content is **opted** in.
- **Isolate origin** by reading what the **model returned** before anything downstream touched it. **Right output, wrong behaviour** is the **integration layer**, and so is **wrong output** from a **truncated or malformed input**. Only wrong output from a **complete, well-formed input** answers to **prompts, examples or model choice**.
- A **failure crossing a boundary carries its identity** or loses it, and **recovery is no more specific** than the error reaching it. One message covering an **invalid identifier**, an **expired token**, a **timeout** and a **refusal** has **discarded what recovery runs** on.
- An **eval measures** whether a change helped, never where it **broke**. **Coverage beats rubric polish**: **20 to 50 cases** drawn from **real failures**, including cases where the **behaviour should not occur**. A **judge means nothing** until its agreement with **human labels is measured**.
- An **average** is only a fact about the **population it averaged**. Nothing can be **sliced along an axis** the **record does not carry**. So **record the category** first and **read the per-case results**, because a **steady mean** hides a **repair to one group** and a break in another.

**ELI5.** A kitchen can pass every taste test at every station and still serve a bad plate, because the handover was never checked. When an order fails, ask if waiting would help. If it would not, fix the order. Keep a ticket log so you can see which station went wrong. And do not trust one average score for the whole menu.

## Endnotes for this chapter

1. The Claude API returns a predictable set of HTTP error codes: `400` `invalid_request_error`, `401` `authentication_error`, `402` `billing_error`, `403` `permission_error`, `404` `not_found_error`, `409` `conflict_error`, `413` `request_too_large`, `429` `rate_limit_error`, `500` `api_error`, `504` `timeout_error` and `529` `overloaded_error`; a `429` raised by reaching a usage tier's spend cap carries no `retry-after` header and keeps failing until access resumes; the official SDKs automatically retry transient failures such as connection errors, rate limits and 5xx server errors with exponential backoff, twice by default, honouring the `retry-after` header when present, and each SDK client accepts a maximum-retries option to configure or disable that behaviour; every API response carries a unique `request-id` header, and the same identifier appears as the `request_id` field in error response bodies for tracking and debugging. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

2. Claude Code retries transient failures up to 10 times with exponential backoff before showing an error, covering server errors, overloaded responses, request timeouts, dropped connections and temporary `429` throttles; a request rejected because the input plus `max_tokens` exceeds the context limit would fail the same way if re-sent unchanged, so Claude Code retries with a reduced `max_tokens` instead; it does not retry a TLS certificate validation failure, nor a server error, dropped connection or stalled stream arriving after Claude has completed a block of text or a tool call, because re-running the request could execute the same tool calls twice, so it keeps what Claude completed, shows an incomplete-response notice and continues the turn from the results of any tool calls Claude completed. Anthropic, *Error reference* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/errors](https://code.claude.com/docs/en/errors)

3. With enhanced telemetry enabled, each step of the agent loop becomes a span: `claude_code.interaction` wraps a single turn from prompt to response, `claude_code.llm_request` wraps each call to the Claude API with model name, latency and token counts as attributes, `claude_code.tool` wraps each tool invocation with child spans for the permission wait and the execution itself, and `claude_code.hook` wraps each hook execution; when the agent spawns a subagent, the subagent's `llm_request` and `tool` spans nest under the parent agent's `claude_code.tool` span so the full delegation chain appears as one trace; telemetry is structural by default, recording durations, model names and tool names on every span, with token counts recorded when the underlying API request returns usage data, while the content the agent reads and writes is not recorded unless opt-in variables are set, which the documentation advises leaving unset unless the observability pipeline is approved to store that data; the CLI fails silently on export errors by default, so an unreachable or rejecting endpoint leaves the agent running normally while the telemetry is dropped with no error surfaced in the application. Anthropic, *Observability with OpenTelemetry* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/observability](https://code.claude.com/docs/en/agent-sdk/observability)

4. The `/context` command shows everything occupying the context window for the current session, including memory files and skills, and is the first check on whether a `CLAUDE.md` file, rule or skill description is present at all; if `/context` confirms the file loaded but a particular instruction is still not followed, the issue is likely how the instruction is written rather than whether it loaded; settings merge across managed, user, project and local scopes with command-line flags and environment variables acting as a further override layer, so when a setting does not seem to apply the value set is usually being overridden by another scope or an environment variable. Anthropic, *Debug your configuration* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/debug-your-config](https://code.claude.com/docs/en/debug-your-config)

5. A `tool_result` block carries an optional `is_error` field, set to true when the tool execution resulted in an error, and Claude uses the returned tool result to continue generating its response to the original prompt. Anthropic, *Handle tool calls* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)

6. Anthropic's guidance on building evaluations for agents states that 20 to 50 simple tasks drawn from real failures is a good start, that both the cases where a behaviour should occur and the cases where it should not should be tested, that a good task is one where two domain experts would independently reach the same pass or fail verdict, that ambiguity in task specifications becomes noise in metrics, that model-based rubrics should be frequently calibrated against expert human judgement, and that graders cannot be known to work well without reading the transcripts and grades from many trials; it distinguishes measuring whether at least one of several attempts produces a correct result from measuring whether all of them do. Anthropic, *Demystifying evals for AI agents* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
