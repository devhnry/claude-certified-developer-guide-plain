# Chapter 9: The Description Is the Input, Not the Documentation

**Summary**: *Two tools can both seem right for one request. The model then decides from the words you wrote, and a name alone gives it almost nothing. Docs written for a colleague skip what matters most: which requests the neighbouring tool owns. We cover the exchange, the description, the schema, checking arguments before dispatch, useful errors, and why a tool set that grew by accretion charges you twice on every request.*

## One Request, Two Tools, and Nothing in the Sentence to Separate Them

Picture a receptionist in a building with two offices. A visitor says, "Pull up everything on Hartley." She can't ask a follow-up. She reads the two door signs and picks one.

The receptionist is the model. The door signs are the tool descriptions. Two tools exist. `search_customers` takes a name or an account number and returns **profile records**. `search_orders` takes a customer or order identifier and returns **line items and delivery state**.

The request itself doesn't name an office. A person would ask. The model can't, so it emits a call.

So what did the choice rest on? The tool definition. On every request, the API builds the system prompt out of your names, descriptions and schemas.<sup>[1]</sup> The model reads it once, at the moment of choosing.

So the rule. Every description needs a **boundary clause**: one sentence naming the requests this tool does *not* serve, and which tool does.

**ELI5.** Two doors, two signs. The visitor can't ask questions. So each sign must say "not me, try the other door."

## The Exchange Has Five Stages, and You Own Four of Them

Claude never runs anything. Think of a note from the receptionist: "send Hartley to room 2." Your code does the walking.<sup>[1]</sup> A `tool_use` block is a proposal from a caller that can be wrong.

| Stage | Who acts | What you owe | The failure it produces |
|---|---|---|---|
| Definitions go out with the request | You | Names, descriptions, schemas, every call | Wrong tool, or space wasted on unused ones |
| `stop_reason: "tool_use"` returns with `tool_use` blocks carrying an `id`, a `name` and an `input` object<sup>[3]</sup> | Claude | Nothing yet | |
| The proposal is inspected | You | A schema check, and a human gate when there is no undo | A bad call reaches a remote service |
| The operation runs | You | Capped retries when the failure is temporary | A single timeout kills the run |
| The outcome goes back | You | One `tool_result` per call, echoing its `tool_use_id`, in the next user turn, results first<sup>[3]</sup><sup>[4]</sup> | A validation error, or a result matched to the wrong call |

Server-executed tools run on Anthropic's side. They cover the middle three stages internally and return `server_tool_use` blocks already resolved, so no `tool_result` is owed. When their internal loop reaches its iteration cap, it returns `pause_turn`. You then resend the conversation to continue.<sup>[1]</sup> The trade is control: validation, approval and the audit record can only live on a machine you own. Chapter 12 covers the loop.

**ELI5.** The receptionist only writes notes. You do the walking and checking. If Anthropic runs the tool, you can't check it first.

## What a Description Omits Becomes a Question the Model Answers by Guessing

Anthropic's test: describe the tool as you would to someone new on the team.<sup>[10]</sup> Flip it. Reread your description and note every question that newcomer would still ask. The model has the same questions. It answers them at selection time by how the request sounds beside the name.

| Left out | What the model is stuck with | What it does |
|---|---|---|
| The return value | It can't tell if the tool answers the request | Calls it, then calls the other one as well |
| Accepted identifiers | It can't tell if it holds the right key | Hands over the ID it has, which is wrong |
| The tool's edge | It can't tell if the neighbour is better | Judges by sound-alike wording |

Three or four sentences cover it: the action, when to call it, what comes back, and the boundary clause. More text isn't safer. A trigger in the ninth sentence competes with eight sentences about behaviour that nobody weighs while choosing.

Two habits beat adjectives. The first is **namespacing**: give related tools a shared prefix, by service or by resource. Anthropic reports that even choosing prefix over suffix shifted tool-use evaluation scores.<sup>[10]</sup> The second: a clause pointing back to earlier turns breaks silently once history is trimmed.

The usual trap is trusting the name. It feels thrifty, since the description costs tokens every request. But a name can't carry applicability. Moving the text to a file or the system prompt neither shortens the request nor sharpens the choice. Deleting it loses the information. Moving it keeps the cost.

Some steps must happen, and no wording guarantees that. That is a setting, not a writing job. `tool_choice` accepts `auto`, `any`, `tool` and `none`. `any` makes the model call something. `tool` names which one.<sup>[2]</sup> To require a first step, name that tool on the first request. A firmer instruction is still advice. With `any` or `tool`, the API prefills the assistant message. No chat text comes before the call.<sup>[2]</sup>

**ELI5.** A sign that skips what's inside and where else to go makes the receptionist guess. If a step is a must, name the tool.

## The Required Array Is Wrong in Both Directions

The sign picks the office. The form filled in at that office is the schema.

Mark every field required and calls don't get fuller. The model must fill a slot it has no source for, so it makes a value up. Mark too few and calls arrive short, so your function invents a default. **Required** means the operation is pointless without that field. Nothing weaker.

Narrow the rest. A short list of allowed values (an enum) removes a decision rather than describing it. A parameter description naming the format settles what system-prompt prose can't. For nested or format-picky inputs, `input_examples` attaches valid samples to the definition. Each is checked against your own schema, and a bad one fails the request with a `400`.<sup>[2]</sup>

When a bad argument could break something, use the stronger switch. `strict: true` restricts sampling to schema-valid output. An integer field then arrives as an integer, not the string spelling of one.<sup>[5]</sup> It covers a subset of JSON Schema. A `pattern` using a backreference, a lookaround or a word boundary won't compile.<sup>[4]</sup>

**ELI5.** The sign picks the office. The form picks what goes in the blanks. Demand every blank and people fib. Demand too few and forms come back thin.

## Check the Proposal at Dispatch, Because That Is the Last Place You Still Own It

Your dispatcher sits between a caller who may be wrong and a system that can't take back a write. Check arguments against the schema there.

Three shortcuts waste that check. Loosen the schema until nothing fails, and a local error turns into a remote one: an outside service becomes the first thing to check your inputs. Log the oddity and send anyway, and it's worse, since your app saw the fault and passed it on. Retry the same request, and you repeat a step that can fail again, uncapped.

Approval belongs here too. It is the last moment a person can see the action. In the Agent SDK, the gate is a callback that holds execution until a decision returns. It has three answers: allow, allow with edited input, or deny with a message Claude reads and may act on.<sup>[9]</sup> A denial with a reason is a fact the model can route around. A silent denial is a gap it must reason across. Gate what can't be undone, a plan about to start running, and results outside expected bounds.

One mechanical trap. Never match on the serialised argument string, because Unicode and slash escaping differ between model versions. Parse the JSON and compare values.<sup>[4]</sup>

**ELI5.** Before a visitor enters the vault, a guard checks the form. If it's wrong, the guard says why. No waving through, no asking the same way again.

## An Error the Model Can Act On Beats Any Kind of Silence

A failing tool still produces information, and the model learns only what your code says. Three of the four usual replies to a locked office tell the receptionist something untrue.

| What you return | What Claude then believes | What follows |
|---|---|---|
| A convincing fake record | A real fact | Spreads through later steps, unlabelled |
| An empty success | The search ran, nothing matched | Someone hears "no records" |
| Nothing, the tool just vanishes | It still owns that ability | Works around a hole it can't name or report |
| `is_error` set, with a short note on what failed<sup>[3]</sup> | A failure, spelled out | Retries, goes around, or reports the limit |

Only the last is true. Truth makes recovery possible, because recovery can't be more specific than the error behind it. Anthropic wants error text a model can act on. Say what would have been valid. Skip the code or traceback.<sup>[10]</sup>

Retry goes underneath, not in place of it. A timeout that clears itself is handled inside the tool, with backoff and a bounded number of attempts. The costly mistake is turning a failure into a success. A visible error halts a run. A made-up value lets it go on the wrong way.

**ELI5.** Office locked? Say "locked, try later." Don't hand over a fake file, an empty folder, or say the office is gone.

## An Overlapping Tool Set Charges You Twice on Every Request

More doors make the receptionist pick worse, most of all where two signs claim the same ground. Fifty tool definitions can take ten to twenty thousand tokens. Accuracy slips once more than thirty to fifty are loaded together.<sup>[8]</sup> The second bill is quiet. Definitions go out on every request next to the tool-use system prompt the API adds, called or not.<sup>[6]</sup>

A tool set is a design with a running cost. It shrinks three ways.

**Consolidate** what is truly one thing. Many operations on one resource can become one tool with an action parameter. That is documented advice. It cuts choices and hides none.<sup>[2]</sup> The bad version is the catch-all dispatcher. One tool covers unrelated contracts, and the choice is pushed into a free-text argument that no per-operation schema limits.

**Expose what the task needs.** A workflow needn't carry every catalogue the app can reach. Narrowing the connected set cuts the context you send and the candidates. A tool for every variation is the reverse error.

**Load on demand** when the set is large. Tool search keeps definitions out of context until Claude looks them up. It fits catalogues over roughly twenty tools where most sit idle. The cost is one extra round trip the first time.<sup>[7]</sup><sup>[8]</sup> Under about ten tools, sending all of them up front is quicker.<sup>[8]</sup> Chapter 10 covers servers that supply big catalogues.

**ELI5.** A hundred doors confuse the receptionist, and you print every sign each time. Merge doors that are really one. Show only today's doors. Keep a huge directory in a drawer.

## How Wrong Answers Are Built on This Material

Wrong answers describe what developers really do: sharper prompts, lower temperature, fewer tools, a router. Four assumptions make them wrong.

- **Advice where a binding rule was needed.** An instruction to include the field, or to think harder about the choice. Instructions are weighed. Schemas, `strict` and `tool_choice` bind. Advice fits only when a scenario asks how to influence behaviour, not guarantee it.
- **A false success covering a real failure.** Placeholder data, an empty result, a tool dropped silently. Each swaps a stoppable error for a wrong answer that travels.
- **The choice moved, not removed.** Merging distinct tools into a generic one, keyword routing, descriptions moved to the system prompt.
- **A dial unconnected to the mechanism.** Lower temperature for a missing parameter, or a reordered tools array because position looks like rank.

Match on the mechanism the scenario names, not its setting.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Two tools get mixed up; descriptions are brief or auto-made | Rewrite each to say what it covers and where it ends next to the other | Merge, route around, or urge care |
| Calls arrive missing required parameters | Tighten the schema: required array, enums, a format per parameter | A sampling setting, or a prompt line |
| Arguments appear that the schema never listed | Check at dispatch, as a known error path | Loosen the schema, or send after logging |
| A tool times out off and on, killing the run | Capped retry inside the tool, then a structured error | An invented record, an empty success, or pulling the tool |
| Definitions swamp context; most unused per task | Narrow the exposed set per task, or load on demand | Treat the set as fixed, or move definitions elsewhere |
| A step must come first | Force that tool on the first request | A firmer instruction, or reviewing the narration afterwards |
| Picking got worse once tools were added | Overlap, fixed by merging and sharper descriptions | A quiet cap on tool count, or order read as rank |

One habit works past the table. Ask where the information an option changes is read: the description at selection time, the schema at generation time, your code at dispatch time, or the result on the next turn. Wrong answers mostly repair the wrong one of those four.

**ELI5.** Wrong answers fix the wrong thing. Yelling at the receptionist or shuffling the doors won't help. Find where the trouble happens and fix it there.

## What to Remember

- A tool call is a proposal from a caller that can be wrong, so never trust it. Claude emits `tool_use` and your code runs it. The result goes back as a `tool_result` echoing the `tool_use_id`, in the very next user turn, one per call, results first.
- The model reads the description when it picks a tool. Say what the tool does, when to reach for it and what it returns. Then add a boundary clause: which requests it does not serve, and which tool does. Three or four sentences. A trigger buried in paragraph two is not read.
- Selection lives in the description. Argument completeness lives in the schema. Wrong tool and missing field are two defects with two fixes, and neither fix covers the other.
- Required means the operation is meaningless without that field. Over-marking forces invented values and under-marking gives short calls. Enums, formats and `input_examples` take away choices the model would guess. An invalid example fails with a 400. `strict: true` goes further, so an integer field arrives as an integer, across a supported JSON Schema subset that excludes complex regex patterns.
- Validate arguments at dispatch, the last point you control them. If you loosen the schema, a remote service becomes your first validator. If you dispatch after logging, you forward a fault you already caught.
- Approval belongs at dispatch too: before irreversible writes, before a plan starts executing, and on results outside expected bounds. Claude can route around a denial that gives a reason. It cannot route around silence.
- Return `is_error` and say briefly what failed, because recovery is never more specific than the error it is given. A placeholder record, an empty success and a silently withdrawn tool each claim something untrue.
- Retry transient failures inside the tool, with backoff and a bounded number of attempts. Sending the same call again unchanged repeats a non-deterministic step with no new input.
- A tool set costs twice: overlapping descriptions make selection ambiguous, and every definition is billed on every request. Fifty tools can use ten to twenty thousand tokens, and accuracy falls once thirty to fifty are loaded.
- Fold one resource's operations under an action parameter. Never fold unrelated contracts into a catch-all, which hides the choice in a free-text argument with no per-operation schema. Exposure is a per-task call: load on demand above roughly twenty tools, send everything below about ten.
- `tool_choice` takes `auto`, `any`, `tool` and `none`. `any` forces a call, `tool` names which one, and under either the API prefills the assistant turn.

**ELI5.** Clear door signs. Only needed blanks on forms. A guard before the vault. Honest notes when a door is locked. A small building.

## Endnotes for this chapter

1. Tool use is a contract in which the model emits a structured request and the application or Anthropic's servers execute it; tools differ by where code runs, with client-executed tools requiring the application to drive a loop keyed on `stop_reason`, and server-executed tools running their own internal loop that returns `pause_turn` when it reaches its iteration limit, with `server_tool_use` blocks requiring no `tool_result`. Anthropic, *How tool use works* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)

2. A user-defined tool definition carries a `name`, a detailed plaintext `description` of what the tool does, when it should be used and how it behaves, and an `input_schema`; the API constructs a system prompt from the tool definitions and configuration; guidance covers namespacing tools with common prefixes and grouping related operations under a single tool with an `action` parameter to reduce selection ambiguity; `input_examples` supplies schema-validated example inputs, with invalid examples returning a `400` error; and `tool_choice` accepts `auto`, `any`, `tool` and `none`, where `any` and `tool` cause the API to prefill the assistant message so no natural-language response precedes the `tool_use` blocks. Anthropic, *Define tools* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)

3. A `tool_use` block carries an `id`, a `name` and an `input` object conforming to the tool's `input_schema`; the continuation is a user-role message of `tool_result` blocks, each carrying the `tool_use_id` of the call it answers, optional `content`, and an optional `is_error` flag set when the tool execution resulted in an error. Anthropic, *Handle tool calls* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)

4. Symptom-to-fix guidance: the wrong tool being called is attributed to description ambiguity and repaired by differentiating tools by when to use them rather than only by what they do; parameters outside a schema are repaired with `strict: true` or `input_examples`; a `pattern` in a strict tool's schema that uses a backreference, a lookaround, a word boundary or a large range cannot compile; every `tool_use` block requires a `tool_result` and those blocks must precede any text in the user message; and string comparison on serialised tool inputs fails across model versions because escaping differs, so inputs must be parsed rather than matched as raw strings. Anthropic, *Troubleshooting tool use* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use)

5. Setting `strict: true` on a tool definition constrains the model's token sampling to schema-valid outputs, guaranteeing that tool inputs match the JSON Schema; without it Claude may return incompatible types such as a string in place of an integer, or omit required fields. The supported JSON Schema subset is documented separately. Anthropic, *Strict tool use* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)

6. The additional tokens attributable to tool use come from the `tools` parameter itself, which carries tool names, descriptions and schemas, from `tool_use` content blocks, and from `tool_result` content blocks; the API also automatically includes a tool-use system prompt whose token count varies by model and by the `tool_choice` setting, and these counts add to the normal input and output tokens for the request. Anthropic, *Tool use with Claude* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

7. Tool definitions and accumulated `tool_result` blocks consume the context window; tool search keeps tool definitions out of context until Claude asks for them, which fits large toolsets of roughly twenty or more tools where most are not needed every turn, trading a small amount of latency for a large reduction in baseline context usage. Anthropic, *Manage tool context* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)

8. Tool definitions can consume large portions of the context window, with fifty tools using ten to twenty thousand tokens, and tool selection accuracy degrades with more than thirty to fifty tools loaded at once; tool search adds one extra round trip the first time Claude discovers a tool, and with fewer than about ten tools loading everything up front is typically faster. Anthropic, *Scale to many tools with tool search* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/tool-search](https://code.claude.com/docs/en/agent-sdk/tool-search)

9. A `canUseTool` callback fires when Claude wants to use a tool that nothing earlier in the permission flow has approved, and execution stays paused until the callback returns; responses include allowing the tool to run as requested, allowing it with modified input, and denying it with a message that Claude sees and may use to adjust its approach. Anthropic, *Handle approvals and user input* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/user-input](https://code.claude.com/docs/en/agent-sdk/user-input)

10. Guidance on describing a tool as you would describe it to a new colleague, on namespacing related tools under common prefixes by service or resource with measurable effects on tool-use evaluations, on returning specific and actionable error messages rather than opaque codes or tracebacks, and on consolidating functionality into fewer high-impact tools rather than wrapping every API endpoint. Anthropic, *Writing effective tools for AI agents* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/writing-tools-for-agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
