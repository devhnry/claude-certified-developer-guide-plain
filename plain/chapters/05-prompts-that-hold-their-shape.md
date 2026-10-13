# Chapter 5: Instruction Placement Is a Trust Decision

**Summary**: *One sentence, written once, put in two different places, produces two systems that fail differently. That is the whole chapter. Where text sits decides three things. How long it applies. How many copies exist. And whether a stranger who supplied a document can edit your rules by writing a line into it. Placement comes first. Clarity, examples, output constraints and the loop that improves them all sit on top of a sort you either did or skipped.*

## The Same Sentence in Two Places Is Two Different Systems

**First, the idea.** Where you put an instruction matters as much as what it says. Think of a restaurant kitchen. The **house rules** are pinned on the kitchen wall (the top-level **`system`** field). Each **order ticket** is a single customer's request (the **user turn**). **Deliveries** from outside suppliers arrive in boxes (**`tool_result`** blocks). A rule pinned on the wall is trusted. A note found inside a delivery box is not.

**The example.** Take two prompts. Both carry the sentence *return one label from the fixed set and nothing else*, **spelled identically**.
- In the first, it sits in the **top-level `system` field** (pinned on the wall). It is **written once**. It applies to every request the service will ever make, including the ones **nobody has written yet**.
- In the second, it was **appended to the user turn** (scribbled on the ticket), under the ticket text, because that is where somebody was working when they thought of it. It now travels inside a string the turn-building code assembles. There are as many **copies as code paths**, and **copies drift** (they slowly stop matching each other).

**What's different?** Same words. Same model. Same ticket. The second system has **no single place** where its rules live. It also puts them in the channel that carries **text somebody else wrote**.

**The placement sort.** Sort every piece of text in a prompt by **two questions**. Call the result the **placement sort**.
- How **long** does this text apply?
- Who could have **written** it?

**Lifetime decides** whether **text repeats**. **Authorship decides** whether it may **instruct**.

**ELI5.** A rule on the kitchen wall is seen by every cook, every day. A rule scribbled on one ticket is only seen once, and it might get copied wrong. A note inside a delivery box could have been written by anyone, so the cook should not take orders from it.

## Three Destinations, and Nothing You Did Not Write Reaches the First

**First, the idea.** The sort has **three outcomes rather than two**. The third is the one developers skip.

| The text | How long it applies | Who could have written it | Where it belongs |
|---|---|---|---|
| Role, tone, standing constraints (the house rules) | Every request, unchanged | You | Top-level `system` |
| The output contract, and the rule that supplied content never instructs | Every request, unchanged | You | Top-level `system` |
| Worked examples of the output (photos of finished dishes) | Every request, unchanged | You | `system`, tagged as examples |
| This request's actual question (the order ticket) | One request | The user in front of you | The user turn |
| A document the user attached | One request | Whoever handed it to them | The user turn, delimited (fenced off) |
| A fetched page, inbound mail, OCR text (text read from a scanned image), a tool's return (the delivery boxes) | One request | Anybody at all | `tool_result` blocks |

**How to read it.** Read the right-hand column downward.
- **Standing rules gather** in one field, **stated once**.
- **Per-request material stays** in the turn.
- **Third-party content** goes into **tool results**.

**Why tool results?** That is where Anthropic documents that it belongs. Deliver it inside `tool_result` blocks rather than in `system` or in plain user text. The reason is that Claude is **trained to treat directives** arriving inside tool results with **more scepticism** than directives elsewhere.<sup>[1]</sup>

**One refinement from Chapter 3.** A message with **`"role": "system"`** may appear after a user turn on **supported models**. It carries the **same authority** as the top-level field, but it **never comes first**. So a rule that only becomes relevant later lands at the end of the history. It does this **without disturbing a cached prefix** (the saved start of the prompt).<sup>[2]</sup>

**The problem: the document promoted to policy.** This is what the sort prevents. It never looks like a security decision at the time. Somebody pastes a contract into the system prompt so the model definitely sees it. That contract now **carries the authority your rules carry**. So any line in it addressed to a reader is **addressed to Claude**. Nobody attacked anything. **Placement did the damage alone**. In kitchen terms, the supplier's note got pinned to the wall.

**The mirror image: the standing rule filed in the last turn.** Someone appends the rule to the newest user message, on a theory about recency (newest text counts most). Recency is not how a **standing constraint holds**. And the constraint now shares a channel with whatever got pasted in.

**ELI5.** The kitchen has three places for paper. House rules go on the wall. Today's order goes on the ticket. Anything from a stranger stays in its box. If you pin a stranger's note on the wall, the cooks will start following it.

## An Instruction Is Checkable or It Is Decoration

**First, the idea.** An instruction only helps if you can tell whether the output followed it.

**Anthropic's test.** Adopt it whole. **Show the prompt to a colleague** with minimal context on the task and ask them to follow it. If that **human would be confused**, so is the model.<sup>[3]</sup>

**What "checkable" means.** A human following *be precise* has no idea when they have complied. Neither has a grader. An instruction is **checkable** when output can be tested against it. For example:
- a **named set of permitted values**
- a **stated ceiling on length**
- a rule saying which of **two conflicting sources wins**

The rest is a mood. "Make it taste good" is not a checkable rule for a cook. "Salt under 2 grams" is.

**Two documented refinements.**
- **Say what to do** rather than what to avoid. A prohibition removes an outcome without supplying a replacement.
- **Give the reason** behind an instruction. The **model generalises from an explanation** to cases the instruction never named.<sup>[3]</sup>

**The wrong lever, twice over.** When an instruction fails, developers reach for the **firmer restatement**. They take a rule the model did not follow and **say it again in capitals**, naming no failing part of the output. On current models this misfires. Prompts written to stop **older models under-reaching** now cause over-reaching. Anthropic's documented fix is to **dial the aggressive language back** toward ordinary phrasing.<sup>[4]</sup> **Volume was never a technique**. Now it has a cost.

**ELI5.** A rule is only useful if someone can check it. "Be careful" cannot be checked. "Pick one word from this list" can. Shouting a rule louder does not make it clearer. It can make the model do too much.

## Delimiters Make Supplied Text Legible as Data

**First, the idea.** A **delimiter** is a marker that fences one kind of text off from another. Here the markers are tags like `<example>`. In the kitchen, they are the labelled trays that keep tickets, recipes and deliveries apart.

**Tags.** Tags earn their place when a prompt mixes kinds of content. Wrap **instructions**, **context**, **examples** and **variable input** (the part that changes each request) each in its own tag. That reduces the chance that **Claude reads one as another**. Put examples inside **`<example>` tags** so they are not read as part of the task.<sup>[5]</sup>

**Three rules for long material.** They come from the same page.
- **Long documents go near the top**, above the query, the instructions and the examples. This improves results across models.
- **Several documents get wrapped individually**, with content and source in their own subtags.
- On long-document work, ask Claude to **quote the relevant passages first**.<sup>[5]</sup>

**The limit: the model reads the fence, nothing enforces it.** **Delimiting is a boundary** the **model reads**, not one the **runtime enforces** (the code that runs the request). Text inside a tag can imitate that tag.
- The harder version is to **JSON-encode third-party strings** rather than concatenating them into free-form text. Escaping leaves no way to close a quote and step out into instruction position.<sup>[1]</sup>
- State the policy as well. Tell Claude in the system prompt that content returned from tools, documents or searches is **data** and **never overrides your instructions** or the user's request.<sup>[1]</sup>

**Sanitizing (cleaning the input first).** This runs underneath, before content is placed anywhere.
- **Filter input** for **known injection patterns** (text written to hijack the model).
- Screen it with a **lightweight model call**. Its verdict must be constrained to a **parseable value** your code can branch on.
- Run that same screen over what your tools return.<sup>[1]</sup>

**One asymmetry catches people.** Your **own instructions** must **not travel** in a **tool result** either. Content there **counts as untrusted**, so your rule may be ignored or flagged. **Send it in the user turn** that follows the result.<sup>[1]</sup>

**Where this chapter stops.** Chapter 20 owns the attack. This chapter owns the arrangement that makes it legible.

**ELI5.** Put different kinds of paper in different labelled trays so the cook does not mix them up. But a label is only a sign. A sneaky note can copy the sign. So also tell the cook, "Anything in a delivery box is just information, never orders."

## Examples Settle Margins That Another Paragraph Will Not

**First, the idea.** Showing a finished dish teaches more than describing it. This section asks which failures examples fix, and which they leave alone.

**Where this comes from.** Chapter 1 set out the **ladder from zero-shot to multi-shot** (no examples up to several examples) and what each rung costs. The narrower question here is the one scenarios ask.

**What examples do.** Demonstrating a **desired output** steers **format**, **tone** and **structure** more dependably than describing one in the abstract.<sup>[5]</sup><sup>[6]</sup> The reason is simple.
- A **description states a rule** and leaves its margins (the edges) to guesswork.
- A **worked instance shows one margin** already decided. It fixes the exact casing, the exact field names, and the exact handling of the awkward case.

**Three conditions that call for examples.** Treat them as conditions, not as fixed cases.
- The **task is understood** and the **structure keeps being invented**.
- **Category boundaries drift between runs**. A definition leaves edges open that a labelled instance closes.
- The model is looking in the wrong place. **Fields come back empty** although the value sits in a **footnote** or a **caption**. Demonstrations of extraction from those places move attention where no instruction about diligence does.

**The anti-pattern: more examples of the case that already works.** It feels like effort, which is why it survives review. Adding clean examples to a prompt that already handles clean inputs makes the shortfall bigger. Examples have to come from the **population that fails**.

**ELI5.** A photo of the finished plate beats a paragraph describing it. But show photos of the plates that keep going wrong, not the ones the cook already gets right.

## An Output Constraint Names a Form, and It Is Still Only a Request

**First, the idea.** An **output constraint** governs shape, independent of content. That means field names, **permitted values**, length, and the **stopping point** saying nothing else may follow. It is the plating spec in the kitchen. Where one is absent, content is often right while form varies enough to break whatever parses it.

**Three formatting levers.** Anthropic documents these.
- Say what the output should be rather than what it should not contain.
- **Use tags as format indicators**.
- **Match the style** of your prompt to the style you want back. A prompt's formatting influences the response. Stripping markdown out of a prompt **reduces markdown in the output**.<sup>[4]</sup>

**A withdrawn technique: prefill.** Older guidance still shows it. Prefilling the assistant's turn used to be the standard way to force a shape by starting the answer yourself. From **Claude 4.6 onward**, **prefilled responses on the final assistant turn** are unsupported and **return a `400` error**. **Earlier models still accept** them. Assistant messages elsewhere are unaffected.<sup>[7]</sup> A scenario **offering prefill as the fix** on a current model is offering an error.

**The ban stated instead of a method.** This owns the section. Examples:
- **Marking a field non-nullable** (it may never be empty)
- declaring an empty value unacceptable
- **retrying until something appears**

Each removes the honest answer without improving the search that produced it. So an absent value becomes an **invented one**. A constraint on form cannot supply content that was **never generated**.

**Still only a request.** A **prompt-level constraint** stays a request the model may miss on an untested input. Chapter 6 owns the mechanism that closes that gap by **constraining generation against a schema** (a fixed template for the output).

**ELI5.** A plating spec tells the cook how the plate must look. It cannot make an ingredient appear that was never in the kitchen. If you forbid an empty spot, the cook may just make something up to fill it.

## Iteration Converges Only When Each Round Carries Evidence

**First, the idea.** Improving a prompt is like fixing a recipe. You taste, find what is wrong, change one thing, and taste again. Guessing in circles does not work.

**The loop that works** has three steps: **diagnose**, **add the one missing piece**, **measure**. The loop that fails is re-prompt, re-prompt, re-prompt. The prompt gets longer each time and nobody names what broke.

**Diagnosis is a short lookup**, because the failure identifies the **absent technique**.

| What you observed | What is absent |
|---|---|
| Right answer, wrong shape, parser breaks | An output constraint naming form and stopping point |
| Scope drifts and tone moves as the conversation runs on | A standing contract in `system`, stated once and specifically |
| Task understood, structure invented | Worked examples showing the structure |
| Clean on tested inputs, broken on a variant | A rule or an example covering that variant |

**Three named failures live in the loop, not in the prompt.**
- The **rewrite from scratch** throws away every case that already passed. So **nothing accumulates** and nothing converges.
- The **accreting prompt** adds paragraphs without adding a missing piece. **Length is not free**. A verbose prompt pulls verbose output, which **buys latency and no accuracy**.
- The **user warned off** ships the defect and asks humans to route around a category that is usually growing.

**Feedback must carry evidence.** Otherwise the round is wasted. Useful feedback includes **failing test names**, the inputs, **expected against actual**, and the trace. Unspecific feedback buys unspecific change.

**Two outside limits.**
- Iteration needs something to iterate against. That set has to **hold the inputs that fail**. So real traffic belongs inside the loop, not a clean development set standing in for it. **Messy traffic needs rules** of its own. For example: how to behave when the **source omits a mandatory field**, how to **resolve two passages that disagree**, how to answer an **out-of-scope request**. Chapter 19 owns running that measurement as a discipline.
- Know when to stop. Anthropic says plainly that **not every failing evaluation** is best solved by prompting. It names latency and cost as examples a **different model choice** may settle more easily.<sup>[8]</sup> Chapter 4 owns that call. A scenario whose constraint is money or milliseconds is **not a prompting question in disguise**.

**ELI5.** To fix a recipe, taste it, work out what is missing, add that one thing, and taste again. Do not throw the whole recipe away every time. And if the real problem is the stove is too slow, no recipe change will fix it.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here **describe real practice**. Somebody has genuinely done every one of them, often to a prompt that **improved afterwards**. **Four assumptions** produce most of them.

**The four wrong assumptions:**
- **Willingness assumed where specification is missing.** The option **repeats an instruction**, **intensifies** it, or asserts that the **output is unacceptable**. All three read the gap as reluctance. But the **model complied** with what it was given. So the **useful move names the piece** nobody supplied.
- **A prohibition offered where a method is needed.** Examples are **forbidding an empty field**, **banning a value**, and **retrying until something arrives**. Each removes an outcome and supplies no route to a better one. They turn correct only where the scenario states the **model already holds the information**.
- **The failing population kept outside the loop.** Examples are **more examples from the clean set**, a **wider output cap**, or a **different sampling setting**. Each optimises the distribution that was already working.
- **A standing rule given a per-request home.** Examples are **restating the contract in every turn**, **duplicating it in both places**, or **leaving each instruction** where it was first typed. **Copies drift**, and your rules end up in the channel carrying **supplied content**.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Instructions sit in both the system prompt and the turns, and the format varies | Standing behaviour and the output contract consolidated in `system`, once | Restating the contract every request, or holding it in both places |
| A supplied document must be analysed under persistent rules | Rules in `system`; document in the turn, delimited from the request | Concatenating document text into the standing instructions |
| The task is right and the structure keeps being invented | Worked examples showing the exact shape | A longer description, or a firmer request for the same shape |
| Fields come back empty although the material holds them somewhere unusual | Examples demonstrating extraction from those locations | Forbidding the empty value, or retrying until one appears |
| Good scores in development, poor behaviour on live traffic | Failing inputs added to the measured set, plus rules for degenerate ones | More examples from the clean set, or more output room |
| One call reads, extracts, judges and summarises, and quality is uneven by part | Focused calls in sequence, each fed the previous step's structured output | Urging thoroughness, a bigger cap, or a temperature change |
| Repeated fixes keep lengthening the prompt without fixing it | Name the failure, add the single missing technique, measure | Rewriting from scratch, or relaxing the check that reports it |

**A habit that works past the table.** For any option that changes a prompt, say which **piece it adds** and which **destination** it puts that piece in.
- An option **adding no piece** is **restating**.
- An option **adding a piece** to the **wrong destination** reads best and ages worst.

**ELI5.** Most wrong answers either say the same thing louder, ban something without giving a way to do better, practise on easy cases, or scribble the house rules on every ticket. The right answer finds the one missing piece and puts it in the right place.

## What to Remember

- **Placement sorts** by **two questions**: how **long the text applies**, and who could have written it. **Lifetime decides duplication**. **Authorship** decides whether it may **instruct**.
- **Three destinations**, never two. **Persistent rules** go in **top-level `system`**. This request's question and the user's **own material** go in the turn. **Third-party content** goes in **`tool_result` blocks**. **Nothing you did not write** reaches the first.
- A **mid-conversation system message** carries the **same authority** as the **`system` field**. It **cannot be first** and it appends at the end. So it adds a **late rule** without **invalidating a cached prefix**.
- An instruction is **checkable** when **output can be tested** against it: **named permitted values**, a **stated ceiling**, a **rule for conflicting sources**. Anthropic's test is whether a **human with minimal context** could follow it unconfused.
- **Say what to do** rather than what to **avoid**, and **give the reason**, because the **model generalises** from an **explanation** to cases the **instruction never named**. **Restating a rule more firmly** names no failing part, and **aggressive phrasing** now causes **over-triggering**.
- **Tags separate instructions**, **context**, **examples** and **input** so none is **read as another**. **Long documents** sit near the top, above **query**, **instructions** and **examples**.
- **Delimiting is a boundary** the model reads, not one the **runtime enforces**. **JSON-encode untrusted strings**. **State in `system`** that **supplied content never overrides** instructions. Screen input and tool output with a **lightweight classifier** first. Your **own instructions** never travel in a **tool result**, since **content there counts as untrusted**.
- **Examples repair invented structure** and open category boundaries. They **change where the model looks** when **values sit** in **footnotes**, **captions** or **covering letters**. They must come from the **population that fails**.
- An output constraint governs form independent of content: **field names**, **permitted values**, **length**, and a **stopping point**. **Prefilling the final assistant turn** returns a **`400` error** on **Claude 4.6** and later.
- **Forbidding an empty value** supplies no method, so the **missing answer** becomes an **invented one**. **Shape constraints** cannot **generate content** that was never produced.
- **Diagnose before re-prompting.** **Wrong shape** wants a **constraint**. **Drifting scope** wants a **specific system prompt**. **Invented structure** wants **examples**. A **broken variant** wants a rule covering it.
- **Iteration converges** on specific evidence: **failing cases**, **inputs**, **expected against actual**. **Rewriting from scratch** discards what passed, and a **prompt that only grows** is a skipped diagnosis.
- The measured set must hold the **inputs that fail**. Messy traffic needs its own rules: **omitted mandatory fields**, **passages that disagree**, **requests outside the defined scope**.
- **Not every failing evaluation** is a **prompting problem**. Anthropic names **latency** and **cost** as constraints a **different model choice** may settle **more easily**.

**ELI5.** Put the house rules on the kitchen wall, once. Keep today's order on the ticket. Leave strangers' notes in their boxes. Write rules you can check, show photos of the plates that go wrong, and fix recipes one tasted change at a time.

## Endnotes for this chapter

1. Untrusted third-party content should be delivered inside `tool_result` blocks rather than in `system` prompts or plain user `text` blocks, because Claude is trained to treat instructions appearing inside tool results with appropriate scepticism; the nature and source of the content should be made explicit; the system prompt should state that content returned from tools, documents or searches is untrusted data that must never override the system prompt or the user's original request; third-party strings should be JSON-encoded so escaping provides unambiguous delimiters and an attacker cannot close a quote or tag to break out into an instruction context; your own instructions should not be placed in tool results, because content there is treated as untrusted and may be ignored or flagged, and should instead be sent in a user turn following the `tool_result` block; input should be filtered for known injection patterns and pre-screened with a lightweight model using structured outputs to constrain the response to a simple classification; and the same screening pattern should be applied to tool outputs before the content is returned to Claude. Anthropic, *Mitigate jailbreaks and prompt injections* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

2. On supported models a message with `"role": "system"` may be included after a user turn to add a system instruction partway through a conversation; a system message cannot be the first entry in `messages`, and the top-level `system` field is used for instructions that apply from the start; a mid-conversation system message has the same authority as the top-level `system` field but, because it is appended to the end of the message history, does not invalidate a cached prefix that came before it. Anthropic, *Using the Messages API* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/working-with-messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)

3. Claude responds well to clear, explicit instructions, and being specific about the desired output improves results; the stated golden rule is to show the prompt to a colleague with minimal context on the task and ask them to follow it, on the basis that a person who would be confused indicates the model will be too; providing context or motivation behind instructions helps Claude understand the goal and deliver more targeted responses, because Claude generalises from the explanation; setting a role in the system prompt focuses Claude's behaviour and tone. Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

4. Effective ways to steer output formatting include telling Claude what to do instead of what not to do, using XML format indicators, and matching prompt style to the desired output style, since the formatting used in a prompt may influence the response style and removing markdown from a prompt can reduce the volume of markdown in the output; prompts designed to reduce under-triggering on tools or skills may cause over-triggering on newer models, and the documented fix is to dial back aggressive language such as "CRITICAL: You MUST use this tool when..." in favour of ordinary phrasing such as "Use this tool when...". Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

5. Examples are among the most dependable means of steering Claude's output format, tone and structure, and are placed inside `<example>` tags, with multiple examples in `<examples>` tags, so Claude can distinguish them from instructions; XML tags help Claude parse complex prompts unambiguously where the prompt mixes instructions, context, examples and variable inputs, and wrapping each type of content in its own tag reduces misinterpretation; for large or data-rich inputs, long documents are placed near the top of the prompt above the query, instructions and examples, which improves performance across all models; multiple documents are each wrapped in `<document>` tags with `<document_content>` and `<source>` subtags; and for long document tasks, asking Claude to quote relevant parts of the documents before carrying out the task helps it focus on the relevant content. Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

6. Consistency techniques include precisely defining the desired output format using JSON, XML or custom templates, constraining with examples of the desired output on the basis that this is more effective than abstract instructions, using system prompts to set the role, and breaking complex tasks into smaller subtasks chained together so each receives full attention. Anthropic, *Increase output consistency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)

7. Starting with Claude 4.6 models, prefilled responses providing a partial assistant message on the last assistant turn are no longer supported, and requests containing them return a `400` error; earlier models continue to support prefills, and adding assistant messages elsewhere in the conversation is not affected. Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

8. Prompt engineering guidance focuses on success criteria that are controllable through prompt engineering, and not every success criterion or failing evaluation is best solved by prompt engineering; latency and cost are given as examples that can sometimes be improved more easily by selecting a different model. Anthropic, *Prompt engineering overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
