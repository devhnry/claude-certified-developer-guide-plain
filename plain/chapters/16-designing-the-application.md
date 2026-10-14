# Chapter 16: Boundaries, Sessions, and Where Instructions Land

**Summary**: *Think of your application as a country with a border. At the border, your material ends and a model starts reading it. Skip the customs post and the border stays open, because every part assumes some other part is watching. This chapter builds the post five times. The five builds: what the interface told the model before your words, what may cross each way, what shape an answer needs so code can use it, when a chat gets wiped, and which tool version runs. One mistake in any gives the same symptom.*

## Every Application Has an Edge, and It Exists Before Anyone Draws It

Your app is the same. A **ticket body**, a **fetched page**, a **customer record** or a **schema** goes in. Something comes out and gets acted on: a database write, a reply on screen, a call to a service that trusts what it gets.

Between those two moments is the border (the edge). Material stops being yours there and starts being read by a model. It exists from the first request. Nobody builds it. Designing it just means you can finally check it.

An edge nobody drew is not missing. It is unchecked, because every part believes the check is someone else's job. Each part passed its own tests. The gap between the parts was never tested by anyone.

A border becomes a **crossing rule** (the customs rules) once you write down three things. What may cross. Which one component decides. What happens to goods that fail.

Without the third, you record violations but still let them through, since logging a violation is not stopping it. Without the second, two teams each build the check their own way, and the two versions drift apart. A check owned by everyone gets written by no one.

The blueprint lists five design areas for a Claude application. They all ask one question about different traffic.

| Design area | What it decides about the edge |
|---|---|
| Interface | What the model has already been told before your instruction shows up |
| Content boundaries | What gets in or out, and who checks it |
| Schema | The form an answer must take so it can be consumed |
| Session hygiene | When the inside gets wiped, and what sets that off |
| Plugin management | Which build of the tools around the edge is live |

A flaw in any row looks the same: something got across and nothing stopped it.

**ELI5.** Every house has a front door, even before you buy a lock. Someone must decide who comes in and who looks. If nobody decides, anyone walks in.

## The Same Instruction Arrives Into a Different Standing Context on Every Interface

Say you write one line of guidance. You send it through the API. Then through the SDK. Then you type it in the terminal. The behaviour can differ all three times, and nothing is broken.

Your line is never the full instruction. It lands after whatever the interface already supplied, and that amount varies a lot. Your line is the last item in a bag someone else packed (the standing context).

The Messages API supplies nothing. It is **stateless**. Every request has to carry the whole conversation, so anything you leave out is gone.<sup>[1]</sup> No project file loads. No saved preference lasts. Only your code remembers.

The SDK is where people trip. If you set no system prompt, it runs a small default that handles tool calling. That default has no Claude Code coding guidelines, no response style and no project context. Choose the `claude_code` preset and the model gets the CLI's full prompt: tool usage instructions, code style and formatting rules, tone and verbosity, security instructions, and working-directory context. Headless CLI runs use that full prompt automatically. That is why an instruction can act one way under `claude -p` and another way in a bare SDK call.<sup>[2]</sup> Same words, different standing prompt, no error.

Project context comes by a different route. `CLAUDE.md` goes into the conversation as project context, not into the system prompt. It therefore sits alongside whichever prompt you picked, and the configured setting sources decide whether it loads, not the preset.<sup>[2]</sup> That is two separate switches. If you assume one drives the other, half your deployments will be wrong. Set both deliberately.

Interactive tools also hold their own history. The CLI, the desktop app, the web version and the editor extension keep separate session stores.<sup>[3]</sup> So there is no single "conversation" you carry from window to window. Each window has its own and none syncs.

| Surface | Already in context when your text arrives | Where the history lives |
|---|---|---|
| Messages API | Whatever the request itself holds | Entirely in your application |
| Agent SDK, no configuration | A small tool-calling prompt | In the SDK, keyed by session ID |
| Agent SDK, coding preset | Complete coding guidance, style, safety and working directory | In the SDK, keyed by session ID |
| Headless CLI | Same complete prompt, automatically | In local transcript files |
| Interactive surfaces | The surface's own settings plus project files | In that surface, not shared |

"Test on every interface" is not something anyone can act on. Instead, put each rule where its interface reads. An API integration never loads project files, so it cannot see a rule kept in one. A terminal session on the preset never sees a rule kept only in a system prompt string. So state the rule once per channel, on purpose, as part of the application and not of one developer's machine.

Anthropic has a test for when to write a custom prompt, and it works as a design question because it is about the product. The less your agent resembles a coding assistant in a repository with a person watching, the more of the standing prompt you write yourself. Four signs. Output that is not read in a terminal. An identity that should not look like a coding tool. A permission setup where nobody approves each step. Work that is not coding, where coding guidance fights your instructions.<sup>[2]</sup>

The anti-pattern is inheriting an instruction by accident. A developer prototypes on the preset and likes the result. They ship an integration with its own prompt. Much of what they liked came from the preset, and it is gone. Users complain about quality, but no error appears, so the cause is hard to find.

**ELI5.** You hand a note to different friends. One already knows the game, another knows nothing. The same note means different things. So write the key rule where each friend will look.

## Context Shapes a Decision; Only a Deterministic Gate Removes One

Claude Code has two memory systems: files you write and notes it builds up. Both load when a conversation starts. Both are read as context, not applied as enforced settings. To stop an action whatever the model decides, the documentation points you to a hook that runs before the tool.<sup>[4]</sup>

This holds well beyond one product. Words that reach the model can sway a choice. Code that runs first takes the choice away. The first kind works by probability. The second either runs or it does not. Only the second binds. A "slow down" sign at the border post asks nicely. A barrier arm (a hook) stops the car.

So a crossing rule that lives only as a sentence in a prompt is a preference the model usually follows. Keep it there, since a model that knows the policy behaves better. It just cannot be the only copy. The exam leans on this: an option that makes an instruction more likely to be followed does not guarantee anything.

Better adherence is still worth the effort. Short, specific instructions get followed more reliably. The advice is plain: keep a project instruction file under about `200` lines, because a longer one eats more context and lowers adherence.<sup>[4]</sup> Concrete rules help too. "Handlers live in this directory" can be checked by a person reading the output. "Keep things tidy" cannot.

**ELI5.** Asking a puppy nicely not to chew shoes helps a little. Shutting the shoes in a cupboard works every time. A prompt asks. A hook or check is the cupboard.

## Content Boundaries Run in Two Directions, and the Outbound One Gets Forgotten

Inbound is the side people design. Untrusted material reaching the model has known handling. Deliver outside content inside `tool_result` blocks, not in system prompts or plain user text. Use the tool description to say what the content is and where it came from. Tell the model in the system prompt that tool and document content is data and never overrides instructions. Wrap outside strings in JSON so an attacker cannot close a delimiter and carry on as if giving orders.<sup>[5]</sup>

Chapter 5 covers where those blocks go in a prompt, and chapter 20 covers the attack. What matters here is placement as a design limit. The channel that content arrives on decides how much authority it has. If a component pastes fetched text into the standing instruction, it has promoted that text, whatever the author meant. It is a parcel pinning on a customs officer's badge.

Two further inbound rules are easy to get backwards. First, keep your own instructions out of tool results. Content there counts as untrusted, so guidance in a result might be ignored or flagged. Put it in the user turn after the result.<sup>[5]</sup> Second, screen tool output the same way you screen user input. Run a small classifier call over what the tool returned. Make it give a verdict the app can parse and branch on. Do it before the content goes back as a result. Screen both directions, because only one looks dangerous.<sup>[5]</sup>

Outbound is where designs fail review. Material sent to the model leaves its perimeter. What the other side does with it is a design input, not a purchasing detail. Ask before you build.

| Question about data leaving | What answers it | What it limits |
|---|---|---|
| Is anything stored once the reply comes back? | Zero retention, switched on for each organisation | Whether prompts and replies sit in storage at all<sup>[6]</sup> |
| Is health data involved? | A signed agreement, plus an organisation set up for it | Which features may carry the data, and which safeguards apply<sup>[6]</sup> |
| Where does the model actually run? | A geography parameter on each request, or a workspace default | Which regions may serve the request, with a stated price multiplier<sup>[7]</sup> |
| Where does the workspace live? | Chosen at creation, and fixed afterwards | A one-time decision made before any app exists<sup>[7]</sup> |

Two details settle exam scenarios. First, regulated content turns up in message content, in attached files, and in the file names and metadata attached to message content. Workspace names, user contact details, billing data and support tickets are not expected to hold it.<sup>[6]</sup> If your boundary guards "the prompt" but not an attachment's filename, it is in the wrong place. Metadata travels with the file, so the rule must cover it.

Second, a real trap, where this chapter's two halves meet. Schemas sent for constrained output are compiled and cached apart from message content. Those cached copies do not get the protections prompts and replies get. So never put regulated content in a schema definition.<sup>[6]</sup> Field names and descriptions feel like settings, so someone eventually puts a patient identifier in an enum. Schemas are data too.

**Least privilege** works in both directions. Limit what the model can reach so a successful injection has little to use. Run tools in sandboxed environments. Keep secrets the model does not need out of reach.<sup>[5]</sup> A boundary that lets everything through still counts as a boundary. Its crossing rule just reads "anything".

**ELI5.** Mail goes two ways. You check what arrives at your house, and you check what you put in the envelope you send. The name on the envelope counts too, not only the letter.

## The Schema Is a Contract With Three Parties, Not Just With the Model

A schema on a request looks like a style note. It is a contract. The model must obey it. Downstream code is written against it. The platform compiles it into something with rules of its own.

The mechanism is **constrained sampling**, built from compiled grammar artifacts made from your schema.<sup>[8]</sup> Asking for a format in a prompt has no such effects. You settle them at design time.

Output order is not your schema's order. Required properties come out first, in schema order, then optional ones. If a consumer needs a set order, mark everything required, or write the parser to expect shuffling.<sup>[8]</sup> A consumer that reads by position breaks the day someone makes a field optional. Read by name, never position.

Capital letters in enum values are not guaranteed. The reply completes normally, with no error and no special stop reason, but the value differs by one capital. Compare case-insensitively. Never define two enum values that differ only in case.<sup>[8]</sup> It shows up in a branch testing exact string equality, far from the request. Lowercase both sides and the problem class disappears.

The schema the model sees may differ from yours. SDK helpers drop features the platform lacks. They move the constraint into the field's description and close objects to extra properties. So number and length bounds are checked by your validation, not by the grammar.<sup>[8]</sup> The contract holds in two places, and only one is the model.

Complexity is a budget with a hard edge. Documented caps limit how many strict tools a request can carry, how many optional parameters all its schemas hold, and how many parameters use union types. Unions cost most, since they multiply compile cost. Exceed the compiled size and the request fails with a complexity error, even if each individual cap was met.<sup>[8]</sup> So schema complexity is shared across the whole request. Budget it there.

One more party shows up most in scenarios. A single call carries exactly one output contract. Take two jobs judged differently: sorting a ticket (success is the right category) and writing a reply (success is an acceptable answer). Those are two contracts, and one call cannot hold both. Merging them to save cost only wins if you ignore quality. Separate calls give each stage its own schema, a prompt aimed at one job, and an evaluation against the right standard.

The named failure is a schema written only for the model. It describes a good answer, but nobody asked the consumer what it needs. Someone adds a field. The lenient parser keeps working. A downstream service silently gets a shape nobody agreed to. Chapter 6 covers checking what comes back. The duty here comes earlier: write the schema from what the consumer needs, and change it on the consumer's schedule. Ask the consumer first.

**ELI5.** A schema is like a form with boxes. The writer, the reader and the printer must all agree on the boxes. Move a box without telling the reader and they get lost.

## Continue, Resume and Fork Answer Different Questions About Whose History You Get

The API has no session notion, since every request brings its own history. The SDK offers three ways to reach an existing session. They differ in how the session is found, not in what happens afterwards.

**Continue** takes the latest session in the current directory, so you track nothing. **Resume** needs a specific identifier your app saved, and multi-user apps need exactly that. **Fork** copies one history into a new session with a new identifier, leaving the old one alone, so you end up with two separate threads.<sup>[9]</sup>

Now treat those as an access question and one turns scary. "Latest session in this directory" does not mean "this user's session". A service juggling several conversations with continue is choosing by recency, not identity. That is the bug an exam will describe: one conversation's context appearing in another, with no bug in the code. Identity must choose the session, and only an identifier does.

Session files stay on the machine that made them. So an app on short-lived workers or containers cannot resume with an identifier alone. A session store copies transcripts to your own backend, and its lookup key comes from the working directory, so a resuming host must use the same directory as the original run.<sup>[9]</sup> That is a deployment limit hiding inside a chat feature. Transcripts do not travel.

Resuming restores less than people expect, deliberately. Full conversation history returns. So do the model and the configured agent. The permission mode returns too, with named exceptions: plan mode and a bypass mode are never restored, so a resumed session starts in whatever mode a fresh one would. Settings given on the command line at launch, such as settings files, server configuration, plugin directories and added directories, must be passed again. The standard settings files are re-read automatically.<sup>[3]</sup> Pass your launch flags again.

One pattern runs through all of it: content comes back, posture does not. Anything widening what the session may do is set up fresh at launch. That is a good default. It also means an operator who resumed and assumed elevated mode returned has less authority than they think. An application that assumed its flags returned has less configuration than it needs. Re-establish posture, openly, every time a session comes back.

**ELI5.** A bookmark can mean "the last page anyone read" or "page 42 of my book". The first might open somebody else's page. The page number always opens yours.

## Three Doors Lead Into a New Conversation, and a Timeout Closes Only One

A user asks about a refund. An hour later they ask something unrelated. The assistant confidently brings up refund details nobody typed. That is stale context leaking into another conversation, and this area exists to stop it.

People usually propose one timeout. It is half an answer. A conversation can end three different ways, and each lets through what the others catch.

| Trigger | What sets it off | Where it falls short on its own |
|---|---|---|
| The clock | Idle time, or total age from the start | A busy session whose topic changed an hour ago |
| An event | Logout, a finished purchase, a role change, an error the app cannot recover from | Long quiet gaps between events |
| Intent | The app judging a request to be new work, or the user asking | Anything the user forgets to ask for, since the guarantee depends on them |

Read the third row closely, since people offer it as enough. If you hand the reset to the user, the guarantee depends on a person remembering. Guarantees do not live in habits.

So a sound answer combines all three. **Expiry** stops an abandoned session living forever. **Reset triggers** clear state the moment a defined event happens. **Fresh-start rules** let the app itself know a request is new work, not a continuation. Each closes a path the other two leave open. So you add them. You do not choose one.

Two facts sit underneath. Transcripts are kept, on a documented default measured in years, or for whatever finite retention period an organisation set. So "the session ended" and "the material is gone" say unrelated things.<sup>[6]</sup> Also, a long-idle session picked up later may be restored from a summary rather than in full, since the cache behind it expired. What the user experiences as continuity and the tokens actually resent are different things.<sup>[3]</sup> Deletion is its own question with its own answer.

The named failure is a session that ends only when someone closes the tab. That is not a missing feature. Nobody specified it, so the default became whatever the interface did.

**ELI5.** A room can be tidied by a timer, by a bell when the game ends, or by a kid saying "clean up". One alone leaves mess sometimes. All three together keep it clean.

## Plugin Versions Are Pinned So a Regression Has Somewhere to Land

The last row of the opening table is the tooling around the edge, and it changes by itself unless someone stops it.

Learn the default. A declared dependency follows the latest version. So an upstream release can change what runs under your extension, with no action, notice or record from you.<sup>[10]</sup> Nothing failed. What is running just stopped matching what was tested.

A version constraint makes that a choice. Hold a dependency in a tested range and installs stay on the highest matching patch. The upgrade happens when someone decides, by publishing a new version with a wider range.<sup>[10]</sup> If several constraints cover one dependency, they intersect, and you get the highest version meeting all of them. If none does, the update is skipped and reported with the constraining extension named.<sup>[10]</sup> A clash looks like a clash, not like odd behaviour.

Resolution checks tags on the repository holding the dependency. The tag name pairs the plugin name with the version, and that version should match the manifest at that commit.<sup>[10]</sup> Two defaults come with this, both crossing rules with the choice already made. Automatic updating is off for marketplaces Anthropic does not operate. And a dependency from a different marketplace than the declaring extension is refused. Only an allowlist on the marketplace hosting the extension being installed opens it, and trust does not pass through middle marketplaces.<sup>[10]</sup> Trust is declared, never inherited.

Chapter 18 treats versioning as day-to-day operations. The design duty is smaller: to blame a component for a regression, you need a record made before the change, written down earlier than the symptom. Pinning makes the record. Rollback is what the record buys. An unpinned dependency does worse than risk a break. It takes away your ability to prove what broke.

One packaging detail counts as design. A bundle's name prefixes every command in it. That lets two bundles ship the same command name without a clash, and renaming the bundle renames them all.<sup>[11]</sup> The name is part of the interface. Choose it once, early, while thinking about the interface and not the folder.

The anti-pattern is the dependency that follows latest. It is rarely chosen. It is a missing decision that looks like keeping up to date.

**ELI5.** A recipe saying "use whatever flour the shop has today" tastes different each week. Nobody knows why. Write the exact flour down, and you can bake last month's good cake again.

## How Wrong Answers Are Built on This Material

Wrong answers here are convincing, since most describe real engineering. One hidden assumption makes each wrong, and four cover most of them.

- **Promising a guarantee from something that only raises adherence.** An option tightens a written instruction, reworks a prompt, or adds guidance on what to refuse, when the scenario says something must never happen. Instructions shift odds. Code that runs first decides. If the requirement says never, ask which component would have to fail for it to happen. Choose the option naming one.
- **A single control against a failure with many entrances.** A timeout for stale context. A screen on user input while tool output goes unchecked. A check at one seam in a system with four. The option is right about its path and silent on the rest, which is why it reads like an answer. When a scenario lists several ways in, it wants a set, not a pick.
- **A boundary around the obvious payload, not its neighbours.** The prompt is protected. Attachment filenames, schema definitions, cached artifacts and transcript retention are forgotten. Ask what else travelled with the content, and what is stored that is not the content.
- **Enforcement placed where the habit is, not where the authority is.** Instructions inside tool results. Standing rules tacked onto the newest turn. A policy written for humans that nobody checks. A session picked by recency when identity was needed. Each puts the control on a channel with no weight. Name the channel an option acts on, then ask if that channel binds anything.

Match on what the scenario is doing, not the setting it is dressed in.

| If the scenario describes | Usual answer | Usual trap |
|---|---|---|
| Old chat context appearing in a different conversation | Expiry, set reset events and app-owned fresh-start rules, all three | One timeout, or telling users to open a new chat |
| One piece of guidance acting differently in the terminal than in an integration | Put the rule on the channel each interface reads | Assuming every surface gets one surface's defaults |
| A need for an action to be impossible | A check in code that runs before the action | Firmer wording, louder emphasis, a better instruction file |
| Outside or third-party content reaching the model | Pass it as tool results, labelled, delimited and screened before return | Pasting it into the standing instruction so the model surely sees it |
| Two stages whose inputs, outputs and success measures differ | Separate calls, each with its own contract and evaluation | One call for both, defended on token cost while ignoring quality |
| Downstream consumers breaking on output that is well formed | Build the schema from the consumer's needs, versioned on its schedule | A schema describing a good answer, with parsing loosened until it passes |
| Regulated or sensitive data in scope | Ask where it shows up, filenames, metadata and schema definitions included | Guarding message bodies only and calling configuration out of scope |
| A behaviour shifted and nobody knows which component moved | Versions pinned before the change, giving a rollback target | Reproducing it, adding logs, or updating everything to current |
| A requirement about where processing physically runs | The geography controls, picked knowing it may be unchangeable later | Treating placement as a detail to sort out after the build |
| Sessions resumed on another machine or worker | External session storage, consistent keys, identity choosing the session | Resuming by recency, or assuming a local transcript can be reached elsewhere |

One habit works beyond the table. For each option, ask what would have to be true for the guarantee to hold, then ask who checks it. If the second answer is the model, the option is an improvement, not a control.

**ELI5.** Wrong answers often sound clever but only ask nicely, or guard one door out of four. Ask who actually stops it. If the answer is "the model, if it feels like it", pick something else.

## What to Remember

- A **crossing rule** has three parts: what may cross, which component decides, and what happens to material that fails. No rule does not mean no edge. It means nothing gets checked, because no component thinks the check is its own.
- Interfaces start with different things in context before your text. The API is stateless and gives nothing. The SDK defaults to a minimal prompt for tool calling, while the coding preset adds full style, safety and working-directory context. Headless runs use that full prompt by default. Any rule your app depends on gets stated once per channel.
- Project instruction files enter as conversation context, not system prompt, and load by setting source, not preset. Two switches. Neither implies the other.
- Context shapes a decision. A deterministic gate removes it. Instruction files and collected notes are read as context and are never enforced configuration. To block an action whatever the model decides, use a hook or a check that runs first.
- Authority follows the channel content came through. Third-party material goes in tool results, labelled and delimited, with the policy in the system prompt. Keep your own instructions out of tool results, since content there is untrusted and may be ignored.
- Boundaries cover outbound traffic too. Regulated data shows up in message content, attached files, and filenames and metadata. It does not show up in workspace names, user contact details, billing or support tickets. Schemas are compiled and cached apart from messages and lack the same protections, so keep regulated values out of schema definitions.
- Geography has two settings: a per-request inference control with a workspace default, and a workspace location fixed at creation that never changes.
- A schema is a contract with the model, the consumer and the platform. Required properties are emitted first, then optional ones. Enum capitalisation is not guaranteed, so compare case-insensitively. SDK helpers strip constraints the platform does not support, and your validation enforces them instead. Strict tools, optional parameters and union types share one complexity budget, and the request fails when it is exceeded.
- A call carries one output contract. Stages judged by different success standards need separate calls and separate schemas. The cost case for merging leaves quality out.
- Continue picks by recency, resume by identifier, and fork copies a history into a new identifier. Wherever more than one conversation runs, identity must select the session, and only an identifier does that.
- Resuming brings back content, not posture. History, model and agent return. Plan and bypass permission modes never return, and launch-time configuration must be passed again. Session files are local to the machine that made them, so resuming on another host needs an external store.
- Three doors lead to a new conversation: the clock (idle or absolute age), an event (logout, completion, role change, unrecoverable error) and intent (the application deciding the request is new work). You need all three, since each covers a path the other two miss. A rule that needs the user to act is no guarantee.
- Ending a session leaves the transcript. Retention follows a documented default measured in years, or the organisation's configured period.
- An unpinned dependency follows latest, so upstream releases change what runs with no action and no record. Constraints intersect across everything that declares them, and a conflict gets reported, never quietly settled.
- To pin down blame you need a record made before the change. Pinning creates it, rollback is what it buys, and an unpinned component removes the ability to prove what broke.

**ELI5.** Draw the border, put a real gate on it and watch both directions. Write down the exact versions you use. Clear old chats three ways so nothing old leaks into something new.

## Endnotes for this chapter

1. The Messages API is stateless, so the full conversational history is sent on every request; a message with the system role may be placed after a user turn on supported models, carrying the same authority as the top-level system field, while the top-level field holds instructions applying from the first turn. Anthropic, *Using the Messages API* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/working-with-messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)

2. The Agent SDK's three starting points for a system prompt: a minimal default covering tool calling that omits Claude Code's coding guidelines, response style and project context; the `claude_code` preset carrying tool usage instructions, code style and formatting guidelines, response tone and verbosity rules, security and safety instructions and working-directory context, optionally with an appended addition; and a custom string, where only what is supplied is sent. Headless CLI runs use the full Claude Code prompt by default, which differs from the SDK's minimal default. The deciding factors for writing a custom prompt are a different surface, a different identity, a different permission model, or non-coding tasks where coding guidance competes with the needed instructions. CLAUDE.md content is injected into the conversation as project context rather than into the system prompt, and its loading is governed by setting sources rather than by the preset. Anthropic, *Modifying system prompts* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)

3. The CLI, desktop app, web version and editor extension each maintain their own session history; a resumed session restores conversation history including tool calls and results, the model, the configured agent and the permission mode, with plan and bypass modes never restored so the session resumes in the mode a new session would start in; command-line configuration for server configuration, settings files, plugin directories, fallback model and added directories must be passed again on resume, while standard settings files are re-read at launch; and a long-inactive, large session may be resumed from a summary because its prompt cache has expired. Anthropic, *Manage sessions* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/sessions](https://code.claude.com/docs/en/sessions)

4. CLAUDE.md files and auto memory are both loaded at the start of every conversation and are treated as context rather than as enforced configuration, with a PreToolUse hook named as the way to block an action regardless of what Claude decides; instruction files should target under `200` lines because longer files consume more context and reduce adherence; and specific, concrete, verifiable instructions are followed more consistently than general ones. Anthropic, *How Claude remembers your project* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

5. Untrusted third-party content should be delivered inside `tool_result` blocks rather than in system prompts or plain user text blocks; the tool description or result structure should make the nature and source of the content explicit; the system prompt should state that content returned from tools, documents or searches is untrusted data that must never override the system prompt or the user's request; untrusted strings should be JSON-encoded so escaping provides unambiguous delimiters; your own instructions should not be placed in tool results, because content there is treated as untrusted and may be ignored or flagged, and should be sent in a user turn following the result; tool outputs should be screened by a lightweight classifier call using structured outputs before being returned as results; and least privilege should be applied so a successful injection can do minimal damage, with sandboxed tools and narrowly scoped permissions. Anthropic, *Mitigate jailbreaks and prompt injections* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

6. Under a zero data retention arrangement, enabled per organisation, Anthropic does not store customer prompts or responses at rest after the API response is returned; HIPAA readiness requires a signed BAA and a HIPAA-enabled organisation and applies encryption, access controls and audit logging rather than immediate deletion; protected health information typically appears in message content, attached files and file names or metadata associated with message content, while workspace names, user information, billing data and support tickets are not expected to contain it; JSON schemas used for structured outputs and strict tools are compiled into grammars cached separately from message content and do not receive the same protections, so PHI must not be included in schema definitions; and local session transcripts are stored for six years by default or for an organisation's configured finite conversation retention period, with remote session transcripts retained for six years. Anthropic, *API and data retention* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/api-and-data-retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)

7. The `inference_geo` parameter controls where model inference runs for a specific request, with workspace settings restricting the available geographies and setting a default when the parameter is omitted; workspace geography is set when the workspace is created and cannot be changed afterwards; and regional inference is priced at 1.1 times the standard rate across all token pricing categories. Anthropic, *Data residency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/data-residency](https://platform.claude.com/docs/en/manage-claude/data-residency)

8. Structured outputs constrain responses to a schema using constrained sampling with compiled grammar artifacts; required properties are emitted first in schema order followed by optional properties, so schemas whose output order matters should mark all properties required or account for reordering; enum and const capitalisation is not guaranteed and a differing value completes normally with no error and no special stop reason, so enum values should be compared case-insensitively and values differing only in capitalisation avoided; SDK helpers transform schemas by removing unsupported constraints such as numeric and length bounds, moving them into the field description and adding `additionalProperties: false`, so the model receives a simplified schema while the code enforces the original constraints through validation; and complexity limits cap strict tools per request, total optional parameters and parameters using union types, with additional internal limits on compiled grammar size producing a `400` error when exceeded. Anthropic, *Structured outputs* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/structured-outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

9. Continue picks up the most recent session in the current directory with no identifier tracked, while resume takes a specific session ID and is required for multiple sessions such as one per user; forking creates a new session starting from a copy of the original's history with its own session ID, leaving the original's ID and history unchanged; session IDs are read from the result message; and session files are local to the machine that created them, so resuming on another host requires a session store adapter whose lookup key derives from the working directory. Anthropic, *Work with sessions* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

10. By default a plugin dependency tracks the latest available version, so an upstream release can change it without warning; a version constraint holds a dependency at a tested range until the dependent plugin publishes a new version with a wider constraint; where several installed plugins constrain the same dependency the ranges are intersected and resolved to the highest version satisfying all of them, and when no version satisfies every range the update is skipped and reported with the constraining plugin named; constraints resolve against git tags on the repository hosting the dependency, tagged as the plugin name paired with the version and matching the manifest version at that commit, with non-git sources checked at load time and the dependent plugin disabled when unsatisfied; auto-update is off by default for non-Anthropic marketplaces; and a dependency in a different marketplace from the plugin declaring it is refused unless the root marketplace names the target in its allowlist, with trust not chaining through intermediate marketplaces. Anthropic, *Constrain plugin dependency versions* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/plugin-dependencies](https://code.claude.com/docs/en/plugin-dependencies)

11. A plugin manifest defines the plugin's identity through its name, description and version; plugin skills are always namespaced with the plugin's name as the prefix so that plugins shipping identically named skills do not collide, and changing the name field changes that prefix. Anthropic, *Create plugins* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
