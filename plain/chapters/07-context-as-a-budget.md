# Chapter 7: The Window Is a Budget, and Everything Competes

**Summary**: *By the time an agent reaches its twentieth tool call, most of the window (the desk) is holding work that is already finished. It was useful once. It is still paid for on every request, and it still competes for attention with the rule you set three turns ago. This chapter covers four things. First, where the budget goes before your current question is even added. Second, why overspending shows up as odd behaviour instead of an error. Third, the two levers that free up room. Fourth, what compaction is allowed to throw away.*

## Everything Claude reads shares one small desk

**First, the idea.** Claude can only look at so much at once. That limit is called the **context window**. Think of it as a desk. Whatever is on the desk, Claude can see.

**What's on the desk?** Say your agent is **twenty tool calls** into a job. Before your next instruction, the desk already holds:
- the **system prompt** (the rule sheet)
- every message in the request, including **tool results, images and documents** (every file opened)
- your **tool definitions** (the manuals)
- space for the **output** for the turn (Claude's reply), including **extended thinking**<sup>[1]</sup>

**What about caching?** **Cached prefixes** (parts of the prompt Claude has seen before) are on the desk too. Caching is a discount on things you keep putting on the desk. It changes what those tokens (small chunks of text) cost you. It does not change whether they **take up room**.<sup>[1]</sup>

**The problem: finished work never leaves.** Most of what is on the desk has already done its job. Call it **spent context**. It is content fetched for a step that finished. It is **resent on every later request**. It uses the same budget as the question you actually want answered. Anthropic's account of context engineering says this is about **attention, not storage**. Context is finite. Every token you add uses up a **limited attention budget**. So the goal is not a bigger desk. The goal is a desk with only the smallest set of **high-signal tokens** (the ones that matter).<sup>[4]</sup>

**Why you won't notice while building.** **Test fixtures** (the sample files you test with) are small. **Production tool outputs** often run several times longer than the fixtures you built against. So a session that held together for **twenty turns** in testing can **fill up at turn eight** once real documents flow through it. The **window did not change**. Each turn just puts more papers on the desk.

**What to do:** measure the budget, don't assume it. The **token counting endpoint** takes the same body as a real request and **returns a count** without running inference (without running the model).<sup>[6]</sup>

**ELI5.** Claude has a small desk. Every paper it reads stays on the desk, even after it is finished with it. When the desk gets too full, Claude starts to lose track. So you keep only the papers that matter.

## Too many papers is one problem; the wrong paper getting lost is another

**First, the idea.** Overspending the desk shows up in two ways. Only one of them raises an error.

**Bloat (the desk is piling up).** Bloat is a size problem. **Requests grow**, so the **bill grows**, and **latency follows**. If the input alone finally **exceeds the window**, the API rejects the request with a **`400`**.<sup>[1]</sup> All of this shows up in a dashboard.

**Drift (Claude stops looking at the right paper).** Drift is a behaviour problem, and it **reports nothing**. Claude answers from **specifics settled ten turns ago**. It quietly **stops following a rule** set at the start. It **picks the wrong tool** for a step it would have got right earlier. A person reading the transcript sees plausible work.

| The symptom | What it means | The misreading it invites |
|---|---|---|
| Every turn costs more than the last on one unchanged task | Spent material (old papers) is being resent in full | Blaming the model tier for latency |
| Tool choices correct for four turns, wrong on the fifth | Accumulated results now outweigh the instructions | Rewriting the tool descriptions |
| Answers lean on stale detail nobody has mentioned in ten turns | Old specifics still carry full weight | Reading it as a retrieval or memory defect |

**The third row is where most debugging time goes.** Nothing about a **tool schema** (a tool's definition) changed between turn four and turn five. What changed is the **volume of finished work** sitting on the desk between the **instructions** and the **decision**.

**Why a bigger desk does not help.** **More room is not a treatment for drift.** A **window twice the size** keeps every distraction at full detail and **leaves space for more**. Chapter 1 drew a line between capacity and selection on one request. This is the same line, one level up. Suppose someone proposes putting a corpus of tens of thousands of documents into every prompt. The objection that holds up is not a document limit. Even if the window were big enough, you would still **pay input on the whole corpus** for every query. Attention would also be spread across all of it.

**ELI5.** Sometimes the desk gets so full that a bill arrives and the work gets slow. Other times nothing looks wrong, but Claude forgets the rule you gave it earlier. A bigger desk only gives the papers more space to pile up.

## Two ways to clear the desk: throw papers away, or swap the pile for a summary

**First, the idea.** There are two levers to free up room. **Context editing deletes** and **compaction rewrites**. Exam scenarios turn on the difference between them.

**Clearing tool results (throw old papers away).** This removes the oldest tool interactions once a prompt passes a trigger. The trigger is **100,000 input tokens** by default. It keeps the **three most recent** by default.<sup>[2]</sup> Each cleared result leaves **placeholder text** behind (a sticky note saying "something was here"). So Claude reads that something was removed, not that it never happened.<sup>[2]</sup> The parameters are where the judgement lives:
- **`exclude_tools`** names tools whose results are **never cleared**.
- **`clear_at_least`** refuses to clear at all unless the pass frees a **worthwhile minimum**.
- **`clear_tool_inputs`** clears the call parameters as well as the results.<sup>[2]</sup>

A companion strategy **clears thinking blocks**.<sup>[2]</sup> All of this runs **server side**. So your application keeps its own full history and never has to resync.<sup>[2]</sup>

**Compaction (swap the pile for a one-page summary).** The strategy **triggers on input tokens**. The default is **150,000**, and it can **never be below 50,000**. Claude writes a summary into a **`compaction` block** that you pass back. On later requests, **every content block before it is ignored**.<sup>[3]</sup> It costs a **separate sampling step** (an extra model call). That step is billed and counted against rate limits. The summary is written by the model already named in your request. There is no cheaper option.<sup>[3]</sup>

| | Clearing tool results | Compaction |
|---|---|---|
| What happens to the material | Removed, with a placeholder marking the gap | Rewritten as a summary; earlier blocks then ignored |
| What survives | Whatever your parameters protect | Whatever the summariser thought to write down |
| What it costs | Cache invalidation where the clearing happens | A billed extra sampling step |
| Reach for it when | Old tool output is the bulk of the growth | The thread is long and continuity still matters |

**A third source of pressure: the manuals.** **Tool definitions** (the manuals) answer to neither lever. They sit at the **front of every request** instead of piling up behind it. The documented answers are **deferring them until Claude asks**, or **collapsing a call chain** into **one sandboxed script**.<sup>[5]</sup> Chapter 9 covers those. Chapter 8 covers caching.

**ELI5.** You can clear a messy desk in two ways. You can throw away old papers and leave a sticky note saying one was there. Or you can replace the whole pile with a one-page summary. The first loses the papers. The second loses whatever the summary did not mention.

## A rule that lives only in the pile can be lost when the pile is summarised

**First, the idea.** **Compaction keeps the gist.** That is the whole point of it, and it is also the whole hazard.

**The problem.** Run a long task through several passes. A **rule stated once**, in turn three, gets summarised. Then it is **summarised again from that summary**. Each pass is free to decide it was not worth keeping. **Nothing raises an error** when it goes. The first sign is an agent calmly breaking a rule it followed an hour earlier.

**The anti-pattern: the remembered constraint.** It looks like the right instinct. A team notices the rule getting lost, so they **state it again in the conversation**. Sometimes they add an instruction to remember it. But that restatement **sits inside the region being rewritten** (the pile that is about to be summarised). The same process that dropped the rule can drop it again.

**What to do.** The decision rule is about **location, not emphasis**. A constraint that must **hold for the whole run** belongs **outside the compactable region**. Put it in the **system prompt** (the rule sheet), or in a record your application puts back in on each turn.

**Threshold tuning is not the fix.** It looks like one. Raise the trigger and compaction runs less often on more material. Lower it and compaction runs more often on less. Both change the **frequency of the loss**. Neither changes what a **summary may leave out**.

**Claude Code makes the boundary concrete.** **Path-scoped rules and nested memory files** load into message history when their trigger file is read. So **compaction summarises them away** with everything else. The documented fix for a rule that must persist is to move it to the **project-root memory file**.<sup>[8]</sup> Skill bodies are put back in after a compaction. But a large one is **truncated to a cap**, and the truncation **keeps the start of the file**. So the **instructions that matter** belong at the top.<sup>[8]</sup>

**One more control.** Custom summarisation instructions **replace the default prompt completely**. They do not add to it.<sup>[3]</sup> Suppose the summariser is only asked to summarise the conversation. It returns a readable account of what happened. It drops the **file paths, the decisions and the errors** already resolved.

**ELI5.** A one-page summary only keeps what the writer thought was important. If your rule is only written on one of the old papers, the summary may leave it out. So put the rule on the rule sheet that never gets swapped out.

## Use a second desk so the papers never land on this one

**First, the idea.** Clearing and compaction both work on material that has **already arrived**. The third technique, **isolation**, **keeps it from arriving**.

**Subagents (a helper with their own desk).** A **subagent** runs in its **own conversation**. Its **intermediate tool calls and results** stay there. Only its **final message returns** to the parent. So a subagent can **read dozens of files** without any of that content landing in the caller's window.<sup>[7]</sup> Send the large read somewhere else, and you get the answer without the journey.

**The catch: separate desks share nothing.** **Separate agents share no context.** The only thing that crosses from parent to subagent is the **prompt string** on the tool call that launched it. So **file paths, error text and decisions** already taken are there only if something put them there.<sup>[7]</sup> The anti-pattern is the **assumed handoff**. That means designing as though a later step can see what an earlier one found, because both happened inside one run. To be reliable at a boundary, **write the findings into the prompt**.

**Multi-step workflows (one job per desk).** **Multi-step workflows** give you the same isolation without separate agents. Each step gets only the **material its own job needs**. Take reviewing a long document. **Narrow passes over each section** catch local errors. A **contradiction between two sections** is only visible to a pass whose scope is that comparison. Running the whole document three times and voting repeats one attention problem three times. When humans or model passes agree on something everybody missed, that is **not detection**.

**What isolation costs.** Chapter 12 covers choosing between a workflow and an agent. Chapter 13 covers building the loop. What **isolation costs is visibility**. The **subagent's reasoning goes** when its context goes.

**ELI5.** Give a helper their own desk for the messy job. They bring you back only the answer. But they cannot see your desk, so you must tell them everything they need.

## Prompt engineering is what you say once; context engineering is what stays on the desk

**First, the idea.** Everything in this chapter has a name. It is not the name most people reach for.

**Two terms, two jobs.** People use the two terms as synonyms, but they describe **different jobs at different scales**.
- **Prompt engineering composes a single exchange.** That means the **wording of an instruction**, the examples beside it, and the shape the answer must take. Its unit is **one request**. Its question is **what to say**. Anthropic's own guidance is scoped that way. It also says that not every failing result is best solved by changing a prompt at all.<sup>[9]</sup>
- **Context engineering decides** what sits on the desk **across a run**. That means what gets fetched, what survives the next turn, what is compacted, and what is handed to a subagent so it never lands here. Its unit is the **whole session**. Its question is **what should be present**, which is a different question from what to say. Anthropic frames the window as a **finite resource** with diminishing returns. Every extra token draws on the same **attention budget**.<sup>[4]</sup>

**Why the terms blur.** On one call the two collapse into each other. They separate the moment a task runs long. A prompt can be **word-perfect** and the run still **degrades**. By turn forty, the instruction is **competing with thirty-nine turns** of material that finished its job long ago. No rewrite of the instruction reaches that.

**How to tell them apart.** **Length is the discriminator.** If the task is **short and single-turn**, the lever is the **wording**. If it is **long and multi-step**, the lever is **what you let pile up** on the desk.

**ELI5.** Prompt engineering is writing one good note. Context engineering is deciding what stays on the desk all day. One good note cannot help if the desk is buried in old papers.

## How wrong answers are built on this material

**First, the idea.** Wrong answers here are **competent engineering** aimed at the **wrong quantity**. **Four assumptions** produce nearly all of them.

**The four wrong assumptions:**
- **Capacity offered where competition is the problem.** Examples are a **larger window** (a bigger desk), a **bigger model**, or **extended context**. Each answers material that does not fit. None of them helps with material that fits and **drowns out what matters now**.
- **A frequency dial offered against a loss.** Examples are raising a **compaction threshold**, lowering it, or compacting on a schedule. All three change **how often summarisation runs**, not **what it may discard**.
- **Continuity destroyed to remove volume.** Examples are restarting every few calls, truncating to the latest turn, or dropping tool calling. **Growth stops** because the **task state went with it**.
- **Context assumed to travel.** This means treating a **later step**, a **separate agent** or a **post-compaction turn** as able to see what an earlier one established. Nothing carries over unless **something carries it**.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| An agent degrades after a fixed number of tool calls, window already large enough | Prune spent tool output or compact, protecting the current task state | A larger window, a different framework, merged tools |
| A rule is violated only after several compactions | Move it outside what compaction may rewrite: system prompt or a reinjected record | A higher threshold, or an instruction to remember it |
| History is resent in full and requests grow steadily | Summarise or trim older turns, keeping what is still in use | Capping the reply length, or discarding history outright |
| A step must reason without seeing the whole prior conversation | Scope each step to what it needs, by subagent or multi-step workflow | One global prompt handed to every step |
| A corpus far larger than any window is proposed for every prompt | Retrieve the relevant passages per query | A document-count limit, or splitting the corpus across parallel requests |
| A later step depends on something an earlier one established | Pass it explicitly in the prompt that starts the step | Assuming it is visible because it happened in the same run |
| Answers keep leaning on stale specifics from many turns ago | Compact, so the gist stays and the specifics lose weight | Truncating to the latest turn, or resetting every turn |
| A prompt is already precise and a long multi-step run still drifts | Change what the window holds, not what the instruction says | Rewriting or lengthening the instruction, which cannot reach material that accumulated around it |

**A habit that works past the table.** For any option you are offered, ask one question. Does it change how **much room exists**, how **often something is discarded**, or what may be **discarded**? Drift answers only to the third.

**ELI5.** Most wrong answers either buy a bigger desk, change how often you tidy, or throw out everything. None of those fix the real problem. The real problem is which papers are on the desk.

## What to remember

- The window is **one budget** that everything draws on: the **system prompt**, every message (including **tool results, images, documents, tool definitions**), and the turn's own **output and thinking**. **Cached prefixes still occupy** it. Caching changes **price, not space**.
- **Spent context** is material that **already did its job** and is **still resent every turn**. It still **costs tokens** and **competes for attention**. It is the bulk of a long agent run.
- **Bloat is size** and **drift is behaviour**. Bloat raises cost and eventually causes a **`400`**. Drift **reports nothing**. It shows up as **stale detail, dropped constraints and worse tool choices**. If **tool selection fails** after a fixed number of turns, that is a **window symptom**, not a **schema symptom**.
- A **bigger window does not treat drift**, because it **keeps every distraction** at full detail.
- Two levers, two mechanisms. **Clearing removes old tool results** and leaves a **placeholder**. It is tuned by **`keep`, `clear_at_least` and `exclude_tools`**. **Compaction rewrites history** into a summary and **ignores every block before** it. It costs an extra billed **sampling step**.
- Compaction is **lossy by design**. So anything that must **hold for the whole run** lives outside it: the **system prompt**, or a **record put back in each turn**. **Restating the rule** in the conversation puts it back inside the **region being summarised**. Threshold changes **alter frequency**, never what a **summary may drop**.
- **Isolation keeps material out** instead of shrinking it. A subagent's **tool calls and results** stay in its **own context**, and only its **final message returns**. **Separate agents share no context**, so the **launching prompt** is the **only channel**, and what it leaves out is missing. The price is **visibility**.
- **Prompt engineering and context engineering** are **different jobs at different scales.** Prompt engineering **composes one exchange**. Its unit is a **single request** and its question is **what to say**. Context engineering **decides what occupies the window** across a run. Its unit is the **whole session** and its question is **what should be present**. **Length separates them**. On one call they collapse together. On a long run only the second reaches the problem.

**ELI5.** Claude has one small desk. Everything it reads goes on the desk and stays there. You can throw old papers away, swap the pile for a summary, or give a helper a second desk. Anything that must never be lost goes on the rule sheet, not in the pile.

## Endnotes for this chapter

1. Everything in the request counts toward the context window: the system prompt, every message in `messages` including tool results, images and documents, and the tool definitions; the output Claude generates for the turn, including its extended thinking, counts too. Cached prompt prefixes still occupy the context window, because prompt caching changes what you pay for those tokens rather than whether they count. If the input alone already exceeds the model's context window, the API returns a `400` `invalid_request_error`. The context window functions as working memory, and accuracy and recall degrade as the token count grows, a phenomenon named context rot. Anthropic, *Context windows* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/context-windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)

2. The `clear_tool_uses_20250919` strategy clears tool results when conversation context grows beyond a configured threshold, clearing the oldest tool results in chronological order and replacing each cleared result with placeholder text indicating to Claude that it was removed; its `trigger` defaults to 100,000 input tokens, `keep` defaults to 3 tool uses, `clear_at_least` ensures a minimum number of tokens is cleared each time and withholds the strategy if that minimum cannot be met, `exclude_tools` lists tool names whose uses and results should never be cleared, and `clear_tool_inputs` controls whether tool call parameters are cleared alongside the results; the `clear_thinking_20251015` strategy manages thinking blocks on the same footing; context editing is applied server-side before the prompt reaches Claude, and the client application maintains the full unmodified conversation history with no need to sync; tool result clearing invalidates cached prompt prefixes when content is cleared. Anthropic, *Context editing* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/context-editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)

3. Compaction automatically summarizes older context when approaching the context window limit, enabled by adding the `compact_20260112` strategy to `context_management.edits`; its `trigger` defaults to `{"type": "input_tokens", "value": 150000}`, `input_tokens` is the only supported trigger type, and `value` must be at least 50,000 tokens; the API returns a `compaction` block containing the summary, the block must be passed back on subsequent requests, and when the API receives it all content blocks before it are ignored; compaction requires an additional sampling step which contributes to rate limits and billing; the model specified in the request is used for summarization, with no option to use a different or cheaper model; custom instructions supplied through the `instructions` parameter do not supplement the default prompt but replace it completely. Anthropic, *Compaction* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)

4. Context engineering is described as the set of strategies for curating and maintaining the optimal set of tokens during inference; context is treated as a finite resource with diminishing marginal returns, drawing on a limited attention budget that every additional token depletes, and the stated objective is finding the smallest possible set of high-signal tokens that maximise the desired outcome. Compaction, structured note-taking in external memory, and sub-agent architectures that return condensed summaries are given as the long-horizon techniques. Anthropic, *Effective context engineering for AI agents* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

5. Tool definitions and accumulated `tool_result` blocks consume the context window, and four approaches address this at different points: tool search keeps tool definitions out of the context window until Claude asks for them, trading one extra turn of latency for a large reduction in baseline context usage; programmatic tool calling collapses a sequence of tool calls into a single script run in a sandbox so the intermediate results never enter the conversation history; prompt caching reduces what you pay for tokens already in context rather than reducing their number; and context editing removes old `tool_result` blocks once they have served their purpose. The approaches compose. Anthropic, *Manage tool context* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)

6. The token counting endpoint accepts the same structured list of inputs used for creating a message, including system prompts, tools, images and PDFs, and returns the total number of input tokens without running inference; it is supported on all active models and is free to use, subject to requests-per-minute rate limits. Anthropic, *Token counting* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)

7. Because subagents are separate agent instances, each subagent runs in its own conversation which starts fresh unless it is a fork; intermediate tool calls and results stay inside the subagent and only its final message returns to the parent, so a research subagent can explore dozens of files without that content accumulating in the main conversation. A non-fork subagent's context window starts fresh with no parent conversation, and the only content passed from parent to subagent is the Agent tool's prompt string, so any file paths, error messages or decisions the subagent needs must be included directly in that prompt. Anthropic, *Subagents in the SDK* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)

8. When a long session compacts, Claude Code summarizes the conversation history to fit the context window, and what happens to instructions depends on how they were loaded: path-scoped rules and nested CLAUDE.md files load into message history when their trigger file is read, so compaction summarizes them away with everything else, and a rule that must persist across compaction should have its `paths:` frontmatter dropped or be moved to the project-root CLAUDE.md; skill bodies are re-injected after compaction, but large skills are truncated to fit a per-skill cap and the truncation keeps the start of the file, so the most important instructions belong near the top of `SKILL.md`. Delegating large reads to a subagent keeps the file contents in the subagent's context window rather than the caller's. Anthropic, *Explore the context window* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window)

9. Prompt engineering guidance is scoped to success criteria that are controllable through prompting, and states that not every success criterion or failing evaluation is best solved by prompt engineering. Anthropic, *Prompt engineering overview* (Claude Platform Docs, accessed 2026-09-13), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
