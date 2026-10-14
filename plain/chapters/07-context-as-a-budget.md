# Chapter 7: The Window Is a Budget, and Everything Competes

**Summary**: *Picture an agent on its twentieth tool call. Most of what it carries is finished work. That work was useful once, but it is resent on every request, and it competes for attention with the constraint you set three turns ago. This chapter covers what fills the budget before your question arrives, why overspending looks like odd behaviour instead of an error, the two levers that free room, and what compaction may throw away.*

## Everything in a Request Draws on One Budget, Including What Is Already Finished

Think of the context window as a desk. Everything the model reads has to sit on it. Finished papers still take up space.

Take an agent **twenty tool calls** into a task. Before the current instruction arrives, the desk already holds:

- The system prompt.
- Every message, with tool results, images and documents inside.
- Your tool definitions.
- The output for this turn, including extended thinking.<sup>[1]</sup>

Cached prefixes sit there too. Caching changes what those tokens cost, not whether they take up room.<sup>[1]</sup>

Most of this is **spent context**: material fetched for a step that is done. It gets resent on every later request, and it draws on the same budget as your live question.

Anthropic frames this as attention, not storage. Each token you add uses up a limited attention budget. So keep the smallest set of high-signal tokens. Do not just buy more desk.<sup>[4]</sup>

Development hides this because test fixtures are small. Real tool outputs often run several times longer. A session that lasted twenty turns in testing can fill at turn eight. The window did not shrink. Each turn spends more.

So measure it. The token counting endpoint takes the same body as a real request and returns a count. It runs no inference.<sup>[6]</sup>

**ELI5.** Your desk is only so big. Old papers you finished with stay there unless you move them. Soon there is no space for the paper you need right now.

## Bloat Is a Size Problem and Drift Is an Attention Problem

An overspent desk shows up in two ways. Only one raises an alarm.

**Bloat** is size. Requests grow, so the bill and latency grow. If input alone passes the window, the API rejects it with a `400`.<sup>[1]</sup> A dashboard shows all of this.

**Drift** is behaviour. It raises no flag. Claude answers from details settled ten turns ago. It stops following a rule from the start. It picks the wrong tool for a step it got right before.

| What you see | What is going on | Wrong diagnosis |
|---|---|---|
| Cost climbs each turn, task unchanged | Finished material is resent whole | Blame the model tier |
| Correct tool choice, then a wrong one on turn five | Piled-up results outweigh the instructions | Rework tool descriptions |
| Answers cling to detail from ten turns back | Old specifics keep full weight | Call it a memory bug |

Most debugging time goes to the third row. Between turn four and turn five, no schema moved. The pile of finished work between your instructions and the decision did.

A bigger window does not fix drift. A desk twice the size keeps every old paper at full detail and has space for more. Chapter 1 drew the line between capacity and selection for one request. This is that line, one level up.

Say someone wants a corpus of tens of thousands of documents in every prompt. The objection that holds is not a document limit. Grant the room and you still pay input on the whole corpus per query, with attention spread across all of it.

**ELI5.** A full desk can be slow and costly, and you notice. A cluttered desk is sneakier. You grab the wrong paper and nobody tells you why.

## Two Levers Reclaim Room: Delete What Is Spent, or Compress It

You can bin old papers, or swap a stack for one short note. **Context editing** deletes. **Compaction** rewrites. Exam scenarios turn on that difference.

**Clearing tool results** drops the oldest tool interactions when the prompt passes a trigger. The trigger is **100,000 input tokens** unless you change it. The **three most recent** stay, also by default.<sup>[2]</sup> Each cleared result leaves placeholder text, so Claude sees something was removed.<sup>[2]</sup>

Three parameters tune it.

- `exclude_tools` names tools whose results are never cleared.
- `clear_at_least` skips clearing unless it frees a worthwhile minimum.
- `clear_tool_inputs` clears the call parameters too.<sup>[2]</sup>

Another strategy clears thinking blocks.<sup>[2]</sup> It all runs server side. Your app keeps the full history and never resyncs.<sup>[2]</sup>

**Compaction** summarises. It triggers on input tokens: **150,000** by default, and never below **50,000**. Claude writes a summary into a `compaction` block, which you pass back. On later requests, every content block before it is ignored.<sup>[3]</sup>

It costs a separate sampling step, billed and counted against rate limits. The model in your request writes the summary. There is no cheaper option.<sup>[3]</sup>

| | Clearing tool results | Compaction |
|---|---|---|
| Effect | Deleted, with a placeholder | Summarised; earlier blocks ignored |
| Keeps | What your parameters protect | What the summary happens to mention |
| Price | Cache invalidation where it clears | A billed sampling step |
| Pick it when | Tool output is most of the growth | Thread is long, continuity matters |

Tool definitions are a third pressure. Neither lever helps, because they sit at the front of every request instead of piling up behind it. Two documented answers: defer them until Claude asks, or collapse a call chain into one sandboxed script.<sup>[5]</sup> Chapter 9 owns those. Chapter 8 owns caching.

**ELI5.** You can bin old papers and leave a sticky note. Or you can write one short summary and bin the stack. Binning is clean. Summarising keeps the story but can lose details.

## A Constraint That Lives Only in the History Is a Constraint Compaction May Delete

Compaction keeps the gist. That is its purpose and its hazard.

Say you state a rule once, at turn three. Over a long task it is summarised, then summarised again. Any pass may judge it not worth carrying. No error appears. The first sign is an agent calmly breaking a rule it followed an hour ago.

The tempting fix is the **remembered constraint**: say the rule again in the chat, maybe with "remember this". It feels right. But the reminder lands in the part of history that gets rewritten. Whatever dropped the rule can drop the reminder.

So location matters, not emphasis. A rule that must hold for the whole run goes outside the compactable region. Use the system prompt, or a record your app reinjects each turn. Picture a label taped to the desk, not a paper in the pile.

Tuning the threshold only seems to help. A higher trigger runs compaction less often on more material. A lower one runs it more often on less. Both change how often loss happens. The summary can still drop the same things.

In Claude Code you can see exactly where the line falls. Path-scoped rules and nested memory files load into message history when their trigger file is read. So compaction summarises them away. The documented repair is to move a must-keep rule to the project-root memory file.<sup>[8]</sup>

Skill bodies come back after compaction. A large one is cut to a cap, and the cut keeps the start of the file. So put key instructions at the top.<sup>[8]</sup>

Also, custom summarisation instructions replace the default prompt completely.<sup>[3]</sup> Ask only for a summary and you get a readable story. It drops the file paths, decisions and resolved errors.

**ELI5.** If you shrink a pile of notes into one page, the small things may vanish. So write the big rule on the desk itself, not in the pile. Writing it again inside the pile does not help.

## Isolation Moves Material Out of the Window Rather Than Shrinking It

Clearing and compaction handle material after it lands. Isolation keeps it from landing.

Send a helper to another room to read dozens of files. They return with one note, and your desk never sees the files. That is a **subagent**. It has its own conversation. Its tool calls and results stay there. Only its final message returns to the parent.<sup>[7]</sup>

Separate agents share no context. Only the prompt string on the launching tool call crosses over. So file paths, error text and earlier decisions arrive only if someone wrote them in.<sup>[7]</sup>

The **assumed handoff** is the trap. You expect a later step to see what an earlier one found, since both ran together. It cannot. Write the findings into the prompt.

Multi-step workflows isolate without separate agents. Each step gets only what its job needs. In a long document review, narrow passes over each section catch local errors. A contradiction between two sections shows only to a pass scoped to that comparison. Running the whole document three times and voting repeats one attention problem three times. Agreeing on a miss is no detection.

Chapter 12 covers workflow versus agent, and chapter 13 the loop. What you give up is visibility. When the subagent's context goes, so does its reasoning.

**ELI5.** Send a helper to read the big pile in another room. They bring back a short note and your desk stays tidy. But they only know what you told them before they left.

## Prompt Engineering Writes One Exchange; Context Engineering Curates the Whole Run

People use these two terms as synonyms. They are different jobs at different scales.

**Prompt engineering** shapes one exchange: the wording, the examples, the shape of the answer. Its unit is one request. Its question is what to say. Anthropic limits its own guidance to that scope. It adds that some failures are not best fixed by editing a prompt.<sup>[9]</sup>

**Context engineering** decides what sits in the window across a run. What gets fetched? What survives the next turn? What is compacted? Its unit is the whole session. Its question is what should be present. Anthropic calls the window finite, with diminishing returns.<sup>[4]</sup>

On one call, the two blur. A long task pulls them apart. A word-perfect prompt can still drift. By turn forty, the instruction competes with thirty-nine turns of finished material. No rewrite reaches that.

Length is the test. Short and single-turn: change the wording. Long and multi-step: change what you let pile up.

**ELI5.** Prompt engineering is writing one good note. Context engineering is keeping the whole desk in order all day. A perfect note still gets lost on a messy desk.

## How Wrong Answers Are Built on This Material

Wrong answers are sound engineering aimed at the wrong target. Four habits cause almost all of them.

- **More room when the problem is competition.** A larger window, bigger model or extended context helps when things do not fit. It does nothing when they fit and crowd out what matters now.
- **A timing dial against a loss.** Raising the threshold, lowering it, or compacting on a schedule only moves when summarising runs. What it may discard stays the same.
- **Wiping the thread to cut volume.** Restarting every few calls, keeping only the last turn, or dropping tool calling. Growth stops, but the task state is gone.
- **Assuming context travels.** A later step, another agent or a post-compaction turn will not see what came before unless you pass it along.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| Agent degrades after N tool calls, window is big enough | Prune old tool output or compact, keep current task state | Bigger window, new framework, merged tools |
| Rule broken only after several compactions | System prompt or reinjected record | Higher threshold, or "remember this" |
| Full history resent, requests keep growing | Summarise or trim old turns, keep what is live | Cap reply length, or drop history |
| A step must reason without the full conversation | Scope each step: subagent or multi-step workflow | One global prompt for all steps |
| Corpus far bigger than any window, in every prompt | Retrieve relevant passages per query | Document-count limit, parallel splits |
| Later step needs an earlier finding | Pass it in the starting prompt | Assume it is visible |
| Answers use stale specifics from many turns back | Compact: gist stays, specifics fade | Truncate to last turn, or reset each turn |
| Precise prompt, long run still drifts | Change what the window holds | Rewrite or lengthen the instruction |

A habit that works beyond the table: for any option, ask what it changes. Is it how much room exists, how often something gets dropped, or what may get dropped? Only the last one cures drift.

**ELI5.** Wrong answers buy a bigger desk, tidy more often, or throw everything out. The right answer decides which papers stay on the desk.

## What to Remember

- One budget holds the system prompt, every message (tool results, images, documents), tool definitions, and the turn's output and thinking. Cached prefixes still take space. Caching changes price only.
- Spent context is finished material resent each turn. It makes up most of a long agent run.
- Bloat raises cost and eventually a `400`. Drift raises nothing: stale detail, dropped constraints, worse tool choice. Wrong tools after a set number of turns point at the window, not the schema.
- A bigger window does not treat drift. It keeps every distraction at full detail.
- Clearing removes old tool results and leaves a placeholder, tuned by `keep`, `clear_at_least` and `exclude_tools`. Compaction rewrites history into a summary and ignores every block before it, at the cost of an extra billed sampling step.
- Compaction is lossy by design. Rules that must hold for the whole run live in the system prompt or a record reinjected each turn. Restating the rule in the chat puts it back in the summarised region. Thresholds change frequency, never what a summary may drop.
- Isolation keeps material out. A subagent's calls and results stay in its own context and only its final message returns. Agents share nothing but the launching prompt. The price is visibility.
- Prompt engineering composes one exchange (what to say). Context engineering decides what fills the window across a run (what should be present). Length separates them, and on a long run only the second helps.

**ELI5.** Keep the desk small and tidy. Bin or summarise old papers, tape the big rules to the desk, and tell any helper everything they need before they leave.

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
