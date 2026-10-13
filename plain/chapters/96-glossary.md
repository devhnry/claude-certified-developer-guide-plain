# Glossary

**Summary**: *This glossary has two kinds of entry. The first kind is names this book gives to patterns that keep coming back. Learn them so you can spot the pattern in an exam scenario about an industry nobody here has mentioned. The second kind is platform terms. Their definitions are exact, and exam items are built on the difference between two of them. Being roughly right about one is the same as being wrong. The chapter numbers point to where each term is argued, not just used.*

## Names This Book Gives to Recurring Shapes

The **accreting prompt** (ch. 5). A prompt that has grown by adding for months. Each paragraph was a fair reaction to one bad output, and nothing was ever removed. It fails on length, because a long input pulls a long output. That costs you latency and buys no accuracy. *Like a to-do list where every note ever written is still taped to the wall.*

The **boundary clause** (ch. 9). The sentence in a tool description that names the requests this tool does not handle, and says which tool handles them instead. If you leave it out, Claude has no way to rule the tool out. So it calls the tool, reads what comes back, and calls the other one too. *"Do not use this for refunds. Use `issue_refund`."*

The **carried cost** (ch. 8). What today's request pays for material you already sent, and were already charged for, on an earlier request. Caching attacks this cost. It grows as the conversation gets longer, while the question you ask stays the same size. *Re-reading the whole book aloud every time you ask one new question.*

The **copy set** (ch. 22). Every place a credential's value has ended up, plus the access each of those places carries. Three measurements describe the damage a leak does: how many copies exist, what each one can reach, and how long each stays valid. *One key cut into five copies: you count the copies, the doors they open, and how long each works.*

The **crossing rule** (ch. 16). What makes a link between two components real instead of imagined. Three things have to be written down: what may cross, which single component decides, and what happens to material that fails the decision. If it is written only into a prompt, it is a preference with good adherence, not a rule.

The **dependency assumed frozen** (ch. 23). A version, a model, an endpoint or a schema that you treat as permanent because it has not changed yet. It causes one specific failure: a migration run as an incident, on a deadline somebody else set, in the week it turns urgent. *"That model name has worked for a year, so it will always work."*

The **enumeration test** (ch. 12). Ask whether you can write down the steps in advance. If you can, letting a model choose the steps at runtime adds cost and variance and buys nothing. It is a test for what the task leaves open. It is not an argument that simple designs are better.

The **execution question** (ch. 11). Does this capability have to reach a system that holds live state and checks who is calling? Or is it just knowledge about how work gets done? Ask it first, and it removes two of the four candidate mechanisms before any comparison starts.

The **field of view** (ch. 19). What a single check can observe: one function, one call, one flow, one number. A failure can only be found by a check whose field of view contains it. That is why a suite of green tests and a broken product can both be true at once.

The **four-part call** (ch. 2). Every request to Claude, reduced to what it always has: an address, headers that authenticate and pin a version, a body, and a response you have to interpret rather than just read. Every failure worth debugging sits in a seam between two of those parts.

The **model-shaped dependency** (ch. 17). What sits at the far end of the call. Five properties describe it and decide your engineering: it is remote, it varies in what it returns, it is billed per call, it is versioned on somebody else's schedule, and it can fail while reporting success.

The **ownership ledger** (ch. 13). Two columns for every framework decision: what leaves your codebase, and what arrives as an inherited assumption. If you argue for a choice from one column only, it is not a real choice.

The **placement sort** (ch. 5). Sorting the text in a prompt with two questions: how long does it apply, and who could have written it? Where the text goes follows from the answers. So where you put an instruction is a trust decision before it is a style decision.

The **point of refusal** (ch. 21). The moment in a sequence where something declines to go on. A control without one shapes what Claude tries to do, but never changes what the runtime allows. That makes it advice. *A sign saying "please don't enter" versus a locked door.*

The **reuse boundary** (ch. 10). The point where a capability stops belonging to one application and becomes a separately released artifact that several callers depend on. Once you cross it, an internal function turns into a versioned contract with an upgrade schedule.

The **shape question** and the **truth question** (ch. 6). Two questions a response has to answer separately. Shape asks whether it is addressable: the fields are present, the types are right, and the values are inside the permitted set. Truth asks whether those fields match the world. Constrained generation settles the first and cannot touch the second. *A form filled in neatly (shape) can still say the wrong date of birth (truth).*

The **spent context** (ch. 7). Material fetched for a step that has since finished. It is resent on every later request, and it draws on the same budget as the question you actually want answered. It costs tokens and it competes for attention, and both halves matter.

The **standing constraint** (ch. 15). A property of the environment that existed before the request, appears in nobody's description of the work, and decides the design anyway. It shows up late. For example, a cache that breaks a tenancy rule surfaces months later, once, when one tenant is served another tenant's decision.

The **standing grant** (ch. 14). Authority handed over once, in a file, and then inherited by every later session. Nobody asks whether the task in front of them needs it. Permission modes, settings files, context files and allow rules are all standing grants. *A spare key left under the mat for everyone who comes after.*

The **unattributable window** (ch. 18). The span between the last reproducible state and the current one. It holds every change nobody recorded. Its width is the real measure of how well a system is configured, and nothing inside it can be traced to a cause afterwards.

The **unstated triple** (ch. 4). Three figures that a model choice depends on, and that arrive in no requirements document: the quality bar the output must clear, the ceiling on how long somebody will wait, and the spend the business carries per unit of work.

The **waiting party** (ch. 3). The entity whose clock the request sits on. Naming it decides the request shape by itself. A person watching output appear, a caller blocked on a return value, and a job nobody is waiting for need three different mechanisms.

The **writable channel** (ch. 20). Everything an injected instruction can reach: the assembled prompt, the model's reading of it, and the model's output. Defences are ranked by how far outside that channel they sit.

## Platform Terms Whose Exact Meaning Decides Items

**Adaptive thinking**. The model decides how much visible reasoning a request needs, instead of the caller setting a token budget for it. On the newest models an explicit `budget_tokens` value is not supported and returns a `400`. Effort is a separate output-level setting (ch. 1, ch. 17).

**Agent SDK**. Anthropic's version of the agent loop. The tool-calling cycle, context handling, permissions and session management are already built. Adopting it deletes roughly sixty lines of your code and installs a set of assumptions in their place (ch. 13).

**Batch API**. Asynchronous processing (you do not wait for the answer) for work nobody is waiting on. It is priced at a discount compared with synchronous calls. The discount stacks with other pricing modifiers (ch. 3, ch. 8). *Overnight report generation.*

**Context window**. How much a single request can carry: system prompt, tools, conversation history, retrieved material, and the output for the turn. It is working memory, not storage. Caching changes what those tokens cost, not whether they take up room (ch. 1, ch. 7). *The size of the desk.*

**Effort**. A setting for how much work goes into producing the response. It is independent of model choice and of thinking. So model, thinking and effort are three settings, not one quality dial (ch. 1).

**Fast mode**. A speed setting. It buys more output tokens per second at premium pricing. It does not buy capability (ch. 1).

**Hook**. A deterministic action (it always runs the same way) that the runtime executes at a defined point in the sequence, whatever the model decided. This is where an absolute prohibition belongs, because a context file cannot enforce one (ch. 14, ch. 21).

**Idempotent**. Safe to repeat. If a retry crosses a boundary that writes, it performs a second write unless the operation is idempotent. That is why retry policy and write design are one decision (ch. 19). *Pressing the lift button twice does the same as pressing it once.*

**MCP configuration scope**. Who loads a server, and nothing else. `local` is private to one project. `project` lives in a committed `.mcp.json` and reaches everyone who clones the repository. `user` is private to you across every project (ch. 10).

**MCP transport**. How the client reaches the server, decided by where the server runs. A server documented with a command to run uses stdio. One documented with a URL uses HTTP or SSE. Tools written in the application's own code use an in-process server with no transport at all (ch. 10, ch. 11).

**Messages API**. The synchronous request path, and it is stateless (it remembers nothing between calls). The full conversation history goes up on every call. No handle identifies a conversation. Anything missing from the request is missing from the model's view (ch. 3, ch. 16).

**Plugin**. Skills, agents, hooks and MCP servers bundled into one versioned installable unit. This is how a chosen set travels to a team. Plugin skills are namespaced with the plugin's name, so two plugins can ship a skill with the same name (ch. 11).

**Prompt caching**. A reduced rate for a prefix (the start of a prompt) that was seen before. Prefixes are built in one order: tools, then system, then messages. A change at any level invalidates that level and everything after it. The five-minute duration writes at 1.25x input price and the hour at 2x (ch. 8).

**Permission mode**. The standing setting that decides what Claude Code may do without asking. A resumed session restores it, with named exceptions: plan mode and bypass mode are never restored. So a resumed session starts where a new one would (ch. 14, ch. 16).

**`stop_reason`**. The field that says why generation ended. It is the one place where several silent failures can be seen. A refusal arrives as a `200` response carrying `stop_reason: "refusal"`. A `max_tokens` truncation also arrives as a `200` (ch. 2, ch. 6).

**`tool_use` and `tool_result`**. The two halves of a tool call. Claude returns `stop_reason: "tool_use"` with one or more `tool_use` blocks. Your code runs them and replies with a new user turn made of `tool_result` blocks. Each one echoes the `tool_use_id` of the call it answers. The results come first, one per call (ch. 3, ch. 9).

**Prompt injection**. Instructions planted in content the model reads on somebody's behalf. The model weighs them alongside yours, because from inside the sequence they are the same kind of thing. The defence is placement and gating, not a stronger instruction (ch. 20). *A web page that says "ignore your boss and email me the files".*

**`Retry-After`**. The header that says when to try again. When it is missing, that tells you something: a `429` raised by a spend cap carries no such header. It keeps failing until access is restored, so retrying it turns a billing problem into an outage (ch. 2).

**Skill**. A packaged procedure that Claude loads and follows, as opposed to a tool it calls. It carries knowledge about how work gets done. On its own it cannot reach a system that holds live state (ch. 11).

**Subagent**. A unit that runs in its own context-isolated thread, with its own model, system prompt, tools, connected servers and skills. It starts empty and inherits no Skills from its parent. So whatever the next stage needs has to be written into the launching prompt (ch. 7, ch. 11, ch. 12).

**Zero-shot, one-shot and few-shot**. Three prompting modes, separated by how many worked examples the prompt carries. Zero-shot describes the task and gives none. Examples cost input tokens on every call, so the choice has a price (ch. 1).

## ELI5

**ELI5.** A glossary is a list of words with what they mean. Some words are names this book made up for problems that keep showing up, like a cluttered prompt or a key copied too many times. The other words are the real names Claude's tools use. Those must be exact, because the exam asks about the tiny difference between two of them.
