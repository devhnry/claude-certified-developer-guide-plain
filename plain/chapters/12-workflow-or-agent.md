# Chapter 12: Known Steps Take a Chain; Unknown Ones an Agent

**Summary**: *Two systems can share a model, a tool set and a goal, yet differ in one big way: who picks the next move. If the model picks too often, you pay for a decision your team made years ago, and a fan-out can push the bill to fifteen times a chat. If code picks too often, the design snaps on the first input that is off the route. Everything here hangs on one question. What do you truly not know before the run starts?*

## Every Step You Can Write Down in Advance Is a Step No Model Needs to Choose

Think of a restaurant kitchen. A line cook follows a recipe card, same order every night. A head chef tastes the sauce and decides what to do next. The card is a workflow. The chef is an agent.

Here is a real case. A team wants help with **code review**. People have done it by hand for two years, and the routine never changed. Get the diff. Check it against the house style rules. Spot tests that should have changed and did not. Write a summary. Post it.

Five steps, always in that order. Write them down.

That one act decides the design. When you can list the steps before any input shows up, a **chain of prompts** (the recipe card) wins. It costs less and runs the same way twice. Each stage takes one input and returns one output. If one fails, you know its name and have a saved test case to rerun.

Now hand the same five steps to an agent. It first spends a model call deciding which step comes first. Your team settled that two years ago. You pay tokens and a round trip, and Tuesday's run may choose differently than Monday's.

Call this the **enumeration test**. Could you list the steps before the input arrives? If so, put the plan in code and let the model work inside each step. If not, the model holds the plan and your code sets the limits. Anthropic frames the same split as control flow. A workflow sends models and tools down paths fixed in code. An agent steers itself and decides how to get the job done.<sup>[1]</sup> The real issue is who owns the next decision.

Apply the test to each workload separately. A dependency review follows fixed rules. A debugging helper digs through unfamiliar code. They get different answers, so give them different designs. One checklist makes the debugger trudge through pointless steps. One flexible planner makes every dependency review re-decide what the rules decided.

Hard steps with messy input still go to the model. Code only takes what nobody doubted: the order.

**ELI5.** A recipe card lists every step, so the cook never wonders what comes next. If you can write the steps down, do. Spend the thinking on the tricky parts.

## Five Workflow Shapes, Each Selected by a Different Thing the Task Leaves Open

Do not memorise these as a menu. Sort them by what the run cannot know when it begins, because that is how exam scenarios describe them.

| What is unsettled when the run begins | The shape that answers it | What it buys, and what it charges |
|---|---|---|
| Nothing. Order is fixed and every step feeds on the one before | A chain of calls, one per step | Each call is simpler, so accuracy improves. Total time adds up across steps |
| Which known category the input falls into | A sorting call, then one handler per category | Handlers can specialise. A wrong label sends the request to the wrong handler |
| Nothing, and the parts are independent | Start all parts together, merge afterwards | Wait time drops toward the slowest part. Every part is still paid for |
| Nothing, but a single attempt is not reliable | Run the same job a few times and reconcile | Agreement builds confidence. Cost rises with each attempt |
| Which subtasks the input needs at all | A coordinating call chooses the split, workers do it, a last pass combines | The split suits the input. You gain a coordinator to supervise |
| How many rounds until a written standard is met | A call that makes, a call that critiques, repeated | Clear gains per round if the criteria are explicit. Rounds are uncapped unless you cap them |

These are **prompt chaining**, **routing**, **parallelisation** (in two flavours), **orchestrator-workers** and **evaluator-optimizer**. Anthropic states when each fits. Treat those statements as quick tests.<sup>[1]</sup>

Chaining suits fixed subtasks. It spends a little time to buy accuracy, since each call carries less. Routing has two demands: categories that truly need different handling, and a sorter you can trust. A poor sorter gives a request expert care from the wrong expert, and that spoils every branch. Parallelisation splits work for speed or repeats a job for confidence. Evaluator-optimizer needs written criteria and proof that another round helps. A good hint: human feedback visibly improves the output.

Orchestrator-workers marks the chapter's edge. The other four keep control flow in code. This one lets the model split the work, because the subtasks depend on the input. It is the head chef reading today's orders and deciding who cooks what. Budgets and handoffs, below, apply once you pick it.

**ELI5.** Different jobs need different kitchens. A line of cooks does fixed steps. A host sorts guests to tables. Many stoves cook at once. Ask what you do not know yet.

## An Agent Earns Its Cost Where Later Steps Depend on What Earlier Steps Find

Imagine debugging a system you have never opened. Autonomy exists for this. The reason is not difficulty. It is that nobody can script the investigation. What you check third depends on what the first two showed. The stack trace points at one module. You read it, rule out the obvious cause, and a new suspect appears. That next tool call exists only because of the last result. The path is found as you walk it. The head chef tastes, then reaches for salt.

Keep this trait narrow. Adaptivity pays when step three exists only because of what step two found. Input that merely varies does not count. If the variations are a known list, you want routing.

The loop fits in a breath. The model gets the request, its standing instructions, its tool definitions and any history. It replies, or asks for a tool. The tool runs and hands back its output. This repeats until a reply carries no tool calls.<sup>[2]</sup> Each real result from the environment lets the next choice beat a guess.<sup>[1]</sup> No observable feedback means nothing to adapt to. Feedback is the fuel.

Scenarios probe this. The route now comes from a model reasoning over a growing pile of results, not from branches a reviewer can read. Normal logs fall short, because the key decisions sit in a transcript. Errors snowball, since a wrong turn at step four feeds step five. And nothing ends the loop unless you built a way to.

So build exits that do not rely on the model choosing to stop. The SDK offers two caps that work with or without its cooperation. One caps tool-use round trips. The other caps spend. Each reports its own error subtype, so your code can tell "done" from "cut off."<sup>[2]</sup> Anthropic likewise pairs autonomy with a maximum iteration count.<sup>[1]</sup> A run that hit its turn limit and one that finished look alike in a log holding only the final message.

Two named mistakes flank this, and both look like good engineering.

**Autonomy bought on a settled sequence** happens more often. Someone picks an agent because agents feel modern, for work a coworker could recite. Each run pays for a planning call that settles nothing and differs from the last. You bought only variance, like asking the head chef to improvise a dish that has a card.

The reverse is a **fixed checklist forced onto an investigation**. It assumes you know the order of inquiry. In unfamiliar territory you do not, so the assistant plods through irrelevant steps while the real clue sits untouched.

Anthropic's starting advice: for many applications, one well-tuned call with retrieval and worked examples is plenty. Add structure only when the simpler shape clearly fails.<sup>[1]</sup>

**ELI5.** A chef who tastes, then decides what to add, is an agent. A cook who adds the same thing every time is not. Give the chef a timer, or the tasting never stops.

## The Choice Is Made Per Path, So One System Can Hold a Chain and a Loop

People argue as if a product is all chain or all agent. Real products rarely are.

The test asks about a route through work, and one product can hold several routes. Take invoices. Ninety-odd percent arrive in a format someone already documented. They get the same extraction and validation each time, so a model choosing the order gains nothing. The rest are malformed. For those there is a true choice: return it, query the sender, or hand it to a person. You cannot know which until you see what is wrong.

Test each route alone and the answers are obvious. Test "the invoice system" as one lump and your answer is wrong for about half the traffic.

The fitting design is coded steps for the settled route, plus a model-driven step only where the route forks unpredictably. Line cooks fill the usual orders and the chef takes the strange one. That is one rule used twice, not a halfway point, and it follows Anthropic's advice to start simple and add structure only where the simple shape clearly breaks.<sup>[1]</sup> "Breaks" is a fact about a path, not a product.

One pattern for everything is the error. That one decision causes both named mistakes. Choose the loop, and the settled route pays for planning on every invoice about a question never open. Choose the chain, and the odd invoice meets a branch nobody could write. Your logs usually show the traffic mix, so you can price each mistake.

**ELI5.** Most invoices are plain, so a simple recipe handles them. A few are odd, so a clever helper looks at just those.

## A Coordinator Owns the Budget, the Validation and the Contract at Every Handoff

A **manager or supervisor hierarchy** has one agent that cuts a request into parts and passes each part to a specialist. Picture the head chef passing tickets to the grill, pastry and salad stations. Every specialist gets a private conversation, a tool list, and a history that only it reads. On the managed platform each agent has its own model, system prompt, tools, connected servers and skills, and runs in a context-isolated thread with its own event stream. Tools, servers and context are shared with nobody.<sup>[3]</sup>

Three facts decide scenarios, and none shows in a diagram.

Delegation goes one level deep. A coordinator calls agents on its roster. An agent that is itself a coordinator cannot join that roster, and adding one fails validation.<sup>[3]</sup> The depth limit is configured, so the tree stays shallow by design. The SDK has a depth cap too. It defaults to three layers below the main conversation and can be set down to none.<sup>[4]</sup>

Threads persist. A coordinator can send a follow-up to an agent it used earlier, and that agent still remembers its previous turns.<sup>[3]</sup> So delegation need not be one shot, which is what lets a review loop exist.

Spend is pooled. One session budget covers every thread, and each thread pauses on its own when the cap arrives.<sup>[3]</sup> In the SDK, what subagents spend counts toward the query total. After the cap is hit, the next spawn fails.<sup>[2]</sup>

Now the failure the exam leans on most. **Delegation without governance** is a coordinator that hands out tasks and takes back whatever arrives. It behaves like a mailing list. Answers come in clashing formats. One worker's broken output feeds the next stage. Workers disagree and nobody resolves it. A user reading the final answer spots the problem first.

The cure is to enforce rules at each handoff, in three parts. Give every subagent its own budget, so one worker cannot drain the run. Check each result against a defined shape before passing it on. And write a contract for every handoff, so both sides agree what "finished" holds.

Three substitutes fall short. Retries with a shared trace help recovery but block nothing flowing downstream. Letting workers argue it out removes the coordinator whose job that was. Folding everything into one call throws away the isolation and parallelism the design was built for.

Good assignments are the other half of the job. Anthropic's research system found that terse instructions made agents misread the task or run the same searches twice. The fix was to give each subtask an objective, an output format, advice on tools and sources, and boundaries marking where to stop.<sup>[5]</sup> The coordinator's prompt also says how much effort a question merits. A plain lookup needs one agent and a few tool calls. Broad research gets many more.<sup>[5]</sup> Without that rule the system launched dozens of agents for questions one could answer.

**ELI5.** A head chef who hands out tickets must set each station's budget and taste every plate. Each ticket says what a finished dish looks like. Otherwise stations send out anything.

## Fifteen Times the Tokens of a Chat, and Parallel Exploration Is What Buys It Back

The published figures are big. An agent burns about four times the tokens of a chat. A multi-agent system burns about fifteen times.<sup>[5]</sup> Each worker keeps its own context and spends its own tokens in it, so the cost hits both input and output. Every context gets billed.

See what that money bought. One setup used Claude Opus 4 as lead and Claude Sonnet 4 as workers. On an internal research eval it beat a lone Claude Opus 4 by 90.2%. Anthropic's analysis credits token spend for most of the performance variance.<sup>[5]</sup> So the design mostly wins by buying more parallel computation. That gain is real, and it is what the invoice pays for.

Pay only under narrow conditions. Fan-out earns its multiplier when work splits into parts nobody waits on: many separate sources, material bigger than one context window, or many complex tools.<sup>[5]</sup> It is ruled out when all agents need the same context, when pieces lean on each other, and for most coding, where each step uses the previous result.<sup>[5]</sup> Moving context between agents costs about as much as acting on it.<sup>[6]</sup>

The classic misuse is **fan-out on a dependent chain**, often sold as a speed fix. Something runs slow, so it is cut across parallel workers. Time barely improves, since the pieces always waited on each other. Cost multiplies. Slicing a sequence never makes it parallel. You get a sequence spread over more contexts.

One cost sits outside the arithmetic. Each new worker is another place the run can break. The retry-or-give-up rule, the backoff and the fallback must be wired into every worker. One worker hitting a rate limit with no backoff can hold the compilation step open while the coordinator waits for a reply that never comes. Orchestration multiplies failure handling.

Two levers cut the multiplier. Put a capable model on the coordinator and cheaper ones on the workers, so you skip top rates in every parallel context. And keep the roster honest. Independent agents given truly separate ground have returned largely different findings, which is what the split is for.<sup>[6]</sup> Workers who overlap duplicate each other's spend.

**ELI5.** Ten cooks use ten times the groceries. That pays off only if they cook ten different dishes at once. If each waits on the one before, you spent more and finished at the same time.

## A Subagent Starts Empty, So Whatever the Next Stage Needs Has to Be Written Into the Prompt

Isolation makes delegation worth it, and wrecks handoffs when forgotten.

Say you launch a subagent that is not a fork. It begins with a blank page. Its only link to the parent is the prompt string you pass at launch. File paths, error messages and past decisions reach it only because someone typed them in.<sup>[7]</sup> Nothing is inherited. Coming back, the child's tool calls and results stay inside it, and just its final message returns.<sup>[7]</sup> A worker may read dozens of files while the caller's window grows by one summary. Chapter 7 covers that as a context technique. The design lesson: nothing crosses in either direction unless something carries it. A note through a kitchen hatch carries only what is written on it.

Rules carry over unevenly. Skills do not travel with a delegated task, so a worker needing them must have them registered. Permission scope does travel across the boundary unchanged. Project-level context files load. The parent's conversation, its invoked skills and its already-read files do not.<sup>[8]</sup> A standing preference stated once in the main chat must be repeated in the delegation prompt.

So record handoffs and do not narrate them. The stage that sees a detail writes it down. A later stage cannot rebuild a line range nobody kept. Suppose a coordinator gathers three workers' findings and asks a final stage to attribute each claim to a file. It never saw those facts, so it guesses, and a claim lands on the wrong file. The cure is a structured record made at the moment of observation: path, symbol, line range and the snippet that proves it.

Two weak alternatives show why. **Concatenation passed off as integration** hands the last stage every transcript with no structure, so credit gets worked out twice. **Regular expressions over summaries** extract only what a summary happened to mention, so every gap reads as "no findings."

Ordering needs similar care. Say a report stage starts before its source stage finishes. It writes claims no one can check. Of three fixes, one works. Pruning afterwards leaves a report shaped by unverifiable claims. Telling the stage to wait asks it to see a state it cannot see. Hunting for a word like "done" in the text is guessing from prose. The working fix is to block the downstream stage on an explicit signal the producing stage sets: a status plus a structured manifest of what it made.

Coverage follows the same logic. If output reads well but one region is thin, more effort aimed the same way re-samples the same blind spot, and a higher fixed iteration count spends more with no aim. What helps is a check against the intended scope, plus a way to act on gaps. A coordinator review names the thin region, sends follow-up work there, and reruns the synthesis. Hosted sessions formalise this as an outcome with a rubric. A grader scores the artifact in a separate context window, so the implementer's choices cannot sway it, and its explanation goes back for the next round.<sup>[9]</sup>

**ELI5.** A helper sent to the pantry knows only what is on your note, and comes back with one answer. So write the note well, and make them jot down what they find.

## Memory Is a Design-Time Decision About What Survives the Session

When the loop ends, whatever the agent gathered ends with it. What the next session knows is your choice up front. Call it the agent's **memory scope**. Errors go two opposite ways. Keep too much in the conversation and every call grows heavy, since the full history is re-read each turn. Record too little and the agent has no continuity, because whatever nobody saved vanishes at session close.

| Scope | What is still there next session | What it costs | What it drops |
|---|---|---|---|
| Held in the conversation | Nothing. State lasts across turns, not restarts | No lookup work. Token cost climbs each turn | Everything, on a new or cleared session |
| Written to external storage | What was written, readable across sessions, users and instances | Lookup delay, plus code to read and write | Nothing on the saving side |
| Condensed and reinjected | A summary of the earlier talk | Less per session than replaying it all | Any detail the summary missed |
| Nothing kept | Nothing, on purpose | No extra work | All earlier sessions |

The first row feels great in a prototype. History sits in the message list and goes out on every call. Then cost grows with session length and delay rises as the window fills. The cure is a refactor that lands at the worst time, under production pressure. Deciding early costs an afternoon. Deciding late costs a release.

The managed platform gives external storage a concrete form. A memory store is a folder of documents attached to the session. The agent uses its normal file tools on it, and a line in the system prompt says where it is. Every edit saves an immutable version, so you get an audit trail and point-in-time recovery. Read-only access suits sessions that should use shared reference notes but not change them.<sup>[10]</sup>

**Resumability** is a different need from memory, not a bigger one. Picture a half-hour task with defined intermediate points. Its state must outlive the process doing the work, so a broken run reloads from the last finished point. A longer timeout makes breaks rarer but not survivable. A duplicate copy running beside it doubles cost, and a shared interruption kills both. Anthropic agrees. Restarts are expensive, so it pairs the model's flexibility with deterministic retry logic and regular checkpoints, letting a run resume where the error hit.<sup>[5]</sup>

**ELI5.** When the day ends, the helper forgets everything unless it is in a notebook. Decide up front what goes in. A notebook also lets the helper continue after the lights go out.

## A Framework Wraps the Same Loop and Charges in Visibility

**Agent frameworks** exist because everyone keeps rebuilding the same loop. Strands, LangGraph and PydanticAI belong to a group that includes Anthropic's own SDK. They cover the identical parts of every build: calling the model, defining and parsing tools, chaining calls.<sup>[1]</sup> Nobody should write those twice.

The price is what you can see. Such layers can bury the prompts and responses below them, so debugging gets harder, and mistaken beliefs about what lies beneath cause many bugs. Anthropic's advice is to begin with the model API directly, since many patterns need only a few lines.<sup>[1]</sup> If you use a framework, learn what is inside. Removing layers on the way to production is a normal path, not a retreat.

A deeper question sits under that one: who runs the loop? With the **Messages API** you own each iteration and each exit. An SDK runs that loop inside your process and supplies tool execution and iteration structure. A hosted agent service runs loop and sandbox on its side. You define the agent once as a versioned resource, events flow in from your app, and results stream back.<sup>[11]</sup> Chapter 13 covers that choice and what you hold on each path.

All three share one fact. A framework settles how much of the loop someone else maintains. It has no view on whether the task needed a loop at all. A scale point makes the same argument. When orchestration outgrows one conversation, the plan can move into a script the runtime runs. The branching and in-between results stay out of every context window, and the conversation sees only the finished answer.<sup>[12]</sup> That is the enumeration test again, pointed at the coordination.

**ELI5.** A kitchen gadget saves time but hides what it does to the food. When the dish tastes odd, you cannot tell why. Learn how it works.

## How Wrong Answers Are Built on This Material

The wrong options here name designs that exist. Teams ship each one, so scanning for nonsense finds nothing. Four hidden assumptions cover almost all of them.

- **Autonomy offered where the sequence was already settled.** The option lets the model plan, though the scenario calls the steps repeatable, fixed or hand-run. It spends a model call on something already decided. It turns correct only if the path depends on earlier findings.
- **Isolation assumed away, or bought and discarded.** Some options let agents share a chat, pass every old message to every agent, or remove the coordinator. Each denies what makes delegation worth the cost. At a handoff, the question is what actually gets passed, never whether a fact can be seen.
- **Coordination swapped for watching, bargaining or tidying.** Tracing, retries and dashboards let bad output flow on. Peer settlement hands workers a conflict the coordinator exists to resolve. Generating then pruning leaves a structure built on claims that never held. Each is a real practice aimed one step off the failure.
- **Capacity or effort offered where structure is the problem.** A bigger window for tangled sub-problems that already fit. A higher iteration count for a coverage gap that more of the same effort re-samples. A longer timeout for interruptions that must be survived. Name what an option changes, then check the scenario cared about that.

Match on what the scenario does, not the industry it wears.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Steps are repeatable, known, or done by hand already | A fixed run of prompts, one per step | A model-planned route that is settled, or a shuffled one |
| The right path is unknown at the start and hangs on findings | Planning that adapts per discovery and carries findings along | A fixed checklist, dropped interim results, or a restart when a lead dies |
| One system has a stable-rule job and an open-ended job | Separate structures, split on whether the next step is known ahead | One structure for both, either way, or one giant prompt |
| Findings reach a later stage under the wrong file, or lose detail | A structured record made where the observation happened | Pasted transcripts, pattern-matched summaries, or a last stage that rebuilds it |
| A later stage starts before an earlier one finishes | Block it on a status and manifest the producing stage sets | Guessing completion from prose, or generating first and pruning later |
| A top component reads requests and subordinates keep their own histories and tools | A coordinator with isolated context per subagent | One shared history, a pipeline, or an index lookup |
| Workers return clashing or malformed output that flows on anyway | Per-worker budgets, schema checks before handoff, explicit contracts | Retries with a shared trace, peer negotiation, or one call |
| One request mixes unrelated sub-problems and progress gets lost | A worker per sub-problem, with the coordinator tracking what is done | A larger window, or an agent keeping its own tally |
| Output is coherent but one area of the material is thin | A coverage check against what should exist, plus targeted follow-up | Repeating the broad task, a higher iteration count, or hiding the thin part |
| Subtasks have different success criteria and one may send work back | A state-driven structure with defined moves between subtasks | A straight chain with no way back, or one loop holding every tool |
| A task runs tens of minutes and has named intermediate points | State saved at each point and reloaded on resume | A longer timeout, or a duplicate copy beside it |
| Cost multiplied after a fan-out and answers barely improved | Check if the pieces were ever independent. One agent may fit | Calling parallel workers a speed fix, or adding more |
| One flow has a routine majority and a small unpredictable rest | Coded steps for the routine path, model called only at the fork | Any one pattern for the whole system, either way |

One habit beats the table. List what the scenario leaves unknown and what it settles. Nearly every wrong answer puts a decision on the wrong side.

**ELI5.** Wrong answers sound like real kitchens. Ask what the cook already knows and what the cook cannot know yet. A wrong answer puts the thinking in the wrong place.

## What to Remember

- The **enumeration test**: could you list the steps before the input arrives? If so, code holds the plan and the model works inside each step. If not, the model holds the plan and code holds the limits: turn caps, spend caps, validation.
- A workflow sends models and tools down paths fixed in code. An agent steers itself. Model and tools can match while the owner of the next decision differs.
- Five workflow shapes, chosen by what the run does not know: chaining for a fixed ordered split, routing for known categories, parallelisation for independent parts or repeated tries, orchestrator-workers when the subtasks depend on the input, evaluator-optimizer when criteria are written and another round helps.
- Adaptivity pays only when a later step exists because of what an earlier one found, so an unfamiliar system is the standard case. Variable input alone is a routing problem.
- An agent loop will not stop by itself. Build exits in: a maximum turn count and a spend ceiling returning distinct error states, never the model deciding it is done.
- A coordinator owns the budget, the checking and the handoff contract: a spend limit per worker, each result checked against a defined shape before moving on, and an agreed meaning of a finished subtask. Tracing and retries block nothing downstream. Peer negotiation deletes the component whose job it was.
- A delegated subtask needs an objective, an output format, named tools and sources, and a boundary. Short instructions give workers who misread the job or duplicate each other.
- A multi-agent system costs about fifteen times a chat and an agent about four, since every worker spends its own tokens on its own context. Only real parallel exploration earns that back: separate sources, material beyond one window, many tools. Tightly coupled work pays for fan-out and gains nothing.
- Fan-out adds places to fail, so retry, backoff and fallback belong on each worker. One stuck worker can keep the synthesis step waiting forever.
- A subagent starts without the parent conversation. The launching prompt is the only way in, and only its final message comes back. Skills do not carry over to a delegated task. Permission scope does.
- No later stage can recover a fact nobody recorded, so whoever sees a detail writes it down: path, symbol, line range, evidence snippet. Ordering depends on a status the producing stage sets, not on wording in its prose.
- Memory scope is set at design time. Conversation state dies at the session edge. External storage lasts across sessions and users but adds lookup delay. Summaries keep only what the summariser chose. Stateless keeps nothing. Resumability needs state that outlives the process. A longer timeout only makes interruption rarer.
- Frameworks wrap the same loop and cost visibility, hiding the prompts and responses below. Start with the model API, learn what a framework does underneath, and cut layers on the way to production.
- Pattern choice belongs to a path, not a system. Run the enumeration test on each route alone. A settled route takes code. A model step belongs only where the route forks unpredictably. One choice for the whole product causes both named mistakes: paying for planning on the settled majority, and having no branch for the exception.

**ELI5.** If you know the steps, write a recipe. If not, let a chef taste and decide, with a timer and a budget. Check what each helper hands back.

## Endnotes for this chapter

1. The distinction between workflows, where LLMs and tools are orchestrated through predefined code paths, and agents, where the model dynamically directs its own processes and tool usage; the augmented model as the building block; the five workflow patterns of prompt chaining, routing, parallelisation with its sectioning and voting variants, orchestrator-workers and evaluator-optimizer, each with the condition that selects it; the advice to start with the simplest pattern and to optimise a single call with retrieval and in-context examples before adding structure; the statement that agentic systems trade latency and cost for task performance; the role of ground truth from the environment at each step and of stopping conditions such as a maximum iteration count; and the guidance on frameworks, that they simplify calling models, defining and parsing tools and chaining calls, that they add abstraction layers which obscure prompts and responses and complicate debugging, that incorrect assumptions about what sits underneath are a common source of error, and that reducing abstraction layers is appropriate when moving to production. Anthropic, *Building Effective AI Agents* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)

2. The agent loop as receive prompt, evaluate and respond, execute tools, repeat until a response carries no tool calls, then return the result; a turn defined as one round trip of tool calls and results; the maximum turn and maximum budget options, which count tool-use round trips and spend respectively and return `error_max_turns` or `error_max_budget_usd` result subtypes; and the budget cap covering subagents, whose spend counts toward the query total, with a further spawn failing once the cap is reached. Anthropic, *How the agent loop works* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/agent-loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)

3. Multiagent orchestration lets one agent coordinate others, which act in parallel with their own isolated context; each agent runs in its own session thread with its own conversation history; each agent uses its own model, system prompt, tools, MCP servers and skills, and tools, MCP servers and context are not shared; threads are persistent, so a coordinator can send a follow-up to an agent it called earlier and that agent retains its previous turns; the coordinator delegates to only one level of agents, and referencing an agent that has its own roster fails the create or update request with a validation error, with a maximum of 20 unique agents in a roster; and a session budget is a single shared cap across all of a session's threads, with threads pausing independently as it is reached. Anthropic, *Multiagent orchestration* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)

4. Subagent depth, concurrency and spend can each be capped; by default a subagent can spawn subagents of its own up to three layers below the main conversation, the limit is configurable, and setting it to one turns nesting off. Anthropic, *Create custom subagents* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

5. The lead agent analysing a query, developing a strategy and spawning subagents that explore different aspects simultaneously; agents using roughly four times the tokens of chat interactions and multi-agent systems roughly fifteen times; a multi-agent system led by Claude Opus 4, with Claude Sonnet 4 in the worker role, outperforming single-agent Claude Opus 4 by 90.2% on an internal research eval, with token usage accounting for most of the performance variance; the conditions under which the pattern is worth its cost, being heavy parallelisation, information exceeding a single context window and numerous complex tools, and the conditions under which it is not, being tasks requiring all agents to share the same context, domains with many dependencies between agents, and most coding tasks; the requirement that each delegated subtask carry an objective, an output format, guidance on tools and sources, and clear boundaries, without which agents duplicate work or leave gaps; the observed failure of short vague instructions producing subagents that misinterpreted the task or repeated each other's searches; effort-scaling rules embedded in the lead agent's prompt; and the treatment of statefulness, compounding errors and durable execution, where restarts are expensive so deterministic safeguards such as retry logic and regular checkpoints allow an agent to resume from where the error occurred. Anthropic, *How we built our multi-agent research system* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)

6. Multiagent approaches suit highly parallelisable problems with independent sub-problems and struggle on interdependent tasks; in a vulnerability-scanning study, independent parallel agents and a coordinating swarm found largely different results, with only twelve vulnerabilities in common; and agents face a knowledge-transfer disadvantage in that transmitting context between them costs about as much as acting on it. Anthropic, *Patterns and problems in multiagent systems* (Anthropic Research, accessed 2026-09-09), [https://www.anthropic.com/research/multiagent-systems](https://www.anthropic.com/research/multiagent-systems)

7. Subagents are separate agent instances, so each runs in its own conversation that starts fresh unless it is a fork; intermediate tool calls and results stay inside the subagent and only its final message returns to the parent; the only content passed from parent to subagent is the Agent tool's prompt string, so file paths, error messages and decisions the subagent needs must be included directly in that prompt; multiple subagents can run concurrently so independent subtasks finish in the time of the slowest; and each subagent can carry a tailored system prompt and be limited to a specific tool set. Anthropic, *Subagents in the SDK* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)

8. A non-fork subagent starts with a fresh, isolated context window and does not see the parent conversation's history, the skills already invoked, or the files already read; its initial context contains its own system prompt, the delegation message, the project context-file hierarchy, preloaded skills named in its own definition, and a git snapshot; a standing preference stated in the main conversation must be restated in the delegation prompt; and the main conversation's output style and auto memory never reach it. Anthropic, *Create custom subagents* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

9. An outcome tells a session what the end result should look like and how to measure its quality, and the agent self-evaluates and iterates toward it; a grader is provisioned automatically to evaluate the artifact against a required rubric, and it uses a separate context window to avoid being influenced by the main agent's implementation choices; the grader's explanation of which criteria passed or failed is handed back to the agent for the next iteration, and evaluation results are `satisfied`, `needs_revision`, `max_iterations_reached`, `failed` or `interrupted`. Anthropic, *Define outcomes* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/define-outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes)

10. Each session starts with a fresh context by default and any state built up is gone when the session ends; a memory store is a workspace-scoped collection of text documents mounted as a directory inside the session sandbox, which the agent reads and writes with its ordinary file tools, with a note describing each mount added automatically to the system prompt; every change to a memory creates an immutable version, giving an audit trail and point-in-time recovery; and access defaults to read-write with read-only supported. Anthropic, *Using agent memory* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/memory](https://platform.claude.com/docs/en/managed-agents/memory)

11. Two ways of building are contrasted: direct model prompting through the Messages API, suited to custom agent loops and fine-grained control, and a pre-built configurable agent runtime on managed infrastructure, suited to long-running and asynchronous work, where the agent is defined once as a versioned resource and the application sends events and streams results back. Anthropic, *Claude Managed Agents overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/overview](https://platform.claude.com/docs/en/managed-agents/overview)

12. With subagents, skills and agent teams, Claude is the orchestrator, deciding turn by turn what to spawn next, and every result lands in a context window; a dynamic workflow moves the plan into a script, which holds the loop, the branching and the intermediate results, so the conversation's context holds only the final answer. It suits tasks needing more agents than one conversation can coordinate. Anthropic, *Orchestrate subagents at scale with dynamic workflows* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows)
