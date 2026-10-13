# Chapter 6: Schema-Valid Is Not the Same as Correct

**Summary**: *A schema tells you the response arrived with the right fields carrying the right types. It says nothing about whether the numbers in those fields are true. A response can be well formed, confidently worded and wrong. No validator can tell that apart from well formed and right. This chapter covers four jobs that sit between the model and your database. First, fixing the shape while the answer is being generated. Second, checking the response when it arrives. Third, parsing it so it survives surprises. Fourth, checking the content against something the model did not produce.*

## A Response Can Satisfy Every Rule You Wrote and Still Be Wrong

**First, the idea.** A program that reads Claude's answer needs two different things. The answer must have the right **shape** (the right fields and types). It must also be **true**. Checks that look at shape cannot tell you about truth.

**The analogy for this chapter: a receiving dock.** Think of a warehouse loading dock. A parcel arrives. The **response** (the parcel) comes in from outside. A **schema** (the packing-slip form) says which boxes the slip must have and what goes in each. A clerk, the **validator** (the dock clerk), checks that every box on the slip is filled in and that the entries are the right kind. The clerk does not open the parcel. Whether the goods inside match what you ordered is a different check. It needs something from outside the parcel, like the purchase order.

**The problem.** Suppose a reporting pipeline lifts figures out of filings into a ledger. Responses come back as JSON. Every field is present. Every type matches. The wording around each number is calm and specific. Nothing raises an error for weeks. Then a **reconciliation** (a check of the ledger against the source) turns up several figures that were **plausible, well formed and wrong**.

Go looking for the check that should have caught it. Every check there was **reading form**. The validator asked whether `revenue` was a number, and it was. **Nothing asked** whether it was the **right one**. The clerk checked the slip. Nobody counted the goods.

**Two questions.** Any check you can run answers one of two questions.
- The **shape question** asks whether the response is addressable (can be read field by field). Are the **fields present**? Are the **types right**? Are the values inside the **permitted set**?
- The **truth question** asks whether those fields **match the world**.

Constrained generation (the pre-printed form), schema validation (the dock clerk) and defensive parsing (a careful unpacking routine) answer the first question. They do it completely and cheaply. **Not one touches the second.**

**The anti-pattern: validity read as verification.** It survives code review because the **green check is real**. Something was genuinely verified. It was the **shape**.

**ELI5.** Imagine a parcel with a neat, filled-in label. The label can be perfect even when the thing inside is wrong. A clerk who only checks the label will say "all good". To know the thing inside is right, someone has to check it against something that did not come from the parcel.

## A Prompt Asks for a Shape; a Grammar Removes the Alternatives

**First, the idea.** You can ask Claude for a format in the prompt, or you can make the API enforce it. The second way removes the chance of a wrong shape. The first only makes it less likely.

**Asking in the prompt (a polite note on the slip).** Chapter 5 covered asking for a format in the prompt. That works most of the time. An **instruction holds** on the **inputs you tested** and slips on the one you did not.

**Structured outputs (a pre-printed form with tick boxes).** Structured outputs close the gap in the API instead of in the wording. You supply a **JSON Schema** (a written description of the shape you want). A **grammar** (a set of rules about which output is allowed) compiled from it constrains generation. A response **violating the schema cannot be produced** at all.<sup>[1]</sup> The form has no space where a wrong entry could go.
- `output_config.format` with `type: "json_schema"` **binds the final response**.
- `strict: true` on a tool definition **binds tool names** and inputs.
- You can use either one or both in one request.<sup>[1]</sup>

Chapter 9 owns the tool half. This chapter owns what comes back.

**Why it is not just "better prompting".** The difference from a prompt-level request is **not degree**. **Constraining generation removes the failure class**. **Hardening the parser** (making your reading code more forgiving) changes only how **loudly the consumer fails**.

**What the guarantee costs.** Every cost follows from the grammar.
- Compiling one adds **latency** (waiting time) on the first call with a new schema. So a schema held still is **cheaper** than one **rebuilt per tenant**.
- Every request then carries an **added system prompt** describing the format.
- A **schema too complex to compile** is refused outright. Optional fields are most of what makes one complex.<sup>[1]</sup>

**The old way.** **Prefilling the assistant turn** (starting Claude's reply for it) was the old way to force a shape. **Structured outputs** are its documented replacement on **Claude 4.6 and later**.<sup>[2]</sup>

**Agents.** Agents get the same mechanism one level up. The **Agent SDK validates** the result against your schema. It **re-prompts on a mismatch**. It gives up with the subtype `error_max_structured_output_retries`.<sup>[3]</sup> A quieter failure sits beside it. A run can **end with subtype `success`** and **no `structured_output`** at all.<sup>[3]</sup>

**ELI5.** You can write "please fill in the form neatly" on a sheet of blank paper. Most people will, but not always. Or you can hand out a form where wrong answers have no box to go in. The second way costs a bit of setup, but a wrong shape can't come out.

## Three Documented Ways a Guaranteed Schema Hands You Something Else

**First, the idea.** **Constrained decoding** (generating only allowed output) guarantees generation. It does not guarantee every response object that reaches your parser. Three documented exceptions arrive as an **ordinary 200** (the normal "success" status code).

| The exception | What the receiving code does |
|---|---|
| A safety refusal, `stop_reason` of `refusal`, arriving as a `200` rather than an error (the parcel arrives as a polite "we can't send this" note)<sup>[4]</sup> | Branch before parsing. On some models, retry the request elsewhere<sup>[4]</sup> |
| The output ceiling reached, `stop_reason` of `max_tokens`, structure cut mid-object (the form is torn off halfway)<sup>[1]</sup> | Raise the ceiling and retry. Do not try to salvage a fragment<sup>[1]</sup> |
| An enum (a fixed list of allowed values) in different capitalisation, completing with no error and no special `stop_reason` (the entry is written in a different style of lettering)<sup>[1]</sup> | Compare enums case-insensitively. Never define two that differ only in case<sup>[1]</sup> |

**Why the last one matters.** It teaches the chapter's point twice. **Nothing reports anything**. And a value your **code switches on** (chooses a branch by) matches no branch.

**What to do.** Read `stop_reason` before you read the content.

**ELI5.** Even with a special form, sometimes the clerk gets a note saying "no", a form torn in half, or an entry written in capitals when you expected small letters. All of these arrive looking like a normal delivery. So the clerk must look at why the delivery stopped before reading it.

## Validation on Receipt Needs a Destination for the Failure

**First, the idea.** **Validating** means running the response against the schema in your own process, on arrival, before anything downstream sees it. This is the dock clerk's job. It is also where you decide what happens to a parcel that fails.

**Why check again?** That sounds redundant, and it is not. Several **SDKs strip constraints** such as `minimum` and `maxLength` before sending. So Claude sees a simplified schema while your **code still enforces the originals**.<sup>[1]</sup> The range rule is enforced on receipt.

**Where the failure goes.** The destination matters more than the check, because a check with **no destination** is a crash with extra steps. There are three choices:
- Retry the call.
- **Reject the record** into a queue somebody works (a returns shelf that a person empties).
- **Route it to a person.**

**Choose by category, not by a number.** Choosing between those needs **categories** rather than a number. Say a pipeline routes everything on one **global threshold** (a single confidence cut-off). It has flattened three situations onto one axis:
- an **optional field genuinely absent**
- a **required field too poor to read**
- a **document never in scope**

**No cut separates them.** So name the three, give an example of each, and route on the category.

**ELI5.** When the clerk finds a bad parcel, there must be a place to send it. Maybe back to the sender, onto a shelf for a person to check, or straight to the manager. And "one score out of ten" can't tell "this box was meant to be empty" from "this box is smudged" from "this parcel isn't ours". Give each its own name and its own route.

## Defensive Parsing Survives the Unexpected and Still Reports It

**First, the idea.** **Defensive parsing** means reading the response in a way that does not break when something odd shows up. It must also say so when it happens.

**Two failures bracket this.**
- **Crashing on anything unfamiliar** is the outage you were asked to prevent.
- **Dropping whatever fails to conform** is worse. The **pipeline reports success** and the **records stay invisible**. The **silent drop** is the anti-pattern. It is attractive because it makes the alert stop. It is like throwing away every odd parcel and telling the boss nothing is missing.

**Graceful means both halves.** The **malformed case survives**. And every rejection leaves a **log line**, a metric and the payload, so the rate is a number somebody can see.

| The surprise | What survives it |
|---|---|
| A field you did not expect (an extra line on the slip) | Ignore it, and record that it arrived. A new field is how a producer announces a change |
| A value that is missing | Keep absent, null and empty as three states. Merging them invents information |
| A type that does not match | Convert where the conversion is exact. Reject where it is a guess. A string that fails to become a number is a rejection, never a zero |

**The same rule runs the other way.** It applies where your code feeds the model. A tool that **swallows its failure** and returns an **empty result** gets read as valid data. Then the model **reasons confidently on nothing**. Mark the failure so the turn carries it. Catch the SDK's **typed exception classes** (named error types) instead of matching error text.<sup>[5]</sup>

**ELI5.** A good clerk does not crash when a parcel looks strange, and does not quietly bin it either. They set it aside and write it in the log. That way, someone can see how many odd parcels came in.

## A Check Only Counts If Its Truth Comes From Outside the Model

**First, the idea.** Now the **truth question**. The tempting answers to it share one defect. They ask the parcel to vouch for itself.

**Four tempting checks that fail.**
- **Self-reported confidence score.** One **generation rates another**, with no new information arriving in between. That rating runs highest where the estimate is most **confidently mistaken**. That is the case you wanted it for.
- **Majority vote.** Sample the prompt several times and take the majority. A **stable error converges** as smoothly as a right answer does.
- **Agreement read as proof.** Anthropic documents **best-of-N** (running the same prompt several times and comparing) as a way to notice **inconsistency** across outputs. That is a signal that something may be wrong.<sup>[6]</sup> **Agreement** is **not the reverse signal**, though it gets read as one constantly.
- **A stronger model.** The error rate falls, but the **class of failure stays**. It stays **undetected** by anything downstream.

**Correlated verification** is the name for all four. The rule underneath is short. A **check catches a confident wrong answer** only when its own **correctness** rests on something **established outside the model**. This is the purchase order. It does not come from the parcel.

**The unglamorous work is the answer.**
- **Recompute derived values** in code and compare. **Arithmetic** is the cheapest **independent authority** you own.
- **Cross-check totals and identifiers** against the source records. That is where a figure lifted from a filing meets the filing.
- **Enforce range and consistency rules** drawn from the **domain** (the subject area) rather than from the response.
- Route every violation to **human review** instead of **retrying** until the check passes.

**Two documented techniques narrow the problem beforehand.**
- **Restricting Claude to the supplied documents** rather than its general knowledge cuts the class of claims that have **no source** at all.<sup>[6]</sup>
- **Citations return the exact passages** supporting each claim, so a person or a program can check them.<sup>[7]</sup>

**Provenance belongs in the schema.** Provenance means where a claim came from. It belongs in the schema for the same reason the figures do. Somebody acting on a claim needs its support as addressable fields that answer four questions:
- What kind of **source** was it?
- Which **passage or returned value** does it rest on?
- When was that **observed**?
- Has anybody **checked** it?

Squeezing that into a tidier narrative removes what the reviewer came for. **Attaching the raw transcript** instead hands every reviewer the same reconstruction job.

**A mirror case: sources that disagree.** When two **credible sources disagree**, a single confident answer gets **manufactured rather than found**.
- **Averaging invents** a third figure nobody reported.
- **Keeping the larger** one calls a preference a finding.
- **Searching until something backs** one of them is a hunt whose verdict was fixed before it began.

Carry both, attributed, with the **conflict marked**. An output that **represents the disagreement** is the accurate one.

**ELI5.** If you ask a parcel "are you right?", it will say yes. So don't ask it. Count the goods yourself, compare them to the order, and keep a note of where each fact came from. If two trusted orders say different things, write both down instead of picking one.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here describe **real engineering**, and somebody has shipped every one. **Four assumptions** produce most of them.

**The four wrong assumptions:**
- **Shape offered against a truth problem.** The **output validated** and was **wrong anyway**. The option adds a **schema**, a **stricter validator** or a **better prompt**. All three answer a question about **parse failures nobody asked**.
- **A check drawn from the process** it is checking. Examples are **self-reported confidence**, **majority vote**, **self-grading** and a **larger model**. Each fails where the **answer fails**, which is the only place it was needed.
- **Cooperation requested where enforcement is available.** Examples are asking for **JSON**, asking **more firmly**, or **retrying** until something parses. **None fixes the boundary**, and none detects being ignored.
- **A failure removed from view** instead of from the **system**. Examples are **dropping non-conforming output** quietly, **coercing an absent value** into a present one, or **deleting the source** that disagrees. The symptom stops and **nothing improved**.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Output validates and is wrong anyway | Recompute or cross-check outside the model, route violations to a person | A stronger model, a stricter schema, a model-filled confidence field |
| The format varies between calls and a program consumes it | Constrain generation to a declared schema, then validate on receipt | A regular expression over today's formatting, or a firmer prompt |
| Code crashes on an unexpected field, a missing value or a wrong type | Parse defensively: survivable, and still visible | Dropping non-conforming output silently, or leaving the crash |
| Credible sources disagree, or a claim must support somebody else's decision | Carry conflict and provenance as fields: source, excerpt, timestamp, verification state | Averaging, keeping the larger, or a narrative the reviewer reassembles |
| Extraction routes everything on one confidence threshold | Name and exemplify the outcomes: absent-optional, unreadable-required, out of scope | One global cut, or retrying until every field fills |
| The response is refused, truncated, or oddly cased | Branch on `stop_reason` before parsing; compare enums case-insensitively | Treating any `200` as a successful generation |

**A habit that works past the table.** For any option offered as a **reliability fix**, ask what it would take for the output to be **wrong and still pass** it. If **nothing outside the model** was consulted, it answers the **shape question**.

**ELI5.** Most wrong answers either check the label harder, ask the parcel to vouch for itself, or hide the bad parcels. None of those count the goods. Only a check from outside the parcel can.

## What to Remember

- Every check answers the **shape question** (**fields, types and permitted values**) or the **truth question** (whether **content matches the world**). **Schema validation**, **constrained generation** and **defensive parsing** answer only the first.
- **Structured outputs** compile your **JSON Schema into a grammar** that constrains generation, so **violating output cannot be produced**. `output_config.format` **binds the final response**. `strict: true` **binds tool names** and inputs.
- **Constraining generation removes the failure class**. **Parsing harder** changes only how **loudly the consumer fails**. A **prompt-level format request** holds on the inputs you tested and **slips** on the one you did not. The grammar costs **first-call latency**, an **added system prompt**, and **refusal** of a **schema too complex to compile**.
- **Three documented escapes** return `200` without usable structure: a **refusal**, a **`max_tokens` truncation**, and an **enum in different capitalisation** carrying **no error** and no special `stop_reason`. **Read `stop_reason`** before content, and **compare enums** case-insensitively.
- **SDKs strip range and length constraints** from the **schema** they send, so your own **validation on receipt** enforces them. A validation failure **needs a destination**: **retry**, **reject** into a queue, or **route** to a person. Choose by **named category**, because **absent-but-optional, unreadable-but-required and out-of-scope** are outcomes **no confidence number separates**.
- **Defensive parsing survives** the surprise and still reports it. **Tolerate unknown fields**. Keep **absent, null and empty** distinct. **Reject a type mismatch** instead of coercing a guess. **Log every rejection**. The **silent drop** is the worse failure, because the **pipeline reports success** while **records disappear**.
- A check **catches a confident wrong answer** only when its own correctness rests on something **established outside the model**. **Self-reported confidence**, **majority vote** and a **bigger model** all fail where the **answer itself fails**.
- Independent verification is **arithmetic and lookups**. **Recompute derived values**. **Cross-check totals** against source records. Enforce **domain range rules**. Send violations to **human review**. **Provenance** is a field: **source type, excerpt, timestamp, verification state**. Conflicting credible sources are carried with the **conflict marked**, because **averaging invents a number** nobody reported.

**ELI5.** A neat label does not mean the goods are right. Use a pre-printed form so the label is always neat. Have a clerk check it and send bad ones somewhere useful. Never bin the odd ones quietly. And check the goods against the purchase order, not against the parcel.

## Endnotes for this chapter

1. Structured outputs constrain Claude's responses to follow a specific schema by compiling the JSON schema into a grammar used for constrained sampling, so that responses violating the schema cannot be generated; `output_config.format` with `type: "json_schema"` controls the response format and `strict: true` guarantees schema validation on tool names and inputs, and the two may be used independently or together in one request; the compiled schema is temporarily cached, so a first call on a new schema carries the compilation; when structured outputs are in use Claude automatically receives an additional system prompt explaining the expected output format; explicit limits apply to the number of strict tools, optional parameters and parameters using union types, with a `400` error reading "Schema is too complex for compilation" beyond them, and each optional parameter roughly doubles a portion of the grammar's state space, so the documented mitigations include reducing optional parameters and simplifying nested structures; schema compliance is not guaranteed on a refusal (`stop_reason: "refusal"`) or on reaching the token limit (`stop_reason: "max_tokens"`, for which the documented response is to retry with a higher `max_tokens`); enum and const capitalisation is not guaranteed, the response completes normally with no error and no special `stop_reason`, and the guidance is to compare enum values case-insensitively and avoid enum values differing only in capitalisation; several SDKs transform schemas by removing constraints such as `minimum`, `maximum`, `minLength` and `maxLength` and adding `additionalProperties: false`, so that Claude receives a simplified schema while your code still enforces all constraints through validation. Anthropic, *Structured outputs* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/structured-outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

2. Claude 4.6 and later models do not support prefilling assistant messages, and a request whose last assistant message is a prefill returns a `400` `invalid_request_error`; the documented alternatives are structured outputs on models that support them, system prompt instructions, or `output_config.format`. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

3. The Agent SDK accepts an `outputFormat` or `output_format` option of `type: "json_schema"` with a JSON Schema, validates the agent's output against that schema and re-prompts on a mismatch, and returns a result subtype of `error_max_structured_output_retries` when no valid output remains after the retry limit; a result can also end with subtype `success` and no `structured_output` value, for example when the run completes without the agent producing a structured output, and that case should also be treated as a failure. Anthropic, *Get structured output from agents* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/structured-outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs)

4. Every Messages API response includes a `stop_reason` field indicating why Claude stopped generating, and it should be checked in response handling to decide whether to use the response as-is, continue, retry, or fall back; a refusal is returned by safety classifiers as a normal HTTP `200` response with `stop_reason` of `refusal` rather than as an error, and a refused request on some models can usually be served by retrying on another Claude model; `stop_reason` values are distinct from errors, which indicate failures in processing the request. Anthropic, *Stop reasons and fallback* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)

5. The official SDKs raise typed exceptions rather than returning raw JSON, and the documented guidance is to catch the SDK's typed classes rather than string-matching error messages, handling the most specific classes first. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

6. Documented techniques for minimising hallucinations include best-of-N verification, running Claude through the same prompt multiple times and comparing outputs on the basis that inconsistencies across outputs could indicate hallucinations; chain-of-thought verification; iterative refinement; and external knowledge restriction, explicitly instructing Claude to use only information from provided documents rather than its general knowledge. Anthropic, *Reduce hallucinations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

7. Citations ground responses in supplied source documents and return the exact passages that support each claim, so the sources behind a response can be tracked and verified. Anthropic, *Citations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/citations](https://platform.claude.com/docs/en/build-with-claude/citations)
