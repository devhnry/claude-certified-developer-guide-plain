# Chapter 13: The Loop, the Harness, and What You Stop Owning

**Summary**: *There are three ways to get the same loop, and picking one is bookkeeping, not taste. Adopt a framework and the iteration, the dispatch and the history leave your code. A subprocess model, a configuration format and someone else's data policy move in. Add it up wrong and you rebuild half of what you adopted, or regulated data runs through a runtime that was never covered for it. This chapter reads both sides of that ledger, then puts hooks where the rules must hold.*

## Adopting the SDK Deletes Code and Installs Assumptions

Think of a restaurant. You can cook in your own kitchen, join a franchise, or rent a kitchen run by someone else. Each way removes work and adds rules. The loop is the cooking.

The loop is about sixty lines. Send the messages, read the reply, run the requested tools, add the results, send again. It is the first thing you write for a tool-using model, and it works by the second afternoon.

Then a teammate says "use the Agent SDK" (the franchise). Those sixty lines leave your repository. So does the dispatch table, which maps a tool name to a function. So does the list holding the conversation history. Three things you no longer maintain.

They did not vanish. The SDK runs the same loop, in the same process, against the same model.<sup>[1]</sup> What changed is who fixes it when it breaks. It is no longer you. In return, your app carries new assumptions. A session maps to a running process. Transcripts land on a local filesystem. Tools are declared, not dispatched.

Call this the **ownership ledger**. Every build choice here has two columns. Left: what leaves (iteration, sandbox, retries, runtime). Right: what arrives (an inherited execution model, a configuration format, a data policy, someone else's release schedule). Read only the left and you have not made a choice. Both are always full.

**ELI5.** A franchise buys the stove for you, but you follow its menu. Count what you give up and what you take on.

## The Loop Is Five Steps and Ends Only When a Response Carries No Tool Calls

Picture a cook at the pass. Each order slip means fetching ingredients, then reading the next slip. The cook stops when a slip asks for nothing. You will meet this loop in every implementation.

In code terms, the model gets the prompt, system prompt, tool definitions and any history. It answers with text, tool requests, or both. The tools run and the results go back in. This repeats until a reply has no tool calls.<sup>[2]</sup> One full cycle is a **turn**. A turn finishes without handing control back to the calling application.<sup>[2]</sup>

```
repeat:
    send    system prompt + tool definitions + history + newest input
    receive the reply
    stop    if the reply requests no tools
    execute every tool the reply requested
    return  one result per request, all of them, before the next reply
    check   the turn count and the spend against their ceilings
```

Wire four things, whoever runs the loop. Teams skip the fourth.

1. Register the tools, each with a schema naming its arguments.
2. Scope the system prompt to the task and its tools. Broad prompts route worse.
3. Run and answer every tool call. Answer all calls from one reply together before the next reply.
4. Set exit conditions. With no stopping rule, the loop keeps asking for tools after the work is done.

At the end, your app branches on the result's subtype. The run succeeded, hit the turn ceiling, hit the spend ceiling, or errored. Only success has final text.<sup>[2]</sup> Code that reads the text unchecked works until the first day a limit hits. Cost and usage come back on every subtype, failures too, so a failed run still costs money.<sup>[2]</sup>

**ELI5.** A helper keeps asking for tools until it needs none. You still say when to quit. Then you check whether it finished or got cut off.

## One Session Is One Subprocess Holding a Shell, a Directory and a Transcript

The SDK is not a thin wrapper over one web request. Starting a query launches a separate command-line process. The SDK talks to it over standard input and output. It owns a shell, a working directory and session transcripts on local disk.<sup>[3]</sup> So concurrency is capped by how many such processes fit in memory. Each keeps its own filesystem state.<sup>[3]</sup>

The subprocess came with the loop, and it settles every hosting question below. It is the right column made real, like the franchise's fixed kitchen layout.

Three more things come with it.

**Tools become declarations.** A custom tool has four parts: a name, a description the model reads when deciding to call it, a schema for the arguments, and the function that runs.<sup>[4]</sup> If the function raises an error, the SDK catches it and gives the model an error result. A crash becomes a message the model reacts to, not a page to a human.<sup>[4]</sup>

**Availability and permission are separate levers.** A tool left off the list stays out of context, so the model never tries it. A scoped rule blocking matching calls leaves the tool visible. The model may spend a turn on something that was never going to run.<sup>[4]</sup> Chapter 14 covers permission modes.

**Continuity is an identifier.** Continuing picks up the most recent session in the working directory. Resuming takes a specific session identifier. Forking copies the history into a new identifier and diverges, leaving the original untouched.<sup>[5]</sup> All three keep the conversation. None keeps the filesystem. So a forked run that edits a file has edited it for every other run in that directory.<sup>[5]</sup>

Cost tracking shifts too. Each query reports its own total. No session figure exists, so you add up the calls yourself.<sup>[6]</sup> With subagents, the per-call usage figure covers the main loop only. Whole-tree numbers come from the per-model breakdown.<sup>[6]</sup>

**ELI5.** Each helper gets its own workshop and desk. Copying a chat does not copy the desk, so two helpers can mess up one desk.

## A Custom Loop Is Justified by a Constraint the Library Cannot Meet, Never by Preference

Writing the loop yourself against the Messages API is cooking in your own kitchen. You get full control and full responsibility. Context management, parallel tool handling, retries and exit conditions become code your team writes and keeps alive. Build your own harness only when a constraint rules the library out, the deployment cannot fit what a library assumes, or you need to understand the loop before putting an abstraction on it.

The costly mistake is picking a path, then rebuilding the parts that made you pick it.

The commonest form is **the framework kept as a type definition**. A team adopts the SDK, then hand-writes the iteration and the history layer anyway. The library only supplies a shape for declaring tools. Now two records of the conversation exist, and no reviewer can say which one the model saw.

**Structured calls abandoned for prose.** Asking the model to state its plan in text, then parsing it, is not lighter tool use. It throws away the schema, the part that made the request machine-readable. 

**A persistence layer nobody requested.** Say history moves to a separate store though nobody asked for durability. Two places own the state, and syncing them needs a maintainer.

Each looks like care but adds more code than either honest option. Pick a path, then hand it loop, dispatch and history together.

**ELI5.** If you joined the franchise, let them cook. Cooking your own version gives two cooks and two recipes. Nobody knows which one the customer got.

## Where Data May Be Processed Rules Out Deployment Models Before Preference Is Weighed

**Managed Agents** is the third path, the rented kitchen. Anthropic runs the iteration and the execution sandbox. You define the agent once as a versioned resource, referenced by identifier. Your app sends events in and streams results back.<sup>[7]</sup> Four pieces make it up. The agent is the model, system prompt, tools, connected servers and skills. The environment is where sessions run. The session is one running instance doing one task. The events cross in both directions.<sup>[7]</sup>

These sessions are stateful by design. History, sandbox state and outputs sit on Anthropic's side. That storage is why Zero Data Retention does not currently cover them, and neither does a HIPAA business associate agreement.<sup>[7]</sup> Protected health information, or a zero-retention commitment, rules this path out. That is a fact, not a judgement call.

**Self-hosted sandboxes** sit in between. Orchestration stays with Anthropic. Tool execution moves to infrastructure you control. So the filesystem the agent reads, the processes it starts and the network it reaches fall under your policy.<sup>[8]</sup> The model still sees every tool input and every tool result, because it cannot pick its next step without them.<sup>[8]</sup> Cooking in your own kitchen does not hide the order slips from the restaurant.

| Question | Managed, cloud sandbox | Managed, self-hosted sandbox | SDK, self-hosted |
|---|---|---|---|
| Who drives the loop | Anthropic | Anthropic | Your app |
| Where tools run | Anthropic's sandbox | Your host | Your host |
| Who limits network reach | Anthropic's egress controls | Your firewall | Your firewall |
| Who hardens the image and runtime | Anthropic | You | You |
| Who gets paged | Anthropic | You, for the worker | You |

Self-hosting shares the duty. It does not hand it over. You own image quality and runtime hardening, and Anthropic does not inspect the image. You own egress restriction, or a compromised tool execution reaches any host. The environment key, which lets the worker claim work and post results, goes in a secrets manager. Conversation content and tool output stay in the worker, so retention, redaction and deletion are yours.<sup>[9]</sup> Four things are beyond the provider's reach. It cannot know your key leaked, verify what you put in the image, isolate one tool execution from another in the sandbox, or enforce retention on data that already reached the worker.<sup>[9]</sup>

Self-hosting the SDK has a smaller version of this. Local disk does not survive a restart, a scale-down or a move to another node. A session store mirrors transcripts alone. Memory files and other working-directory artifacts need a strategy of your own.<sup>[3]</sup> In a container serving several tenants, filesystem settings and project context files carry one tenant's material into another's session. Switch them off, and give each tenant its own working directory and configuration directory.<sup>[3]</sup>

Two named failures cause most wrong answers. **Compliance deferred to a later migration**: pilot on the easy path, move later. Regulated data sits outside policy for the whole pilot. **Exception assumed granted**: draft a policy amendment while rolling out anyway. Same violation, plus paperwork.

**ELI5.** Some rules say food may never leave your building. Then the rented kitchen is out, however handy. And if you cook at home, the restaurant still reads each order slip.

## A Hook Fires at a Fixed Point Whether or Not the Model Cooperates

Picture a head chef checking every plate before it leaves the pass. A **hook** is that check. It is a callback the runtime calls at a named moment in the loop: before a tool runs, after it returns, when a prompt is submitted, when the agent finishes, when a subagent starts or stops, and before context is compacted.<sup>[2]</sup> Hooks run in your application's process, not the agent's context window, so registering one costs no tokens.<sup>[2]</sup>

A hook is not a request. A callback firing before a tool runs can refuse it, and the tool does not run. The model gets the refusal as the tool's result and usually tries another route.<sup>[10]</sup> A system prompt line is advice the model weighs against everything else. A hook is code that runs.

Four mechanics decide the rest.

**Position decides what a hook can do.** Only a check before the action can stop it. A callback after can log, swap the result before the model reads it, or add context, but cannot recall what went out. **Audit offered as prevention** is the classic mistake. The logging is real, but it arrives one step late.

**The strictest answer wins.** When callbacks and rules disagree, deny beats defer, defer beats ask, and ask beats allow. One denial blocks the call, whatever the others said.<sup>[10]</sup>

**Order is not promised.** Matching callbacks run at once and finish in no set order, so none may assume another has run.<sup>[10]</sup>

**Patterns match names, not arguments.** A matcher filters on which tool is called. Checks on a path, a command or a value go inside the callback.<sup>[10]</sup> A callback that returns without blocking has the same limit. It suits logging, metrics and notifications, and cannot refuse or alter anything, because the loop has moved on.<sup>[10]</sup>

Managed Agents gets there with a permission policy on each toolset. A tool runs automatically, or the session pauses for a human. The built-in agent toolset allows by default. Connected server toolsets ask by default, so a tool added to a server later does not run unreviewed.<sup>[11]</sup> Custom tools your app executes itself sit outside permission policies entirely. That puts the approval decision back into code someone writes.<sup>[11]</sup> Chapter 21 returns to hooks as a safety tool. For building, one rule is enough. Name the moment, then check whether it falls before or after the thing you must control.

**ELI5.** A chef who looks at each plate before it leaves can send it back. A chef who only writes it in a book afterwards cannot.

## How Wrong Answers Are Built on This Material

Every wrong answer here is real engineering that a good team has shipped. Some answer a question one clause off. Four assumptions build nearly all of them.

- **Preference weighed against a constraint that already decided.** The scenario names a residency rule, a retention commitment or a regulator. The option weighs it against delivery speed. But such a requirement sets the allowed options before anything is compared.
- **Half-adoption dressed as caution.** You pick a path, then rebuild one of its core services or add a store nobody asked for. It looks prudent but gives one piece of state two owners.
- **Recording mistaken for preventing.** Logs, traces and post-run review are offered where something must be stopped. A refusal must arrive while the call is still a request, because a returned tool call has nothing left to withhold. Read the requirement's verb, then put your code on the matching side.
- **A boundary inferred from where code runs.** Someone assumes local execution means nothing crosses to the provider. Or that a managed runtime inherits coverage the account already holds. Ask what each component must see. That is your boundary.

Match the scenario's behaviour, not its industry.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| A residency, retention or regulatory rule applies, and a hosted option is offered | Use the deployment the rule allows, then cut its running cost | Trading the rule for speed, piloting first, or assuming an exception |
| Team chose a framework and is wiring tools | Let it own loop, dispatch and history | Hand-writing any of them, or adding an unrequested store |
| One action must never happen | A check before the tool runs that can refuse | Logging afterwards, or banning it in the system prompt |
| Execution must stay in a network boundary, orchestration may be outside | Run tools on infrastructure you control | Thinking nothing then reaches the provider |
| Long task, no local process held open, no data rule | A managed runtime owning session and sandbox | Rejecting it on preference, or using it with regulated data |
| Run must stop on a stated condition | A ceiling the runtime enforces and reports | Waiting for the model to decide it is done |
| Cost across a run with subagents | Whole-tree accounting over every model | The main loop's usage figure, which stops at the first nesting |
| A rule must cover tools not yet added | A default that asks | An allow list of today's tools |

One habit beats the table. Find the stated constraint first. Then see which options survive it.

**ELI5.** Read the rules of the game first. A clever move that breaks a rule is still wrong.

## What to Remember

- The ownership ledger: each path has two columns, what leaves the codebase and what arrives as an inherited assumption. One column alone is not a choice. Adopting the SDK removes loop, dispatch and history. It adds a subprocess per session writing transcripts to local disk.
- The agent loop: prompt, system prompt, tool definitions and history go in. The model answers or requests tools. Results go back. It ends only when a reply requests no tools. One cycle is a turn, and it completes without returning control to the caller.
- Four things get wired on every path: tools registered with schemas, a system prompt scoped to the task and its tools, every tool call executed and answered together before the next reply, and explicit exit conditions. The model deciding it is finished stops nothing.
- Branch on the result's subtype, never the text. A run succeeds, hits the turn ceiling, hits the spend ceiling, or errors. Final text exists only on success. Cost and usage arrive on all four.
- A custom loop needs a constraint the library cannot meet, never unfamiliarity. It costs you context management, parallel tool handling, retries and exit conditions as code humans maintain.
- Half-adoption is the expensive answer. Hand-writing the loop or the history after choosing a framework leaves two sources of truth. Parsing intent from prose discards the schema that made a call machine-readable.
- Managed Agents runs the loop and the sandbox, with the agent as a versioned resource addressed by identifier. Its sessions are stateful and stored server-side. So Zero Data Retention does not cover them, nor does a HIPAA business associate agreement. That rules the path out whatever else fits.
- A self-hosted sandbox moves tool execution onto local infrastructure while orchestration stays with Anthropic. The model still sees every tool input and result. Image hardening, egress, key rotation and retention become the operator's job.
- A hook runs at a named point in the loop, inside the application process, not the context window, so it costs no tokens. The most restrictive decision wins. Matching callbacks run in parallel in no fixed order. Matchers filter tool names, not arguments.
- Refusal works only in front of the action. A denial before a tool executes stops the call. Code behind it can describe, replace or annotate a result and cannot unmake it. Audit trails and traces answer a reporting requirement, never a prohibition.

**ELI5.** Count what you give up and take on. Tell the helper when to stop. Put the checker before the door.

## Endnotes for this chapter

1. The Agent SDK makes the agent loop and context management that power Claude Code programmable as a library in Python and TypeScript. Anthropic, *Agent SDK overview* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview)

2. The cycle of receiving a prompt with the system prompt, tool definitions and conversation history, evaluating and responding with text or tool calls, executing tools and feeding results back, repeating until a response carries no tool calls, and returning a final result; a turn defined as one round trip that completes without yielding control to the caller; the result subtypes `success`, `error_max_turns`, `error_max_budget_usd` and `error_during_execution`, with the result text present only on `success` while cost, usage, turn count and session identifier are carried on every subtype; and the commonly used hook events with the points at which they fire, together with the statement that hooks run in the application process rather than inside the agent's context window and therefore consume no context. Anthropic, *How the agent loop works* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/agent-loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)

3. The SDK spawns a separate `claude` CLI subprocess communicated with over stdio, which owns a shell, a working directory and JSONL session transcripts on local disk, with one subprocess per session and host concurrency bounded by memory; agent state on local disk not surviving a container restart, scale-down or move to another node; a `SessionStore` adapter mirroring transcripts only, leaving memory files and other working-directory artifacts to a separate storage strategy; multi-tenant isolation requiring filesystem settings to be disabled, auto memory disabled, a per-tenant configuration directory and a per-tenant working directory passed explicitly, with per-tenant egress rules at the proxy; and the observation that Anthropic token cost typically dominates container infrastructure cost by an order of magnitude or more. Anthropic, *Hosting the Agent SDK* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/hosting](https://code.claude.com/docs/en/agent-sdk/hosting)

4. A custom tool defined by four parts, being a name, a description Claude reads to decide when to call it, an input schema and an async handler, registered on an in-process MCP server; the SDK catching uncaught handler exceptions and returning them as error results so a handler error does not stop the agent loop; and the separation of availability, which controls whether a tool appears in Claude's context, from permission, which controls whether a call is approved once attempted, with a scoped block rule leaving the tool visible so Claude may waste a turn attempting it. Anthropic, *Give Claude custom tools* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/custom-tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)

5. Continue finding the most recent session in the current directory, resume taking a specific session identifier, and fork creating a new session that begins with a copy of the original's history and diverges while the original's identifier and history stay unchanged; and the statement that sessions persist the conversation rather than the filesystem, so file edits made by a forked agent are real and visible to any session working in the same directory. Anthropic, *Work with sessions* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

6. Each `query()` call returning its own `total_cost_usd` with no session-level total provided, so an application making multiple calls accumulates the totals itself; and the `usage` field covering only the main agent loop, with `modelUsage` or `model_usage` required for whole-tree token and cost accounting because `usage` undercounts as soon as nesting occurs. Anthropic, *Track cost and usage* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/cost-tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

7. Managed Agents as a pre-built configurable agent runtime on managed infrastructure, contrasted with direct model prompting through the Messages API for custom agent loops and fine-grained control; the four concepts of agent (model, system prompt, tools, MCP servers and skills), environment (an Anthropic-managed cloud sandbox or a self-hosted sandbox), session (a running agent instance performing a task) and events (messages exchanged between application and agent); the agent created once and referenced by identifier across sessions, with results streamed back over server-sent events and event history persisted server-side; and the statement that Managed Agents is stateful by design, storing conversation history, sandbox state and outputs server-side, and is for that reason not currently eligible for Zero Data Retention or HIPAA Business Associate Agreement coverage. Anthropic, *Claude Managed Agents overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/overview](https://platform.claude.com/docs/en/managed-agents/overview)

8. Self-hosted sandboxes keeping orchestration on Anthropic's side while moving tool execution into infrastructure the customer controls, so the agent's code, filesystem and network egress stay in that environment; tool inputs and outputs still flowing to Anthropic's control plane where Claude runs, so the model can see results and determine the next step; and the comparison of cloud environment against self-hosted sandbox across where tools run, network reach, file and repository mounting, memory stores and lifecycle. Anthropic, *Self-hosted sandboxes* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)

9. The shared responsibility model for self-hosted sandbox environments: Anthropic secures the control plane, while sandbox image quality and runtime hardening, network egress controls, environment service key storage and rotation, isolation of untrusted workloads, per-session credential handling, tool-execution blast radius, and log retention and session content all fall to the customer; and the four things Anthropic states it cannot do, being knowing that a key leaked, verifying the customer's worker build, isolating individual tool executions inside the customer's sandbox, and enforcing data retention once session content has reached the customer's worker. Anthropic, *Security model* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security)

10. A `PreToolUse` callback returning a deny decision stopping the tool call, with a reason passed to the model so it avoids retrying; the precedence order in which deny takes priority over defer, defer over ask and ask over allow, with any hook returning deny blocking the operation regardless of the others; all matching hooks running in parallel with non-deterministic completion order, so each must act independently; matchers matching tool names rather than file paths or other arguments, with argument-level filtering done inside the callback; and asynchronous hook output being unable to block, modify or inject context because the agent has already moved on, making it suitable only for side effects such as logging, metrics or notifications. Anthropic, *Intercept and control agent behavior with hooks* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

11. Permission policies controlling whether server-executed tools run automatically or wait for approval, with `always_allow` executing the tool with no confirmation and `always_ask` pausing the session until an approval or denial is returned; the agent toolset defaulting to `always_allow` and MCP toolsets defaulting to `always_ask` so that tools newly added to an MCP server do not execute without approval; and custom tools being executed by the customer's own application and therefore not governed by permission policies. Anthropic, *Permission policies* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/permission-policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)
