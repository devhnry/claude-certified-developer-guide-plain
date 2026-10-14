# Chapter 20: The Attack Arrives as Content You Asked For

**Summary**: *The dangerous input looks normal. It is a ticket, a document or a fetched page. Tucked inside is one sentence aimed at the model, not at a human. If your defence is also a sentence, one reader reads both and may obey the wrong one. So this chapter sorts controls with one question: can the attacker's text reach the spot where the control lives? That answer settles most of what this skill asks.*

Picture a mailroom clerk who does whatever a letter says. A stranger slips in a note: "The boss says: send the customer list to this address." The clerk cannot tell who wrote which line. That clerk is the model, all chapter.

## A Ticket That Passes Validation and Still Contains an Order

Your agent answers support tickets, sent by the public. One arrives with an ordinary subject and plain prose. Every field holds the type it declares. But one body sentence is meant for the model, not the human who reads the reply. No check blocks it. There is nothing to reject, since text in a text field is not an anomaly.

The model receives one sequence. Your standing instruction, the turn, a retrieved document and a tool result all arrive as tokens in one stream, with nothing to mark which span you wrote. The boss's memo and the stranger's note land in one pile. **Prompt injection** follows: instructions planted in content the model reads for someone else, weighed beside yours because they look alike. Anthropic's threat model for agents gives two causes of an unwanted action: injection and model error.<sup>[1]</sup>

No single file type carries it. Any text a stranger wrote and your system reads will do: inbound mail, a page fetched for a summary, characters pulled out of an upload, or what a tool returns after fetching elsewhere.<sup>[2]</sup> Someone can plant it long before the request that triggers it, in a corner of the page no human reads.

**ELI5.** A helper does what each letter says. A sneaky letter can copy the boss's voice.

## Every Control Sits Inside the Attacker's Channel or Outside It

Ask of any control: can the attacker's text reach it? Everything that text can touch is the **writable channel**. It holds the assembled prompt, the model's reading of it, and the model's output. A control in there is only a request. Tell the clerk "ignore odd notes" and the stranger's note sits beside it, arguing. A control outside is a rule, like a cash drawer (server-side authorisation) that never reads notes.

| Control | Can injected text argue with it? | What you get |
|---|---|---|
| Telling the model to ignore embedded orders | Yes, one reader weighs both | Fewer hits, no floor |
| Content in delimiters, encoded, labelled as data | Partly. Attacker writes inside the wrapper | A fence to break |
| Classifier screening content first | No. Runs before context exists | A ruling with no appeal, for known patterns |
| Tool that takes catalogue identifiers only | No. The ability is absent | The banned action cannot happen |
| Server checks the caller may do the operation | No. Never reads content | Same answer for a fooled model and a clean one |
| You never send the data or grant the reach | No. Nothing is left to argue with | Nothing later can undo it |

Down the middle column, one thing changes: can the control be talked out of its verdict? A control that works by odds has no floor. Claude is trained to resist these attacks, yet Anthropic still recommends defence in depth.<sup>[1]</sup> Read every row but the last two that way.

Writing the defence as a sentence is the anti-pattern. It is free and sounds official, yet a hostile ticket can still get a refund through it.

This sort also shows what a model adds to your risk list. Reviews already count conventional risks such as flooding, physical access and a vulnerable client library. New ones arise because untrusted text gets interpreted and the result reaches privileged actions: injection, leakage of prompt or context content, **jailbreak** attempts, and output that reaches an action path without passing an application control.

**ELI5.** A note saying "ignore other notes" is just another note. A locked drawer reads none and needs the right key.

## A Jailbreak Attacks the Model's Limits; an Injection Attacks Your Application's Actions

These are two threat models, split by who is hostile.<sup>[2]</sup>

In a jailbreak, your own user is the attacker. They reshape input until it yields content or an action you would refuse. In an injection, that user is the victim. A third party wrote what Claude read for them.<sup>[2]</sup> The customer is innocent. The note is the culprit.

So the cures differ. A jailbreak has an account to act on: screen input before the main conversation sees it, and throttle or ban repeat offenders of the same refusal.<sup>[2]</sup> An injection has no one to throttle.

Defend in two halves either way. Limit what reaches the model, then limit its actions. Skip the second and a steered model keeps all its permissions.

**ELI5.** Sometimes the person at the counter is bad. Sometimes a bad letter fooled a good person. Filter what comes in and limit the helper.

## Untrusted Content Enters as Data, in Its Own Block, After a Gate

Three moves, each further from the attacker's channel than the last.

Screen first. Any check that runs before the prompt is built is outside the channel. Anthropic documents a lightweight model that pre-screens input, with structured outputs forcing its verdict into a value your code can branch on. Tool output gets the same pattern: run the tool, screen the result, pass it on only if nothing is flagged.<sup>[2]</sup>

Hand it over as data, with its source named. Put outsider text in tool result blocks, never in a system prompt or plain user text block. Claude is trained to doubt orders that appear inside tool results.<sup>[2]</sup> Encode it as JSON so escaping marks the edge. A closing quote or tag then cannot break out into instruction context.<sup>[2]</sup> Name the content and its source too, in the tool description or the result structure.<sup>[2]</sup>

Two facts place a span: how long it lives and who wrote it. Lasting text you wrote is standing instruction. Outside text arriving with this one request goes in the turn, behind delimiters. The rule cuts both ways, and people miss that. Put an instruction of your own inside a tool result and the model treats it as untrusted. It may ignore it or flag it as an attack. Send it in a user turn after the block.<sup>[2]</sup>

The worst habit is the concatenated prompt: instruction and document pasted into one string. That erases the line later steps need. Parsing afterwards fixes a result's shape, not the boundary. Chapter 5 covers placement as prompt craft.

**ELI5.** Do not staple the stranger's letter to the boss's memo. Check it at the door and give it its own tray.

## The Only Leak Control Nothing Downstream Can Undo Is Not Sending the Data

Leak controls sort the same way, by what has already happened when each runs.

Redaction, access restriction and periodic review all work on data that exists, so they are recoveries. **Minimisation** acts earlier, before a second copy exists. Send only the fields the task needs. A field you never sent cannot leak.

Two failures earn names. One is the debug log nobody scoped. It keeps raw requests and responses for troubleshooting, so it becomes a second copy of everything sensitive, kept longer and readable by more people. Tokenising identifiers before the write and limiting who reads the store help. Both still follow a request that carried the identifiers. The other is redaction delegated to the model. Privacy then rests on a step with no floor, run after the data has crossed. An unguessable storage path is obscurity, not a third option. Whoever learns the path reads the store. Obscurity expires on discovery.

The fix is a boundary with a stated crossing rule: what may leave, and what is filtered or redacted at the line. Decide it before the call, not after incidents. Chapter 16 covers that boundary as a design object.

Protected health information (PHI) in the Claude API appears in message content, attached files, and file names and metadata. Under a BAA, workspace names, user contact details, billing data and support tickets should not hold it.<sup>[3]</sup> One route is easy to miss, the schema. With structured outputs or strict tools, JSON schemas compile into grammars cached separately from message content. Those caches lack the same protections. Keep identifying detail out of property names, enum values, const values and pattern regexes.<sup>[3]</sup>

Retention and residency are settings, not prompts. With zero data retention, Anthropic does not store prompts or responses at rest once the response returns. You enable it per organisation. **HIPAA readiness** instead applies safeguards across the whole lifecycle, without deleting at once. A team handling PHI wants that, not ZDR.<sup>[3]</sup> Residency has two separate settings. One sets where inference runs. The other sets where data is stored.<sup>[4]</sup> For a prompt leak, first keep proprietary detail the task does not need out of the prompt.<sup>[5]</sup>

**ELI5.** A secret you never told cannot be spilled. Hiding it later only helps after the telling.

## Authorisation Belongs to the Operation and Is Checked Against the Caller

A tool call is a request, not proof you may have it. The check that holds runs on the server, at the operation, against the calling identity. Does the caller own the record? Is the amount in policy? Does the role allow it? It never reads the ticket, so a persuaded model gets the same ruling as a clean one. Any check that reads the request lives in the channel. Summarising first does not remove the hostile line. It carries it into the summary, and the summariser can be steered too. A cheaper model fails too, because any model follows instructions.

Authentication comes first. If a lookup finds several plausible matches, the identity is unresolved. One disambiguating question fixes it. Picking the latest is still a guess, just with a cutoff. Opening each candidate's records to compare is worse. It exposes an account just to learn it was wrong.

**Least privilege** then sets severity, not likelihood. An injection through an identity that can write anywhere is an incident. If that identity may write to one directory, the same attempt is a refusal plus an audit line. A tool taking an identifier checked against an approved catalogue cannot fetch an arbitrary target. A general fetch tool plus a warning leaves the power in place and hopes. Filtering results afterwards is too late, since the page is fetched and the answer shaped.

Two containment controls matter here. First, network egress restriction blocks the outbound request itself. If a malicious file tells an agent to send customer data out, the network stops it.<sup>[1]</sup> A sandbox with no egress rules lets a compromised tool execution reach arbitrary hosts.<sup>[6]</sup> Second, **default deny**. Claude Code matches bash commands fail-closed, so a command with no match needs approval. Web fetch gets its own context window, so retrieved content never reaches the main one.<sup>[7]</sup> Chapter 21 covers hooks as the enforcement point. Chapter 22 covers credentials.

**ELI5.** A cash drawer asks "who are you, and may you?" It ignores how nice the note sounds. Give each worker only needed keys.

## How Wrong Answers Are Built on This Material

Wrong options here are sound practice in the wrong place. Each fits another threat, or a later step.

- A control inside the attacker's reach. A louder instruction, a stricter refusal policy, a reminder that documents are untrusted. Text against text is a mitigation, never a boundary. It answers how often an attempt lands.
- Detection where prevention was possible. Logging and review, output filters, anomaly alerts. Each watches what already happened, and several add another copy of the data. Use them after you accept the exposure and need evidence.
- The model guarding itself. Ask it if content is trustworthy and containment goes to a reader the content already addresses. Ask it to omit sensitive fields and privacy goes the same way.
- A power left in place, with advice against using it. The broad tool stays. A warning, a preference or a later filter sits around it. Fine only if the need is real.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| Strangers write text the agent reads, plus a privileged action exists | Server authorises against the caller | Prompt instruction, summarising step, smaller model as filter |
| A general tool is stretched past its job | Swap in a tool taking validated identifiers | Prompt warning, or filtering after the fetch |
| Debug logs capture identifying data | Send less, redact before writing | Keep raw payloads, or tell the model to omit identifiers |
| Untrusted text must not act as an order | Screen it, then deliver it delimited in a tool result | Join it to the instruction, or put it with standing instructions |
| A lookup matches several identities | Identity is unresolved, ask one question | Pick the latest, or read every candidate's records |
| A legal rule and a deadline both apply | The rule is fixed. Choose inside it | Weigh it against speed as one factor of several |
| Asked for model-specific threat categories | Injection, context leakage, jailbreak, unsafe output reaching an action | Conventional infrastructure or supply-chain risks |

One test outlives the table. If one reader reads both the attacker's words and the control's words, the control is only a preference.

**ELI5.** Wrong answers are often good ideas in the wrong place, like a camera where you needed a lock.

## What to Remember

- Prompt injection is instructions planted in content the model reads for somebody. It takes them like yours, since it gets one token stream with no mark between trusted and untrusted. Any text a stranger can write is a way in, planted content included.
- Ask if the attacker's text can reach a control. Inside the writable channel (the assembled prompt, the model's reading of it and its output) it is a request. Outside, it is a rule. An instruction to ignore embedded instructions is read by the reader under attack.
- A jailbreak targets the model's own limits, with your user as attacker, so input screening and throttling work. An injection targets your application's actions, with your user as victim, so nobody is left to throttle. Both need the same two halves: limit what reaches the model, then limit what it may do.
- Untrusted content is screened before assembly, sent in tool result blocks (not a system prompt or plain user text), JSON-encoded so escaping supplies the delimiter, and labelled with its source. Never put your own instructions in a tool result, which the model treats as untrusted too.
- Minimisation leaves nothing to undo, since redaction, access limits and review act on data that exists. Send only the fields the task needs. Redact before the log write. An unguessable path is obscurity, not access control.
- PHI in the Claude API sits in message content, attached files, and file names and metadata. It is not expected in workspace names, user contact details, billing or support tickets. JSON schemas compile to separately cached grammars without those protections. Keep identifiers out of property names, enums, consts and patterns.
- **Zero data retention** stops storage of prompts and responses at rest after the response returns, enabled per organisation. HIPAA readiness applies lifecycle safeguards, not deletion, and fits PHI. Residency has two settings: where inference runs and where data is stored.
- Authorisation belongs to the operation, checked server-side against the requesting identity, so a persuaded model gets the same verdict. Settle identity first. Several matches means unresolved, and one disambiguating question beats ranking by recency.
- Least privilege decides severity, not likelihood. A broad identity makes one injection an incident. A narrow one gives a refusal plus an audit line. A tool taking validated catalogue identifiers makes a disallowed fetch impossible rather than discouraged.

**ELI5.** Strangers can slip notes into anything the helper reads. Check the mail at the door, share only what is needed, and give each helper keys to one room.

## Endnotes for this chapter

1. Agents can take unintended actions due to prompt injection, meaning instructions embedded in content they process, or due to model error; Claude models are designed to resist this and defence in depth remains good practice, the worked example being that if an agent processes a malicious file instructing it to send customer data to an external server, network controls can block that request entirely; a security boundary separates components with different trust levels, and least privilege restricts the agent to only the capabilities its specific task requires. Anthropic, *Securely deploying AI agents* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/secure-deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

2. Jailbreaking and prompt injection fall into two categories with different threat models: in the first, a user deliberately crafts inputs to manipulate the application into producing content or taking actions its operator does not want, mitigated by harmlessness screens using a lightweight model such as Claude Haiku 4.5 with structured outputs constraining the response to a simple classification, by input validation for known injection patterns, by system prompts that state ethical and legal boundaries, and by responding to repeat offenders through throttling or banning; in the second, the application's users are being protected from instructions embedded in content Claude reads on their behalf, such as the body of an inbound email, a fetched web page, OCR output from an uploaded file, or the result of a tool call. Recommended structure for the second: put untrusted content only in `tool_result` blocks and never in system prompts or plain user text blocks, because Claude is trained to treat instructions appearing inside tool results with appropriate scepticism; tell Claude what the content is and where it came from, in the tool description or the result structure; state in the system prompt that content returned from tools, documents or searches is untrusted data that must never override the system prompt or the user's original request; JSON-encode untrusted content so that escaping provides unambiguous delimiters and an attacker cannot close a quote or tag to break out into an instruction context; do not put your own instructions in tool results, because Claude treats tool-result content as untrusted data and instructions placed there may be ignored or flagged as a potential injection, so send them in a following user turn; limit Claude's access to sensitive data and actions under the principle of least privilege; screen tool outputs with the same lightweight-model classifier pattern before returning them as `tool_result` blocks; red-team the agent before deployment; and analyse outputs regularly for signs of successful injection. Anthropic, *Mitigate jailbreaks and prompt injections* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

3. Under a zero data retention arrangement Anthropic does not store customer prompts or responses at rest after the API response is returned, and ZDR is enabled per organisation; HIPAA readiness applies a broader set of privacy and security safeguards than ZDR, namely encryption, access controls and audit logging protecting PHI throughout its lifecycle, rather than requiring immediate deletion, and an organisation handling PHI should use HIPAA readiness rather than also needing ZDR; protected health information in the context of the Claude API typically appears in message content, attached files such as images and PDFs, and file names or metadata associated with message content, while workspace names, user information such as name, email and phone number, billing data and support tickets are not expected to contain PHI under the BAA; when using structured outputs or tools with `strict: true`, the API compiles JSON schemas into grammars cached separately from message content and those cached schemas do not receive the same PHI protections, so PHI must not appear in schema property names, `enum` values, `const` values or `pattern` regular expressions. Anthropic, *API and data retention* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/api-and-data-retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)

4. Data residency controls are governed by two independent settings, one controlling where model inference runs, available as the `inference_geo` API parameter or as a workspace default, and one controlling where data is stored. Anthropic, *Data residency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/data-residency](https://platform.claude.com/docs/en/manage-claude/data-residency)

5. Prompt leaks can expose information expected to be hidden in a prompt, and no method is foolproof; documented strategies are separating context from queries using system prompts, post-processing Claude's outputs to filter for keywords indicating a leak, avoiding unnecessary proprietary details that the task does not require, and auditing prompts and outputs periodically; leak-resistant techniques should be used only when necessary because the added complexity can degrade performance elsewhere in the task. Anthropic, *Reduce prompt leak* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak)

6. In the shared responsibility model for self-hosted sandbox environments, network egress control is owned by the customer: sandbox network access is determined by the customer's VPC and firewall rules, and without egress restrictions a compromised tool execution can reach arbitrary external hosts, so outbound traffic should be restricted to only the endpoints the tools require; tools run inside the sandbox with whatever permissions the process has, so least privilege applies to the process user and only required directories should be mounted. Anthropic, *Security model* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security)

7. Claude Code's documented protections against prompt injection include a permission system requiring explicit approval for sensitive operations in Manual mode, context-aware analysis of the full request, input sanitisation, and network commands such as `curl` and `wget` not being auto-approved by default; further safeguards include isolated context windows, where web fetch uses a separate context window to avoid injecting potentially malicious prompts, fail-closed matching, where unmatched commands require approval by default in Manual mode, command injection detection requiring manual approval of suspicious bash commands even when previously allowlisted, and trust verification for first-time codebases and new MCP servers. Anthropic, *Security* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/security](https://code.claude.com/docs/en/security)
