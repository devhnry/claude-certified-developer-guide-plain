# Glossary

**Summary:** *Two kinds of entry, and each goes wrong differently. First, names this book made up for patterns that keep coming back, so you can spot one in a scenario from an industry we never mentioned. Second, platform terms. Their meanings are exact and items turn on the gap between two of them, so roughly right is wrong. Chapter numbers point to where the idea is argued, not just used.*

## Names This Book Gives to Recurring Shapes

The accreting prompt (ch. 5). A prompt that gets a new paragraph every month. Each one answered one bad output. None was ever removed. It breaks on length: long input pulls long output, adding latency and no accuracy.

The boundary clause (ch. 9). One sentence in a tool description. It lists the requests the tool does not handle and names the tool that does. Without it, Claude cannot rule the tool out. It calls it, reads the result, then calls the other tool too.

The carried cost (ch. 8). Each request pays again for material you sent, and already paid for, earlier. Caching attacks it. It grows with the conversation while your new question stays the same size.

The copy set (ch. 22). List every place a credential's value ends up stored, and the access each place gives. Three numbers size a leak: copies, what each reaches, how long each stays valid.

The crossing rule (ch. 16). It tells you if a link between components is real or only drawn on a diagram. Write down what may cross, which one component decides, and what happens to material that fails. If it lives only in a prompt, it is a wish that usually gets followed.

The dependency assumed frozen (ch. 23). A version, model, endpoint or schema you treat as permanent because it has not changed yet. Then you run a migration as an incident, on a deadline someone else set, in the week it turns urgent.

The enumeration test (ch. 12). Can you write the steps down ahead of time? Then a model picking them at runtime only adds cost and variance. It shows what the task leaves open, not that simple designs always win.

The execution question (ch. 11). Must this capability reach a system that holds live state and checks its callers? Or is it knowledge about how to do the work? Ask it first. Two of four candidate mechanisms drop out before any comparison.

The field of view (ch. 19). What one check can see: a single function, call, flow or number. A check finds a failure only if the failure is inside its view. So green tests and a broken product can coexist.

The four-part call (ch. 2). Any request to Claude has an address, headers that authenticate and pin a version, a body, and a response you interpret, not just read. Bugs hide where two parts meet.

The model-shaped dependency (ch. 17). What sits at the far end of the call. Five properties shape your engineering: it is remote, what it returns varies, it is billed per call, someone else sets its version schedule, and it can fail while reporting success.

The ownership ledger (ch. 13). Keep two columns for each framework decision: what leaves your codebase, and what arrives as an inherited assumption. Judging by one column is not a choice.

The placement sort (ch. 5). Sort the text in a prompt with two questions. How long does it apply? Who could have written it? Placement follows the answers, so it is a trust decision before a style one.

The point of refusal (ch. 21). A step in the sequence where something is able to say no. A control that lacks one only shapes what Claude tries to do. It never changes what the runtime allows. That makes it advice.

The reuse boundary (ch. 10). The line where a capability stops belonging to one application. It becomes its own released artifact, and several callers rely on it. Crossing makes an internal function a versioned contract with an upgrade schedule.

The shape question and the truth question (ch. 6). A response has to pass two separate tests. Shape: can you address it? Fields are present, types are right, values fall in the permitted set. Truth: do those fields match the real world? Constrained generation handles shape and cannot touch truth.

The spent context (ch. 7). Material fetched for a step that is over, yet resent with every later request. It draws on the same budget as your real question. It costs tokens and competes for attention.

The standing constraint (ch. 15). A fact about the environment that predates the request. Nobody mentions it, yet it decides the design, and it shows up late. A cache breaks a tenancy rule, and months later, once, one tenant is served another tenant's decision.

The standing grant (ch. 14). Authority given once, in a file, then inherited by every later session. Nobody asks if the task at hand needs it. Allow rules, permission modes, settings files and context files all count.

The unattributable window (ch. 18). The span from the last reproducible state to the current one. Every change nobody recorded sits inside it. Its width measures how well the system is configured. Nothing in it can be traced later.

The unstated triple (ch. 4). Three figures a model choice depends on, which no requirements document gives: the quality the output must reach, the longest anyone will wait, and what the business spends per unit of work.

The waiting party (ch. 3). Whoever's clock the request runs on. Naming it settles the shape. Someone watching output appear, a caller blocked on a return value, and a job nobody waits for need three different mechanisms.

The writable channel (ch. 20). Everything an injected instruction can reach: the assembled prompt, the model's reading of it, and its output. Defences rank higher the further outside it they sit.

**ELI5.** Problems come back in new clothes. A nickname lets you say "that one again" on sight.

## Platform Terms Whose Exact Meaning Decides Items

**Adaptive thinking**. The model decides how much visible reasoning a request deserves. The caller sets no token budget. On the newest models an explicit `budget_tokens` value is not supported and returns a `400`. Effort is a separate output-level setting (ch. 1, ch. 17).

**Agent SDK**. Anthropic's own build of the agent loop. The tool-calling cycle, context handling, permissions and session management come ready made. Using it removes roughly sixty lines of your code and brings in a set of assumptions (ch. 13).

**Batch API**. For work nobody waits on. It runs asynchronously and costs less than synchronous calls. The discount stacks with other pricing modifiers (ch. 3, ch. 8).

**Context window**. How much one request can carry: system prompt, tools, conversation history, retrieved material and the turn's output. It is working memory, not storage. Caching changes their cost, not whether they take room (ch. 1, ch. 7).

Effort. A dial for how much work goes into the response. It is separate from model choice and from thinking. So model, thinking and effort are three settings, not one quality dial (ch. 1).

Fast mode. A speed setting. You pay premium prices for more output tokens per second. It buys no capability (ch. 1).

**Hook**. An action the runtime always runs at a set point in the sequence, whatever the model decided. Put a flat ban here, because a context file cannot enforce one (ch. 14, ch. 21).

**Idempotent**. Safe to repeat. A retry that crosses a writing boundary writes a second time unless the operation is idempotent. So retry policy and write design are one decision (ch. 19).

**MCP configuration scope**. Only tells you who loads a server. `local` is private to one project. `project` sits in a committed `.mcp.json` and reaches everyone who clones the repository. `user` is private to you across every project (ch. 10).

**MCP transport**. How the client reaches the server, set by where the process runs. A server documented with a command to run uses stdio. One documented with a URL uses HTTP or SSE. Tools written in the application's own code use an in-process server, with no transport at all (ch. 10, ch. 11).

**Messages API**. Synchronous requests, no memory between them. The full history goes up on every call. No handle identifies a conversation. Anything missing from the request is missing from the model's view (ch. 3, ch. 16).

**Plugin**. Skills, agents, hooks and MCP servers bundled as one versioned installable unit. That is how a chosen set reaches a team. Each plugin skill is prefixed with the plugin's name, so two plugins can ship skills with one name (ch. 11).

**Prompt caching**. You pay less for a prefix the system has seen before. Prefixes build in one order: tools, then system, then messages. A change at any level voids that level and everything after it. Five minutes of caching writes at 1.25x input price. An hour writes at 2x (ch. 8).

**Permission mode**. The standing setting for what Claude Code may do without asking. A resumed session restores it, with named exceptions. Plan mode and bypass mode are never restored, so a resumed session starts where a new one would (ch. 14, ch. 16).

**`stop_reason`**. The field that says why generation ended. Several silent failures show only here. A refusal arrives as a `200` response with `stop_reason: "refusal"`. A `max_tokens` cut-off arrives as a `200` too (ch. 2, ch. 6).

**`tool_use` and `tool_result`**. A tool call has two halves. Claude returns `stop_reason: "tool_use"` with one or more `tool_use` blocks. Your code runs them, then replies with a new user turn of `tool_result` blocks. Each echoes the `tool_use_id` of the call it answers. Results come first, one per call (ch. 3, ch. 9).

**Prompt injection**. Instructions planted in content the model reads for someone. It weighs them beside yours, because from inside the sequence they look like the same kind of thing. Defend by placing and gating, not by a louder instruction (ch. 20).

**`Retry-After`**. This header tells you when to try again. Its absence tells you something. A `429` from a spend cap has none and keeps failing until access is restored. Retrying turns a billing problem into an outage (ch. 2).

**Skill**. Claude loads a skill and follows it, as opposed to calling a tool. It is a packaged procedure holding knowledge about how work gets done. On its own it cannot reach a system holding live state (ch. 11).

**Subagent**. It runs in its own thread, isolated from the parent's context, with its own model, system prompt, tools, connected servers and skills. It starts empty and inherits no Skills from its parent, so the launching prompt must carry whatever the next stage needs (ch. 7, ch. 11, ch. 12).

**Zero-shot, one-shot and few-shot**. Three prompting modes, told apart by the number of worked examples in the prompt. Zero-shot describes the task and supplies no example. Examples cost input tokens on every call, so the choice has a price (ch. 1).

**ELI5.** Each word here means one exact thing. Test questions hinge on the gap between two of them.
