# Chapter 12: Known Steps Take a Chain; Unknown Ones an Agent

**Summary**: *Two systems can be built on one model, one tool set and one goal, and still differ entirely in who decides what happens next. Lean too far toward autonomy and you pay a model call to reach a conclusion somebody reached years ago. The bill also runs to fifteen times a chat once the work fans out. Lean too far the other way and the design fails on the first input that does not fit the route it was handed. This chapter is the architecture arranged around one question: what is genuinely not known before the run starts.*

## Every Step You Can Write Down in Advance Is a Step No Model Needs to Choose

**First, the idea.** Some jobs have steps you already know, in an order you already know. Those jobs do not need a model to decide what comes next. You write the order down in code, and the model only does the work inside each step.

**The analogy for this chapter: a kitchen.** A kitchen has two ways of making food. One is a **recipe card**. The steps are printed, in order, and the cook just follows them. That is a **workflow** (a path fixed in code). The other is a **chef who tastes as they go**. They decide the next move from what they find in the pot. That is an **agent** (a model that directs its own process). In both kitchens the cook is the same **model** and the pantry is the same **tool set**. The only difference is who decides the next step. The exam uses the real words, so every kitchen word below comes with its real term in bold.

**The example.** A team wants an assistant for their **code review**. The **sequence is already settled**, because humans have been **running it by hand** for **two years**. Pull the diff. Check it against the house style rules. Look for tests that should have moved and did not. Summarise what changed. Post the summary.

**Five steps**, same order, every time. Now **write them down**. That is the **recipe card (the chain of prompts)**.

That act **settles the architecture**. When the **sequence is knowable** before the input arrives, a **chain of prompts** is **cheaper, reproducible and inspectable** at every stage. Each stage takes one input and produces one output. Run it twice and the request travels the same route both times. Something breaks and the stage that broke has a **name and a fixture** (a saved test input) you can rerun.

**What goes wrong with an agent here.** Hand those five steps to an agent instead and the first thing it does is **burn a model call** working out **which one comes first**. That is the chef stopping to decide whether to read the card. That call has **exactly one job**. It reaches a **conclusion the team reached** two years ago. You pay tokens for it. You pay a round trip for it. And you accept that Tuesday's run may reach a different conclusion.

**The enumeration test.** Can you write the sequence down before the input arrives?
- If you can, **code holds the plan** (the recipe card) and the model does the work inside each step.
- If you cannot, the **model holds the plan** (the chef decides) and your **code holds the limits**.

Anthropic draws the same line by asking where control flow (who decides the next step) lives. A workflow runs models and tools along **paths fixed in code**. An agent **directs its own process** and keeps control of how the task gets done.<sup>[1]</sup> Control flow is the **whole question**.

**Run the test on each workload.** The test has a second use, and it is the one scenarios reach for. Run it on **each workload separately** rather than once on the whole system. A **dependency review** that **follows fixed rules** and a **debugging assistant** that **explores unknown code** answer the test differently. So they should **not share a structure**. Force both through one checklist and investigations march through steps that do not apply. Give both an adaptive planner and every dependency review pays for a decision the rules already made. **One structure**, **two badly served workloads**.

**This is not a vote for simple.** The enumeration test is **not an argument for simplicity**. It is an argument about where a **decision gets made**. A step whose content is **genuinely hard**, needing judgement over **ambiguous input**, still belongs to the model. What belongs in code is the part nobody was ever unsure about: **which step follows which**.

**ELI5.** If you already know the steps, write them on a recipe card and let the cook follow the card. Do not pay a chef to think about it again every day. Let the cook think hard only inside a step that is truly tricky.

## Five Workflow Shapes, Each Selected by a Different Thing the Task Leaves Open

**First, the idea.** There are named patterns for workflows. Do not learn them as a list. Learn them by what the run does not know when it starts.

**Why not a catalogue.** The **named patterns** get taught as a **catalogue**. That is the wrong shape for using them. Sort them instead by what the **run does not know** when it begins, because that is the property a **scenario actually states**. In kitchen terms, these are five kinds of recipe card. Each one fits a different gap in what the cook knows.

| What is unsettled when the run begins | The shape that answers it | What it buys, and what it charges |
|---|---|---|
| Nothing. The order is fixed and each step consumes the last one's output | A chain of calls, one per step | Every call gets an easier job, so accuracy rises. Latency is the sum of the steps |
| Which of a known set of categories this input belongs to | A classifying call in front of handlers written per category | Each handler is tuned for one case. A misclassification sends the request down the wrong branch |
| Nothing, and the parts do not depend on each other | The parts issued at once and joined afterwards | Elapsed time falls toward the slowest part. Every part is still billed |
| Nothing, but one pass is not trustworthy on its own | The same job run several times and the answers reconciled | Confidence from agreement. Cost scales with attempts |
| Which subtasks the input even requires | A coordinating call that decides the split, workers that run it, a synthesis pass | Decomposition that fits the input. A coordinator you now have to govern |
| How many rounds it takes to meet a written standard | A producing call and a critiquing call, looping | Measurable improvement per round, where criteria are explicit. Rounds without a cap |

**The five names.** Those are **prompt chaining** (a recipe with ordered steps), **routing** (a host who sends each order to the right station), **parallelisation** in its two variants (several cooks working at once), **orchestrator-workers** (a head chef who splits the order), and **evaluator-optimizer** (cook and taster in a loop). Anthropic attaches a **selecting condition** to each one. The conditions are worth holding as **tests** rather than as descriptions.<sup>[1]</sup>

**What each one wants:**
- **Chaining** wants a task that **splits cleanly into fixed subtasks**. It **trades latency for accuracy** by giving every call less to do.
- **Routing** wants two things at once. The categories must **genuinely deserve separate handling**. And you need **classification you can trust** with the routing decision. Miss the second and the whole arrangement degrades, because a misrouted request gets handled well by the wrong specialist. Bad classification **poisons every branch**.
- **Parallelisation** **splits on independence** when the goal is speed. It **repeats one job** when the goal is confidence.
- **Evaluator-optimizer** wants written criteria and a demonstrable gain from another round. The honest signal that it fits: a **human articulating feedback** measurably improves the output.

**The odd one out.** Orchestrator-workers sits on this chapter's boundary and is worth marking as such. The other four have their **control flow written down**. This one **hands the decomposition** itself to the model, because the subtasks **depend on the specific input** and cannot be fixed in advance. The **model decides the split**. Everything later in this chapter about coordination, **budgets and handoffs** starts applying the moment you choose it.

**ELI5.** There are five kinds of recipe card. Pick the one that matches what the cook does not know yet. If the head chef has to decide how to split the order, that is the one where you must start watching the budget.

## An Agent Earns Its Cost Where Later Steps Depend on What Earlier Steps Find

**First, the idea.** An agent is worth paying for when the next step cannot be known until you see what the last step found. That is the chef tasting the sauce and deciding what to add.

**The case autonomy was built for.** Debugging an **unfamiliar system** is the case **autonomy was built** for. The reason is **structural** rather than a matter of difficulty. Nobody can write that investigation down in advance, because the **third thing worth checking** depends entirely on what the **first two returned**. A stack trace points at a module. Reading the module **rules out the obvious cause** and raises a different one. The next tool call exists because of that result and would never have been chosen otherwise. The **path is discovered, not planned**.

**The property to look for.** It is narrow. A **later step that exists** because of an **earlier finding** is what **adaptivity buys**. **Variability** in the input alone does not qualify. A known set of variations is a **routing problem**.

**The loop.** It is short enough to hold in one sentence. The model is handed the request along with its **standing instructions** (the **system prompt**), its tool schemas (the descriptions of its tools) and whatever history exists. It either answers or asks for a tool. The tool runs and the result goes back. The **cycle repeats** until a response arrives carrying **no tool calls**.<sup>[2]</sup> In the kitchen, this is taste, adjust, taste again, until the dish is done.

**Feedback is the fuel.** **Ground truth from the environment** at each step is what makes the **next decision better than a guess**.<sup>[1]</sup> An agent on a task with **no observable feedback** has nothing to adapt to. A chef who cannot taste is just guessing.

**What comes with the loop.** This is the part scenarios test:
- The **route through the work** is now produced by the model reasoning over whatever has piled up. It is no longer **branching logic** a reviewer can read line by line.
- **Operational logs stop being enough**, because the interesting decisions happen inside a **transcript**.
- **Errors compound**. A **wrong turn** at step four is the input to step five.
- The loop will **not stop on its own** unless you tell it how.

**Exit conditions.** So **exit conditions** belong in the design. They must not depend on the **model volunteering to finish**. The SDK gives you **two caps** that hold without cooperation. One is a **ceiling on tool-use round trips**. The other is a **ceiling on spend**. Each returns its own **error subtype**, so your code can tell a finished task from a **truncated** one.<sup>[2]</sup> Anthropic pairs autonomy with a **maximum iteration count** for the same reason.<sup>[1]</sup> A run that stopped because it **ran out of turns** and a run that stopped because it was done look identical in a log that records only the last message.

**Two named anti-patterns.** They sit either side of this. Both **read as competence**.

- **Autonomy bought on a settled sequence** is the commoner one. Somebody reaches for an agent because agents are the interesting architecture, on a task whose steps a colleague could **recite from memory**. Every run pays for a **planning call that decides nothing**, and every run differs from the last with no gain in what the system can do. You **bought variance** and nothing else.
- **A fixed checklist imposed on an investigation** is the mirror. It presumes the **order of inquiry is known**, which is precisely what an unfamiliar system denies. You watch an assistant march through irrelevant steps while the actual lead goes uninvestigated.

**Where to start.** Anthropic's advice is blunt, and it survives contact with production. **Optimising a single call** with retrieval and **worked examples** (sample answers placed in the prompt) is enough for many applications. Add structure only where the **simpler shape demonstrably fails**.<sup>[1]</sup>

**ELI5.** A chef who tastes needs a timer, or they might keep fiddling forever. Use the tasting chef only when the next move depends on the last taste. If the steps are the same every day, a recipe card is cheaper.

## The Choice Is Made Per Path, So One System Can Hold a Chain and a Loop

**First, the idea.** A single application can have more than one route through it. You pick recipe card or tasting chef for each route, not once for the whole restaurant.

**Not one or the other.** The **two patterns** get argued as though a system has to be one or the other. **Most systems** that **reach production** are not.

**The invoice example.** Look at what the enumeration test is actually asked about. It is a question about a **route through work**, and a **single application** routinely carries **more than one route** with different properties. Invoices are the clean case.
- **Ninety-odd percent** of them arrive in a shape somebody has **already written down**. They move through the same extraction and the **same validation every time**. They would gain nothing from a **model choosing the order**.
- The **remainder arrive malformed**. What happens next is a **real decision** among several live options: send it back, ask the submitter, escalate to a person. **Nobody can say in advance** which applies, because that depends on what the malformation turns out to be.

**Test each route.** Run the test on **each route separately** and both answers are obvious. Run it once on "the invoice system" and whichever answer you get is **wrong for half the traffic**.

**The shape that fits.** Use a **coded sequence for the settled route** (the recipe card). Add a **model-driven step** (the tasting chef) at the one point where the **route forks unpredictably**. That is not a compromise between two architectures. It is the **same rule applied twice**. It is also what Anthropic's own advice implies: **start simple**, and add structure only where the simple shape is demonstrably failing.<sup>[1]</sup> Demonstrably failing is a **property of a path**, not of a product.

**The anti-pattern.** The **whole-system pattern choice** is the anti-pattern. It produces both of this chapter's **named errors at once** from a single decision.
- Pick the loop, and the settled route **pays a planning call** on every invoice to decide something that was **never open**.
- Pick the chain, and the exception **falls through a branch** nobody could write.

The **traffic profile** tells you how much each mistake costs. It is usually in the logs already.

**ELI5.** Most days the kitchen makes the same dish, so use the recipe card. Once in a while a strange order comes in, so call the chef for that one. Do not make everybody follow one way for everything.

## A Coordinator Owns the Budget, the Validation and the Contract at Every Handoff

**First, the idea.** When one agent splits work among others, it becomes a coordinator. In the kitchen, that is the **head chef** (the **coordinator**, also called the orchestrator) handing orders to **station cooks** (the **subagents**, or workers). The head chef is responsible for the budget, for checking the plates, and for what each handoff must contain.

**What the hierarchy is.** A **manager or supervisor hierarchy** is one agent that **decomposes a request** and **delegates the pieces** to specialists. Each specialist holds a **separate conversation** (its own station), a tool list of its own, and a **history nobody else reads**. The managed-agent surface makes it concrete. Every agent carries its own model, system prompt, tools, connected servers and skills. Each runs in a **context-isolated thread** with its own event stream. Tools, servers and context are **shared with nobody**.<sup>[3]</sup>

**Three properties decide scenarios.** None of them shows up in a diagram.

1. **Delegation goes one level.** A coordinator calls the agents on its roster. An agent that is itself a coordinator cannot go on that roster. The attempt **fails validation**.<sup>[3]</sup> Depth is a **configured limit** rather than an open tree, so the hierarchy stays **shallow by construction**. The SDK exposes the same idea as a **depth cap**, **three layers** below the main conversation by default and **settable down to none**.<sup>[4]</sup>
2. **Threads persist.** A coordinator can send a **follow-up** to an agent it already used. That agent still holds everything from its **earlier turns**.<sup>[3]</sup> Delegation is **not necessarily one-shot**, which is what makes a **review loop** possible.
3. **Spend is pooled.** A **session budget** is a **single cap** shared across every thread. Threads **pause independently** as it is reached.<sup>[3]</sup> On the SDK side, subagent spend counts toward the query total. Once the cap is hit, the **next spawn fails** outright.<sup>[2]</sup>

**The failure mode.** This is the one the exam tests hardest. **Delegation without governance** is an orchestrator that **hands out work** and **accepts whatever comes back**. It looks like an architecture and behaves like a **mailing list**. Here is what goes wrong:
- Subtasks return in **incompatible shapes**.
- One worker's **malformed output** becomes the next stage's input.
- Contradictions between workers **never get reconciled**.
- The first human to notice is a user reading the final answer.

**Nothing checked anything** on the way.

**The repair.** It is **enforcement at the point of handoff**, in three parts:
- A **budget per subagent**, so no single worker can consume the run.
- Validation of each result against a **defined shape** before it moves on, so a malformed return stops where it was produced.
- An **explicit contract per handoff**, so both sides agree what a **finished subtask** contains.

**Alternatives that fail.** Two plausible ones fail for reasons worth naming:
- **Retries plus a shared trace** improve recovery and make the **postmortem easier**. But they **intercept nothing** on the way downstream, which is precisely the failure described.
- Letting workers see each other and **negotiate their differences** asks them to settle contradictions among themselves. It **deletes the component** whose job that was.

**Collapsing** everything back into **one call** is the third. It **abandons the isolation** and the parallelism you built the architecture for, rather than managing them.

**Delegation detail.** This is the other half of what a coordinator owns. Anthropic's research system found that subtasks handed out as **short instructions** produced agents that **misread the assignment** or **repeated each other's searches**. The repair was to give every subtask four things:
- an **objective**
- an **output format**
- guidance on which **tools and sources** to use
- **boundaries** saying where it stops<sup>[5]</sup>

**Effort scaling.** That system also encodes how much **effort a query deserves**, directly in the **coordinator's prompt**. A **simple lookup** gets one agent and a handful of tool calls. Genuinely broad research gets many more.<sup>[5]</sup> Without the scaling rule, the observed behaviour was **dozens of agents spawned** for questions that needed one.

**ELI5.** The head chef hands out orders, but must also check every plate before it leaves. Each station gets a small food budget and a clear order ticket that says what a finished plate looks like. If the head chef just accepts whatever comes back, bad plates reach the customer.

## Fifteen Times the Tokens of a Chat, and Parallel Exploration Is What Buys It Back

**First, the idea.** Many cooks cost a lot more than one. It is only worth it when the work really splits into parts that can happen at the same time.

**The numbers.** They are published and they are not small. An agent uses roughly **four times the tokens** of a chat interaction. A **multi-agent system** uses roughly **fifteen**.<sup>[5]</sup> Every worker (every station) **holds its own context** and spends its own tokens against it. So the multiplier lands on input and output alike. Every **context is paid** for.

**What it bought.** Set that beside what the architecture delivered. A system running Claude **Opus 4 as the lead** with **Claude Sonnet 4 workers** beat a single-agent Claude Opus 4 baseline by **90.2%** on an internal research eval. Anthropic's analysis attributes most of that **performance variance** to **token spend**.<sup>[5]</sup> The shape works largely because it buys more **parallel computation**. That is a real gain. It is also the **whole invoice**.

**When fan-out earns it.** The qualifying condition is narrow. **Fan-out** (splitting work across many workers at once) **earns the multiplier** on work that genuinely splits into parts nobody has to wait on:
- research across many **separate sources**
- material **larger than one context window**
- a surface with **many complex tools**<sup>[5]</sup>

**When it does not.** The disqualifying conditions are just as specific:
- tasks where every agent needs the **same context**
- domains with **heavy dependencies** between the pieces
- **most coding work**, where each step consumes the last one's result and there is little left to explore in parallel<sup>[5]</sup>

Later Anthropic research sharpens the edge. **Moving context between agents** costs about as much as acting on it. So coordination is **nowhere near the cheap part** of the design.<sup>[6]</sup>

**The anti-pattern: fan-out on a dependent chain.** It usually arrives as a **latency fix**. Work that ran slowly gets split across **parallel workers**, on the reasoning that simultaneous work finishes sooner. **Elapsed time barely moves**, because the pieces were waiting on each other all along. The **bill multiplies**. Splitting a sequence does **not make it parallel**. You get a sequence with more contexts in it. In the kitchen, hiring ten cooks does not help if each one has to wait for the sauce before they can start.

**A control cost the arithmetic does not show.** Every worker you add is another point at which the **run can break**. The **retriable-versus-terminal decision** (is this error worth trying again, or is it final), the backoff (waiting before a retry) and the fallback all have to be **wired into each one separately**. Say a single worker meets a **rate limit** with nothing to back off with. It can hold the compilation step open while the coordinator waits for a return that never arrives. Orchestration does **not replace failure handling**. It **multiplies the work**.

**Two levers.** They reduce the multiplier without abandoning the shape:
- Run the coordinating agent on a **capable model** and the **workers on cheaper ones**, so top-tier rates are not paid across every parallel context.
- Keep the **roster honest**. Independent agents pointed at **genuinely separate territory** have been observed returning **largely different findings**, which is the return the split was supposed to produce.<sup>[6]</sup> **Overlapping workers** are **money spent twice**.

**ELI5.** More cooks means more groceries and more wages. It pays off only when the cooks can work at the same time on different things. If every cook has to wait for the one before, you just pay more for the same slow dinner.

## A Subagent Starts Empty, So Whatever the Next Stage Needs Has to Be Written Into the Prompt

**First, the idea.** Each station cook starts with an empty counter. They know only what is written on the order ticket. If the head chef forgets to write something on the ticket, the cook never learns it.

**Isolation cuts both ways.** **Isolation** is the property that makes **delegation useful**. It is also the property that **breaks handoffs** when a designer forgets it holds.

**What crosses the boundary.** A **subagent** that is **not a fork** begins with **no parent conversation**. The only content crossing from parent to child is the **prompt string** (the order ticket) on the call that launched it. File paths, error text and decisions already taken are present because **somebody put them** there.<sup>[7]</sup> **Nothing arrives by inheritance**. Going the other way, intermediate tool calls and results stay inside the child. Only its **final message returns**.<sup>[7]</sup> A worker can read dozens of files and the caller's window **grows by a summary**. Chapter 7 owns that trade as a context technique. Architecturally what matters is the consequence: **nothing crosses unless something carries** it, in either direction.

**Constraints inherit unevenly.** That is where a design gets caught.
- **Skills do not carry** over to a delegated task. A worker depending on a specific instruction set needs it registered against that worker.
- **Permission scope does carry** over and is not reset at the boundary.
- **Project-level context files load**. The parent's own conversation, its invoked skills and its already-read files do not.<sup>[8]</sup>
- A **standing preference** you stated once in the main conversation has to be **restated in the delegation prompt** to reach the agent doing the work.

**Record, do not narrate.** Handoffs get **recorded rather than narrated**. The stage that **observes a detail** is the stage that **writes it down**, because no later stage can recover a **line range nobody kept**. Say a coordinator collects three workers' findings and asks a synthesis stage to **attribute claims to files**. It is asking for facts that stage never saw. Guessing is where a claim gets attached to the wrong file. The repair is a **structured record** produced at the **point of observation**: path, symbol, line range, and the snippet standing as evidence.

**Two named alternatives that fail instructively:**
- **Concatenation offered as integration** hands the synthesiser every transcript and **imposes no structure** at all. Attribution then gets worked out a **second time downstream**, when it was free the first time.
- **Regular expressions over summaries** extract whatever a summary happened to mention. Every **omission stays omitted** and reads as an absence of findings.

**Sequencing between stages.** It needs the same treatment. A report stage that **runs before its source stage** has finished produces **claims nobody can check**. Three repairs suggest themselves while only one works:
- **Generating first and pruning afterwards** leaves a report whose shape was set by claims that could never be checked.
- Asking the report stage to hold off requires it to observe a state it cannot see.
- Scanning a message for the right words reads **done-ness out of prose**.

The one that works is to **block the downstream stage** on an **explicit signal the producing stage sets**. That signal is a status plus a **structured manifest** (a list) of what it produced. The ordering then rests on a fact.

**Coverage.** It is the same argument one level up. Say output reads coherently but **one region is thin**. More effort aimed the same way **re-samples the same blind spot**. A **higher fixed iteration count** spends more without pointing it anywhere. Effort has to be aimed. What closes a gap is an explicit **check against the intended scope**, plus a route for acting on whatever it finds missing. That means a coordinator review that **names the thin region**, **dispatches follow-up work** at it, and **reruns the synthesis**.

**Outcomes and graders.** Hosted sessions formalise this as a **defined outcome** with a rubric. A **grader** evaluates the artifact in a **separate context window**, precisely so the implementation choices it is judging cannot influence it. Its explanation goes back for the next round.<sup>[9]</sup>

**ELI5.** A station cook only knows what is on the order ticket. If a detail matters, write it on the ticket, and have each cook write down what they saw as they saw it. Do not hope the next person remembers.

## Memory Is a Design-Time Decision About What Survives the Session

**First, the idea.** When a session ends, everything the agent learned ends with it, unless you saved it somewhere. In the kitchen, the question is what goes into the **notebook** (the **memory**) that the next shift can read.

**Memory scope.** An agent loop ends and everything it accumulated ends with it. What the next session knows is a choice you make at **design time**. Call that choice the agent's **memory scope**. The two ways of getting it wrong pull in **opposite directions**:
- Too much state carried in the conversation **inflates every call**, because the whole history gets **re-read on every turn**.
- Too little written down anywhere **strips the agent of continuity**. **Whatever nobody recorded** is gone the moment the **session closes**.

| Scope | What is still there next session | What it costs | What it drops |
|---|---|---|---|
| Held in the conversation | Nothing. State survives turns, not restarts | No retrieval work; token cost grows with every turn | Everything, on a new session or a clear |
| Written to external storage | Whatever was written, readable across sessions, users and instances | Retrieval latency, plus the read and write logic to maintain | Nothing on the persistence side |
| Condensed and reinjected | A summary of the prior conversation | Less per session than replaying history in full | Any detail the summariser did not think to keep |
| Nothing kept | Nothing, by design | No overhead at all | Everything from earlier sessions |

**The trap.** The first row **prototypes beautifully**. History goes in the message list, the list goes up on every call, and it works for a while. Then **cost scales with session length** and **latency climbs** as the window fills. The fix is a refactor that is mechanically simple and arrives at the **worst possible moment**: under production pressure, on a deadline already running. **Deciding at design time** costs an afternoon. Deciding under **pressure costs a release**.

**How the managed platform does it.** The managed platform gives the external row a documented shape. A **memory store** is a collection of documents **mounted into the session** as a directory (the notebook on the shelf). The agent reads and writes it with the **same file tools** it uses for everything else. A note in the **system prompt** says where to look. Every change creates an **immutable version**, so you get an **audit trail** and a **point-in-time recovery** path. Access can be **granted read-only** where a session should consume **shared reference material** without adding to it.<sup>[10]</sup>

**Resumability.** It separates memory from persistence proper, and it is a different requirement rather than a stronger one. Say a task runs for half an hour with **defined intermediate points**. It needs state that **outlives the process** computing it, so an interrupted run reloads from the **last completed point** instead of starting over.
- A **longer timeout makes interruption rarer** without making it **survivable**.
- A **duplicate copy** running alongside **doubles the cost** and loses both to any interruption they share.

Anthropic reaches the same conclusion operationally. **Restarts are expensive**, so the answer pairs the model's adaptability with **deterministic retry logic** and **regular checkpoints** that let a run resume from where the error hit.<sup>[5]</sup>

**ELI5.** When the shift ends, the cook forgets everything unless they wrote it in the notebook. Writing everything in the notebook takes time to look up. Writing nothing means starting over each day. Decide what goes in the notebook before the restaurant opens, not in the middle of a rush.

## A Framework Wraps the Same Loop and Charges in Visibility

**First, the idea.** An agent framework is like a **meal kit**. It comes with the common parts already done, so you do less work. But you cannot see exactly what is in each bag.

**What frameworks are for.** **Agent frameworks** exist because the loop has a **shape everybody rebuilds**. Strands, LangGraph and PydanticAI belong to a category that also holds **Anthropic's own SDK**. The category earns its place by handling the parts that are **identical in every implementation**: calling the model, defining and parsing tools, chaining calls together.<sup>[1]</sup> Nobody should **write those twice**.

**What they charge.** What they **charge is visibility**. Anthropic is direct about the tradeoff:
- Those layers can **obscure the prompts and responses** underneath, which makes debugging harder.
- **Wrong assumptions** about what sits below the abstraction are a **common source of error**.
- The recommendation is to start against the **model API directly**, because many of these patterns run to a few lines of code.<sup>[1]</sup>

Use a framework and you should **understand its internals**. Moving into production, **reducing abstraction** is a legitimate direction of travel rather than a regression.

**Who runs the loop.** Underneath the framework question sits a different one. There are three answers:
- Write it against the **Messages API** and you own every **iteration and every exit condition**.
- An SDK runs the same loop **inside your process** and supplies tool execution and iteration structure.
- A **hosted agent service** runs the loop and the sandbox elsewhere. The agent is defined once as a **versioned resource**, and events go in from your application while **results stream out**.<sup>[11]</sup>

Chapter 13 owns that choice and what each path leaves you holding.

**What holds across all of them.** A framework decides how much of the loop **somebody else maintains**. It has **no opinion** about whether the task **needed a loop** at all. A meal kit does not tell you whether you needed to cook.

**One scale point.** It is worth carrying, because it is the same argument in different clothes. When orchestration grows past what a **single conversation can coordinate**, you can move the **plan into a script** that the **runtime executes**. That keeps the **branching and the intermediate results** out of every context window. The conversation receives only the **finished answer**.<sup>[12]</sup> That is the **enumeration test** again, aimed at the coordination rather than at the task.

**ELI5.** A meal kit saves you from chopping the same onions every time, but you cannot always see what went in. Use it if you know what is inside. And a kit never tells you whether you needed to cook at all.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers on the exam are real designs that real teams have built. They go wrong because of one hidden assumption. Learn the four assumptions and you can spot them.

**Why they are hard to spot.** Wrong answers here **name real architectures**. None of them is stupid. Every one describes something a **competent team has shipped**, which is why reading for **obvious nonsense finds nothing**. What separates them is a **single assumption underneath**. **Four assumptions** produce nearly all of them.

**The four wrong assumptions:**
- **Autonomy offered where the sequence was already settled.** The option lets the **model plan a path**, on a scenario describing steps as **repeatable**, fixed, or **already run by hand**. It is **not a weaker answer** than the chain. It **pays a model call** to decide something the scenario **stated as decided**. It becomes correct only when the scenario says the **path depends on what earlier steps find**.
- **Isolation assumed away**, or **paid for and then discarded.** These are options that treat **separate agents** as **sharing a conversation**, that **forward every prior message** to every agent, or that **delete the coordinating component**. All three deny the property that makes **delegation worth its cost**. The **design question** at a handoff is never whether a **fact is visible**. It is what **gets passed**.
- **Coordination replaced by observation**, by **negotiation**, or by **cleanup.** **Tracing, retries and dashboards** intercept **nothing on the way downstream**. **Peer-to-peer reconciliation** asks workers to settle **contradictions the coordinator exists** to settle. **Generating output** and **pruning it afterwards** leaves the structure shaped by **claims that never held**. Each is a **real practice aimed** one step away from the stated failure.
- **Capacity or effort offered** where **structure is the problem.** Examples are a **larger window** against **interleaved sub-problems that already fit**, a **higher iteration count** against a **coverage gap** that more of the same effort will **re-sample**, and a **longer timeout** against **interruptions that need surviving** rather than avoiding. **Name the quantity the option changes**, then check whether the scenario named that quantity.

**Match on what the scenario** is doing rather than on the **industry it is dressed** in.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| The steps are repeatable, known, or already run by hand | A fixed sequence of prompts, one per step | Letting the model plan a route that is already decided, or randomising it |
| The correct path is unknown at the start and depends on what is found | Planning that adapts to each discovery, carrying findings forward | A fixed checklist, ignoring intermediate results, or restarting when a lead dies |
| One system holds a stable-rule workload and an open-ended one | Different structures, split on whether the next step is known in advance | One structure imposed on both, in either direction, or one large prompt for everything |
| Findings reach a later stage attached to the wrong file, or missing detail | A structured record written where the observation was made | Concatenating transcripts, pattern-matching summaries, or asking the last stage to reconstruct it |
| A later stage runs before an earlier one has finished | Block it on an explicit status and manifest the producing stage sets | Inferring completion from prose, or generating first and pruning after |
| A top component interprets requests and subordinates keep their own histories and tools | A coordinator with per-subagent isolated context | Reading it as one shared history, as a pipeline, or as retrieval from an index |
| Workers return contradictory or malformed output that moves downstream anyway | Per-worker budgets, schema validation before the handoff, explicit contracts | Retries plus a shared trace, peer negotiation, or collapsing to a single call |
| One request interleaves several unrelated sub-problems and progress gets lost | One worker per sub-problem, with completion tracked by the coordinator | A larger window, or asking the agent to keep its own running tally |
| Output is coherent but one region of the material is thin | A coverage check against what should be there, plus targeted follow-up work | Repeating the broad assignment, raising the iteration count, or hiding the thin section |
| Subtasks have different success criteria and one may hand work back | A state-driven structure with defined transitions between subtasks | A linear chain with no return path, or one loop holding every tool |
| A task runs for tens of minutes and has named intermediate points | State persisted at each point and reloaded when the run resumes | A longer timeout, or a duplicate copy running in parallel |
| Cost multiplied after a fan-out and the answers barely improved | Check whether the pieces were ever independent; a single agent may fit | Treating parallel workers as a latency fix, or adding more of them |
| One flow has a routine majority and a small unpredictable remainder | A coded sequence for the routine path, with the model invoked only where it forks | Any option choosing one pattern for the whole system, in either direction |

**A habit that does more than the table.** Before comparing options, name what the scenario says is unknown when the run begins, and what it says is already settled. Almost every wrong answer here moves a decision to the wrong side of that line.

**ELI5.** Wrong answers sound like good kitchen ideas, but they fix the wrong thing. Ask two questions. What does the cook not know yet? What is already decided? A wrong answer lets a chef re-decide something the recipe card already settled, or hands a fixed card to a problem that needs tasting.

## What to Remember

- The **enumeration test**: can the **sequence of steps** be **written down before the input arrives**? If it can, **code holds the plan** and the model works inside each step. If it cannot, the **model holds the plan** and **code holds the limits**: turn caps, spend caps, validation.
- **Workflows run models and tools** along **paths fixed in code**. An **agent directs its own process** and decides how the task gets done. Same model, same tools, different owner of the next decision.
- **Five workflow shapes**, each **selected by what the run does not know**: **chaining** for a fixed ordered split, **routing** for known categories needing separate handling, **parallelisation** for independent parts or for repeated attempts, **orchestrator-workers** when the subtasks themselves depend on the input, **evaluator-optimizer** when criteria are written down and another round measurably helps.
- **Adaptivity is warranted** only where a **later step exists** because of what an **earlier one found**, which is why an unfamiliar system is the canonical case. **Variable input alone is a routing problem**, not a reason for autonomy.
- An **agent loop does not stop on its own**. Exit conditions belong in the design, enforced by a **maximum turn count and a spend ceiling** returning distinct error states, never by the model choosing to finish.
- A **coordinator owns budget, validation and the handoff contract**: a **spend limit per worker**, **each result checked** against a **defined shape before it moves** on, and an **agreed definition of a finished subtask**. **Tracing and retries** intercept **nothing on the way downstream**, and **peer negotiation deletes the component whose job** it was.
- **Delegated subtasks need an objective**, an **output format**, **named tools and sources**, and a **boundary**. Short instructions produce workers that misread the assignment or repeat each other's work.
- A **multi-agent system costs roughly fifteen times a chat** and an **agent roughly four**, because every **worker spends its own tokens** on its **own context**. The multiplier is bought back **only by genuine parallel exploration**: separate sources, material larger than one window, many tools. **Tightly coupled work pays the fan-out** and collects **no parallel benefit**.
- **Fan-out multiplies failure sites**, so **retry, backoff and fallback** apply to each **worker separately**. One stalled worker can hold the synthesis step open indefinitely.
- A **subagent starts with no parent conversation**: the **launching prompt is the only channel** in, and **only its final message returns**. **Skills do not carry** over to a delegated task, while **permission scope** does.
- **No later stage** can **recover a fact nobody recorded**, so **whichever stage sees a detail writes it down**: **path, symbol, line range, evidence snippet**. **Sequencing rests** on a **status the producing stage sets**, never on words found in its prose.
- **Memory scope is decided at design time**: **in-conversation** state dies at the session boundary, **external storage** survives across sessions and users at the price of retrieval latency, **summarisation** keeps only what the summariser chose, **stateless** keeps nothing by design. **Resumability needs state outliving the process**. A longer timeout only makes interruption rarer.
- **Frameworks wrap the same loop** and **charge in visibility**, obscuring the prompts and responses underneath. Start against the model API directly, understand what a framework does below its abstraction, and **reduce layers moving into production**.
- The **pattern choice belongs to a path**, **not to a system.** Run the **enumeration test on each route separately**: a **settled route takes code**, and a **model-driven step belongs** only where the **route forks unpredictably**. One decision made for the whole product **produces both named errors at once**, paying for planning on the settled majority and having no branch for the exception.

**ELI5.** Use a recipe card when you know the steps. Use a tasting chef only when the next step depends on what the last one found. If the chef hires helpers, check every plate, give each helper a clear ticket, and watch the food bill. Write down what must survive the shift, and decide each route on its own.

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
