# Chapter 8: Cost Follows What You Resend, Not What You Ask

**Summary**: *A chat gets pricier per exchange as it grows, even though each question is the same size. The work did not change. The history grew, and it grows again next turn. Read the bill this way and three topics become one question asked three times. What gets resent? What rate is it charged at? What could be read back instead of processed again?*

## Turn Forty Costs More Than Turn One Because It Carries Turn One

Imagine a tutor who forgets everything between questions. Before each answer, you read the whole notebook aloud. Your page-40 question is one line. The reading is forty pages.

The API works like that. Every request carries the full history: system prompt, tool definitions, every earlier exchange and every tool result. In a forty-turn task, the first turn is sent forty times. So cost grows with roughly the square of the turn count, not in a straight line.<sup>[1]</sup>

Call this **carried cost**. It is what a request pays again for material an earlier request already paid for. The model needs that history, so it is not waste. But it is the part that grows while the questions stay put. On a long run it dwarfs anything you save by trimming the current turn.

So a per-request average forecasts long sessions badly, unless it came from real ones. And the best lever is not deleting history. It is paying a tenth of the price for the same words (the notebook read at the cache rate).

**ELI5.** A helper forgets everything after each question, so you read them your whole notebook first. The notebook keeps growing. Each tiny question costs more.

## Input, Output and the Two Cache Rates Are Four Different Prices

A token is not a token. Kinds differ in price, so a cost model counts each.

| What is charged | Rate, against base input | What it covers |
|---|---|---|
| Input | 1x | The full request, history too |
| Output | Higher, per token | The reply, capped by `max_tokens` |
| Cache write, 5 minutes | 1.25x | New text after your checkpoint |
| Cache write, 1 hour | 2x | Same, held longer |
| Cache read | 0.1x | Text that hit a live entry |

The newest frontier model charges five times its input rate for output. So a chatty model is expensive in a way a shorter prompt never fixes. Reasoning tokens are output too.

Why? The model reads your prompt in one pass but writes one token at a time. So input and output sit on separate budget lines. One averaged rate under-prices any design that talks a lot.

Three facts follow.

- A read costs a tenth. So a five-minute write pays for itself after one hit. The hour version pays back after two.
- The discounts stack. Asynchronous submission takes half off every token, cached ones too, on top of a cache read.<sup>[2]</sup><sup>[6]</sup>
- `max_tokens` is a cap the model cannot see. Lowering it never makes Claude save words. The turn that needed the room is cut off, discarded and still billed. A **task budget** is different. The model can watch it, so it changes behaviour.<sup>[1]</sup>

**ELI5.** Re-reading a page costs a little. Writing a new one takes far longer. A bookmark makes re-reading nearly free.

## A Projection Needs Five Quantities, and Every One Is Knowable Before You Ship

Forecasts rarely fail on maths. Someone dropped a number and put a comparison in its place.

| Quantity | Where it comes from before launch | If you lose it |
|---|---|---|
| Requests per period | Your forecast, or the traffic this replaces | Nothing to multiply the price by |
| Tokens sent per request | Counted, not guessed. The counting endpoint takes a real request body and returns the count without running inference. It is free.<sup>[5]</sup> | The biggest term becomes an opinion |
| Tokens returned per request | A sample run on typical inputs | The pricier side vanishes |
| Rates for the model and features chosen | Published, per model and per operation | You price somebody else's design |
| Share of input expected from cache | The prefix you can hold stable | Cache savings overstated tenfold |

Two traps look like diligence. The **borrowed baseline** scales last year's cost per request, or another team's. That imports a different token mix and price list. The **deferred number** says token counts can't be known until production. That discards what the bill is proportional to.

**ELI5.** To guess a taxi fare you need distance, speed and price per mile. Skip one and you are wishing. Most of them can be measured before you leave.

## You Cannot Cut What You Have Not Attributed

Log three things on every call: tokens in, tokens out, and which feature made the call.

Without them, a spike says only that the total is high. One step often carries most of the spend.

So measure before you fix. Without numbers, every fix hits everything. The **uniform cut** trims every feature equally, even ones that never drove the bill. The **blanket downgrade** gives up quality everywhere to save money that sat in a few places.

Three details keep the numbers honest.

- Parallel tool calls in one turn share an identifier and repeat the same usage. Deduplicate them. Do not add them.
- Once an agent spawns subagents, the plain usage field undercounts. The per-model breakdown gives the whole-tree total.
- Totals come per call. If a session makes several calls, you accumulate them.<sup>[7]</sup>

Claude Code itself attributes recent use to skills, subagents, plugins and MCP servers. Per-user metrics export over OpenTelemetry.<sup>[8]</sup>

**ELI5.** A phone bill is high. Which app ate the data? Trimming every app a bit won't help. Find the greedy one first.

## Caching Reuses the Prefix Instead of Deleting It

Say a chat app gets expensive. The urge is to cut: keep two messages, summarise each turn, drop tool results. Each saves money by hurting the product. Caching attacks the same cost and leaves the content alone.<sup>[1]</sup> Think of a copy of the notebook the tutor already read (a cache entry), not torn-out pages.

A prefix is built in one order: tools, then system, then messages. A change at any level invalidates that level and all after it. The text must match exactly, byte for byte. A **cache checkpoint** marks where a reusable stretch ends. You get four per request at most, and writes happen only at a checkpoint. A later request hashes its own checkpoint. With no match, it walks back at most 20 positions, hunting for an entry an earlier request wrote.<sup>[3]</sup>

The commonest failure: put the checkpoint on a block that changes every request. The saved copy is keyed to text that never returns. You pay every write and read nothing back. The **moving prefix** is the same bug placed earlier. A timestamp or request ID sits before the stable content. Anthropic measured a 25-token status line at the front of a system prompt. It lifted one run from $0.59 to $4.24, worse than caching off.<sup>[1]</sup> Put per-request text in the latest user message.

Three conditions must hold together.

| Condition | Why it bites |
|---|---|
| The prefix is identical | One added word before the checkpoint forces a full reprocess |
| It returns within the lifetime | Five minutes by default, refreshed free on each hit. The clock starts when the request starts, not when the reply ends |
| It clears the minimum length | The minimum depends on the model. A short prompt runs uncached with no error<sup>[3]</sup> |

The last row is quiet, and that is the trap. Both usage counters read zero. That is the whole signal. The two diagnostics differ too. Usage says whether the cache hit. Cache diagnostics says what changed, naming the first divergence among model, system, tools and messages.<sup>[4]</sup>

The default lifetime fails one pattern. A loop that waits on people returns after minutes, so the entry expires unused. The hour-long write fixes that. It costs twice the price and pays back on the first miss it prevents.<sup>[1]</sup>

**ELI5.** Keep a copy the tutor already read, instead of tearing out pages. It only helps if it is word for word the same, you return soon, and it is long enough.

## How Wrong Answers Are Built on This Material

Wrong cost answers apply a real saving to the wrong term, so each sounds fine. Four habits cause most of them.

- **Deletion where reuse was possible.** Chopping history, summarising, dropping tool results. Fine for finished material (chapter 7). Wrong when the chat still needs a stable prefix.
- **A missing term.** Output left out, counts postponed, or a figure borrowed. That only works if the missing number never varies. No scenario says so.
- **An untargeted fix for an unlocated problem.** Across-the-board cuts, the cheapest model, or "growth is unavoidable". All assume spend is even. Nobody measured that.
- **A hidden control treated as a budget.** A lower reply cap decides what survives, not what you spend.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Chats grow longer, each exchange costs more, requests the same | Cache the stable prefix, so resent history bills at the read rate | Keeping only recent turns, or summarising each turn |
| Nobody knows which feature drives the bill | Measure token use per feature first | An even cut, a downgrade, or shrugging at growth |
| A forecast is due before launch | Volume, tokens up and down, rates, expected cache reads | Scaling a per-request cost taken from elsewhere |
| Caching is on, read counter stays at zero | Find the byte that moves ahead of the checkpoint | Extra checkpoints, or a longer lifetime |
| High volume, and no one waits on single results | Asynchronous submission, discounting every token | Treating it as interactive, or paying for savings with quality |
| Cap spend without breaking hard turns | A budget the model can see, with a hard limit behind it | A lower response cap, which discards work and still bills it |

One habit outlasts the table. Ask of any option: does it move fewer tokens, change their rate, or only change where the bill shows?

**ELI5.** Bad answers fix the wrong thing. They tear out pages when a bookmark would do.

## What to Remember

- Carried cost is paying again for material sent on an earlier request. Every turn resends the whole history, so a long task's cost grows with roughly the square of its turn count while the questions stay the same size.
- Four rates, not one price: input at 1x, output higher per token, cache writes at 1.25x for five minutes and 2x for an hour, cache reads at 0.1x. A read repays a five-minute write after one hit and an hour write after two. The multipliers stack with the asynchronous discount.
- A projection needs five quantities: request volume, tokens sent, tokens returned, rates for the model chosen, and the share expected from cache. All are knowable before launch, because the counting endpoint returns input tokens free, without running inference.
- Attribution comes before optimisation. Log tokens in, tokens out and the calling feature per call, because any remedy without it is across the board and hurts features that never drove spend. Deduplicate parallel tool calls sharing one identifier, read subagent spend from the per-model breakdown, and add up per-call totals yourself.
- Caching reuses the prefix instead of deleting it, beating truncation and per-turn summarising while the conversation needs its history. Prefixes build tools, then system, then messages, so a change at one level invalidates everything after.
- A cache checkpoint marks where a reusable stretch ends, four per request at most. A write happens only at a checkpoint, and a read walks back 20 blocks at most to find one. A checkpoint on content that changes each request pays every write and reads nothing back.
- Caching needs three conditions together: identical bytes, a return inside the lifetime (five minutes, refreshed free on each hit), and a prefix over the model's minimum. Falling short is silent: no error, both usage counters at zero. Diagnostics then names the first divergence among model, system, tools and messages.
- A task budget is visible to the model, so it changes what Claude does. `max_tokens` caps a response invisibly: lowering it discards the turn that needed the room and bills it anyway.

**ELI5.** Long chats cost more because the whole notebook is read each time. Use a bookmark so most of it is read cheaply. Measure before you cut.

## Endnotes for this chapter

1. Every turn of an agentic task resends the entire growing conversation, so a 40-turn task sends its first turn 40 times and task cost grows with roughly the square of turn count; caching does not stop the resending, but each resend is billed at the cache-read rate, a tenth of the input price, with the 1.25x cache-write rate paid only on what is new. Content that changes per request, such as a timestamp or a queue position, placed ahead of the stable prefix turns every request into a full cache write: a 25-token status line at the front of the system prompt cost $4.24 per run instead of $0.59, more than running with caching off. For a loop that waits on humans between turns, the 1-hour cache duration costs 2x the input price to write instead of 1.25x and pays for itself on the first prevented miss. A task budget saves money because the model sees a live token countdown and self-regulates; `max_tokens` is a safety cap that saves nothing, because it caps a single response invisibly to the model, and the turns that needed the room are discarded and still billed. Anthropic, *Optimizing for cost and intelligence* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)

2. Prompt caching uses pricing multipliers relative to base input token rates: a 5-minute cache write is 1.25x base input price, a 1-hour cache write is 2x, and a cache read is 0.1x, so caching pays off after one cache read for the 5-minute duration or after two for the 1-hour duration. These multipliers stack with other pricing modifiers, including the Batch API discount and data residency. The published rate card lists Claude Fable 5 at $10 per million base input tokens and $50 per million output tokens. Anthropic, *Pricing* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)

3. Cache prefixes are created in the order `tools`, `system`, then `messages`, and changes at each level invalidate that level and all subsequent levels; cache hits require 100% identical prompt segments up to and including the block marked with cache control. Up to 4 cache breakpoints may be defined; cache writes happen only at a breakpoint, and on each request the system computes the prefix hash at the breakpoint and walks backward one block at a time through a lookback window of 20 blocks checking for entries prior requests wrote. Placing the breakpoint on content that changes every request means the lookback finds nothing, so the correct placement is the last block whose prefix is identical across the requests that should share a cache. The default cache lifetime is 5 minutes, refreshed for no additional cost each time the cached content is used, and measured from the start of the request that writes or reads the entry rather than from the end of its response. There is a per-model minimum cacheable prompt length; requests to cache fewer tokens than the minimum are processed without caching and no error is returned, and the way to verify is that both `cache_creation_input_tokens` and `cache_read_input_tokens` are 0. Anthropic, *Prompt caching* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

4. Without cache diagnostics the only signal of a miss is `usage.cache_read_input_tokens` dropping to zero, with no indication of what changed. Passing the previous response `id` as `diagnostics.previous_message_id` makes the API compare the two requests and report the first point of divergence as `model_changed`, `system_changed`, `tools_changed` or `messages_changed`; the response reports the earliest divergence only. Diagnostics answers whether the request changed, while `usage.cache_read_input_tokens` answers whether the cache hit. Anthropic, *Cache diagnostics* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics)

5. The token counting endpoint accepts the same structured list of inputs used for creating a message, including system prompts, tools, images and PDFs, and returns the total number of input tokens without running inference; it is free to use and supported on all active models, and is documented as a way to manage costs proactively and make model routing decisions. Anthropic, *Token counting* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

6. The Message Batches API processes large volumes of requests asynchronously, reducing costs by 50% and increasing throughput, with most batches finishing in less than 1 hour and results available within 24 hours; the discount applies to every token of a request, including cached ones. Anthropic, *Batch processing* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/batch-processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

7. When Claude uses multiple tools in one turn, all messages in that turn share the same ID with identical usage data, so deduplicate by ID to avoid double-counting. The result message carries `total_cost_usd` and cumulative usage for that call; where the agent spawns subagents, the per-model usage map is what gives whole-tree token accounting, because the plain `usage` field undercounts as soon as nesting occurs. Each call returns its own total and the SDK provides no session-level total, so an application making several calls accumulates them itself. Anthropic, *Track cost and usage* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/cost-tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

8. The `/usage` command shows detailed token usage for the current session, and on a plan it also breaks recent usage down by attribution to skills, subagents, plugins and individual MCP servers, each as a percentage of the total, alongside behavior flags raised when a behaviour such as long context or cache misses accounts for 10% or more of recent usage. OpenTelemetry export works on every setup and is the only option that streams per-user token and cost metrics into an organisation's own observability stack in near real time. Anthropic, *Manage costs effectively* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs)
