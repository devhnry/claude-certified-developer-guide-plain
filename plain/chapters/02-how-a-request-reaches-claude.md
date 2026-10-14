# Chapter 2: Four Parts to Every Call, and Three Places It Breaks

**Summary**: *Each request to Claude has the same four parts. Each failure worth debugging happens in one of three gaps between them. Learn the gaps and many exam scenarios answer themselves. You will know which failures deserve a retry, which need repair before sending, and which come back looking healthy. Otherwise you lose an afternoon adding backoff to a broken request, or filing a network ticket about an answer the model gave on purpose.*

## Four Parts Go Out on Every Call, and the Fourth One Is a Contract

Picture mailing a parcel. You write an address, show ID, put something inside, and get a receipt back that you must read. That parcel is the analogy for this chapter: every call to Claude is a parcel through the post.

Write one call by hand, once, in a file you will delete. A library does this for you later, but a layer you never saw gets blamed wrongly.

Claude sits behind a **REST API** at `https://api.anthropic.com`. To send a message you use `POST /v1/messages`.<sup>[1]</sup> That is the address. Three headers go along, and all are required.<sup>[1]</sup>

- A credential: an `x-api-key` value, or an `Authorization` bearer token.
- An `anthropic-version` value, such as `2023-06-01`.
- `content-type: application/json`.

Next comes a JSON body, then the response, where most developers stop looking and the strange failures live.

Call this the **four-part call**: address, headers, body, response. The response needs interpreting, not just reading.

| Part | Carries | Failure looks like |
|---|---|---|
| Address | Where it goes and how | A `404`, though the path looks fine |
| Headers | Who you are, which API version, what format | `401` or `403`, identical each time |
| Body | Your JSON | A `400`, or a `413` over 32 MB |
| Response | Status, headers and a JSON body | No sign at all, until a later step breaks |

Look at the last row. "Delivered" does not say what is inside. The **status code** is like that. It says whether the exchange finished. The body tells you what arrived. Those are two questions, and code that checks one while assuming the other is the commonest bug here.

**ELI5.** Calling Claude is like mailing a parcel. You need an address, proof of who you are, a thing inside, and a receipt. "Delivered" does not mean the right toy is in the box.

## The Client Library Is Somebody Else's Maintained Copy of That Boilerplate

Anthropic ships official clients in seven languages: Python, TypeScript, C#, Go, Java, PHP and Ruby. There is also an `ant` command-line tool for scripts and hands-on use.<sup>[2]</sup> A client sends the required headers itself, so nobody has to remember the version pin or credential.<sup>[1]</sup>

Think of the library as a clerk who fills in your forms. It uses the same endpoint and model as a handwritten call, so answers are no better. What moves is who owns the dull jobs:

- Errors are typed exceptions, not raw JSON. The docs say to catch the classes, most specific first, not match message text.<sup>[3]</sup>
- Retries are built in.
- Paged lists come with an iterator that walks the cursor for you.<sup>[1]</sup>
- Non-streaming messages are checked against a ten-minute ceiling before sending, and TCP keep-alive helps an idle path survive mid-call.<sup>[3]</sup>
- Each `request-id` is a readable property, not buried in headers.<sup>[3]</sup>

None of that is hard. It is upkeep, and it falls on whoever wrote the client.

Three anti-patterns follow. Each skips the clerk.

The first is the hand-rolled client. It tempts because version one works. Pick any HTTP library, type three headers, send JSON, and you are done in twenty minutes. You have built a private fork of a library nobody wanted, and you now follow every API change by hand.

The second is a foreign client plus a translation shim. It usually arrives as "portability". Anthropic does publish libraries that expose Claude through another framework, including one shaped like the OpenAI SDK, and says they are not general-purpose Messages API clients.<sup>[2]</sup> A shim adds a second API's rules and one more layer to debug, for a provider switch nobody has scheduled.

The third is the subprocess call. That tool is for scripts and hands-on use.<sup>[2]</sup> A service that launches it for each request gives up typed errors and connection reuse, and starts a new process every time.

**ELI5.** A client library is a clerk who fills in the post-office forms for you. You could do it yourself, but then you must keep up when the rules change.

## Retries Default to Two Attempts, and Two Is a Setting Rather Than a Law

Suppose the delivery truck breaks down. Your parcel is fine. Official clients retry transient failures with exponential backoff, which means waiting longer after each try. The default is twice. They obey a `retry-after` header when the service sends one. Every client has a maximum-retries option that adjusts the count or switches retrying off.<sup>[3]</sup> The list of retried failures is fixed: any connection error, `408`, `409`, `429`, and every code from 500 up.<sup>[4]</sup>

A default exists, and you can change it. Scenarios turn on one half.

| What someone says | Verdict |
|---|---|
| Nothing happens unless your code retries | Wrong. A default policy runs |
| It runs but is locked | Wrong. You can set the maximum, even to zero |
| Only network faults retry | Wrong. Throttling retries too, and it is the common case |
| A default exists and a setting changes it | Right, the only fit for a client library |

Tell your teammate this: a policy is running whether or not anyone picked it. A team on a tight latency budget can turn it down, or off, in one line.

The anti-pattern is a retry loop around a retry loop. Wrap three of your own attempts around the default of two and you make nine trips to a service that wanted you to slow down. Nobody plans this. The outer loop's author did not know the inner one existed. It is two clerks re-sending the same parcel.

Two traps live close by.

- A timeout over the whole request lifecycle does not restart on a retry.<sup>[4]</sup> A generous deadline can expire just before a retry would have worked.
- Some `429` errors will not clear. A usage tier's spend cap raises one with no `retry-after` header, and it fails until access returns.<sup>[3]</sup> Retrying without a limit turns a billing problem into an outage.

**ELI5.** When the mail truck breaks down, the post office tries again on its own, twice. You can ask for more or fewer. If you also keep re-sending the parcel, it goes out again and again.

## Persistent and Two-Way Are Separate Properties, and Only One Needs a WebSocket

Compare a phone call with a mailbox. At the words "real time", teams grab a **websocket**. That is the wrong cue. Two separate properties pick the shape: how long the link lasts, and how many directions carry messages nobody requested.

| Shape | Sends unprompted | Cost | Fits |
|---|---|---|---|
| Request and response | Neither side | New connection each time | A single question |
| Repeated polling | Neither side | Many requests, data as old as the interval | Cheap checks on slow data |
| Held-open one-way response | Server only | Connection busy until the reply ends | Text appearing in pieces for a waiting person |
| WebSocket | Both sides | Keep-alive, reconnecting and monitoring | Long exchange with pushes both ways |

Read down the first column. News arrives the moment it happens, from the other side, unrequested. Replies use the same connection. The link lasts minutes or hours, not milliseconds. A websocket exists for that mix, and each substitute brings back what it removed.

Polling slips in unnoticed. It is walking to the mailbox every five minutes. A shorter interval buys freshness with extra requests, and never reaches zero, so data is always as old as the gap between checks. Polling relabelled as real time is the anti-pattern. The tell is a plan that improves when a number shrinks.

The other substitute is subtler. A held-open HTTP response moves data in one direction only. Claude's own streaming works this way, through **server-sent events**.<sup>[5]</sup> Chapter 3 covers reading one. It suits output arriving bit by bit. But it is no channel. To reply you open a new request, the very cost a persistent connection removes. Name this too: a held-open response treated as a two-way channel.

Anthropic uses it where both properties apply. An MCP tunnel joins Claude to servers inside a private network over an outbound-only connection, so no inbound firewall port opens and nothing faces the public.<sup>[6]</sup> The encrypted handshake with the customer's proxy is carried within the tunnel's WebSocket stream.<sup>[7]</sup> Which end opened the connection and which end sends over it are different facts. Mix them up and a security review asks for a firewall change nobody needs.

**ELI5.** A phone call stays open and either person can speak. A mailbox needs you to keep walking over. A radio lets only one side talk.

## Three Seams, and Only the Middle One Deserves Another Attempt

Back to the parcel. The label can be wrong, the truck can break, or it can arrive with the wrong thing inside. A failure in the four-part call lands in one of three seams. Naming the seam first is the main debugging skill, because each seam needs its own fix and gets worse under a neighbour's fix.

| Seam | Looks like | Fix | Makes it worse |
|---|---|---|---|
| Integration | `400`, `401`, `403`, `404`, 413; repeats identically<sup>[3]</sup> | Correct the request, key or size | Backoff, paying again for one answer |
| Transport | Connection faults, `429`, `500`, 529; intermittent, heavier under load<sup>[3]</sup> | Capped retries with backoff, respecting `retry-after` | A faster loop, or no cap |
| Output | `200` OK, but the content is no use | Validation, a schema, a fallback model | Trusting the status code |

The **integration seam** is the wrong label on the parcel. It is wholly the caller's. Nothing varies. A request that failed in testing fails at three in the morning too. A request over the 32 MB limit gets a `413` and will not pass on try four.<sup>[3]</sup>

The **transport seam** is the broken truck. The library's retry policy exists for this. Only here is another attempt reasoned, not hopeful. A `529` says the service is temporarily overloaded. For a `500`, the docs say to retry with exponential backoff.<sup>[3]</sup>

The **output seam** is the wrong thing in the box. It hurts most because everything earlier worked. When Claude refuses, you still get a successful `200`, with `stop_reason` set to `refusal`. Usually you send the same request to another model.<sup>[8]</sup> Streaming makes it sharper. An error can occur after the API already returned a `200`, so it never reaches the usual error path.<sup>[3]</sup> In a log, a refusal looks like an answer unless your code marked which was which.

One free habit finishes this. Every response has a `request-id`, the tracking number on the parcel. Support asks for it because it is the only handle that points at one call.<sup>[1]</sup> Log it on failure, and your report stops being a story about a bad afternoon.

**ELI5.** A parcel can fail three ways. The address is wrong, so resending never helps. The truck broke, so trying again can work. Or it holds the wrong thing, and you only learn by opening it.

## Eleven Documented Codes, and the Seam Each One Belongs To

Take the seam into the exam. The codes are a lookup, and a half-remembered one is worse than none. It puts a code in the wrong seam with full confidence, then applies the wrong fix.<sup>[3]</sup>

Seven codes mean your request, credential or account is wrong. Retrying fixes none.

| Code | Error type | Meaning |
|:----|:------------------|:--------------------------|
| `400` | `invalid_request_error` | Bad format or content; also the home of unlisted 4XX codes |
| `401` | `authentication_error` | Key is broken, revoked or out of date |
| `402` | `billing_error` | Payment details need a look |
| `403` | `permission_error` | Valid key, wrong permissions |
| `404` | `not_found_error` | No such path, or no such id in the URL |
| `409` | `conflict_error` | Writes collided, or a unique value is taken |
| `413` | `request_too_large` | Bigger than the endpoint allows |

Four codes blame the service or your call rate. Waiting is part of each fix.

| Code | Error type | Meaning |
|:----|:------------------|:--------------------------|
| `429` | `rate_limit_error` | Rate limit, monthly cap or workspace spend limit |
| `500` | `api_error` | Anthropic's own systems failed |
| `504` | `timeout_error` | Processing took too long |
| `529` | `overloaded_error` | Service briefly swamped |

Three of the eleven deserve a second look.

First, `400`. It is a catch-all, not a diagnosis. It takes 4XX codes that have no entry of their own. Your own organisation or workspace spend limit returns one, except on a Claude Code workspace, which can return `429`.<sup>[3]</sup> So a `400` does not prove a malformed body.

Second, `401`, `402` and `403`. Each says the caller cannot continue, for three unrelated reasons: a bad key, an unpaid account, or a good key missing this one permission. That is three repairs. A retry is not one of them.

Third, `409`, the odd one in the first table. The client retries `409` by default, along with connection errors, `408`, `429` and `500` or above.<sup>[4]</sup> That seems to clash until you see what a conflict is: something another writer may already have let go. Retrying is the documented fix.<sup>[3]</sup> The rest of that table fails identically forever.

**ELI5.** Each code is a stamp on your parcel. Most say "you made a mistake, fix it first". A few say "we are busy, try later".

## How Wrong Answers Are Built on This Material

Wrong answers here are seldom impossible. They are real techniques applied one seam over. Three assumptions cause most.

- A library is missing or fixed. Choices split into "your code must do it" and "the library does it and you cannot change it". Both miss the truth: a documented default with a setting. For transient failures, the surviving answer says a default runs and can be configured.
- Freshness paid for with request volume, sold as a connection. Asking again and again is offered where you need to be told. It suits slow data. It is wrong when the other end knows first, because delay stays stuck at whatever interval someone chose.
- A status code read as a ruling on the content. Options calling `200` success and all else failure skip a whole seam. Scenarios punish this when a pipeline breaks after a call that never errored.
- A heavier integration chosen over the maintained one. A general HTTP client, another provider's library or a shell-out can pass for good judgement. Ask what you now follow by hand when the API changes.

Match on what the scenario does, whatever domain it is set in.

| Scenario says | Usual answer | Usual trap |
|---|---|---|
| Server pushes updates and the app talks back | A protocol for a lasting two-way link | Anything where freshness depends on how often you ask |
| Teammate asks if app code needs its own retries | A default policy exists, exposed as a setting | Calling it missing, or fixed |
| A new integration, in a language with an official client | Use that client the documented way | Redoing headers, retries and parsing on plain HTTP |
| A call fails identically each time | Request, credential or size is wrong, and it is yours | Backoff on a failure that never changes |
| Failures are patchy and worsen with load | Capped backoff retries that respect the stated wait | A tighter loop, or retrying a spend cap forever |
| No error, but a later step failed | Inspect the body and stop reason, then validate | Trusting a good status code as a good answer |
| A status code arrives and an option sorts it by number alone | Ask if a later try could change the result, then fix the seam that owns it | `400` as proof of a bad body, or `409` as unfixable by retrying |
| Provider portability is the stated reason | Weigh the extra layer against an unscheduled switch | A foreign client plus a translation shim |

Name the seam before the fix. Say aloud whether the failure was in what you sent, in getting it there, or in what came back. About half the options stop looking plausible.

**ELI5.** A wrong test answer is often a good fix for a different problem, like repairing the truck when the label is wrong. Ask which failure you have first.

## What to Remember

- The **four-part call**: address, headers, body, response. Headers hold a credential, `anthropic-version` and content type. The reply has a status code, headers and a body to read separately.
- Official clients cover seven languages and send the required headers. Only the upkeep changes hands.
- Clients retry transient failures twice by default, with exponential backoff, obeying `retry-after`. Maximum retries can go up, down or to zero.
- Retried by default: connection errors, `408`, `409`, `429`, and `500` or above. Loops stacked on the client's multiply attempts. An outer deadline does not restart.
- A spend-cap `429` has no `retry-after`. Retrying forever causes an outage.
- Eleven codes: `400` invalid request, `401` authentication, `402` billing, `403` permission, `404` not found, `409` conflict, `413` too large, `429` rate limit, `500` internal, `504` timeout, `529` overloaded. Only `409` looks like an integration failure yet is retried, because the conflict can clear.
- Persistent and two-way are separate. Polling pins staleness to the interval. A held-open response is one-way. A websocket lets both ends send unprompted.
- Three seams: integration (4xx, identical each time, yours), transport (connection faults and 5xx, retry with backoff), output (`200` with unusable content, fix with validation or another model).
- A refusal is a successful `200` with `stop_reason: refusal`, and a streamed error can follow a `200`. Status-code-only handling misses a whole seam.
- Every response has a `request-id`. Log it on failure.

## Endnotes for this chapter

1. The Claude API is a RESTful API at `https://api.anthropic.com`; all requests must include a credential header (`x-api-key` or `Authorization`), an `anthropic-version` header such as `2023-06-01`, and `content-type: application/json`, which the client SDKs send automatically. The page also documents the `request-id` response header and the auto-paginating iterators the SDKs provide. Anthropic, *API overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/overview](https://platform.claude.com/docs/en/api/overview)

2. Anthropic publishes an `ant` command-line tool for shell scripting and interactive use, client SDKs in seven languages, and framework-specific libraries which expose Claude through another framework's API surface and are not general-purpose Messages API clients. Anthropic, *CLI, SDKs, and libraries* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/cli-sdks-libraries/overview](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)

3. HTTP status codes and their error types, the 32 MB request size limit, the instruction to retry a `500` with exponential backoff, the note that a spend-cap `429` carries no `retry-after` header, the default of two automatic retries with exponential backoff and a configurable maximum-retries option, typed SDK exceptions, the ten-minute validation and TCP keep-alive behaviour, the `request-id` header, and the fact that an error can occur after a streaming response has already returned a 200. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

4. The set of errors retried by default is all connection errors, `408` Request Timeout, `409` Conflict, `429` Rate Limit and `500` or above, with a default of two retries configurable through the client's maximum-retries option; a retried request does not restart a context timeout set for the request lifecycle. Anthropic, *Go SDK* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go)

5. Setting `"stream": true` on a message returns the response incrementally using server-sent events. Anthropic, *Streaming messages* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)

6. MCP tunnels connect Claude to MCP servers running inside a private network over an outbound-only connection, removing the need to open inbound firewall ports or expose services to the public internet. Anthropic, *MCP tunnels* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview)

7. The inner TLS handshake between Anthropic's backend and the customer's proxy is carried inside the tunnel's plaintext WebSocket stream, and the term "outbound-only" describes the connection rather than the requests carried over it. Anthropic, *Architecture and components* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/concepts](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/concepts)

8. A refusal is a successful HTTP `200` response carrying `stop_reason: "refusal"` rather than an error, and the same request can usually be sent to another Claude model to get an answer. Anthropic, *Refusals and fallback* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
