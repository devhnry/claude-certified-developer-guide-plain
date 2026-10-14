# Chapter 19: A Test Says It Broke; a Trace Says Where

**Summary**: *Four "where" questions drive this chapter. Where does an error's cause sit? That tells you if waiting helps. Where in the run did it fail? Only a step-by-step record shows that. Did it start in your integration layer or the model's output? Most scenarios hinge on this. Where in a population does a measurement hold? That limits what an average can say. Guess wrong and every later fix hits the wrong target.*

The analogy for this chapter: a house's plumbing. Pipes are components, joins are seams, dye followed through the pipes is a trace, and the water bill is an eval.

## A Green Suite Is a Claim About Parts, Not About the Product

Say retrieval, the prompt builder and the model call all pass their tests. The whole flow still answers a policy question from general knowledge, not the retrieved policy. No error appears.

The join broke. Retrieval hands over a list of records, but the builder wants text. So the prompt holds noise. Both parts are right. Nobody wrote their contract, so nothing tested it.

A check sees only a small window: one function, one call, one flow, one number. Call that its **field of view**. A bug is found only by a check whose window holds it. A **seam** is the join between two components, like a pipe fitting. It belongs to neither neighbour, so it stays unchecked until a check looks right at it.

Counting coverage by component is the trap. Fittings are not pipes.

**ELI5.** Every pipe holds water, yet the floor is wet. The leak is where two pipes meet. Test the joins.

## An Error's Bucket Is Where Its Cause Lives, Not Which Status Code Carried It

Ask of any failure: could time alone change the result?

If so, the cause is the state of the world: capacity, load, a per-minute cap, a dropped connection. Documented cases are `429` rate limits, `529` overloads, 5xx server faults and timeouts.<sup>[1]</sup> Only here is waiting a real fix (the water pressure may return).

If not, the request itself is wrong: a broken body, a revoked key, a missing permission, a missing resource. Those are `400`, `401`, `403` and 404.<sup>[1]</sup> Resending gets the same error every time. Repair or reject it. Neither is a retry.

This mapping is a hypothesis, and two documented cases break it in opposite ways. A spend-cap `429` has no `retry-after` header and keeps failing until access resumes.<sup>[1]</sup> Same status, other bucket. The missing header gives it away. In the other direction, a request too large for the context fails identically if re-sent. So Claude Code lowers `max_tokens` and sends a different request.<sup>[2]</sup>

Reading the status as the diagnosis is the error. The code hints. The header, message and request ID settle it.<sup>[1]</sup>

**ELI5.** No water because the town supply is off? Wait. No water because you never opened the tap? Waiting changes nothing.

## Misclassifying Costs Silence in One Direction and Noise in the Other

Treat a permanent failure as retriable and every try is certain to fail. The budget drains. The real error surfaces late, dressed as slowness. On a rate limit, each try deepens the limit.

Treat a temporary failure as permanent and a glitch that would clear in seconds reaches a person as a broken feature. Someone reports it that day, while the first mistake looks like latency and lasts months. When unsure, call it terminal: the cheaper guess.

A different question sits underneath: has anything already happened? **Retriability** comes from the cause. Safety comes from what the first try committed. If a request fails after Claude finished a tool call, Claude Code will not re-issue it, because the retry would run those calls twice.<sup>[2]</sup> A retry over a writing boundary is a second write, unless idempotent (safe to repeat).

Where recovery stops is a routing decision. Retry mechanics live in chapter 2. Impact and recoverability say if a person must act now. One severity level says nothing.

**ELI5.** Saying "it will fix itself" wrongly wastes months. Saying "it's broken" wrongly costs one call. And never press "pay" twice.

## A Trace Records Each Step, and It Gets Built Before the Failure

A test says something failed, not which step. A **trace** is the missing record of every step: prompt, tool calls, intermediate output and timing. The bad step is visible. It is dye poured in before the leak.

The Agent SDK shows a shape to copy. Each turn of the loop is a span. Each API call is a child span with model name, latency and token counts. Each tool call is a child span, with the wait for permission split from the run itself. A subagent's spans sit under the parent's tool span, so a chain of delegations reads as one trace.<sup>[3]</sup>

Two facts limit it. Telemetry is structural by default: durations, model and tool names. What the agent reads and writes is opt-in.<sup>[3]</sup> So the default trace shows which step and how long, never what was said. Also, export fails quietly. If the collector is unreachable, the agent runs on and the telemetry is dropped. Your application raises no error.<sup>[3]</sup> The dye can fail like the pipes.

**ELI5.** A trace is a diary of what a robot did. You find that step four forgot the sugar. Start the diary before the cake fails.

## The Model's Output Is the Line, and You Read It Before Blaming Either Side

Open the trace and read what the model returned before later code touched it.

| What the trace shows | Where the fault is | What changes |
|---|---|---|
| Right content, mishandled by the system | Below the model | Parser, handoff, tool wrapper, dispatcher |
| Wrong content, and the input was cut off, garbled or missing its retrieved context | Still below the model | Whatever built the input |
| Wrong content from a whole, well-formed input | The model's output | Examples, constraint, prompt, model choice |

The middle row eats weeks. It looks like a model failure, so model fixes leave it untouched. So blame the model only after reading the input it really got. Read what was sent, not the template that should have made it. Config debugging works the same way. Confirm the instruction reached the context window. If it did, the wording is the problem.<sup>[4]</sup>

A failure crossing a boundary keeps its identity or loses it. Chapter 6 covers the tool-result half, where `is_error` lets the model treat a failure as a failure, not data.<sup>[5]</sup> The general point: one message for an invalid identifier, an expired token, a timeout and a policy refusal has erased the differences recovery needs. Recovery can only be as precise as the error it receives.

**ELI5.** A letter has wrong words. Check what the writer was given first.

## An Average Is Only a Fact About the Population It Averaged

An **eval** is a check that looks at the whole run's output. It cannot find where something broke. It answers what nothing else can: did your change help, on a fixed set of cases? A water bill shows use fell, not which pipe leaks.

Build cases before polishing the rubric. Anthropic suggests starting with 20 to 50 tasks from real failures. Include cases where a behaviour should and should not happen.<sup>[6]</sup> A judge (a model that grades answers) outputs a confident number. It means nothing until you measure its agreement with expert human judgement, and recalibrate as things drift.<sup>[6]</sup> A fuzzy task spec becomes noise in the metric. So a good case is one where two domain experts, working alone, reach the same verdict.<sup>[6]</sup>

Now granularity. A total says nothing about its parts. To slice by category, each record must carry its category, since you cannot measure along an axis the data lacks. So when groups differ, add that field first. A flat average can hide a change that fixed one group and broke another. So read each case, not just the mean.

**ELI5.** A class averages a B, but some kids got A's and some F's. Look at each group.

## How Wrong Answers Are Built on This Material

Wrong answers are sound engineering done too early or too broadly. Four habits cause most:

- Fixing before locating: lowering a sampling setting, swapping models, raising a threshold, adding a validator. Each is right only once the break is pinned down.
- Merging what should stay apart: one severity for all errors, one message for all backend faults, one confidence cut for all outcomes, an empty result for a failure. The scenario names the merge as the symptom; more of it looks like tidying.
- A total where a segment was named: a global threshold, one overall accuracy number, review spread evenly over categories. All suit a uniform population, which the scenario has ruled out.
- Repeating what must change: retrying a rejection, duplicating requests against a rate limit, retrying forever, adding a new credential to a throttle. Right only when time could move.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| A status points to temporary pacing or capacity | Back off with a cap, respecting the wait the service gives | New credential, duplicate request, or removing the check |
| One request sometimes works, sometimes fails | Log full input and output for both, then compare | Tweaking a parameter, counting how often, or calling it normal |
| Each component passes, the flow is wrong | Test the handoff with real output from the step before | More component tests, or blaming the model |
| One overall number, but errors clump by category | Tag items with category, measure each, sample within clumps | A global threshold, acting on the total, or reviewing only low-confidence items |
| Part of a job failed, the rest worked | Report the failed part: what was tried, failure type, any partial result | Returning nothing, stopping everything, or retrying without limit |

One habit outlasts the table. For any proposed fix, ask what it would need to observe to be right. Then check who observes it.

**ELI5.** A tricky answer is a good tool at the wrong time. Ask what you must see to know a fix works.

## What to Remember

- Every check has a **field of view**: the slice of the run it can see, such as one function, call, flow or number. A seam lies inside neither component. So an all-green suite speaks for the parts, not the product.
- Ask if time alone could change the result. Yes is a transient cause, and waiting is the fix: `429`, `529`, 5xx and timeouts. No means the request is at fault, so repair or reject: `400`, `401`, `403` and `404`. A status only proposes a cause: a spend-cap `429` has no `retry-after` and never clears alone.
- The two misclassifications cost differently. Retrying a terminal failure drains the budget, delays the real error and deepens a rate limit. Giving up on a retriable one shows a broken feature, fixed that day, so say terminal when unsure. Retriability comes from the cause. Safety comes from what already happened. A retry across a writing boundary is a second write unless idempotent.
- A trace logs each step: prompt, tool calls, intermediate output, timing. "A case failed" becomes "step four failed, and here is what it received". Default telemetry is structural: durations, model and tool names, no content until opted in.
- Read the model's raw return before downstream code touched it. Right output with wrong behaviour is the integration layer. So is wrong output from a truncated or malformed input. Only wrong output from a complete, well-formed input is for prompts, examples or model choice.
- A failure crossing a boundary keeps its identity or loses it. Recovery is no sharper than its error. One message for an invalid identifier, an expired token, a timeout and a refusal drops what recovery runs on.
- An eval tells you if a change helped, not where it broke. Coverage beats rubric polish: 20 to 50 cases from real failures, including cases where the behaviour should not occur. A judge is meaningless until its agreement with human labels is measured.
- An average describes only the population it averaged. You cannot slice along an axis the record lacks. So record the category first and read per-case results, since a steady mean can hide a repair to one group and a break in another.

**ELI5.** Test the joins. Keep a diary. Check what the model was handed. Distrust one average.

## Endnotes for this chapter

1. The Claude API returns a predictable set of HTTP error codes: `400` `invalid_request_error`, `401` `authentication_error`, `402` `billing_error`, `403` `permission_error`, `404` `not_found_error`, `409` `conflict_error`, `413` `request_too_large`, `429` `rate_limit_error`, `500` `api_error`, `504` `timeout_error` and `529` `overloaded_error`; a `429` raised by reaching a usage tier's spend cap carries no `retry-after` header and keeps failing until access resumes; the official SDKs automatically retry transient failures such as connection errors, rate limits and 5xx server errors with exponential backoff, twice by default, honouring the `retry-after` header when present, and each SDK client accepts a maximum-retries option to configure or disable that behaviour; every API response carries a unique `request-id` header, and the same identifier appears as the `request_id` field in error response bodies for tracking and debugging. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

2. Claude Code retries transient failures up to 10 times with exponential backoff before showing an error, covering server errors, overloaded responses, request timeouts, dropped connections and temporary `429` throttles; a request rejected because the input plus `max_tokens` exceeds the context limit would fail the same way if re-sent unchanged, so Claude Code retries with a reduced `max_tokens` instead; it does not retry a TLS certificate validation failure, nor a server error, dropped connection or stalled stream arriving after Claude has completed a block of text or a tool call, because re-running the request could execute the same tool calls twice, so it keeps what Claude completed, shows an incomplete-response notice and continues the turn from the results of any tool calls Claude completed. Anthropic, *Error reference* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/errors](https://code.claude.com/docs/en/errors)

3. With enhanced telemetry enabled, each step of the agent loop becomes a span: `claude_code.interaction` wraps a single turn from prompt to response, `claude_code.llm_request` wraps each call to the Claude API with model name, latency and token counts as attributes, `claude_code.tool` wraps each tool invocation with child spans for the permission wait and the execution itself, and `claude_code.hook` wraps each hook execution; when the agent spawns a subagent, the subagent's `llm_request` and `tool` spans nest under the parent agent's `claude_code.tool` span so the full delegation chain appears as one trace; telemetry is structural by default, recording durations, model names and tool names on every span, with token counts recorded when the underlying API request returns usage data, while the content the agent reads and writes is not recorded unless opt-in variables are set, which the documentation advises leaving unset unless the observability pipeline is approved to store that data; the CLI fails silently on export errors by default, so an unreachable or rejecting endpoint leaves the agent running normally while the telemetry is dropped with no error surfaced in the application. Anthropic, *Observability with OpenTelemetry* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/observability](https://code.claude.com/docs/en/agent-sdk/observability)

4. The `/context` command shows everything occupying the context window for the current session, including memory files and skills, and is the first check on whether a `CLAUDE.md` file, rule or skill description is present at all; if `/context` confirms the file loaded but a particular instruction is still not followed, the issue is likely how the instruction is written rather than whether it loaded; settings merge across managed, user, project and local scopes with command-line flags and environment variables acting as a further override layer, so when a setting does not seem to apply the value set is usually being overridden by another scope or an environment variable. Anthropic, *Debug your configuration* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/debug-your-config](https://code.claude.com/docs/en/debug-your-config)

5. A `tool_result` block carries an optional `is_error` field, set to true when the tool execution resulted in an error, and Claude uses the returned tool result to continue generating its response to the original prompt. Anthropic, *Handle tool calls* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)

6. Anthropic's guidance on building evaluations for agents states that 20 to 50 simple tasks drawn from real failures is a good start, that both the cases where a behaviour should occur and the cases where it should not should be tested, that a good task is one where two domain experts would independently reach the same pass or fail verdict, that ambiguity in task specifications becomes noise in metrics, that model-based rubrics should be frequently calibrated against expert human judgement, and that graders cannot be known to work well without reading the transcripts and grades from many trials; it distinguishes measuring whether at least one of several attempts produces a correct result from measuring whether all of them do. Anthropic, *Demystifying evals for AI agents* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
