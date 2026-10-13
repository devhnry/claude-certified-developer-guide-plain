# Chapter 2: Four Parts to Every Call, and Three Places It Breaks

**Summary**: *Every request to Claude carries the same four parts. Every failure worth debugging sits in one of three seams (the gaps) between them. Keep the seams apart and a whole family of exam scenarios answers itself. Which failures deserve another attempt? Which need fixing before the call leaves the building? Which arrive with a perfectly healthy status code? Mix them up and you lose an afternoon adding backoff to a malformed request, or filing a network ticket about an answer the model gave on purpose.*

## Four Parts Go Out on Every Call, and the Fourth One Is a Contract

**First, the idea.** Calling Claude is like sending a parcel through the post and waiting for a reply. Every call has the same four parts. We will use that post office picture for the whole chapter.

**The four parts.** Claude is reached over a **REST API** (a web service you talk to with ordinary web requests) at `https://api.anthropic.com`. A message goes to **`POST /v1/messages`**.<sup>[1]</sup> That is the **address** (the street address on the parcel). Then come **three headers**, and none of them is optional. Headers are the labels on the outside of the envelope:
- a **credential**, which is either an **`x-api-key`** value or an **`Authorization` bearer token** (your ID at the counter)
- an **`anthropic-version`** value such as `2023-06-01` (which edition of the rules you are using)
- **`content-type: application/json`** (what language the letter is written in)<sup>[1]</sup>

Then comes the JSON **body** (the letter inside). Then comes the **response** (the reply that comes back). Developers stop paying attention to the reply, and that is where the interesting failures live.

I call this the **four-part call**: an **address**, **headers** that prove who you are and pin a version, a **body**, and a **response** you have to interpret instead of just reading.

**Why write it out by hand once.** Do it once in a scratch file nobody keeps. Not because it ships that way. Everything a client library does later is one of these four parts. A failure inside a part nobody has looked at gets blamed on the nearest part somebody has.

| Part | What it carries | What its failure looks like |
|---|---|---|
| Address (the street address) | Endpoint and HTTP method | A `404`, on a path that looks right |
| Headers (the labels and ID) | Credential, API version, content type | A `401` or a `403`, identical on every attempt |
| Body (the letter) | The JSON payload of the request | A `400`, or a `413` past 32 MB |
| Response (the reply) | Status code, headers, JSON body | Nothing at all, until something downstream falls over |

**The last row is the one to stare at.** A **status code** says whether the **exchange completed**. That is like the post office telling you the parcel was delivered. The **body** says what **came back**. That is what the reply letter actually says. These are two separate questions. Code that checks the first and assumes the second is the most common mistake on this material.

**ELI5.** Sending a message to Claude is like posting a letter. It needs an address, labels on the envelope, the letter itself, and a reply. A stamp saying "delivered" does not tell you what the reply says. You have to open the reply and read it.

## The Client Library Is Somebody Else's Maintained Copy of That Boilerplate

**First, the idea.** A **client library** is ready-made code that does the post office paperwork for you. You could do it by hand, but then you own the upkeep.

**What Anthropic publishes.** Anthropic publishes **official clients for seven languages**: Python, TypeScript, C#, Go, Java, PHP and Ruby. It also publishes an **`ant` command-line tool** for **shell scripting** and interactive use.<sup>[2]</sup> A client sends the required headers itself. So the version pin and the **credential** are no longer things anybody has to remember.<sup>[1]</sup>

**What stays the same.** The library and a hand-written HTTP call reach the **same endpoint and the same model**. The **answer does not get better**. What changes is **who owns the boring parts**. There are more of them than you would guess:
- Errors arrive as **typed exceptions** (named error classes) instead of raw JSON. The documentation says to **catch those classes** instead of matching on message text, **most specific class first**.<sup>[3]</sup>
- A **retry policy** is already there.
- List endpoints come with an **iterator that follows the page cursor**.<sup>[1]</sup>
- Non-streaming message requests are checked against a **ten-minute ceiling** before they are sent. The socket is set up with **TCP keep-alive**, so an idle network path is less likely to drop under the call.<sup>[3]</sup>
- The **`request-id`** on every response is exposed as a property, not buried in a pile of headers.<sup>[3]</sup>

None of that is hard. All of it is **maintenance**, and the cost lands on whoever wrote the code.

**Three anti-patterns (things that look smart and are not).**
- **The hand-rolled client.** It is tempting because the first version works. A **general HTTP library**, three headers typed out, a JSON body, done in twenty minutes. What you built is a **private fork** of a library nobody wanted to own. Now you have to **track the API by hand**, forever, at whatever priority that work gets.
- **The foreign client plus a translation shim.** It usually shows up dressed as portability. Anthropic does publish libraries that expose Claude through another framework's surface, including a path that speaks the OpenAI SDK's shape. It says plainly that these are not **general-purpose Messages API clients**.<sup>[2]</sup> A shim gives you a second API's rules and **one more layer to debug through**. In return you get a provider switch nobody has scheduled.
- **The subprocess call.** The command-line tool is documented for **shell scripting and interactive use**.<sup>[2]</sup> A service that runs it once per request gives up **typed errors and connection reuse**. It pays for a process boundary on every call instead.

**ELI5.** A client library is a helper who fills in the post office forms for you and keeps up with changes to them. You could fill them in yourself. But then every change is your problem, and the parcel gets no faster.

## Retries Default to Two Attempts, and Two Is a Setting Rather Than a Law

**First, the idea.** When a call fails for a reason that has nothing to do with your request, the official clients try again on their own. That is a **retry**. How many times is a setting you can change.

**What the clients do.** The official clients **retry transient failures** (failures that may pass on their own) with **exponential backoff** (waiting longer after each failed try). The default is **two retries**. They honour a **`retry-after` header** when the service sends one. Every client has a **maximum-retries option** that **adjusts or switches off** this behaviour.<sup>[3]</sup> The retried set is named too: **connection errors of any kind**, `408`, `409`, `429`, and anything at or above 500.<sup>[4]</sup> In the post office picture, this is the delivery van going back out after a breakdown.

Both halves of that sentence matter. Exam scenarios almost always turn on one of them.

| Claim about the library's retries | Verdict |
|---|---|
| Nothing happens unless application code does it | Wrong. A default policy ships and runs |
| Something happens and nothing can change it | Wrong. Maximum retries is a client option, and zero disables it |
| Connection faults retry, throttling passes through | Wrong. Throttling is in the retried set, and it is the common case |
| A default exists and a setting adjusts it | Correct, and the only description that fits a client library |

What to tell a teammate sits between the two obvious answers. A **policy is already running**, whether or not anybody chose it. A team on a **tight latency budget** can **turn it down** or off in one line.

**Anti-pattern: a retry loop wrapped around a retry loop.** This is plain arithmetic. Three attempts of your own around a default of two gives **nine trips** to a service that has already asked for a pause. Nobody writes that on purpose. It happens because the person who wrote the outer loop assumed the inner one did not exist.

**Two more traps nearby.**
- A **timeout set across a whole request lifecycle** does not **restart** when the library retries.<sup>[4]</sup> So a generous outer deadline can run out in the middle of a retry that was about to work.
- Not every `429` is temporary. One raised by a **usage tier's spend cap** carries no **`retry-after` header**. It keeps failing until access is restored.<sup>[3]</sup> So an **unbounded retry loop** against it turns a **billing problem into an outage**.

**ELI5.** If the delivery van breaks down, the post office sends it out again by itself, two more times. You can ask for more tries or none. Do not hire your own extra vans on top, because then the same parcel gets sent nine times. And if the account is out of money, trying again forever never helps.

## Persistent and Two-Way Are Separate Properties, and Only One Needs a WebSocket

**First, the idea.** People say "real time" and reach for a **websocket** (a connection that stays open and lets both sides send at any time). That is the wrong trigger. Two separate properties decide the shape. How long does the relationship last? And can both sides send messages that nobody asked for?

In post office terms, a normal call is one letter and one reply. A websocket is a standing phone line that either end can speak into.

| Shape | Who can send unprompted | What it costs | When it fits |
|---|---|---|---|
| Request and response | Neither end | One connection setup per exchange | A question with one answer |
| Repeated polling | Neither end | Request volume, and staleness bounded by the interval | Cheap checks on something that changes slowly |
| Held-open one-way response | Server only | A connection tied up for the length of the response | Output arriving in pieces while a human waits |
| WebSocket | Both ends | A connection to keep alive, reconnect and monitor | A long-lived exchange where both ends push |

**When a websocket fits.** Read down the first column. Updates arrive as they happen, from the other end, without being asked. Messages go back over the same connection. The relationship lasts minutes or hours, not milliseconds. That mix is what a websocket was built for. Every substitute brings back something the websocket was meant to remove.

**Polling (the substitute people accept without noticing).** Polling means asking again and again, like walking to the post office every five minutes to ask "anything for me?" A shorter interval buys **freshness with request volume**. The interval never reaches zero, so the data is always as old as the gap between checks. **Polling relabelled as real time** is the anti-pattern. The tell in a scenario is a fix that gets better when a **number gets smaller**.

**The held-open response (the subtler substitute).** An ordinary **HTTP response held open** carries **data one way**, from the server to you. Claude's own streaming works exactly like this, over **server-sent events**.<sup>[5]</sup> Chapter 3 covers what that means for reading a message. It is the right shape for **output arriving piece by piece**. It is not a two-way channel. Your only way to say anything back is to **open a fresh request**, which is the cost a persistent connection was meant to remove. So treating a held-open response as a two-way channel is worth naming as a mistake.

**Where Anthropic uses the real thing.** An **MCP tunnel** connects Claude to servers inside a **private network** over an **outbound-only connection**. So no **inbound firewall port** has to be opened and nothing is exposed to the public internet.<sup>[6]</sup> The encrypted handshake to the customer's proxy is then carried inside that **tunnel's WebSocket stream**.<sup>[7]</sup> Which **end opened the connection** and which end sends over it are two different facts. Mixing them up is how a security review ends up asking for a **firewall change nobody needs**.

**ELI5.** Asking "anything for me?" over and over is polling. It is always a little out of date. A phone line that stays open lets either side speak the moment something happens. Only use the phone line when both sides really need to speak first.

## Three Seams, and Only the Middle One Deserves Another Attempt

**First, the idea.** A **seam** is a place where one part hands off to the next. In the post office picture, a parcel can go wrong at the counter, on the road, or in the reply. Every failure in the four-part call lands in one of **three seams**. **Naming the seam first** is the whole diagnostic skill. Each seam has its own fix, and each gets worse under the fix that belongs to its neighbour.

| Seam | How it announces itself | What repairs it | What makes it worse |
|---|---|---|---|
| Integration (the counter) | `400`, `401`, `403`, `404`, 413. Identical on every attempt<sup>[3]</sup> | Fix the request, the credential or the size | Backoff, which pays repeatedly for the same answer |
| Transport (the road) | Connection faults, `429`, `500`, 529. Intermittent, clustering under load<sup>[3]</sup> | Bounded retries with backoff, honouring `retry-after` | A tighter loop, and no ceiling on attempts |
| Output (the reply) | HTTP `200`, and the content is unusable | Validation, a schema, a fallback model | Reading the status code and stopping there |

**The integration seam (the counter).** This seam belongs **entirely to the caller**. Its signature is **determinism**: the same bytes fail the same way at three in the morning as they did in the test. A `413` past the **32 MB request ceiling** will never work on the fourth attempt.<sup>[3]</sup>

**The transport seam (the road).** This is what the library's retry policy is for. It is the only seam where trying again is a **reasoned act, not a hope**. A **`529`** reports the service is **temporarily overloaded**. A `500` carries the documented instruction to retry with **exponential backoff**.<sup>[3]</sup>

**The output seam (the reply).** This is where developers get hurt, because **everything above it worked**.
- A **refusal arrives as a successful `200`** response carrying a **`stop_reason` of `refusal`**. The usual fix is to send the same request to a **different model**, not to treat the response as an error.<sup>[8]</sup>
- With a streamed response it is worse. An error can happen after the API has **already returned a `200`**, so it does not come through the normal error path at all.<sup>[3]</sup>
- A person reading a log line **cannot tell a refusal from an answer** unless somebody wrote code to record which one it was.

**One cheap habit.** Every response carries a **`request-id`**. Support asks for it because it is the only **handle that identifies a single call**.<sup>[1]</sup> It is like the tracking number on a parcel. **Log it on failure** and a bug report stops being a story about a bad afternoon.

**ELI5.** A parcel can go wrong in three places. The counter might turn it away, and trying again will not help. The road might be blocked, and trying again later can work. Or the reply might arrive looking fine but say "sorry, can't help". Work out which place it went wrong first. Then pick the fix.

## Eleven Documented Codes, and the Seam Each One Belongs To

**First, the idea.** The seam is what you carry into a question. The **status codes** are a lookup table. A table you half remember is worse than none, because it **sorts confidently** into the **wrong seam** and then applies that seam's fix.<sup>[3]</sup>

**Seven codes: the request, the credential or the account is wrong.** Another attempt changes nothing for any of them.

| Code | Error type | What it means |
|:----|:------------------|:--------------------------|
| `400` | `invalid_request_error` | The format or content of the request, and the catch-all for 4XX codes with no entry of their own |
| `401` | `authentication_error` | The key is malformed, revoked or expired |
| `402` | `billing_error` | Billing or payment details need attention |
| `403` | `permission_error` | The key is genuine and is not entitled to this resource |
| `404` | `not_found_error` | The endpoint path, or a resource id inside the URL |
| `409` | `conflict_error` | A concurrent modification, or a unique value already taken |
| `413` | `request_too_large` | Past the byte ceiling for that endpoint |

**Four codes: the service, or the pace you call it at, is the issue.** Waiting is part of every fix.

| Code | Error type | What it means |
|:----|:------------------|:--------------------------|
| `429` | `rate_limit_error` | A rate limit, a monthly spend cap, or a workspace spend limit |
| `500` | `api_error` | A fault inside Anthropic's own systems |
| `504` | `timeout_error` | The request timed out while being processed |
| `529` | `overloaded_error` | The service is temporarily overloaded |

**Three of the eleven are worth a second look.**
- **`400` is a catch-all, not a diagnosis.** It covers **4XX codes** that have no entry of their own. A **spend limit** you set on your own organisation or workspace returns one. The exception is a **Claude Code workspace**, which can answer `429` instead.<sup>[3]</sup> So a `400` is no proof that a body is malformed. A scenario that pairs one with a spend limit is not describing a broken request.
- **`401`, `402` and `403`** all say the **caller may not go ahead**, for **three unrelated reasons**. The **key is bad**. Or the account owes money. Or the key is fine but **lacks this one permission**. That is three fixes, and none of them is another attempt.
- **`409` is the exception in the first table.** The client **retries connection errors**, `408`, `409`, `429` and `500` or above by default.<sup>[4]</sup> That looks like a contradiction until you see what a **conflict** is: a state some other writer may already have let go of. Retrying it is the documented fix.<sup>[3]</sup> Every other code in that first table fails the same way forever.

**ELI5.** The codes are like stamps the post office puts on a returned parcel. Some mean "your form is wrong", so fix the form. Some mean "we are busy", so wait and try again. A few look alike but mean different things, so learn them one by one.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers on integration questions almost never describe something impossible. They describe a **real technique**, explained correctly, but used **one seam over** from where it belongs.

**The assumptions behind most wrong answers.**
- **A library is either absent or immovable.** Options split into "your code must do this itself" and "the library does this and you cannot change it". Both miss what a client library really is: a **documented default with a setting** on it. When a scenario asks what happens to **transient failures**, the answer that holds up says a **default runs** and **can be configured**.
- **Freshness bought with request volume, sold as a connection.** An option that keeps asking is offered against a **requirement to be told**. It is a fine design for **slow-moving data**. It is the **wrong shape** when the **other end knows first**, because **latency stays tied** to whatever **interval somebody picked**.
- **A status code read as a verdict on the content.** Options that **treat `200` as success** and **everything else as failure** ignore a **whole seam**. The scenarios that punish this are the ones where the **pipeline broke downstream** of a call that **never errored**.
- **A heavier integration preferred to the maintained one.** Building on a **general HTTP client**, wrapping a **different provider's library**, or **running a separate process** all look like good engineering. Ask what each one now has to **track by hand** as the API moves.

**Match on what the scenario is doing, not on the domain it is set in.**

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| A service pushes updates continuously and the app also sends messages back | A protocol built for a persistent two-way connection | Any option whose freshness depends on how often you ask |
| A teammate asks whether application code needs its own retry logic | A default policy exists and the client exposes it as a setting | Calling it absent, or correct but unchangeable |
| The language has an official Claude client and the team is starting an integration | Use the client and its documented pattern | Rebuilding headers, retries and parsing against a general HTTP library |
| A call fails the same way on every attempt | The request, the credential or the size is wrong, and it is yours | Adding backoff to a deterministic failure |
| Failures are intermittent and get worse under load | Bounded retries with backoff, honouring the interval the service names | A tighter loop, or retrying past a spend cap forever |
| Nothing errored and a downstream step broke anyway | Inspect the response body and its stop reason, then validate | Treating a healthy status code as a healthy answer |
| A status code arrives and the option sorts it by the number alone | Ask whether a later attempt could change the outcome, then repair the seam that owns it | Treating `400` as proof of a malformed body, or `409` as something retrying cannot clear |
| Portability across model providers is offered as the reason | Cost the extra layer against a switch nobody has scheduled | A foreign client plus a translation shim |

**The habit that carries over.** Name the seam before you name the fix. Say out loud whether the failure is in what you **sent** (the counter), in getting it there (the road), or in what **came back** (the reply). Roughly half the options in front of you stop being plausible.

**ELI5.** Wrong answers are usually good ideas used in the wrong place. Before you pick an answer, ask where the parcel went wrong: at the counter, on the road, or in the reply. Then only look at fixes for that place.

## What to Remember

- The **four-part call** is **address, headers, body, response**. That means an endpoint and method, a **credential plus `anthropic-version` plus content type**, a JSON payload, and a reply with a **status code, headers and a body** that you read separately.
- **Official clients exist for seven languages** and send the **required headers** for you. They reach the **same endpoint and the same model** as a hand-written call. The difference is who **maintains the parts** as the API moves.
- **Clients retry transient failures twice by default**, with **exponential backoff**, honouring **`retry-after`** when present. **Maximum retries is an option** you can raise, lower or set to zero. A default that is **present and adjustable** is the description that fits.
- **Retried by default**: **connection errors, `408`, `409`, `429`**, and **`500` or above**. A **retry loop around the client's own** multiplies attempts. An **outer deadline does not restart** when the library retries.
- A **`429` from a spend cap** carries no **`retry-after`** and keeps failing until access resumes. So **retrying it forever** turns a **billing problem into an outage**.
- **Eleven documented codes**: `400` invalid request, `401` authentication, `402` billing, `403` permission, `404` not found, `409` conflict, `413` too large, `429` rate limit, `500` internal, `504` timeout, `529` overloaded. **`409`** is the only one **shaped like an integration failure** that the client **retries by default**, because the **conflicting state can clear**.
- **Persistent and two-way are separate properties.** **Polling** leaves staleness **tied to the interval**. A **held-open response pushes one way only**, server to client. A **websocket keeps one connection** on which **both ends send unprompted**.
- **Three seams break a call**: **integration** (4xx, identical every attempt, yours to fix), **transport** (connection faults and 5xx, intermittent, retry with backoff), and **output** (**HTTP `200` with unusable content**, fixed by validation or a different model).
- A **refusal is a successful `200`** carrying **`stop_reason: refusal`**, and a **streamed error can arrive after the `200`**. That is why **status-code-only error handling misses an entire seam**.
- **Every response carries** a **`request-id`**. **Log it on failure**, because it is the **only identifier that names a single call** when you report one.

**ELI5.** Every call is a parcel with an address, labels, a letter and a reply. It can go wrong at the counter, on the road, or in the reply. Only road problems are worth trying again. Always keep the tracking number.

## Endnotes for this chapter


1. The Claude API is a RESTful API at `https://api.anthropic.com`; all requests must include a credential header (`x-api-key` or `Authorization`), an `anthropic-version` header such as `2023-06-01`, and `content-type: application/json`, which the client SDKs send automatically. The page also documents the `request-id` response header and the auto-paginating iterators the SDKs provide. Anthropic, *API overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/overview](https://platform.claude.com/docs/en/api/overview)

2. Anthropic publishes an `ant` command-line tool for shell scripting and interactive use, client SDKs in seven languages, and framework-specific libraries which expose Claude through another framework's API surface and are not general-purpose Messages API clients. Anthropic, *CLI, SDKs, and libraries* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/cli-sdks-libraries/overview](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)

3. HTTP status codes and their error types, the 32 MB request size limit, the instruction to retry a `500` with exponential backoff, the note that a spend-cap `429` carries no `retry-after` header, the default of two automatic retries with exponential backoff and a configurable maximum-retries option, typed SDK exceptions, the ten-minute validation and TCP keep-alive behaviour, the `request-id` header, and the fact that an error can occur after a streaming response has already returned a 200. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

4. The set of errors retried by default is all connection errors, `408` Request Timeout, `409` Conflict, `429` Rate Limit and `500` or above, with a default of two retries configurable through the client's maximum-retries option; a retried request does not restart a context timeout set for the request lifecycle. Anthropic, *Go SDK* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/go)

5. Setting `"stream": true` on a message returns the response incrementally using server-sent events. Anthropic, *Streaming messages* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)

6. MCP tunnels connect Claude to MCP servers running inside a private network over an outbound-only connection, removing the need to open inbound firewall ports or expose services to the public internet. Anthropic, *MCP tunnels* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview)

7. The inner TLS handshake between Anthropic's backend and the customer's proxy is carried inside the tunnel's plaintext WebSocket stream, and the term "outbound-only" describes the connection rather than the requests carried over it. Anthropic, *Architecture and components* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/concepts](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/concepts)

8. A refusal is a successful HTTP `200` response carrying `stop_reason: "refusal"` rather than an error, and the same request can usually be sent to another Claude model to get an answer. Anthropic, *Refusals and fallback* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
