# Chapter 13: The Loop, the Harness, and What You Stop Owning

**Summary**: *Three paths lead to the same loop, and choosing between them is an accounting exercise rather than a taste test. If you adopt a framework, the iteration, the dispatch and the history leave your codebase. In their place come a subprocess model, a configuration format and somebody else's data-handling policy. Get the accounting wrong and you rebuild half of what you adopted. Or regulated data ships through a runtime that nothing covered it for. This chapter reads both columns of that ledger. Then it puts hooks where the rules have to hold.*

## Adopting the SDK Deletes Code and Installs Assumptions

**First, the idea.** When you build an agent, you can write the loop yourself or let a library run it. Either way, something moves. Some work leaves your code and some assumptions arrive. This section shows both.

**The analogy: a restaurant kitchen.** You own a restaurant. The **agent loop** (the kitchen's order cycle) takes an order, cooks, serves, and goes back for the next order. You are the **calling application** (the restaurant owner). The model is the chef. Every time I use a kitchen word, the real term is in bold beside it.

**The loop is small.** It is about **sixty lines**. Send the messages, read what comes back, run whatever tools were requested, append the results, send again. Nobody **finds it difficult**. It is the **first thing you write** against a **tool-using model** (a model that can ask to call tools), and it works on the second afternoon. This is you running your own kitchen.

**Then the SDK arrives.** A teammate suggests the **Agent SDK** (a library, like hiring a ready-made kitchen crew), and those sixty lines **leave the repository**. So does the **dispatch table** (the list that maps a tool name to a function, like the board that says which station cooks which dish). So does the list that had been **accumulating conversation history** (the order book). That is **three things** nobody on your team maintains any more.

**What did not change.** None of the three **stopped existing**. The SDK runs the **same loop**, inside the **same process**, against the same model.<sup>[1]</sup> What moved is who **fixes** it when it **breaks**. It is **no longer** you.

**What moved the other way.** A set of **assumptions your application now carries**:
- A session maps onto a running process.
- Transcripts land on a local filesystem.
- Tools are declared rather than dispatched.

**The ownership ledger.** Call this the **ownership ledger**. Every **construction decision** in this chapter has **two columns**. A choice you make by reading only the **left** one is **not a choice**.
- The **left column** is what **leaves**: the iteration, the sandbox, the retries, the runtime.
- The **right column** is what **arrives instead**: an inherited execution model, a configuration format, a data-handling policy, and somebody else's release cadence.

Both columns are **always full**. Nothing is ever **simply gone**.

**ELI5.** Say you hire a kitchen crew so you stop cooking. The cooking still happens. It just happens by their rules, in their way. You gave up some work and took on some of their habits. Always look at both.

## The Loop Is Five Steps and Ends Only When a Response Carries No Tool Calls

**First, the idea.** The loop is a repeating cycle. It stops only when the model's reply asks for no tools. If you know it well, you can spot it whoever built it.

**Why learn it.** Learn the loop at the **level of code** and you can **recognise** it whoever implemented it. This matters because every decision in this chapter is a decision about which parts of it **somebody else implemented**.

**What happens in one cycle (the order cycle).**
- The model **receives the prompt** (the order) along with the system prompt, the tool definitions and whatever history exists.
- It replies with text, with one or more **requests to call a tool**, or with both.
- The **requested tools run** and their **results go back** in.
- The cycle repeats.
- It finishes when a reply arrives carrying **no tool calls** at all.<sup>[2]</sup>

One complete cycle is a **turn** (one trip from order to served dish). A turn runs to completion without **handing control back** to the calling application.<sup>[2]</sup>

```
repeat:
    send    system prompt + tool definitions + history + newest input
    receive the reply
    stop    if the reply requests no tools
    execute every tool the reply requested
    return  one result per request, all of them, before the next reply
    check   the turn count and the spend against their ceilings
```

**Four things get wired.** They are needed no matter who runs that repetition. The **fourth** is the one you skip when the **first three work**.
- Tools have to be **registered**, each with the **schema naming its arguments** (a description of what inputs it takes).
- The system prompt has to be **scoped to the task** and to the tools that exist for it, because a broad system prompt produces **broader and less reliable routing**.
- Every tool call the model issues has to be **executed and answered**. All the calls from one reply must be **resolved together** before the next reply is requested.
- **Exit conditions** have to be defined, because a loop with **no stopping criterion** keeps asking for tools past the point where the work is done.

**How a run ends.** What the application branches on at the end is the **result's subtype**. The run either:
- **succeeded**,
- hit the **turn ceiling**,
- hit the **spend ceiling**, or
- was **interrupted by an error**.

The **final text** is present only on the successful one.<sup>[2]</sup> Code that reads the text without **checking the subtype** works perfectly until the first day a limit bites. **Cost and usage** arrive on **every subtype**, including the failures. So a run that ended badly is **still billable** and still has to be accounted for.<sup>[2]</sup>

**ELI5.** The kitchen keeps cooking dishes while the chef keeps asking for more ingredients. It stops when the chef says "done" without asking for anything. You also set a limit on time and money, because a chef who never says "done" would cook forever. At the end, always check how the night ended before you trust the final dish.

## One Session Is One Subprocess Holding a Shell, a Directory and a Transcript

**First, the idea.** The SDK is not a thin wrapper around a web request. Each session starts a whole separate program. That one fact drives most hosting decisions later in the chapter.

**The surprise.** The SDK is not a **wrapper around an HTTP call**, and treating it as one is where production surprises come from. Starting a query **spawns a separate command-line process** (a separate program) that the SDK talks to over standard input and output. Think of it as the kitchen being its own room. That process owns:
- a **shell** (the stove, where commands run),
- a **working directory** (the counter, where files sit), and
- **session transcripts** written to **local disk** (the order book).<sup>[3]</sup>

So concurrency is bounded by how many of those processes a host's memory holds. Each one keeps its **own filesystem state**.<sup>[3]</sup>

Nobody asked for a **subprocess**. It arrived with the loop, and it **decides every hosting question** later in this chapter. That is the ledger's **right column** made concrete.

**Three more things arrive alongside it.**

**1. Tool definition becomes declarative.** A custom tool is **four parts**: a name, a description the model reads when deciding whether to call it, a schema for its arguments, and the function that runs.<sup>[4]</sup> **Registration replaces dispatch**. A function that **raises** (throws an error) does not **bring the loop down** either. The SDK **catches** it and hands the model an **error result**. So an unhandled exception becomes a message the model reacts to, rather than a page for a human.<sup>[4]</sup>

**2. Availability and permission become separate levers.**
- Leaving a tool out of the list keeps it **out of context**, so **no attempt** is ever made.
- A **scoped rule** blocking matching calls leaves the **tool visible**. So a turn can be spent trying something that was never going to run.<sup>[4]</sup>

Chapter 14 owns the permission modes themselves.

**3. Continuity becomes an identifier.**
- **Continuing** picks up the **most recent session** in the working directory.
- **Resuming** takes a **specific session identifier** and returns to it.
- **Forking** copies the history into a new identifier and diverges, leaving the original thread intact.<sup>[5]</sup>

All three **persist the conversation** and none of them **persists the filesystem**. So a forked run that edits a file has edited it for every other run in that directory.<sup>[5]</sup>

**Accounting shifts too, and quietly.** Each query reports its own total and **no session-level figure exists**. So an application making several calls in one conversation **adds them up** itself.<sup>[6]</sup> Once **subagents** (helpers that run their own conversations) are involved, the per-call usage figure covers the **main loop alone**. Whole-tree numbers come from the **per-model breakdown** instead.<sup>[6]</sup>

**ELI5.** When you hire the crew, they do not just hand you a recipe. They bring a whole kitchen room with its own stove, counter and order book. That room has to live somewhere, and it keeps its own papers. Also, each order gets its own bill, so you add up the bills yourself.

## A Custom Loop Is Justified by a Constraint the Library Cannot Meet, Never by Preference

**First, the idea.** You can write your own loop directly against the **Messages API**. It is allowed. But you need a real reason, because you then do all the work the library would have done.

**What it costs.** Writing the iteration directly against the **Messages API** buys **complete control** and charges **complete responsibility**. Here is what you take on:
- context management,
- parallel tool handling,
- retry behaviour,
- exit conditions.

Every behaviour a library would have supplied for nothing becomes **code humans write**, test and keep working. Your **own harness** (your own kitchen setup) earns its cost in three cases:
- a **constraint rules the library out**,
- the **deployment cannot accommodate** what a library assumes, or
- you need the loop understood before any abstraction sits on it.

**The expensive mistake.** It is rarely picking the **wrong path**. It is picking one and then **rebuilding the parts** of it that were your reason for picking it. Three forms:

- **The framework kept as a type definition.** This is the commonest form. A team commits to the SDK and then **hand-writes the iteration** and the history layer anyway. The library ends up supplying little more than a shape for declaring a tool. **Two sources of truth** now exist for what has happened in the conversation. **No reviewer** can say which one the model **actually saw**.
- **Structured calls abandoned for prose.** Asking the model to state its intention in text and then **parsing that text** is not a lighter version of tool use. It **discards the schema**, which is the one part of the arrangement that made a request **machine-readable**. It leaves the application **inferring an argument list** from a sentence.
- **A persistence layer nobody requested.** Moving conversation history into a separate store, when no requirement mentioned durability, **splits ownership** of the state. Reconciling the two copies is now a **feature with a maintainer**.

Each of those **reads as diligence**. Each is **more code** than either honest option. Having chosen a path, the **consistent setup** hands it the loop, the dispatch and the history together.

**ELI5.** You can run your own kitchen if you have a good reason. But if you hire the crew and then cook everything yourself anyway, you pay twice and nobody knows whose order book is right. Pick one way and let it do its whole job.

## Where Data May Be Processed Rules Out Deployment Models Before Preference Is Weighed

**First, the idea.** The third path is **Managed Agents**, where Anthropic runs the loop for you. Whether you may use it can be settled by a data rule alone, before you compare anything else.

**What Managed Agents is.** It is the third construction path, and it **inverts the arrangement**. Think of it as a ghost kitchen (a kitchen you do not own) run by someone else. Anthropic **runs the iteration** and the **execution sandbox** (the sealed space where tools run). The agent is defined once as a **versioned resource** and referenced by identifier. Your application **sends events** in and **streams results back**.<sup>[7]</sup>

**Four pieces** make it up:
- the **agent**: the model, system prompt, tools, connected servers and skills;
- the **environment**: where sessions execute;
- the **session**: one running instance doing one task;
- the **events**: the messages crossing in both directions.<sup>[7]</sup>

**The fact that decides scenarios.** Those sessions are **stateful by design**. They hold conversation history, sandbox state and outputs on **Anthropic's side**. That storage is why **Zero Data Retention** does not currently cover them, and neither does a **HIPAA business associate agreement**.<sup>[7]</sup> So **protected health information**, or a zero-retention commitment, **removes this path**. It is a **fact** rather than a **judgement**. Nothing about how well it fits operationally reopens it.

**Self-hosted sandboxes (your kitchen, their management).** They sit between the two. **Orchestration stays** on **Anthropic's side**. **Tool execution moves** onto **infrastructure you control**. So the filesystem the agent reads, the processes it starts and the network it can reach all fall under **local policy**.<sup>[8]</sup>

**The part that gets misread.** The **model still sees** every tool input and **every tool result**, because it cannot choose a next step without them.<sup>[8]</sup> Moving execution inside a **boundary** reads like moving the conversation inside it. *It does not.*

| The question the scenario is really asking | Managed, cloud sandbox | Managed, self-hosted sandbox | SDK, self-hosted |
|---|---|---|---|
| Who runs the iteration | Anthropic | Anthropic | The calling application |
| Where tool code executes | An Anthropic sandbox | A host under local control | A host under local control |
| What limits the agent's network reach | Anthropic's egress controls | Local firewall policy | Local firewall policy |
| Who hardens the image and the runtime | Anthropic | The operator | The operator |
| Whose humans are paged when it stops | Anthropic's | The operator's, for the worker | The operator's |

**Self-hosting is shared responsibility.** It is a **shared responsibility** rather than a handover. What stays with you:
- **Image quality and runtime hardening** (the image is the template for the sandbox). Anthropic does **not inspect the image**.
- **Egress restriction** (limits on where traffic can go) stays local. Without it, a compromised tool execution reaches **arbitrary hosts**.
- The **environment key** that authorises work to be claimed and results posted back belongs in a **secrets manager**.
- Conversation content and tool output **pass through the worker** and remain in that environment. So **retention, redaction and deletion** are a local obligation under local policy.<sup>[9]</sup>

**Four things** sit outside the **provider's reach**. It cannot:
- know your key leaked,
- verify what you put in the image,
- isolate one tool execution from another inside the sandbox,
- enforce retention on data that already reached the worker.<sup>[9]</sup>

**Self-hosting the SDK teaches the same lesson in a smaller frame.**
- **Local disk** does **not survive** a restart, a scale-down or a move to another node.
- A session store **mirrors transcripts alone**. Memory files and other working-directory artifacts are left to a strategy you have to pick.<sup>[3]</sup>
- In a container serving several tenants (several customers), **filesystem settings and project context files** carry **one tenant's material** into another tenant's session. The fix is to switch those settings **off** and give every tenant its own **working directory and configuration directory**.<sup>[3]</sup>

**Two named failures** cover most of the wrong answers on this material.
- **Compliance deferred to a later migration.** This proposes piloting on the convenient path and moving once the team knows the shape of the problem. It **processes regulated data outside policy** for the whole of the pilot.
- **The exception assumed granted.** This drafts a policy amendment while the deployment proceeds. It is the same violation with paperwork attached.

**ELI5.** Some food rules say "this food may never leave our building". If a ghost kitchen stores your food on its shelves, that rule decides it before you compare anything else. Even if you cook in your own building, the chef still reads every order slip. Moving the stove does not hide the orders.

## A Hook Fires at a Fixed Point Whether or Not the Model Cooperates

**First, the idea.** A hook is code that runs at a set moment in the loop. It does not ask the model. It just runs. That makes it the right tool when a rule must hold.

**What a hook is.** A hook is a **callback the runtime invokes** at a **named moment** in the **loop**. Think of a checkpoint at the pass, where the kitchen hands dishes to the waiters. The named moments are:
- before a tool executes,
- after it returns,
- when a prompt is submitted,
- when the agent finishes,
- when a subagent starts or stops,
- before context is compacted.<sup>[2]</sup>

Hooks execute in the **application's own process** rather than inside the **agent's context window**, so registering one **costs no tokens**.<sup>[2]</sup>

**A hook is not a request.** That is what makes it the answer to a whole class of scenario. A callback **firing before a tool executes** can **refuse** it, and the tool then does **not run**. The model receives the refusal as the tool's result and generally tries another approach.<sup>[10]</sup> An instruction in a system prompt is **guidance** the model **weighs against everything else** it was handed. A hook is a **branch that executes**.

**Four mechanics** decide the rest.

**1. Position decides capability.** Only a check sitting in **front of the action** can **stop** it. A callback firing **afterwards** can record what happened, replace the result before the model reads it, or attach context. It **cannot recall** what was already sent. **Audit offered as prevention** is the anti-pattern. It survives a first read because the logging is genuine and the report it produces is real. It arrives **one step late**.

**2. The most restrictive answer wins.** Where several callbacks and rules apply to one call, the order of strength is:
- refusal outranks deferral,
- deferral outranks asking,
- asking outranks allowing.

A **single refusal blocks the call** whatever the others returned.<sup>[10]</sup>

**3. Order is not promised.** Every matching callback runs at once and they finish in **no guaranteed sequence**. So each has to work without assuming another already ran.<sup>[10]</sup>

**4. Patterns match names, not arguments.** A matcher filters on the **tool being called**. So anything about a path, a command or a value is a **check written inside the callback**.<sup>[10]</sup> A callback that returns without blocking, letting the loop carry on, is bound the same way. It suits **logging, metrics and notifications**. It can neither refuse nor alter anything, because the loop has already moved on.<sup>[10]</sup>

**Managed Agents does the same thing differently.** It uses a **permission policy** on each toolset. A policy either lets a tool run automatically or **pauses the session** until a human answers.
- The built-in agent toolset **allows by default**.
- Connected server toolsets **ask by default**, so a tool added to a server later does **not execute unreviewed**.<sup>[11]</sup>
- **Custom tools** the application executes itself sit **outside permission policies** entirely. That puts the approval decision back into **code somebody writes**.<sup>[11]</sup>

Chapter 21 takes hooks up again as a safety mechanism. Construction needs one rule from them: **name the moment**, then check whether it falls **before or after** the thing you were asked to control.

**ELI5.** A hook is a guard at the kitchen door. He checks every dish before it goes out, and he does not ask the chef's opinion. A guard who checks after the dish has left can write it down, but cannot stop it. So the guard must stand in front.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here describe real engineering. Every one names something a competent team has shipped. Several answer a question **one clause away** from the one asked. **Four assumptions** produce nearly all of them.

**The four wrong assumptions:**
- **Preference weighed against a constraint that already decided.** The scenario names a **residency rule**, a **retention commitment** or a **regulator**. An option treats it as **one consideration** to be **balanced against delivery speed**. A requirement of that kind **sets the feasible set** before **anything else is compared**. So the option becomes correct only where the scenario **states no such requirement**.
- **Half-adoption dressed as caution.** A path is chosen, then one of its **core services** is **rebuilt by hand** or **supplemented with a store** nothing asked for. It reads as prudence and produces **two owners** for **one piece of state**.
- **Recording mistaken for preventing.** **Logs, traces and post-run review** are offered where the scenario asked that something be **stopped**. A **refusal** has to arrive while the call is **still a request**, because a **returned tool call** has **nothing left to withhold**. Read the **verb in the requirement**, then put your code on the **matching side of the action**.
- **A boundary inferred from where code runs.** **Execution moved onto local hosts** is assumed to mean **nothing crosses to the provider**. Or a **managed runtime** is assumed to **inherit coverage** the account already holds. Ask what each **component must see** to do its job, and you have the **boundary**.

**Match** on what the **scenario** is doing, never on the **industry** it is **dressed** in.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| A residency, retention or regulatory rule applies and a hosted option is offered | Take the deployment the rule permits, then work its operational cost down | Balancing the rule against speed, piloting first, or assuming an exception gets signed |
| The team has committed to a framework and is now wiring tools | Let it own the loop, the dispatch and the history | Hand-writing any of the three, or bolting on a store nothing asked for |
| A specific action must never be performed | A check running before the tool executes, able to refuse it | Logging it afterwards, or forbidding it in the system prompt |
| Execution must stay inside a network boundary, orchestration may sit outside | Move tool execution onto infrastructure under local control | Assuming nothing then crosses to the provider at all |
| A long-running task should not hold a local process open, and no data rule applies | A managed runtime owning the session and the sandbox | Ruling it out on preference, or choosing it with regulated data in scope |
| The run has to stop on a stated condition | An explicit ceiling the runtime enforces and reports | Expecting the model to finish when the work looks done |
| Cost must be attributed across a run that spawned subagents | Whole-tree accounting, across every model that ran | The main loop's usage figure, which stops at the first nesting |
| A rule must hold for tools nobody has added yet | A default that asks rather than allows | An allow list naming the tools that exist today |

**A habit that works past the table.** One habit beats the table. **Name the constraint** the scenario states before you compare anything. Then ask which **options survive** it. Most wrong answers here are sound engineering that the stated constraint had already **taken off the board**.

**ELI5.** Most wrong answers are good ideas used in the wrong place. Before you pick a kitchen, read the house rules first. If a rule already says no, the best-looking kitchen is still the wrong one.

## What to Remember

- The **ownership ledger**: every path has **two columns**. One is what **leaves the codebase**. The other is what arrives as an **inherited assumption**. A choice made from **one column** is **not a choice**. Adopting the SDK removes **loop, dispatch and history** and installs a **subprocess per session** writing **transcripts to local disk**.
- The **agent loop**: **prompt, system prompt, tool definitions and history** go in. The model **answers or requests tools**. **Results go back**. The cycle **ends** only when a reply **requests no tools**. One cycle is a **turn**, and it **completes without returning control** to the caller.
- **Four things get wired** on **every path**: **tools registered with schemas**, a **system prompt scoped** to the task and its tools, **every tool call executed and answered together** before the next reply, and **explicit exit conditions**. The last one matters because the model deciding it is finished stops nothing.
- **Branch** on the **result's subtype**, never on the text. A run **succeeds**, hits the **turn ceiling**, hits the **spend ceiling**, or **errors**. The **final text** exists **only on success**. **Cost and usage** arrive on **all four**.
- A **custom loop** is justified by a **constraint the library cannot meet**, never by unfamiliarity. It charges you **context management**, **parallel tool handling**, **retries and exit conditions** as code humans maintain.
- **Half-adoption is the expensive answer**: **hand-writing the loop or the history** after choosing a framework leaves **two sources of truth** for the conversation. Parsing intent from prose **discards the schema** that made a call machine-readable.
- **Managed Agents** runs the **loop and the sandbox**, with the agent defined as a **versioned resource** addressed by identifier. Its **sessions are stateful** and **stored server-side**. So **Zero Data Retention does not cover** them, and neither does a **HIPAA business associate agreement**. That rules the path out whatever else fits.
- A **self-hosted sandbox** moves **tool execution** onto local infrastructure while **orchestration stays with Anthropic**, and the **model still sees** every tool input and result. Self-hosting makes **image hardening, egress, key rotation and retention** the operator's job.
- A **hook runs** at a **named point** in the loop, inside the **application process** rather than the **context window**, so it **costs no tokens**. The **most restrictive decision wins**. **Matching callbacks** run in parallel in **no fixed order**. **Matchers filter tool names**, not arguments.
- **Refusal works** only in **front of the action**. A **denial** before a tool executes **stops the call**. Code sitting behind it can **describe, replace or annotate** a result and cannot unmake it. **Audit trails and traces** answer a **reporting requirement**, never a **prohibition**.

**ELI5.** Every way of running the kitchen gives something up and takes something on, so look at both. The loop keeps going until the chef asks for nothing. If a rule says "never", put a guard at the door before the dish goes out. Do not just write it in a logbook afterwards.

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
