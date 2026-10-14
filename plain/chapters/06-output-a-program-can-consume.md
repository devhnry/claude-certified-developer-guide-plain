# Chapter 6: Schema-Valid Is Not the Same as Correct

**Summary**: *A schema checks that the right fields arrived with the right types. It cannot say whether the numbers inside are true. Four jobs sit between the model and your database: fix the shape at generation, check the response on arrival, parse it so surprises do not break you, and verify the content against something the model did not write.*

## A Response Can Satisfy Every Rule You Wrote and Still Be Wrong

Picture a clerk at a loading dock. A box arrives. The clerk checks the label and the packing slip, then signs. Nobody opens the box.

A reporting pipeline worked that way. It pulled figures from filings into a ledger. Every response was JSON with all fields present and all types right. Then a **reconciliation**, a comparison of the ledger against the sources, found several figures that looked fine and were wrong.

The validator had asked whether `revenue` was a number. It was. Nobody checked that it was the right one.

So every check answers one of two questions. The shape question: can I use this response? That is the clerk reading labels. The truth question: do the fields match the real world? That is opening the box. Constrained generation, schema validation and defensive parsing all answer the first, cheaply and fully. None of them touches the second.

Mixing the two up has a name: **validity read as verification**. It survives code review because the green check is real. Something was verified. It was the shape.

**ELI5.** A clerk can read a label without looking inside. A neat label does not mean the right thing is in the box. A schema reads the label.

## A Prompt Asks for a Shape; a Grammar Removes the Alternatives

Chapter 5 covered asking for a format in the prompt. That works on the inputs you tested. It slips on the one you did not.

Structured outputs fix this in the API. You give a JSON Schema. The API compiles it into a grammar that limits what the model can write, so a response that breaks the schema cannot be produced.<sup>[1]</sup> `output_config.format` with `type: "json_schema"` binds the final response. `strict: true` on a tool definition binds tool names and inputs. Use either or both together.<sup>[1]</sup> Chapter 9 owns the tool half. This chapter owns what comes back.

This is not a matter of degree. Constraining generation removes the failure class. Hardening the parser only changes how loudly the consumer fails.

The costs come from the grammar. A new schema slows the first call, so a fixed schema beats one rebuilt per tenant. Each request also carries an added system prompt describing the format. A schema too complex to compile is refused. Optional fields add most of that complexity.<sup>[1]</sup>

**Prefilling the assistant turn**, starting the reply for the model, used to force a shape. On **Claude 4.6 and later**, structured outputs replace it.<sup>[2]</sup>

The **Agent SDK** does the same for agents. It re-prompts on a mismatch. When retries run out, it stops with the subtype `error_max_structured_output_retries`.<sup>[3]</sup> A quieter failure exists too. A run can end with subtype `success` and carry no `structured_output` at all.<sup>[3]</sup>

**ELI5.** Asking for a box shape is a note on the door. A grammar is a door that only fits the right box. Building it takes time.

## Three Documented Ways a Guaranteed Schema Hands You Something Else

**Constrained decoding** guarantees what the model writes. It does not guarantee every response object reaching your parser. Three documented cases come back as a normal `200`.

| What happens | How the receiver copes |
|---|---|
| The model refuses. `stop_reason` is `refusal`, delivered as a `200` and not an error<sup>[4]</sup> | Check before parsing. On some models, retry elsewhere<sup>[4]</sup> |
| The token ceiling is hit. `stop_reason` is `max_tokens` and the object is cut off midway<sup>[1]</sup> | Raise the ceiling and retry. Do not patch the fragment<sup>[1]</sup> |
| An enum comes back capitalised differently, with no error and no special `stop_reason`<sup>[1]</sup> | Compare ignoring case. Never define two enums that differ only in case<sup>[1]</sup> |

The last one makes the chapter's point twice. Nothing reports a problem, and your code switches on a value that matches no branch. `"Paid"` arrives where you wrote `"paid"`.

**ELI5.** A truck can bring a half-empty box or a "can't ship" note. Both count as arrived. Read the delivery note first.

## Validation on Receipt Needs a Destination for the Failure

Validating means checking the response against the schema in your own process, before anything downstream sees it. It looks like repeated work, but several SDKs strip constraints like `minimum` and `maxLength` before sending. Claude sees a simplified schema, and your code still has to enforce the originals.<sup>[1]</sup> 

Where a failure goes matters more than the check. With nowhere to go, it is a crash with extra steps. You have three places. Retry the call. Reject the record into a queue someone works. Or route it to a person.

To pick, you need categories, not a number. One global confidence threshold squashes three situations onto one line. An optional field may be truly absent. A required field may be too poor to read. A document may never have been in scope. No cut-off separates them. Name each, give an example, route by name.

**ELI5.** A wrong box needs a shelf. Send it back, park it, or call someone. A clerk with no shelf drops it.

## Defensive Parsing Survives the Unexpected and Still Reports It

Crashing on anything unfamiliar is the outage you meant to prevent. Dropping what does not fit is worse: the pipeline reports success while records vanish. This **silent drop** is the anti-pattern.

Graceful handling has two halves. The odd case survives. And every rejection leaves a log line, a metric and the payload, so someone can watch the rate.

| The surprise | What to do |
|---|---|
| A field nobody expected | Ignore it, but note it arrived. A new field announces a change |
| A value that is gone | Keep absent, null and empty as three states. Merging them invents information |
| The wrong type | Convert if the conversion is exact. Reject if it is a guess. A string that will not become a number is rejected, not made zero |

The same care applies when your code feeds the model. Say a tool swallows its error and returns an empty result. The model reads that as real data and reasons confidently on nothing. Flag the failure. And catch the SDK's typed exception classes, not the error text.<sup>[5]</sup>

**ELI5.** A good clerk neither tosses a strange parcel nor hides it. They set it aside and log it.

## A Check Only Counts If Its Truth Comes From Outside the Model

Now the truth question. The easy answers share one flaw.

Ask the model to score its own confidence, and one generation grades another with no new information. The score runs highest exactly where the answer is most confidently wrong. Run the prompt several times and take the majority, and a steady error wins the vote as smoothly as a right answer. Anthropic documents **best-of-N** to notice when outputs disagree, which hints something may be wrong.<sup>[6]</sup> Switch to a stronger model, and the error rate falls but the kind of failure stays, unseen downstream.

**Correlated verification** names all four. One rule covers it. A check can catch a confident wrong answer only if its own correctness rests on something established outside the model.

The fix is plain work.

- Redo derived values in code and compare. Sums and products are the cheapest outside authority you own.
- Check totals and identifiers against the source records.
- Apply range and consistency rules from the domain, not from the response.
- Send each violation to human review. Do not retry until the check passes.

Two documented techniques help first. Tell Claude to use only the supplied documents, not its general knowledge. Claims with no source drop away.<sup>[6]</sup> And **citations** return the exact passages behind each claim, so a person or program can check them.<sup>[7]</sup>

**Provenance**, where a claim came from, belongs in the schema as fields. Whoever acts on a claim needs four answers. What type of source? Which passage or returned value? When was it seen? Has anyone checked it? A tidy summary strips out what the reviewer came for. A raw transcript makes every reviewer rebuild the same story.

One mirror case. Two credible sources disagree, and the pull is to give one confident answer. That answer is manufactured, not found. Averaging invents a third figure nobody reported. Keeping the larger one dresses a preference up as a finding. Hunting until something backs one side decides the verdict first. Carry both values, name each source and mark the conflict.

**ELI5.** To know a box holds the right thing, look at something other than the packer. Count the items. If two order forms disagree, say so.

## How Wrong Answers Are Built on This Material

Each wrong answer is real engineering that somebody shipped. Four habits cause most.

- **Shape offered for a truth problem.** The output passed and was still wrong. The option adds a schema, a stricter validator or a better prompt.
- **A check borrowed from the thing it checks.** Self-scoring, voting, a larger model. It fails exactly where the answer fails.
- **Asking nicely where you can enforce.** Asking harder, retrying until it parses.
- **Hiding the failure, not fixing it.** Quiet drops, absent values made present.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| Passes validation, still wrong | Redo the math or compare with outside sources, give violations to a person | Stronger model, stricter schema, a confidence field the model fills |
| Format shifts between calls and code consumes it | Declare a schema to constrain generation, then validate on receipt | A regex over today's format, or a firmer prompt |
| Crash on extra field, missing value or wrong type | Survive it and keep it visible | Silent drop, or leaving the crash |
| Credible sources disagree, or a claim feeds someone's decision | Conflict and provenance as fields: source, excerpt, timestamp, verification state | Averaging, picking the larger, or a story the reviewer must rebuild |
| One confidence threshold routes all extraction | Named outcomes with examples: absent-optional, unreadable-required, out of scope | One global cut, or retrying until all fields fill |
| Refused, truncated or oddly cased response | Branch on `stop_reason` before parsing; compare enums ignoring case | Treating every `200` as a good generation |

One habit works beyond the table. When something is sold as a reliability fix, ask how the output could be wrong and still pass.

**ELI5.** Tricky answers sell a better label reader when the trouble is inside the box. Ask: could a wrong box still get through?

## What to Remember

- Every check answers the shape question (fields, types, permitted values) or the truth question (does content match the world). Schema validation, constrained generation and defensive parsing answer only the first.
- Structured outputs turn your JSON Schema into a grammar, so violating output cannot be produced. `output_config.format` binds the final response. `strict: true` binds tool names and inputs.
- Constraining generation removes the failure class. Parsing harder only changes how loudly the consumer fails. A format request in the prompt holds on tested inputs and slips on the untested one. The grammar costs first-call latency, an added system prompt, and refusal of a schema too complex to compile.
- Three documented escapes arrive as an ordinary 200. None has usable structure: a refusal, a `max_tokens` truncation, and an enum in different capitalisation, with no error and no special `stop_reason`. Read `stop_reason` before content, and compare enums case-insensitively.
- SDKs strip range and length constraints from the schema they send, so validate on receipt. A failure needs a destination: retry, reject into a queue, or route to a person. Choose by named category, because absent-but-optional, unreadable-but-required and out-of-scope are outcomes no confidence number separates.
- Defensive parsing survives the surprise and reports it: tolerate unknown fields, keep absent, null and empty distinct, reject a type mismatch instead of coercing a guess, log every rejection. A silent drop is worse, since the pipeline reports success while records vanish.
- A check catches a confident wrong answer only when it rests on something established outside the model. Self-reported confidence, majority vote and a bigger model all fail where the answer itself fails.
- Independent verification is arithmetic and lookups: recompute derived values, cross-check totals against source records, enforce domain range rules, send violations to human review. Provenance is a field: source type, excerpt, timestamp, verification state. Mark conflicts between credible sources, because averaging invents a number nobody reported.

**ELI5.** A neat label does not prove what is in the box. Check what arrives, keep a shelf for odd ones, and open the box yourself.

## Endnotes for this chapter

1. Structured outputs constrain Claude's responses to follow a specific schema by compiling the JSON schema into a grammar used for constrained sampling, so that responses violating the schema cannot be generated; `output_config.format` with `type: "json_schema"` controls the response format and `strict: true` guarantees schema validation on tool names and inputs, and the two may be used independently or together in one request; the compiled schema is temporarily cached, so a first call on a new schema carries the compilation; when structured outputs are in use Claude automatically receives an additional system prompt explaining the expected output format; explicit limits apply to the number of strict tools, optional parameters and parameters using union types, with a `400` error reading "Schema is too complex for compilation" beyond them, and each optional parameter roughly doubles a portion of the grammar's state space, so the documented mitigations include reducing optional parameters and simplifying nested structures; schema compliance is not guaranteed on a refusal (`stop_reason: "refusal"`) or on reaching the token limit (`stop_reason: "max_tokens"`, for which the documented response is to retry with a higher `max_tokens`); enum and const capitalisation is not guaranteed, the response completes normally with no error and no special `stop_reason`, and the guidance is to compare enum values case-insensitively and avoid enum values differing only in capitalisation; several SDKs transform schemas by removing constraints such as `minimum`, `maximum`, `minLength` and `maxLength` and adding `additionalProperties: false`, so that Claude receives a simplified schema while your code still enforces all constraints through validation. Anthropic, *Structured outputs* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/structured-outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

2. Claude 4.6 and later models do not support prefilling assistant messages, and a request whose last assistant message is a prefill returns a `400` `invalid_request_error`; the documented alternatives are structured outputs on models that support them, system prompt instructions, or `output_config.format`. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

3. The Agent SDK accepts an `outputFormat` or `output_format` option of `type: "json_schema"` with a JSON Schema, validates the agent's output against that schema and re-prompts on a mismatch, and returns a result subtype of `error_max_structured_output_retries` when no valid output remains after the retry limit; a result can also end with subtype `success` and no `structured_output` value, for example when the run completes without the agent producing a structured output, and that case should also be treated as a failure. Anthropic, *Get structured output from agents* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/structured-outputs](https://code.claude.com/docs/en/agent-sdk/structured-outputs)

4. Every Messages API response includes a `stop_reason` field indicating why Claude stopped generating, and it should be checked in response handling to decide whether to use the response as-is, continue, retry, or fall back; a refusal is returned by safety classifiers as a normal HTTP `200` response with `stop_reason` of `refusal` rather than as an error, and a refused request on some models can usually be served by retrying on another Claude model; `stop_reason` values are distinct from errors, which indicate failures in processing the request. Anthropic, *Stop reasons and fallback* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)

5. The official SDKs raise typed exceptions rather than returning raw JSON, and the documented guidance is to catch the SDK's typed classes rather than string-matching error messages, handling the most specific classes first. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

6. Documented techniques for minimising hallucinations include best-of-N verification, running Claude through the same prompt multiple times and comparing outputs on the basis that inconsistencies across outputs could indicate hallucinations; chain-of-thought verification; iterative refinement; and external knowledge restriction, explicitly instructing Claude to use only information from provided documents rather than its general knowledge. Anthropic, *Reduce hallucinations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

7. Citations ground responses in supplied source documents and return the exact passages that support each claim, so the sources behind a response can be tracked and verified. Anthropic, *Citations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/citations](https://platform.claude.com/docs/en/build-with-claude/citations)
