# Chapter 5: Instruction Placement Is a Trust Decision

**Summary**: *Put one sentence in two different places and you get two systems that break in different ways. Placement decides how long text applies, how many copies exist, and whether a stranger can rewrite your rules with one line in a document. Sort first. Wording, examples, output limits and the fix-it loop come after.*

## The Same Sentence in Two Places Is Two Different Systems

Picture a restaurant kitchen. The house recipe book is pinned to the wall. Every cook follows it on every order. The order ticket changes with each dish. Supplier boxes arrive at the back door and get checked first. We use it all chapter.

Take two prompts. Both say *return one label from the fixed set and nothing else*.

In the first, the sentence sits in the top-level `system` field (the pinned recipe book). It is written once. It covers every request, even ones nobody has imagined yet.

In the second, someone typed it under the ticket text in the user turn, because that is where they were working. Now it rides inside a string your turn-building code assembles. Each code path makes its own copy, and the copies drift.

Same words, same model, same ticket. Yet the second system has no single home for its rules, and it keeps them in the channel that carries text strangers wrote (a note on the order ticket).

The fix is the **placement sort**: two questions for every piece of text. How long is it true? Who could have written it? Lifetime tells you if it repeats. Authorship tells you if it may give orders.

**ELI5.** A kitchen keeps lasting rules on the wall and tonight's order on a ticket. Write each rule on the wall once. Copy it onto tickets and the copies stop matching.

## Three Destinations, and Nothing You Did Not Write Reaches the First

Developers think of two places. There are three.

| Text | Lifetime | Possible author | Home |
|---|---|---|---|
| Role, tone, standing constraints | Every request | You | Top-level `system` |
| The output contract, plus the rule that supplied content never instructs | Every request | You | Top-level `system` |
| Worked examples of the output | Every request | You | `system`, tagged as examples |
| The question for this request | One request | The user in front of you | The user turn |
| A document the user attached | One request | Whoever gave it to them | The user turn, delimited |
| A fetched page, inbound mail, OCR text, a tool's return | One request | Anyone | `tool_result` blocks |

Outsider content goes in tool results (the supplier's box at the back door). Anthropic says to use `tool_result` blocks, not `system` or plain user text. Claude is trained to doubt orders inside tool results more than elsewhere.<sup>[1]</sup>

Chapter 3 added one twist. On supported models, a `"role": "system"` message can follow a user turn. It has the top-level field's authority but never comes first. So a late rule goes at the end and a cached prefix stays intact.<sup>[2]</sup>

The sort stops a quiet mistake, the document promoted to policy. Someone pastes a contract into the system prompt so the model surely sees it. Now the contract has your rules' authority, and any line addressed to a reader is addressed to Claude. It is a supplier's flyer stapled into the recipe book. Nobody attacked anything. Placement did it.

The mirror mistake is a standing rule put in the newest user message because recent text feels stickier. It does not hold that way, and it now sits beside pasted content.

**ELI5.** Your rules go on the wall, the order on the ticket, and a stranger's stuff in a checked box. A stranger's note never goes in the recipe book.

## An Instruction Is Checkable or It Is Decoration

Write *be precise* and nobody can tell when they have complied. A grader cannot either.

Anthropic's test: hand the prompt to a colleague who knows little about the task. If they would be confused, so is the model.<sup>[3]</sup>

An instruction is **checkable** when you can test output against it. A named list of allowed values works. So does a length ceiling, or a rule for which of two clashing sources wins. The rest is a mood.

Two habits help. Say what to do, since a ban removes one outcome and offers no replacement. And give the reason, which the model stretches to cases your words never named.<sup>[3]</sup>

When an instruction fails, people repeat it in capitals. That names no failing part, and on current models it backfires. Wording meant to stop older models doing too little now makes them do too much. Anthropic's fix is ordinary phrasing.<sup>[4]</sup> Volume was never a technique, and now it costs you.

**ELI5.** "Be nice" is hard to follow. "Say please and thank you" is easy. Say why, and the helper handles new cases.

## Delimiters Make Supplied Text Legible as Data

If a prompt mixes rules, background, samples and user input, give each its own tag. Claude is then less likely to read one as another. Samples go in `<example>` tags so they are not taken as part of the task.<sup>[5]</sup>

Three more rules cover long material. Put long documents near the top, above the query, instructions and examples. Wrap each document alone, with content and source in subtags. For long-document work, have Claude quote the relevant passages first.<sup>[5]</sup>

The model reads a tag. The runtime does not enforce it. A stranger's text can contain a fake closing tag (a forged label on the supplier's box). Stronger: JSON-encode third-party strings instead of pasting them into free text. Escaping leaves no way to close a quote and climb out into instruction position.<sup>[1]</sup> Also tell Claude in `system` that content from tools, documents or searches is data and never overrides your instructions or the user's request.<sup>[1]</sup>

Cleaning comes first. Strip known injection patterns from input, then screen it with a lightweight model call. Make its verdict a parseable value your code can branch on. Screen tool returns the same way.<sup>[1]</sup>

One asymmetry catches people. Your own instructions must not travel in a tool result either, since content there counts as untrusted and your rule may be ignored or flagged. Put it in the user turn that follows.<sup>[1]</sup> Chapter 20 covers the attack. Here, the layout.

**ELI5.** Label every box. But anyone can fake a label, so check what comes in, and never put your own orders in a stranger's box.

## Examples Settle Margins That Another Paragraph Will Not

Chapter 1 covered the zero-shot to multi-shot ladder. Here: which problems do examples fix, and which do they leave alone?

Showing the output you want steers format, tone and structure better than describing it.<sup>[5]</sup><sup>[6]</sup> A description gives a rule and leaves the edges to guesswork. A worked example shows one edge settled, down to casing, field names and the awkward case. It is a photo of the plate, not a speech.

Three situations call for examples. One, the model gets the task but invents the structure. Two, category lines move between runs, since a definition leaves gaps a labelled instance fills. Three, it looks in the wrong place. Fields come back empty although the value sits in a footnote or a caption. Examples that extract from those spots move its attention. Urging diligence does not.

The usual mistake is piling on examples of the case that already works. It feels like effort, so it passes review, but widens the gap. Use inputs that fail.

**ELI5.** A photo of the finished plate teaches more than a speech about neatness. Show the tricky plates that go wrong, not more easy ones.

## An Output Constraint Names a Form, and It Is Still Only a Request

An **output constraint** sets the shape of an answer, whatever the content. It covers field names, permitted values, length, and a stopping point where nothing else may follow. Without one, content may be right while form shifts enough to break your parser.

Anthropic documents three levers. Say what the output should be, not what to leave out. Use tags as format indicators. Match the prompt's style to the reply you want, since formatting rubs off: strip markdown from the prompt and you get less markdown out.<sup>[4]</sup>

Older guides still teach prefilling, which is starting the assistant's answer yourself to force a shape. From **Claude 4.6 onward**, prefilled responses on the final assistant turn are unsupported and return a `400` error. Earlier models still accept them, and assistant messages elsewhere are unaffected.<sup>[7]</sup> So prefill offered as a fix on a current model is an error.

A ban instead of a method is the trap here. Marking a field non-nullable, declaring an empty value unacceptable, retrying until something appears: each removes the honest answer and does nothing for the search. So a missing value becomes an invented one. A rule about form cannot create content that was never generated.

A constraint in the prompt is still a request, and the model may miss it on an untested input. Chapter 6 covers the fix: constrain generation against a schema.

**ELI5.** You can ask for a box of one size. That fixes the shape, not what goes inside. If the helper cannot find the thing, banning "empty" makes it invent something.

## Iteration Converges Only When Each Round Carries Evidence

A good loop is diagnose, add the one missing piece, measure. A bad loop is re-prompt, re-prompt, re-prompt, while nobody names what broke.

Diagnosis is a short lookup from symptom to missing technique.

| Symptom | Missing piece |
|---|---|
| Answer is right but the shape is wrong, so the parser breaks | An output constraint with form and stopping point |
| Scope and tone wander as the chat goes on | One specific standing contract in `system` |
| Task is clear but the structure gets invented | Worked examples of the structure |
| Fine on tested inputs, broken on a variant | A rule or example for that variant |

Three failures live in the loop itself. Rewriting from scratch discards every case that passed, so nothing builds up. An accreting prompt adds paragraphs but no missing piece, and a wordy prompt pulls wordy output, which costs latency and buys no accuracy. And warning users off ships the defect, asking them to avoid a category that usually keeps growing.

Feedback needs evidence: failing test names, the inputs, expected against actual, the trace.

Two outside limits apply. First, the set you iterate against must hold the inputs that fail, so real traffic belongs in the loop, not a tidy development set. Messy traffic needs rules too. What if the source skips a mandatory field? What if two passages disagree? What about an out-of-scope request? Chapter 19 covers running that measurement as a habit.

The other limit is knowing when to stop. Anthropic says prompting is not the best fix for every failing evaluation. For latency and cost, a different model may be easier.<sup>[8]</sup> Chapter 4 covers that call. If the real problem is money or milliseconds, prompting is the wrong tool.

**ELI5.** If the soup tastes off, find out why. Add the one missing thing and taste again. Do not tip out the pot.

## How Wrong Answers Are Built on This Material

Wrong answers here are things people really do. Four assumptions produce most.

- **Blaming willingness for a missing spec.** Repeat it, shout it, or call the output unacceptable. All three treat a gap as reluctance. The model did what it was told, so name the missing piece.
- **A ban where a method is needed.** Forbid an empty field, ban a value, retry until something shows up. None offers a route to a better answer. They fit only when the model already holds the information.
- **Failing inputs left out of the loop.** More clean examples, a wider output cap, a new sampling setting. All tune inputs that already work.
- **A standing rule given a per-request home.** Repeat the contract each turn, copy it to both places, or leave each instruction where it was first typed. Copies drift, and rules land beside supplied content.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| Rules sit in both system prompt and turns, and format varies | Behaviour and output contract in `system`, once | Repeat the contract each request, or keep both copies |
| A supplied document is analysed under lasting rules | Rules in `system`, document in the turn, kept apart from the request | Pasting the document into the standing rules |
| Task is right but structure keeps being invented | Examples of the exact shape | A longer description or a firmer ask |
| Fields come back empty though the data is somewhere odd | Examples that extract from those places | Banning the empty value, or retrying |
| Good in development, poor on live traffic | Failing inputs in the measured set, with rules for odd ones | More clean examples, or more output room |
| One call reads, extracts, judges and summarises, unevenly | A chain of focused calls, each fed the last step's structured output | Urging care, a bigger cap, or a new temperature |
| Fix after fix makes the prompt longer and no better | Name the failure, add one missing technique, measure | Start over, or loosen the check that reports it |

Use this habit on any option. Ask what piece it adds and where it puts that piece. No new piece means it is only restating. A piece in the wrong place looks fine today and fails later.

**ELI5.** Wrong answers sound like what a busy person would do: shout, ban, add easy stuff. Ask what new thing an answer adds, and where.

## What to Remember

- Placement sorts by two questions: how long the text applies, and who could have written it. Lifetime decides copies. Authorship decides who may instruct.
- Three homes, never two. Persistent rules go in top-level `system`. This request's question and the user's own material go in the turn. Third-party content goes in `tool_result` blocks. Nothing you did not write reaches the first.
- A mid-conversation system message has the same authority as `system`, cannot come first, and goes at the end. It adds a late rule and keeps a cached prefix valid.
- An instruction is checkable when output can be tested against it: named permitted values, a stated ceiling, a rule for conflicting sources. Anthropic's test: could a human with minimal context follow it unconfused?
- Say what to do, not what to avoid, and give the reason, because the model generalises from a reason to cases you never named. Saying a rule more firmly names no failing part, and aggressive phrasing now causes over-triggering.
- Tags keep instructions, context, examples and input from being read as each other. Long documents go near the top, above the query, instructions and examples.
- Delimiting is a boundary the model reads, not one the runtime enforces. JSON-encode untrusted strings, say in `system` that supplied content never overrides instructions, and screen input and tool output with a lightweight classifier first. Your own instructions never ride in a tool result, since content there counts as untrusted.
- Examples fix invented structure and blurry category edges. They also change where the model looks when values sit in footnotes, captions or covering letters. Draw them from the inputs that fail.
- An output constraint sets form, whatever the content: field names, permitted values, length, and a stopping point. Prefilling the final assistant turn returns a `400` error on Claude 4.6 and later.
- Forbidding an empty value gives no method, so a missing answer becomes an invented one. Shape constraints cannot create content that was never produced.
- Diagnose before re-prompting. Wrong shape wants a constraint, drifting scope a specific system prompt, invented structure examples, a broken variant a rule covering it.
- Iteration converges on specific evidence: failing cases, inputs, expected against actual. Rewriting from scratch loses what passed, and a prompt that only grows skipped the diagnosis.
- The measured set must hold the inputs that fail. Messy traffic needs its own rules for omitted mandatory fields, passages that disagree, and requests outside the defined scope.
- Not every failing evaluation is a prompting problem. Anthropic names latency and cost as limits a different model choice may settle more easily.

**ELI5.** Rules on the wall, the order on the ticket, strangers' boxes checked. Ask for things you can test. Find what is missing instead of shouting.

## Endnotes for this chapter

1. Untrusted third-party content should be delivered inside `tool_result` blocks rather than in `system` prompts or plain user `text` blocks, because Claude is trained to treat instructions appearing inside tool results with appropriate scepticism; the nature and source of the content should be made explicit; the system prompt should state that content returned from tools, documents or searches is untrusted data that must never override the system prompt or the user's original request; third-party strings should be JSON-encoded so escaping provides unambiguous delimiters and an attacker cannot close a quote or tag to break out into an instruction context; your own instructions should not be placed in tool results, because content there is treated as untrusted and may be ignored or flagged, and should instead be sent in a user turn following the `tool_result` block; input should be filtered for known injection patterns and pre-screened with a lightweight model using structured outputs to constrain the response to a simple classification; and the same screening pattern should be applied to tool outputs before the content is returned to Claude. Anthropic, *Mitigate jailbreaks and prompt injections* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

2. On supported models a message with `"role": "system"` may be included after a user turn to add a system instruction partway through a conversation; a system message cannot be the first entry in `messages`, and the top-level `system` field is used for instructions that apply from the start; a mid-conversation system message has the same authority as the top-level `system` field but, because it is appended to the end of the message history, does not invalidate a cached prefix that came before it. Anthropic, *Using the Messages API* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/working-with-messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)

3. Claude responds well to clear, explicit instructions, and being specific about the desired output improves results; the stated golden rule is to show the prompt to a colleague with minimal context on the task and ask them to follow it, on the basis that a person who would be confused indicates the model will be too; providing context or motivation behind instructions helps Claude understand the goal and deliver more targeted responses, because Claude generalises from the explanation; setting a role in the system prompt focuses Claude's behaviour and tone. Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

4. Effective ways to steer output formatting include telling Claude what to do instead of what not to do, using XML format indicators, and matching prompt style to the desired output style, since the formatting used in a prompt may influence the response style and removing markdown from a prompt can reduce the volume of markdown in the output; prompts designed to reduce under-triggering on tools or skills may cause over-triggering on newer models, and the documented fix is to dial back aggressive language such as "CRITICAL: You MUST use this tool when..." in favour of ordinary phrasing such as "Use this tool when...". Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

5. Examples are among the most dependable means of steering Claude's output format, tone and structure, and are placed inside `<example>` tags, with multiple examples in `<examples>` tags, so Claude can distinguish them from instructions; XML tags help Claude parse complex prompts unambiguously where the prompt mixes instructions, context, examples and variable inputs, and wrapping each type of content in its own tag reduces misinterpretation; for large or data-rich inputs, long documents are placed near the top of the prompt above the query, instructions and examples, which improves performance across all models; multiple documents are each wrapped in `<document>` tags with `<document_content>` and `<source>` subtags; and for long document tasks, asking Claude to quote relevant parts of the documents before carrying out the task helps it focus on the relevant content. Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

6. Consistency techniques include precisely defining the desired output format using JSON, XML or custom templates, constraining with examples of the desired output on the basis that this is more effective than abstract instructions, using system prompts to set the role, and breaking complex tasks into smaller subtasks chained together so each receives full attention. Anthropic, *Increase output consistency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)

7. Starting with Claude 4.6 models, prefilled responses providing a partial assistant message on the last assistant turn are no longer supported, and requests containing them return a `400` error; earlier models continue to support prefills, and adding assistant messages elsewhere in the conversation is not affected. Anthropic, *Prompting best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

8. Prompt engineering guidance focuses on success criteria that are controllable through prompt engineering, and not every success criterion or failing evaluation is best solved by prompt engineering; latency and cost are given as examples that can sometimes be improved more easily by selecting a different model. Anthropic, *Prompt engineering overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
