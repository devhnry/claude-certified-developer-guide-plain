# Chapter 9: The Description Is the Input, Not the Documentation

**Summary**: *A tool name carries three words and no edges. When a request could plausibly be served by either of two tools, the model settles it on the text you wrote, and text written as documentation for a colleague never states the one thing selection actually turns on: which requests belong to the tool next to it. This chapter covers the exchange, the description, the schema, checking arguments before you dispatch them, errors a model can act on, and why a tool set that grew by accretion charges you twice on every request.*

## One Request, Two Tools, and Nothing in the Sentence to Separate Them

**First, the idea.** Claude picks a tool by reading the text you wrote about each tool. Think of Claude as a receptionist (the **model**). On the wall is a staff directory (the **tool definitions**: names, descriptions and schemas). The receptionist never does the work. They fill in a request slip (a **`tool_use` block**) and your staff (**your code**) do the job. The directory is the only thing the receptionist reads when choosing who gets the slip.

**The example.** A customer says: "Pull up everything on Hartley."

Two **tools are registered**:
- `search_customers` (the Customers desk) takes a name or an account number and returns **profile records**.
- `search_orders` (the Orders desk) takes a customer or order identifier and returns **line items and delivery state**.

Nothing in the request **decides between them**. People working a support queue would ask the customer. The model **does not get to ask**. It sends a slip. A **wrong one** runs a query nobody wanted and returns something that looks like an answer.

**What was the choice made on?** Not the request, because the request is **ambiguous by construction**. It was made on the **tool definition** (the directory). On every request the **API assembles it into the system prompt** out of your **names**, your **descriptions** and your **schemas**.<sup>[1]</sup> That text is **not reference material** checked afterwards. It is the entire basis of the choice, read once, as the choice is made.

**The rule of the chapter.** Every description needs a **boundary clause**. That is a sentence **naming the requests** this tool does *not* serve, and saying which **tool serves them instead**. In directory terms: "Customers desk. For order history, go to the Orders desk." Without one, you said what the tool does and **left the model guessing** about the only thing in dispute.

**ELI5.** A receptionist picks a desk by reading the directory on the wall. If the directory does not say which desk to skip, the receptionist guesses. So each entry must say what it is for and what it is not for.

## The Exchange Has Five Stages, and You Own Four of Them

**First, the idea.** Claude **never executes anything**. It sends a **structured request** (the slip), your code **runs the operation**, and the outcome comes back as a new block.<sup>[1]</sup> Treat a `tool_use` block as a **proposal from a non-deterministic caller** (a caller that may give different answers each time). Every failure in this chapter is a stage where that proposal was treated as something stronger.

**The five stages:**

| Stage | Who acts | What you owe | The failure it produces |
|---|---|---|---|
| Definitions travel with the request (the directory goes up with every request) | You | Names, descriptions and schemas, every call | The wrong tool, or context spent on tools nobody used |
| `stop_reason: "tool_use"` returns with `tool_use` blocks carrying an `id`, a `name` and an `input` object<sup>[3]</sup> (the slip comes back) | Claude | Nothing yet | |
| The proposal is inspected (the front desk checks the slip) | You | Schema checking, and an approval gate where the action cannot be undone | A malformed call dispatched to a remote service |
| The operation runs (staff do the job) | You | Bounded retry on failures that pass on their own | One timeout ends the whole run |
| The outcome goes back (the result is handed to the receptionist) | You | One `tool_result` per call, echoing its `tool_use_id`, in the immediately following user turn, results first<sup>[3]</sup><sup>[4]</sup> | A validation error, or a result attached to the wrong call |

**Server-executed tools.** These **collapse the middle three** stages. Anthropic runs them internally and returns `server_tool_use` blocks already resolved, so **no `tool_result` is owed**. If a loop hits its **iteration cap**, it returns **`pause_turn`**, and you resend the conversation to continue it.<sup>[1]</sup>

**What you trade.** You give up control. **Validation, approval and the audit record** (the log of what happened) can only live on a machine you own. Chapter 12 owns the loop around all of this.

**ELI5.** The receptionist only writes slips. Your staff do the real work. You get four of the five steps, so you are the one who must check the slip before anyone acts on it.

## What a Description Omits Becomes a Question the Model Answers by Guessing

**First, the idea.** A description is a directory entry. Whatever it leaves out, the receptionist fills in by guessing.

**The test.** Anthropic's guidance is to **describe a tool** the way you would describe it to **somebody joining the team**.<sup>[10]</sup> The useful form of that test is **negative**. Read your description, then list what a **new colleague** would still have to ask. Every one of those questions gets answered anyway, at **selection time**, from **surface resemblance** (how the request sounds next to the name).

| Left out | What Claude is left holding | What it does instead |
|---|---|---|
| What comes back | Whether this even answers the request | Calls it, reads the result, calls the other one too |
| Which identifiers are accepted | Whether it holds the right kind of key | Passes the identifier it has, which is the wrong kind |
| Where the tool stops | Whether the neighbouring tool fits better | Matches on how the request sounds against the name |

**How long should it be?** **Three or four sentences** covers it. Say the **operation**, the **conditions calling** for it, what it **returns**, and the **boundary clause**. Longer is not safer. A trigger condition sitting in the **ninth sentence** competes with eight sentences of behaviour nobody consults while choosing.

**Two structural aids.** They beat any number of adjectives.
- **Namespacing** puts related tools under a **shared prefix**, by **service** or by **resource**. A catalogue then reads as a set of territories, not a flat list. Anthropic reports that even the choice between **prefix and suffix** moved **tool-use evaluation scores**.<sup>[10]</sup>
- A **boundary clause** that refers to earlier turns **fails silently** once **history is trimmed**, because the turns it appeals to are no longer there.

**The anti-pattern: the name is enough.** It always arrives as a **saving**. The name says it, the description repeats it, and the **description is billed every request**. But the description holds **applicability** (when to use the tool), and a **name cannot carry** that at all. Moving that text into a **separate file**, or into the **system prompt**, neither shortens the request nor improves the choice. Deleting it **deletes the information**. Moving it keeps the information and bills you the same.

**When a step must happen.** Sometimes a step has to happen, and no description makes it certain. That is configuration, not writing. `tool_choice` accepts **`auto`, `any`, `tool` and `none`**. **`any` obliges** some call. **`tool` names** the one.<sup>[2]</sup> To enforce a required first step, **name that tool** on the first request. Instructing more firmly **stays advisory**, and advisory controls are what produce intermittent failures. Under `any` or `tool`, the API **prefills the assistant message**, so **no natural-language preamble** appears ahead of the call.<sup>[2]</sup>

**ELI5.** If a directory entry leaves something out, the receptionist guesses. So write the entry for a new hire: what it does, when to use it, what it gives back, and what it does not cover. If one step is a must, don't ask politely. Tell the system which tool to use.

## The Required Array Is Wrong in Both Directions

**First, the idea.** The **description decides which tool**. The **schema** (the form the slip must follow) decides what arrives inside it. In the opening scenario, wrong tool and missing parameter are both problems, but they are repaired in **different files**.

**Required too much.** Marking **every field required** does not make calls more complete. It makes the model put a value in a slot it has **no source** for. And it will, because the contract said it must.

**Required too little.** Marking too little gives the opposite problem. Calls arrive **short**, and a **function invents a default**.

**What "required" means.** **Required** means the operation is **meaningless without the field**. Nothing weaker.

**Constrain the rest where you can.**
- A **small enumeration** (a short list of allowed values) removes a decision instead of describing it.
- A **parameter description naming the format** settles a shape that prose in the system prompt never reaches.
- Where inputs are **nested or format-sensitive**, **`input_examples`** attaches **valid inputs** to the definition. Each one is checked against your own schema. An **invalid example fails** the request with a **400**.<sup>[2]</sup>

**A stronger setting.** Where a malformed argument would break something, use **`strict: true`**. It constrains sampling to schema-valid output. So a field typed as an **integer arrives as an integer**, not as the string spelling of one.<sup>[5]</sup> It covers a supported subset of **JSON Schema**. A `pattern` that uses a **backreference**, a **lookaround** or a **word boundary will not compile**.<sup>[4]</sup>

**ELI5.** The slip has boxes to fill in. If every box is a must-fill, the receptionist makes things up for boxes they have no answer for. If too few are a must, slips come back half empty. Mark a box required only when the job cannot work without it.

## Check the Proposal at Dispatch, Because That Is the Last Place You Still Own It

**First, the idea.** Your **dispatcher** (the front desk that hands slips to staff) sits between a caller that can be wrong and a system that **cannot take back a write**. It is the last place you still control the slip.

**What to do.** **Validate the arguments** against the schema there. Treat a failure as a **recognised path**, not an exception that ends the run.

**Three alternatives that give the same thing away:**
- **Loosening the schema** until nothing fails. This turns a local error into a remote one, and makes an external service the first thing that ever checks your inputs.
- **Logging the anomaly** and **dispatching anyway**. This is worse, because the application spotted the fault and sent it on regardless.
- **Retrying the identical request unchanged**. This repeats a non-deterministic step with **no bound on attempts**.

**Approval also belongs here.** Dispatch is the **last moment humans can see** a proposed action before it happens. The Agent SDK models the gate as a **callback holding execution** until a decision returns. There are three responses, not two:
- **allow**
- allow with the **input modified**
- **deny**, with a message Claude reads and may act on<sup>[9]</sup>

The last one matters. A **denial delivered as a reason** is a fact the model can **route around**. A denial delivered as **silence** is a gap it has to reason across. Put a gate on an **irreversible action**, a plan about to **start executing**, and a result outside **expected bounds**.

**One mechanical trap.** **Never match** on the **serialised argument string** (the raw text of the arguments), because Unicode and slash escaping differ between model versions. **Parse the JSON** and compare the parsed values.<sup>[4]</sup>

**ELI5.** Before staff act on a slip, the front desk checks it. If the slip is wrong, say so and stop. If the job can't be undone, ask a human first. And when you say no, say why, so the receptionist can try something else.

## An Error the Model Can Act On Beats Any Kind of Silence

**First, the idea.** A tool that fails has **produced information**. What reaches the model depends on what your **code says** about it. Three of the four common choices **say something false**.

| What you return | What Claude now believes | What follows |
|---|---|---|
| A plausible placeholder record | A fact | It propagates into everything downstream, unmarked |
| An empty success | The lookup ran and matched nothing | Somebody is told there are no records |
| Nothing, the tool quietly withdrawn | It still holds a capability it does not have | It reasons around a gap it cannot name or report |
| `is_error` set, with a short statement of what failed<sup>[3]</sup> | A failure, described | It retries, routes around it, or reports the limitation |

**Only the last row is true.** Truth is what makes **recovery possible**, because recovery can be no more specific than the error prompting it. Anthropic's guidance on error text is to make it **actionable rather than opaque**. Name what would have been valid instead of returning a **code or a traceback**.<sup>[10]</sup>

**Where retry fits.** Retry sits underneath that, not instead of it. A **timeout clearing** on its own is **handled inside the tool**, with **backoff** (waiting longer between tries) and a **bounded attempt count**. It never reaches the conversation.

**The expensive anti-pattern.** A **failure converted into a success**. A visible error stops a run. An invented value keeps it going in the **wrong direction**.

**ELI5.** When a desk can't do the job, tell the receptionist plainly, "That failed, and here is why." Don't hand back a fake answer or a blank page. A fake answer sends everyone the wrong way, and a plain "failed" lets the receptionist try something else.

## An Overlapping Tool Set Charges You Twice on Every Request

**First, the idea.** A bigger directory costs you in two ways. Choosing gets harder, and the directory is billed on every request.

**Cost one: worse choices.** **Selection quality falls** as a catalogue grows. It falls fastest where **descriptions overlap**, because two tools claiming the same ground give the model no basis to separate them. There is measured guidance. **Fifty tool definitions** can occupy **ten to twenty thousand tokens** (small chunks of text). Selection accuracy degrades once more than **thirty to fifty** are loaded at once.<sup>[8]</sup>

**Cost two: the bill.** This one is quieter. **Definitions ride on every request** alongside the tool-use system prompt the API adds, whether or not any are called.<sup>[6]</sup>

**What to do.** A tool set is a **design object** with a running bill. It **shrinks three ways**.

**1. Consolidate** what is genuinely one thing. Several operations against the **same resource** can become a **single tool with an action parameter**. This is documented guidance. It reduces the number of choices without hiding any.<sup>[2]</sup>

The version that fails is the **catch-all dispatcher**. That is one tool covering **unrelated contracts**, with the choice pushed into a **free-text argument** where **no per-operation schema** constrains it. The decision did not go away. It moved somewhere with **less structure** around it.

**2. Expose what the task needs.** Nothing says a workflow must carry every catalogue the application can reach. **Narrowing the connected set** shrinks the **transmitted context** and the field of candidates at once. The anti-pattern in the other direction is a **tool for every variation**. That enlarges the exact surface that caused the trouble.

**3. Load on demand** past a certain size. Tool search **keeps definitions out of context** until Claude looks them up. It suits catalogues above roughly **twenty tools** where most sit idle. The price is one **extra round trip** the first time.<sup>[7]</sup><sup>[8]</sup> Below about **ten tools**, sending everything up front is faster.<sup>[8]</sup> Chapter 10 covers the servers that supply large catalogues.

**ELI5.** A giant directory is hard to read, and you pay to print it on every request. So merge entries that are really one desk, show only the entries the job needs, and for a very big directory let the receptionist look entries up only when needed.

## How Wrong Answers Are Built on This Material

**First, the idea.** Every wrong answer here describes something a **working developer** really does. Sharper prompts, lower temperature, fewer tools, a **router**. All real, all used somewhere sensible. **Four assumptions turn them wrong**.

**The four wrong assumptions:**
- **Advice offered where enforcement was required.** An **instruction telling the model** to include the field, or to weigh the choice more carefully. **Instructions are consulted**. **Schemas, `strict` and `tool_choice` bind** (they are enforced). The advice becomes correct only where a scenario asks how to **influence behaviour rather than guarantee** it.
- **A false success substituted for a real failure.** **Placeholder data**, an **empty result**, or a **tool removed without a word**. Each turns a **stoppable error** into a **wrong answer that travels**. Ask what a downstream reader would conclude from the option's return value.
- **The choice relocated rather than removed.** **Merging two distinct tools** into a **generic one**, **routing on keywords**, or moving descriptions into the **system prompt**. All three leave the **decision in play** with less structure supporting it.
- **A dial turned that does not touch the mechanism.** **Lowering temperature** to repair a **missing parameter**, or **reordering the tools array** because **position looks like priority**. Both act on something real that has nothing to do with the fault.

**The habit.** Match on the **mechanism a scenario names**, never on the domain it is dressed in.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Two tools get confused, and their descriptions are short or autogenerated | Rewrite each to state applicability and its boundary against the other | Merging them, routing around them, or urging care |
| Required parameters go missing from calls | Tighten the schema: required array, enums, per-parameter format | A sampling setting, or an instruction in the prompt |
| Arguments arrive that the schema never declared | Validate at dispatch, as a known error path | Relaxing the schema, or dispatching after logging |
| A tool times out intermittently and the run dies | Bounded retry inside the tool, then a structured error | A fabricated record, an empty success, or withdrawing the tool |
| Definitions dominate context and most go unused per task | Narrow what is exposed per task, or load on demand | Treating the surface as fixed, or relocating definitions |
| A specific step must happen before anything else | Force that tool on the first request | A firmer instruction, or checking the narration afterwards |
| Selection got worse when tools were added | Overlapping descriptions, repaired by consolidating and disambiguating | A silent cap on tool count, or ordering read as ranking |

**A habit that works past the table.** Ask where the **information an option changes** is actually read:
- in the description, at **selection time**
- in the schema, at **generation time**
- in your code, at **dispatch time**
- in the result, on the **turn after**

Wrong answers here are overwhelmingly **repairs applied** at the wrong one of those four points.

**ELI5.** Most wrong answers fix the wrong thing. Asking the receptionist to try harder, making the form blank, or shuffling the directory won't fix a problem that lives somewhere else. First find where the problem is, then fix that spot.

## What to Remember

- A **tool call** is a **proposal from a non-deterministic caller**, not trusted input. **Claude emits `tool_use`, your code executes**, and the outcome returns as a **`tool_result` echoing the `tool_use_id`** in the **immediately following user turn**, one per call, results first.
- The **description is read at selection time**. So it states what the **tool does**, when to **reach** for it, what it **returns**, and carries a **boundary clause** naming the **requests it does not serve** and which tool does. **Three or four sentences**. A **trigger buried in paragraph two** is not read.
- **Selection lives in the description**. **Argument completeness** lives in the **schema**. Wrong tool and missing field are **two defects repaired in two places**, and one fix never covers both.
- **Required** means the operation is **meaningless without the field**. **Over-marking forces invented values**, **under-marking** produces **short calls**, and **enums, formats and `input_examples`** remove decisions the model would otherwise guess at. **`strict: true`** goes further. It constrains sampling so an **integer field arrives as an integer**, across a supported **JSON Schema** subset that **excludes complex regex patterns**.
- **Validate arguments at dispatch**, the last point you control them. **Loosening the schema** makes a remote service your **first validator**. **Dispatching after logging** forwards a **fault you already caught**.
- **Approval belongs at dispatch**: before **irreversible writes**, before a plan **starts executing**, and on **results outside expected bounds**. A **denial carrying a reason** is something Claude can route around. **Silence is not**.
- **Return `is_error`** with a **short statement of what failed**, because **recovery is never more specific** than the error it is given. A **placeholder record**, an **empty success** and a **silently withdrawn tool** each assert something untrue.
- **Retry transient failures inside the tool** with **backoff** and a **bounded attempt count**. **Retrying the same call unchanged** repeats a non-deterministic step with no new input.
- A **tool set costs twice**. **Overlapping descriptions** make selection ambiguous, and every **definition is billed** on every request. Fifty tools can occupy **ten to twenty thousand tokens**, and accuracy **degrades past thirty to fifty** loaded.
- **Consolidate one resource's operations** under an **action parameter**. Never merge **unrelated contracts** into a **catch-all**, which moves the choice into a **free-text argument** with **no per-operation schema**. The exposed surface is a **per-task decision**: **load on demand** above roughly **twenty tools**, send everything **below about ten**.
- **`tool_choice`** takes **`auto`, `any`, `tool` and `none`**. **`any` compels** a call, **`tool` names** which one, and under either the API **prefills the assistant turn**.

**ELI5.** Claude is a receptionist who reads a directory and writes slips. Your staff do the work. So write each directory entry clearly, say which desk it is not for, check every slip before acting, and tell the receptionist plainly when a desk fails.

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
