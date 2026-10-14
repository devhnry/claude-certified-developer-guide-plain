# Chapter 3: Messages, Streaming, Batches: Who Is Waiting Decides

**Summary**: *The same model, prompt and document can belong on three different endpoints. What separates them is who is stuck waiting for the answer. Get that wrong and you pay full price for work nobody watched. Or a person stares at a blank panel while a good answer builds out of sight. This chapter walks the API from one message up to forty thousand, always asking that one question.*

## Who Is Waiting Is Established Before Anything Else and Changed Last

Picture a restaurant kitchen. That is our one analogy for the chapter. Three orders arrive for the same dish, made the same way.

One is from a diner at a table, watching the kitchen door. One is from a customer on the phone who needs a reply within **two seconds**. The third is order 8,431 in a catering job for forty thousand meals. Its only deadline is a delivery at eight the next morning.

Call the person who is waiting the **waiting party**: whoever's clock the request runs on. It might be a human watching a screen (the diner). It might be a caller blocked until a value comes back (the phone customer). It might be nobody until a deadline hours away (the catering job). Settle this early. Endpoint, error handling, cost and interface all follow from it. Settle it late and you rebuild all four.

| Who waits | Use | Gain | Price |
|---|---|---|---|
| A person watching the screen | Streamed message | First words in under a second | You handle events and stitch pieces together |
| A caller blocked on the result | One plain message request | One finished object, easy to parse | The caller sits through the whole generation |
| A caller busy with other work | Many plain requests at once | Throughput with no queue | You run into your own rate limits |
| Nobody until a deadline hours off | A batch | Half the token price, high throughput | Hours of wait, not seconds |

Compare rows three and four. People call both "asynchronous", but they solve different problems. Row three is several cooks working at once. Your program stays busy while requests are in flight, and each answer still arrives at normal speed. Row four (a batch) gives up that speed completely and takes a discount in return.

**ELI5.** Some people eat at the table and want food now. Some will wait if it costs less. Before you cook, ask who is waiting and for how long.

## One Message Request Is a Model, a Cap, and a List of Turns

A request has three parts. A model name. A limit on reply length. And `messages`, a list of turns, each with a `role` and a `content` array. Standing instructions skip the turns and go in their own top-level `system` field.<sup>[1]</sup>

Content is not a string. It is a list of typed blocks. So one endpoint can carry text, images, documents, tool calls and reasoning, and a new kind of content only needs a new block type. A reply comes back the same way, holding an `id`, `role: "assistant"`, the blocks, a **`stop_reason`**, and a `usage` object that counts tokens in and out.<sup>[1]</sup>

```
POST /v1/messages
{
  "model":      "<model id>",
  "max_tokens": <ceiling on the response>,
  "system":     "<standing instructions, optional>",
  "messages":   [ { "role": "user", "content": [ <blocks> ] } ]
}
```

Now the fact that shapes everything after it. The Messages API is **stateless**. It remembers nothing, so every call carries the full history.<sup>[1]</sup> There is no conversation ID. A chat is a list you keep. Add Claude's reply, add the next user turn, send it all again.

Two things follow.

First, you can write the "assistant" turns yourself. That is a documented technique. You can even begin Claude's answer: end the list with partial assistant text and Claude carries on from it (prefill).<sup>[1]</sup> Chapter 5 covers that.

Second, you pay for the history. Every old turn is billed as input again. So question ten costs more than question one, though both are the same length. Chapter 7 covers a full window. Chapter 8 covers the maths.

One more detail on `system`, because it exists for caching. On newer models, a `"role": "system"` message may come after a user turn and carries equal authority. It cannot open the list. Since it lands at the end, a cached prefix stays intact.<sup>[1]</sup>

**ELI5.** Claude forgets you as soon as it answers. So each time, you hand it the whole notebook of what was said. A longer notebook costs more to read.

## A Tool Result Is Paired by Identifier, Not by Position or by Narration

In the kitchen, every order has a ticket number. The number says which dish belongs to which order. Tool calls work the same way. Claude asks, you run something, and the answer must match the question. Only one side reads English, so a number does the matching.

Here is the flow. Claude stops with **`stop_reason: "tool_use"`**. It sends one or more `tool_use` blocks, each with an `id`, a `name`, and an `input` object that matches the tool's schema. You run the tool. Then you send a fresh user turn made of `tool_result` blocks. Each repeats the `tool_use_id` (the ticket number) of its call. The output goes in `content`. If the tool failed, set `is_error`.<sup>[2]</sup>

Three rules come with this. Each has teeth.

- Put only result blocks in that message. If you add your own sentence after them, the assistant turn ends and the request may fail.
- Keep the `tools` array identical on the follow-up.
- If the reply had a thinking block, send the assistant content back exactly as it came, signature included. That keeps the reasoning tied to its call.<sup>[3]</sup>

Extra input for Claude waits for its own user message once the turn has closed.<sup>[2]</sup>

Two anti-patterns live here. Both pass a quick code review.

The first is **the result written as prose**. You turn the output into a sentence and send it as a normal user message. A person reads it fine. But the ticket number is gone. With two tools running, nothing says which answer is for which call.

The second is **the result filed in the assistant turn**. The thinking: Claude asked, so it is Claude's. But the assistant turn records what Claude wrote. Putting outside content there falsely claims Claude produced it. It also leaves the original `tool_use` block unanswered.

How tools are described and chosen is Chapter 9. Here we only wire them up.

**ELI5.** Each question gets a numbered ticket. The answer must carry the same number, or nobody knows which question it answers.

## `stop_reason` Says What You Owe the Caller Next

Every successful reply carries a `stop_reason`. It says whether you hold a finished message or a piece of one.<sup>[4]</sup> Think of the kitchen calling out the state of the plate. Group the values by the duty each one creates, because that is what the exam asks.

| Duty | Values | What you do |
|---|---|---|
| None, the answer is whole | `end_turn`, `stop_sequence` | Use it. With `stop_sequence`, check which sequence fired |
| Send a follow-up | `tool_use`, `pause_turn` | `tool_use`: reply with `tool_result` blocks. `pause_turn`: resend the response as it stands so the server-side loop resumes |
| Flag a cut-off answer | `max_tokens`, `model_context_window_exceeded` | Mark it incomplete, or deliberately keep generating |
| Go to another model | `refusal` | Retry on a different Claude model. `stop_details` gives the policy category |

That is seven values and four duties. Two need a closer look.

`pause_turn` and `tool_use` both mean "not done yet". You continue them differently, and that is the trap. With `pause_turn`, the server-side loop hit its iteration limit while running platform tools. You send Claude's own reply back, unchanged. With `tool_use`, Claude is waiting on you. You send your results.<sup>[4]</sup>

A **`refusal`** never looks like trouble. A safety classifier sets it, and it comes back as a normal HTTP `200`. The documented answer is to send the same request to another Claude model.<sup>[4]</sup> Chapter 2 warned that a healthy status code can hide a bad body. This field is where you catch it.

Judging a reply by its status code is the anti-pattern. Reading `stop_reason` is the cure. A pipeline that checks only for `200` forwards truncated documents, open tool calls and refusals. In a log they all look like short answers.

**ELI5.** When Claude stops, it leaves a note saying why. Maybe it finished, ran out of room, or needs something from you. Read the note. A plain "OK" does not say.

## Streaming Changes When the Words Appear, Not What They Cost

Think of a diner served course by course. Set **`"stream": true`** and the reply arrives in pieces over **server-sent events**.<sup>[5]</sup> Each event has a type name and a JSON payload. The order is steady, so you can write a state machine for it.

The order is fixed. First `message_start`, with an empty shell. Then each content block opens (`content_block_start`), fills (`content_block_delta` events) and closes (`content_block_stop`). Changes to the whole message come in `message_delta`. The last event is `message_stop`. `ping` keep-alives can show up anywhere.<sup>[5]</sup>

Three facts matter more than the names.

1. `stop_reason` is `null` in `message_start`. It arrives later, in a `message_delta`.<sup>[4]</sup> Code that reads the first event and moves on read it too early.
2. Errors travel inside the stream. Under heavy load, an `overloaded_error` can arrive as an `error` event on a connection that already returned HTTP `200`. A non-streamed request would have failed with a 529.<sup>[5]</sup> A consumer that handles only text deltas will think the answer was just short.
3. New event types may be added under the versioning policy. Skip types you do not know. Do not crash.<sup>[5]</sup>

Streaming has a second use with no viewer at all. The SDKs can stream under the hood and still give you one complete message. They require it for a large `max_tokens`, because a single long, non-streamed call hits HTTP timeouts.<sup>[5]</sup> That is about transport, not display.

The named anti-pattern is **streaming adopted as a throughput fix**. Words appear sooner, but total generation time does not shrink and the token cost stays put. A backend job that waits for the full message just gains extra event code. Streaming meets one need: a human is watching.

**ELI5.** Streaming is getting the meal course by course. Same time, same cost. It just feels faster because you see food sooner.

## Images and Documents Arrive as Blocks, With Three Ways to Name the Bytes

Say Claude must read a photo of a receipt. There is no separate vision endpoint. You put an `image` block in the user turn, next to your text. You point at the picture in one of three ways: inline `base64`, a `url` to a hosted image, or a `file_id` from the Files API. Formats are JPEG, PNG, GIF and WebP. Nothing larger than 8000 by 8000 pixels is allowed.<sup>[6]</sup>

Several images in one request are read together, which is how page-by-page document work happens. Label each one in your text. In a multi-turn chat, Claude keeps earlier images, so a follow-up about the first two needs no resend.<sup>[6]</sup>

This next limit is easy to trip and hard to spot. Past 20 image blocks in a request, a tighter per-image size rule applies to every image in it. That counts images resent from earlier turns and images inside tool results. Blocks over the limit are rejected with a validation error, not shrunk.<sup>[6]</sup>

PDFs use `document` blocks and the same three routes. Each page is read as text and also turned into an image, so a PDF is billed both ways.<sup>[7]</sup> The page count sets the total. File size does not. Both the size limit and the page limit cover the whole request payload, not only the document.<sup>[7]</sup>

This is where the **Files API** helps. Upload once, get a `file_id`, then use that ID in later requests instead of encoding the content again.<sup>[8]</sup> It fixes base64 resent every turn, which you only notice when a chat about one scanned contract sends the whole contract each time.

Check availability first. The Files API is on the first-party API, and in beta on some cloud paths but not all.<sup>[9]</sup>

**ELI5.** A picture or PDF is just another piece of the message. If you keep showing the same big one, upload it once and say "that one" afterwards.

## Batches Take Half the Price and Hand Back the Correlation Problem

Back to the catering job. This is the **Message Batches API**, the last row of the first table. You submit everything together, and it runs asynchronously at 50% of standard prices. Most batches end in under an hour. Anything still open after 24 hours expires.<sup>[10]</sup>

There are four steps, and you own the last two.

```
create   POST a "requests" list; each entry is a custom_id plus a params
         object holding an ordinary Messages request
poll     the batch carries processing_status: in_progress, then ended
collect  fetch results_url; JSONL, one result object per line
match    join each line back to your work by its custom_id
```

Results come back in any order. So match them by `custom_id`, never by position.<sup>[10]</sup> This is the ticket number again. It is yours to pick: up to 64 letters, digits, hyphens or underscores. Use something your own system already understands, and matching is a join, not a guess.

Each result is one of four types, which matters for billing too. `succeeded` holds the message. The other three, `errored`, `canceled` and `expired`, cost nothing.<sup>[10]</sup> The batch's `request_counts` totals them. One failure leaves the rest alone.<sup>[10]</sup> Results stay available for 29 days from creation. You can cancel mid-flight. The batch still ends, and may hold partial results.<sup>[10]</sup>

A few Messages parameters are rejected in a batch, and each tells you something. `stream` fails because results arrive as a file. Fast mode fails because it speeds up synchronous calls, and a batch has none. Thread parameters fail because a batch request belongs to no thread.<sup>[10]</sup>

Prompt caching stacks with the batch discount. But batch requests run concurrently, so cache hits are best effort.<sup>[10]</sup> Treat that saving as a bonus, not a floor.

Two anti-patterns mirror each other.

**Batch chosen for latency.** This treats "asynchronous" as "faster". A batch returns no single answer sooner. If a caller is blocked on one answer, a batch only lengthens the wait for a tiny saving. The discount only matters at volume.

**A synchronous loop run at batch volume.** This is more common, and it is how an overnight job often starts. Tens of thousands of one-at-a-time calls hit your rate limits, tie up the process, and cost twice what a batch costs. Pick a batch when you have both: high volume, and no one cares when any single answer lands.

**ELI5.** A batch is like dropping off a huge pile of laundry. It costs half as much, but you collect it later and it comes back in no set order. So you write your name on each item.

## Third-Party Providers Keep the Message Shape and Change the Frame Around It

Say your company already pays for Bedrock, and security approved it. So Claude must be reached that way. The choices are **Amazon Bedrock**, **Google Cloud**, **Microsoft Foundry** and **Claude Platform on AWS**. The reasons are rarely technical: a contract, a signed-off security boundary, one billing relationship. The rule applies from the first call.

Most of what you use stays the same. Content blocks, `stop_reason`, tool use and streaming carry across. Anthropic's own client libraries support these platforms directly.<sup>[11]</sup> Bedrock uses the same Messages API shape, on AWS-managed servers inside the AWS security boundary.<sup>[12]</sup>

What changes is the frame. Sign-in comes from the platform, not an Anthropic key. So do endpoints and model identifiers. Billing goes through its marketplace, which is often why the rule exists.<sup>[13]</sup> On Google Cloud the request differs in two ways. The model is named in the endpoint URL, not the body. And `anthropic_version` moves into the body, with a platform-specific value.<sup>[11]</sup> Features vary as well. Something on the first-party API may be beta or missing on a platform. On Foundry it differs even between hosting options.<sup>[9]</sup>

There is one sound answer and two tempting wrong ones.

The sound answer is to use the required path from your first commit. Add a thin layer between your app and the provider, so what differs sits in one spot. Wrong answer one is the **deferred migration**: build on the direct API now, move later. Every request until then breaks the agreement, and the rework is certain. Wrong answer two is the **parallel implementation**. You keep two code paths for good, and the live one still breaks the contract.

**ELI5.** It is the same dish in a different restaurant. Same recipe, but a different door, a different cashier and different menu names. Use the right door from day one.

## How Wrong Answers Are Built on This Material

Wrong answers here are rarely invented. They name a real technique and aim it at a need it does not meet. Four habits cause most of them.

- **Asynchronous read as fast.** The option sells batching as a speed-up. Not blocking feels like speed, but it is not. A batch moves a lot of work, but any one answer is slower. It is right only when the volume is large and no clock sits on single results.
- **Wrong lever for delivery.** The need is about when output reaches someone. The option offers caching, a bigger token cap, a schema or a bigger model. Those change cost, length, shape or skill. None makes a finished answer arrive in pieces.
- **A matched pair swapped for a description.** Tool results sent as prose, under the wrong role, or without the identifier all lose the match the protocol needs. People can read them. The API cannot. Picture two open calls.
- **A non-technical rule put off until later.** Contract routing, data residency and billing come from outside engineering, so people treat them as schedulable. They bind from call one. Meeting the rule later means failing it on every request until then.

Read the scenario for what it needs, not for its industry.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| Thousands of items, no deadline on each, cost matters | Batch, then collect and join the results | A plain loop, or a bigger token cap called "throughput" |
| Users want to see text as it is written | Streaming | Caching, a larger cap, or a schema |
| A tool ran and Claude needs the output | A user turn of result blocks with the call's identifier | Prose, a result in the assistant turn, or standing instructions |
| An answer ended early and nobody knows why | Read `stop_reason`, do what it says | Taking HTTP `200` as proof the content is whole |
| A contract or compliance rule names a cloud | Use that path now, behind one provider seam | Build direct and migrate later, or keep both paths |
| The same big document goes out every turn | Upload once, refer by identifier | Re-encoding the bytes each time |
| Results came back in a different order | Join on the identifier you assigned | Assuming submission order |

One habit beats the table. Name the waiting party. Then ask whether the option works on delivery, cost, shape or capability. Most wrong answers are right answers to one of the other three.

**ELI5.** A wrong answer is often a good tool used for the wrong job, like fixing a slow waiter by buying a bigger oven. Ask who is waiting, then ask what the tool really changes.

## What to Remember

- The Messages API is stateless. Every call sends the whole history: a model, a `max_tokens` ceiling, a `messages` list of role-and-content turns, and standing instructions in the top-level `system` field, not in any turn.
- Content is a list of typed blocks, so one endpoint carries text, images, documents, tool calls and reasoning. A response returns blocks plus `stop_reason` plus a `usage` count.
- The waiting party (a person watching, a caller blocked on the reply, a caller doing other work, or nobody until a deadline) picks the endpoint before you write the prompt.
- Seven `stop_reason` values make four duties: nothing (`end_turn`, `stop_sequence`), send a continuation (`tool_use`, `pause_turn`), declare the answer incomplete (`max_tokens`, `model_context_window_exceeded`), retry elsewhere (`refusal`, which arrives as a normal HTTP `200`).
- A tool result is a user turn of `tool_result` blocks that echo the `tool_use_id`, with nothing else in that message, the same `tools` array, and any thinking block sent back as it came.
- Streaming sends the same message earlier over server-sent events: `message_start`, then block start, deltas and stop, then `message_delta`, then `message_stop`. `stop_reason` is null at the start and arrives in `message_delta`. An overload error can show up as an event after HTTP 200.
- Images and PDFs are content blocks named by inline base64, a URL, or a `file_id` from the Files API. Past 20 image blocks, a tighter dimension limit hits every image in the request, resent ones included.
- A PDF page is billed as text and as an image, because each page is rendered as well as read. Page count drives cost more than file size.
- Batches cost 50% of standard prices, mostly finish within an hour, and expire at 24 hours. Results come out of order, matched by the `custom_id` you assigned. `errored`, `canceled` and `expired` results are not billed.
- `stream` and fast mode are rejected inside a batch, because a batch returns a file and there is no synchronous latency left to tune.
- Non-blocking concurrency is not batching. Async clients keep your process busy and responses still arrive at conversational speed. A batch gives up that speed to buy the discount and the throughput.
- Third-party providers keep the message shape but change the frame: authentication, endpoints, model identifiers and billing become the platform's, and feature availability varies. On Google Cloud the model moves into the URL and `anthropic_version` moves into the body.

## Endnotes for this chapter

1. The Messages API request shape, the stateless requirement to resend full conversational history, synthetic assistant turns, prefilling the last assistant position, the top-level `system` field and the placement and caching behaviour of a mid-conversation system message, the response object with its `content` array, `stop_reason` and `usage`, and the three image source types. Anthropic, *Using the Messages API* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/working-with-messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)

2. A `tool_use` block carries `id`, `name` and `input`; the continuation is a user-role message containing `tool_result` blocks that each carry the `tool_use_id` of the call they answer, optional `content`, and an optional `is_error` flag; further input for Claude is sent as a separate user message after the turn completes. Anthropic, *Handle tool calls* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)

3. The assistant content array is sent back verbatim on the follow-up request so the thinking block, including its signature, stays unchanged alongside the `tool_use` block. Anthropic, *Thinking in tool and multi-turn workflows* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows](https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows)

4. The `stop_reason` values `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`, `refusal` and `model_context_window_exceeded`, their meanings and handling; the requirement that the continuation of a `tool_use` response contain only `tool_result` blocks and keep the same `tools` array; the instruction to continue a `pause_turn` by sending the response back as-is; refusals returning as HTTP `200` with a `stop_details` policy category and being retried on another Claude model; and `stop_reason` being null in `message_start` and delivered in `message_delta` when streaming. Anthropic, *Stop reasons and fallback* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)

5. Setting `"stream": true` returns the response incrementally over server-sent events; the event flow of `message_start`, `content_block_start`, `content_block_delta`, `content_block_stop`, `message_delta` and `message_stop`, with `ping` events interspersed; errors such as `overloaded_error` arriving inside the event stream where a non-streaming request would return HTTP `529`; the instruction to handle unknown event types gracefully; and the SDK facility that streams internally while returning a complete `Message`, which the SDKs require for requests with large `max_tokens` values to avoid HTTP timeouts. Anthropic, *Streaming messages* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)

6. Images are supplied as `image` content blocks using base64, url or file_id source types; supported media types are JPEG, PNG, GIF and WebP; maximum dimensions are 8000 by 8000 pixels; multiple images in one request are analysed jointly and earlier-turn images remain available in later turns; and a request containing more than 20 image blocks applies a stricter per-image dimension limit to every image block in the request, including resent images and images nested inside tool results, with oversized blocks rejected as an `invalid_request_error`. Anthropic, *Vision* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/vision](https://platform.claude.com/docs/en/build-with-claude/vision)

7. PDFs may be provided as a URL, as base64 in document content blocks, or by reference to a file uploaded through the Files API; token cost combines text extracted per page with image token costs because each page is converted into an image; and the size and page limits apply to the entire request payload rather than to the document alone. Anthropic, *PDF support* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/pdf-support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)

8. The Files API provides a create-once, use-many-times pattern: upload a file, receive a `file_id`, and reference that identifier in later Messages requests instead of re-uploading the content. Anthropic, *Files API* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/files](https://platform.claude.com/docs/en/build-with-claude/files)

9. Feature availability is listed per platform across the Claude API, Amazon Bedrock, Claude Platform on AWS, Google Cloud and Microsoft Foundry, with the Files API shown as available on the Claude API and in beta on some platforms; on Microsoft Foundry availability differs between the Hosted on Anthropic and Hosted on Azure options. Anthropic, *Features overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/overview](https://platform.claude.com/docs/en/build-with-claude/overview)

10. The Message Batches API processes large volumes of Messages requests asynchronously at 50% of standard prices, with most batches completing in under an hour and a 24-hour expiry; each request carries a `custom_id` matching `^[a-zA-Z0-9_-]{1,64}$` and a `params` object; `processing_status` moves from `in_progress` to `ended`; results are downloaded from `results_url` in JSONL form with order not guaranteed, so `custom_id` is used to match results to requests; the four result types are `succeeded`, `errored`, `canceled` and `expired`, and the last three are not billed; the failure of one request does not affect others; results remain available for 29 days after creation and a processing batch can be cancelled; `stream`, `speed`, thread parameters and routing hints are rejected in batch requests; and prompt caching stacks with the batch discount but cache hits are best-effort. Anthropic, *Batch processing* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/batch-processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

11. The API for Claude on Google Cloud's Agent Platform is nearly identical to the Messages API with two differences in request format: `model` is specified in the endpoint URL rather than the request body, and `anthropic_version` is passed in the body with a platform-specific value. Anthropic's official client SDKs support the platform. Anthropic, *Claude on Google Cloud* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)

12. Claude in Amazon Bedrock runs on AWS-managed infrastructure inside the AWS security boundary while using the same Messages API shape as Anthropic's first-party API, with AWS-native authentication paths. Anthropic, *Claude in Amazon Bedrock* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)

13. Accessing Claude in Microsoft Foundry bills Claude usage through the Azure Marketplace and manages cost through the Azure subscription, with resources holding security and billing configuration and deployments being the model instances called through the API. Anthropic, *Claude in Microsoft Foundry* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry)
