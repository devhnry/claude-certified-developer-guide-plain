# Chapter 16: Boundaries, Sessions, and Where Instructions Land

**Summary**: *An application has an edge (a border) from the moment it exists. It is the place where material stops belonging to your application and starts being read by a model. If you never draw that border, it is still there, and nothing is checked at it, because every component assumed the next one was looking. This chapter draws the border five times. First, what the interface already placed in front of your instruction. Second, what may cross in either direction. Third, what shape an answer has to hold to be used. Fourth, when a conversation gets cleared. Fifth, which version of the machinery is running. Get any one of them wrong and you see the same symptom.*

## Every Application Has an Edge, and It Exists Before Anyone Draws It

**First, the idea.** Every application has a place where its own material ends and the model's reading begins. We will call it the **edge**. Think of it as a border between two countries. The rest of this chapter keeps that picture.

**The picture.** Your application is one country. The model is the country next door. Goods (the **material**) cross the border in both directions. The border post is the **edge**. The customs rules are the **crossing rule**. The officer who applies the rules is the **single component that decides**. Goods that get turned back are the **material that fails** the check. One honest limit on the picture: the officer is not a clever person who can be talked round. In this chapter the officer is a component, and the best kind is code that always does the same thing.

**What crosses the border.** Something goes in. It might be a **ticket body**, a **fetched page**, a **customer record**, or a **schema** (a description of what shape the answer has to have). Something comes back out and lands somewhere that acts on it. That could be a database write, a rendered reply, or a call to a service that trusts what it was handed.

**Where the border is.** Between those two moments there is a place where material stops belonging to the application and starts being read by a model. That place exists from the first request anybody sends. Nobody has to design it. Designing it is what makes it checkable.

**The problem: a border nobody drew.** An edge nobody drew is not an edge that is missing. It is an edge where nothing gets checked, because no component believes the check belongs to it. Each piece passed its own tests. The seam between them was never anybody's test.

**What to write down.** Three things have to be written down before an edge becomes a **crossing rule**:
- what is **permitted to cross** (what the customs rules allow)
- which **single component decides** (which officer stands at the post)
- what happens to **material that fails** the decision (what happens to goods turned back)

Here is what goes wrong if you skip one:
- Drop the third and the arrangement still reports honestly and still lets everything through. That is because logging a violation and stopping one are different features.
- Drop the second and the check gets implemented twice, differently, and the two copies drift. No human owns a shared check, so nobody writes one.

**Five design areas.** The blueprint (the exam outline) names **five design areas** for a Claude application. All five are the same question aimed at different traffic.

| Design area | What it settles about the edge |
|---|---|
| Interface | What already sits inside the boundary before your instruction arrives |
| Content boundaries | What is allowed to cross, inbound and outbound, and who checks |
| Schema | The shape material has to hold to cross outward and be consumed |
| Session hygiene | When everything inside the boundary is cleared, and on what trigger |
| Plugin management | Which version of the machinery around the edge is currently running |

Read that table as one subject, not five. A defect in any row shows up as the same symptom. Material crossed, and nothing stopped it.

**ELI5.** Every app has a border where its own stuff meets the model. If nobody guards the border, everybody thinks someone else is guarding it. So you write down what may cross, who checks, and what happens to things that fail.

## The Same Instruction Arrives Into a Different Standing Context on Every Interface

**First, the idea.** The same sentence of guidance can behave differently depending on how you send it. That happens because each **interface** (API, SDK, terminal and so on) has already put different things in front of the model. In our picture, each interface is a different border post. Each one already has its own pile of papers waiting on the other side before your goods arrive.

**The problem.** Write one sentence of guidance. Send it through the API. Send the identical sentence through the SDK, then type it into the terminal. Three different behaviours are a normal outcome. No interface is broken.

**Why.** Your sentence is never the whole instruction. It joins whatever the surface already put in front of the model. The surfaces differ a lot in how much that is. Your text is the last layer.

**The Messages API supplies nothing.** The **Messages API** is **stateless** (it remembers nothing between requests). So every request carries the full conversational history explicitly. Anything not written into that request is absent.<sup>[1]</sup> No project file loads. No standing preference persists. Your code is the only thing that remembers anything.

**The SDK is where the surprise usually lands.**
- With **no system prompt configured**, the SDK runs a **minimal default**. It covers tool calling. It leaves out Claude Code's coding guidelines, its response style and its project context.
- Ask for the **`claude_code` preset** instead and the model receives the full prompt the CLI uses. That means tool usage instructions, code style and formatting rules, tone and verbosity, security instructions, and context about the working directory.
- **Headless CLI runs** use that full prompt by default. That is exactly why an instruction that behaved one way under `claude -p` behaves another way under a bare SDK call.<sup>[2]</sup>

Same words, different standing prompt, and no error anywhere.

**Project context arrives on a separate track.** `CLAUDE.md` is injected into the conversation as project context. It is not put into the **system prompt**. So it works together with whichever prompt was chosen. It loads according to the configured **setting sources**, not according to the preset.<sup>[2]</sup> That makes two independent switches. A design that assumes one implies the other will be wrong on half its deployments. Set both on purpose.

**Interactive surfaces keep their own histories.** The CLI, the desktop app, the web version and the editor extension each keep a **separate session store**.<sup>[3]</sup> "The conversation" is not one object that the user moves between windows. Each window keeps its own, and none of them syncs.

| Surface | What is already in context before your text | Who holds the history |
|---|---|---|
| Messages API | Only what the request contains | Your application, entirely |
| Agent SDK, unconfigured | A minimal prompt covering tool calling | The SDK, per session ID |
| Agent SDK with the coding preset | Full coding guidance, style, safety, working directory | The SDK, per session ID |
| Headless CLI | The same full prompt, by default | Local transcript files |
| Interactive surfaces | That surface's own configuration and project files | That surface, separately from the others |

**What to do.** The design consequence is narrower than "test on every interface", which is advice nobody can act on. A rule your application depends on has to be stated where the interface will actually read it, and the interfaces read different places. For example:
- A constraint that lives in a project file is invisible to an API integration that never loads project files.
- A constraint written into a system prompt string is absent from a terminal session that uses the preset.

So behaviour that is meant to hold everywhere gets stated once per channel, on purpose. That statement is part of the application. It is not part of somebody's local setup.

**When to write your own prompt.** Anthropic has its own test for whether a custom prompt is warranted. It is worth borrowing as a design question, because it is about the product, not the prose. The further your agent sits from a coding assistant working in a repository with a human watching and steering, the more of the standing prompt you should write yourself. Four signs:
- a **different surface**, where output is not read in a terminal
- a **different identity**, which should not present as a coding tool
- a **different permission model**, where nobody approves each step
- work that is **not coding at all**, where coding guidance competes with the instructions you need<sup>[2]</sup>

**The anti-pattern: the instruction inherited by accident.** Somebody prototypes against the preset and likes the behaviour. Then they ship an integration that supplies its own prompt. Half the behaviour they liked came from the preset and is now gone. The symptom is a quality complaint, not an error. Nobody removed anything on purpose, which is why the loss is hard to trace.

**ELI5.** Each way of talking to Claude has already put a different pile of papers in front of it before your note arrives. So the same note can get a different answer. Write down the rules you need in every place Claude will look.

## Context Shapes a Decision; Only a Deterministic Gate Removes One

**First, the idea.** Words you put in front of the model can nudge what it does. Only code that runs before an action can stop the action. In our picture, a notice pinned up at the border asks goods to behave. A barrier that physically will not lift is different.

**Memory is read as context.** Both of Claude Code's **memory systems** load at the start of every conversation. One is the files you write. The other is the notes it builds up. Both are read as context, not as enforced configuration. To block an action regardless of what the model decides, the documentation points at a **pre-tool hook** instead.<sup>[4]</sup>

**The general rule.** That distinction applies well beyond any one product.
- Text that reaches the model **influences a decision**.
- Code that runs before the action **removes the decision**.
- Everything on the first side works in degrees. It is probabilistic. Everything on the second side either runs or does not.

Only one of them binds.

**What this means for a crossing rule.** A crossing rule written only as a sentence in a prompt is a **preference with good adherence** (the model usually follows it). It belongs in the prompt as well, because a model told what the policy is behaves better than one left to guess. But it cannot be the only place. The exam tests exactly this. An option that improves how reliably an instruction is followed is not an option that guarantees anything.

**Adherence is still worth working on.**
- Specific, concise, well-structured instructions are followed more consistently than long ones.
- The documented sizing guidance is blunt. Keep a project instruction file under about **200 lines**, because a longer file uses more context and reduces adherence.<sup>[4]</sup>
- Concreteness is the other half. A rule stating which directory handlers live in is checkable by a human reading the output. A rule saying to keep files organised is not.

**ELI5.** A sign on the wall asking people to behave works most of the time. A locked door works every time. If something must never happen, use the locked door. Use the sign as well, because it helps.

## Content Boundaries Run in Two Directions, and the Outbound One Gets Forgotten

**First, the idea.** Content can cross the border coming in, and it can cross going out. Everybody designs for coming in. Going out is where reviews fail.

**Inbound: untrusted material reaching the model.** This is a documented threat with documented handling. The steps are:
- Deliver **third-party content** inside **`tool_result` blocks**. Do not put it in system prompts or plain user text.
- Say in the **tool description** what the content is and where it came from.
- State in the system prompt that tool and document content is data that **never overrides instructions**.
- **Wrap third-party strings in JSON**, so an attacker cannot close a delimiter (the marker that ends a piece of text) and carry on as an instruction.<sup>[5]</sup>

Chapter 5 covers where those blocks sit in a prompt. Chapter 20 covers the attack itself. What matters here is the placement rule read as a design constraint, not as a security tip. The channel a piece of content arrives on is what sets its authority. So a component that joins fetched text onto a standing instruction has promoted it, whatever anybody intended.

**Two more inbound rules, easy to get backwards.**
- Your own **instructions do not belong in tool results**. Content there is treated as untrusted, so guidance placed in a result may be ignored or flagged. Send it in the **user turn that follows** the result instead.<sup>[5]</sup>
- **Screening runs on tool output** as well as on user input. That means a **small classifier call** (a quick extra check by a model) over what the tool returned. It gives a **parseable verdict** that the application branches on. This happens before the content is handed back as a result at all. Screen both directions, because only one of them looks dangerous.<sup>[5]</sup>

**Outbound: material leaving your perimeter.** Outbound is the direction that fails a review. Material crossing to the model leaves whatever perimeter it was sitting in. The properties of the receiving side are a design input, not a purchasing detail. Ask before you build.

| Outbound question | What settles it | What it constrains |
|---|---|---|
| Is anything kept after the response returns | A zero-retention arrangement, enabled per organisation | Whether prompts and responses persist at rest at all<sup>[6]</sup> |
| Is health information in scope | A signed agreement and a readiness-enabled organisation | Which features may carry it, and what safeguards apply<sup>[6]</sup> |
| Where does inference physically run | A per-request geography parameter, or a workspace default | Which regions may serve the request, at a stated price multiplier<sup>[7]</sup> |
| Where is the workspace itself | Chosen at creation and not changeable afterwards | A decision you make once, before there is an application<sup>[7]</sup> |

**Two details that decide exam scenarios.**

*First: where regulated content actually turns up.* It shows up in **message content**, in **attached files**, and in **file names and metadata** tied to message content. Workspace names, user contact details, billing data and support tickets are **not expected to carry** it.<sup>[6]</sup> Suppose you draw a boundary around "the prompt" and not around the filename of the attachment. Then it is drawn in the wrong place. Metadata travels with the file, and the rule has to cover it. In our picture, it is like checking the crate but not the label stuck on the outside.

*Second: a genuine trap.* It sits where this chapter's two halves meet. Schemas sent for constrained output are **compiled and cached separately** from message content. Those cached schemas do not get the same protections as prompts and responses. So **regulated content must not appear in a schema definition**.<sup>[6]</sup> Field names and descriptions feel like configuration, not data. That is why somebody eventually writes a patient identifier into an enum (a fixed list of allowed values). Schemas are data too.

**Least privilege.** This is the last rule, and it applies in both directions at once.
- **Scope what the model can reach**, so a successful injection has little to work with.
- Run tools in **sandboxed environments**.
- Keep secrets it does not need out of its reach entirely.<sup>[5]</sup>

A boundary that permits everything through is still a boundary. It is just one where the crossing rule reads "anything".

**ELI5.** Guard the border in both directions. Things coming in might be tricks. Things going out might be private. Check the crate and the label on it, and give the model only the keys it really needs.

## The Schema Is a Contract With Three Parties, Not Just With the Model

**First, the idea.** A **schema** looks like a formatting preference. It is really a contract. Three parties depend on it, and each one cares about different things. In our picture, a schema is a customs form that the officer, the receiving warehouse and the shipping company all have to read the same way.

**Three parties, one document.** A schema attached to a request binds in three directions at once:
- the **model** is constrained by it
- **downstream code** is written against it
- the **platform** compiles it into something with properties of its own

**The mechanism.** **Constrained sampling** (the model can only produce text that fits the schema) uses **compiled grammar artifacts** built from the schema.<sup>[8]</sup> That has consequences no prompt-level formatting request has. They are design consequences, not runtime ones.

**Property order is not schema order.** **Required properties appear first**, in the order the schema gives them. **Optional properties follow**. If output order matters to a consumer, either mark everything required or write the parsing so reordering is expected.<sup>[8]</sup> A consumer that reads by position breaks the first time somebody makes a field optional. Read fields by name, never by position.

**Enum values may not match your capitalisation.** The response completes normally. It raises no error and carries no special stop reason. The value just differs from the schema in a capital letter. So compare case-insensitively, and never define two enum values that differ only in case.<sup>[8]</sup> This surfaces in a downstream branch that checks for exact string equality, several stages away from the request. Lowercase both sides before comparing, and that whole class of defect disappears.

**The schema the model receives may not be the one you wrote.** **SDK helpers strip features** the platform does not support. They add the constraint to the field's description instead, and they close objects to additional properties. So numeric and length bounds are **enforced by your validation**, not by the grammar.<sup>[8]</sup> The contract is still honoured. It is honoured in two places, and only one of them is the model.

**Complexity is a budget with a hard edge.** There are documented ceilings on three things:
- how many **strict tools** one request may carry
- **optional parameters** across all schemas in the request
- parameters with **union types** (a field that can be one of several types). These are the expensive ones, because they multiply compilation cost.

If you go past the compiled size, the request **fails outright** with a **complexity error**, even when every individual limit was met.<sup>[8]</sup> So schema design is a shared resource across a request. It is not a per-field decision. Budget it across the whole request.

**One call carries exactly one output contract.** This is the point scenarios test hardest. Say a system does two things that are judged differently. One is a classification, where success means the right category. The other is a drafted reply, where success means an acceptable answer. Those are two contracts, and one call cannot hold both. The usual argument for merging them is cost. That argument only holds while quality is left out of the comparison. Separate calls give each stage three things:
- a **schema shaped for its own output**
- a **prompt aimed at one job**
- an evaluation against the standard that actually applies to it

**The named failure: the schema written for the model alone.** It describes what a good answer contains. It reads beautifully. It never asked the consumer what it needs to do with the result. Then somebody adds a field, the parser keeps working because the parser was lenient, and a downstream service quietly receives a shape nobody agreed to. Chapter 6 covers validating what comes back. The design duty here comes earlier. Write the schema from the **consumer's requirements**, and change it on the **consumer's schedule**. Ask the consumer first.

**ELI5.** A schema is a form that three people have to read the same way: the model, the program that uses the answer, and the platform. If you design the form only for the model, the other two get surprised. So ask the person who uses the answer what they need, and keep one job per form.

## Continue, Resume and Fork Answer Different Questions About Whose History You Get

**First, the idea.** The SDK gives you three ways to get back into an existing conversation. They differ in how the session is found. In our picture, a session is a case file kept at the border post. The three ways are three different ways to pull a file.

**No interface defines a session for you.** The API has no such concept, because every request carries its own history. The SDK gives you **three ways** to reach an existing session. They differ in how the session is found, not in what they do afterwards.
- **Continue** picks up the **most recent session** in the current directory. Nothing has to be tracked.
- **Resume** takes a **specific identifier** that your application captured and stored. This is what multi-user applications need.
- **Fork** copies an existing history into a new session with a new identifier. The original's history is left untouched. So two independent threads exist afterwards.<sup>[9]</sup>

**The access-control problem.** Read those definitions as an access-control question and one of them becomes alarming. "The most recent session in this directory" is not the same statement as "this user's session". In a service handling several conversations at once, continue resolves by recency, not by identity. This is the shape of defect an exam will describe. Context from one conversation shows up in an unrelated one, and there is no bug anywhere in the code. Identity has to select the session, and only an identifier does that.

**Session files are local.** Session files are local to the machine that created them. So an application running on ephemeral workers or containers cannot resume by identifier alone. Attaching a **session store** mirrors transcripts to your own backend. The lookup key comes from the **working directory**, so a resuming host has to match the directory the original run used.<sup>[9]</sup> That is a deployment constraint hiding inside a conversation feature. Transcripts do not travel, and neither does the assumption that they do.

**Resuming restores less than people assume.** The gaps are deliberate.
- Conversation history returns in full.
- The model and the configured agent return.
- The **permission mode returns**, with named exceptions. **Plan mode** and a **bypass mode** are never restored. A resumed session starts in the mode a new session would.
- Command-line configuration passed at launch has to be passed again. That includes settings files, server configuration, plugin directories and added directories. The standard settings files are re-read on their own.<sup>[3]</sup>

Pass your launch flags again.

**The pattern.** Content is restored and posture is not. Posture means anything that widens what the session may do. That gets re-established on purpose at launch. This is the right default. It also explains two surprises:
- An operator who resumed and assumed their elevated mode came back is running with **less authority** than they think.
- An application that resumed and assumed its flags came back is running with **less configuration** than it needs.

So re-establish posture at launch, explicitly, every time the session comes back.

**ELI5.** A conversation is a folder. Continue grabs the newest folder. Resume grabs the folder with the name you wrote on it. Fork photocopies a folder so you have two. If lots of people use your app, always ask for the folder by name, or you will hand one person another person's papers.

## Three Doors Lead Into a New Conversation, and a Timeout Closes Only One

**First, the idea.** Old material turning up in a new conversation is what this whole area exists to prevent. There are three separate ways a conversation can end. A timeout covers only one of them. In our picture, this is about when a case file is closed and the desk cleared at the border post.

**The failure.** **Stale context leaking** into an unrelated conversation has a specific shape. Material that was correct for a finished task turns up in a task that has nothing to do with it. It is phrased confidently. It comes from nothing the current user said. Nobody typed it.

**Why one timeout is not enough.** A single timeout is the usual proposed fix, and it is half an answer. There are three separate ways a conversation ends, and each one lets through material that the others catch.

| Door | What triggers it | What it fails to cover alone |
|---|---|---|
| The clock | Idle time, or an absolute age since the session started | A session in continuous use that changed subject an hour ago |
| An event | Logout, a completed transaction, a role change, an error the application cannot recover | Nothing at all happening for a long stretch between events |
| Intent | The application deciding this request begins new work, or the user saying so | Anything the user does not think to ask for, since the guarantee then rests on their behaviour |

**Look hard at the third row.** It is the one that gets offered as sufficient. Handing the reset to the user makes the property depend on a human remembering. Guarantees do not live in habits.

**What a defensible answer looks like.** All three together:
- **expiry**, so an abandoned session cannot live forever
- **reset triggers**, so defined events clear state the moment they happen
- **fresh-start rules**, so the application itself knows when a request is new work and not a continuation

Each door closes a path the other two leave open. That is why the arithmetic here is addition, not selection.

**Two operational facts sit under the design.**
- **Transcripts are retained.** The documented default is measured in years. Or it is whatever finite retention period an organisation has configured. So "the session ended" and "the material is gone" are unrelated claims.<sup>[6]</sup>
- A long-idle session that is picked up again may be **restored from a summary** instead of in full. That is because the cache behind it has expired. So the continuity a user feels and the tokens actually resent are two different things.<sup>[3]</sup>

Deletion is a separate question with a separate answer.

**The named failure.** It is the session that ends only when somebody closes the tab. That is not a missing feature. It is a feature that was never specified, so the default became whatever the interface happened to do.

**ELI5.** A conversation can end in three ways: the clock runs out, something important happens, or someone says "this is new work". Any one alone leaves a gap. So use all three. And remember that closing the conversation does not mean the record is thrown away.

## Plugin Versions Are Pinned So a Regression Has Somewhere to Land

**First, the idea.** The last area is the machinery around the edge, such as plugins. It changes by itself unless somebody stops it. In our picture, these are the tools and staff at the border post. If the supplier swaps them overnight, you will not know which one changed.

**The default.** This is the part worth memorising. A declared dependency (a plugin your plugin needs) **tracks the latest** available version. So an upstream release changes what is running under your extension. You get no action, no notification and no record on your side.<sup>[10]</sup> Nothing failed. The set of things running just is no longer the set that was tested.

**A version constraint turns that into a decision.** Hold a dependency inside a **tested range** and installs stay on the **highest matching patch**. The upgrade moves to a moment somebody chose, by publishing a new version with a wider range.<sup>[10]</sup>

**Several constraints intersect.** When several constraints sit on the same dependency, they intersect. The result is the highest version that satisfies all of them. When nothing satisfies every range, the **update is skipped and reported**, with the constraining extension named.<sup>[10]</sup> A conflict shows up as a conflict, not as odd behaviour.

**How it resolves.**
- Resolution runs against **tags** on the repository holding the dependency. The tag follows a **naming convention** that pairs the plugin name with the version. That version is expected to **match the manifest** at that commit.<sup>[10]</sup>
- **Automatic updating is off by default** for marketplaces Anthropic does not operate.
- A dependency living in a different marketplace from the extension declaring it is **refused by default**. It is opened only by an allowlist on the marketplace hosting the extension being installed. Trust deliberately does **not chain through intermediates**.<sup>[10]</sup>

Both defaults are crossing rules with a default already chosen. Trust is declared, never inherited.

**What belongs to design.** Chapter 18 covers versioning as an operational practice. What belongs to design is narrower, and it is a single duty: **attribution requires a record made before the change**. A regression can be traced to a component only if what that component was is written down somewhere that predates the symptom. Pinning is how the record gets made. **Rollback** (going back to the last good version) is what the record buys. An unpinned dependency does not just risk breaking. It removes the possibility of proving what broke.

**A packaging detail that matters for design.** A bundle's name is a **prefix on every command** it ships. That is what lets two bundles ship the same command name without colliding. Renaming the bundle renames all of them.<sup>[11]</sup> The name is part of the interface. So it is chosen once, early, by somebody thinking about the interface and not about the directory.

**The anti-pattern: the dependency that tracks latest.** It is almost never a decision. It is the absence of one, wearing the look of staying current.

**ELI5.** If your tools update by themselves, one day something breaks and you cannot tell which tool changed. So you write down the exact version you tested and only change it on purpose. Then you can always go back to the one that worked.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers on application design are unusually convincing, because most of them describe real engineering that a competent team does. What makes one wrong is a single assumption sitting under it. Four assumptions produce most of them.

**The four wrong assumptions:**
- **A guarantee claimed for a mechanism that only improves adherence.** An option strengthens a written instruction, restructures a prompt, or adds guidance about what the model should refuse. It answers a scenario asking that something never happen. But instructions shift probability. Code that runs before the action decides. Whenever the requirement contains the word "never", ask which component would have to fail for the outcome to occur. Then pick the option that names one.
- **One control offered against a failure with several entrances.** Examples are a timeout aimed at stale context, a screen on user input while tool output goes unchecked, or a check at one seam in a system with four. The option is correct about the path it covers and silent about the rest. That is what makes it read as an answer. A scenario naming several ways in wants a set, not a pick.
- **A boundary drawn around the obvious payload and not around its neighbours.** Prompts get protected while attachment filenames, schema definitions, cached artifacts and transcript retention go unconsidered. Ask what else travelled with the content, and what is stored that is not the content.
- **Enforcement placed where the habit is, not where the authority is.** Examples are instructions written into tool results, standing rules appended to the newest turn, a policy documented for humans and checked by nobody, and a session that resolves by recency where identity was required. Each one puts the control on a channel that carries no weight. Name the channel each option acts on. Then ask whether that channel binds anything.

Match on what the scenario is doing, not on the domain it is dressed in.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Context from a finished conversation surfaced in an unrelated one | Expiry, defined reset events, and application-owned rules for starting fresh, together | A single timeout, or asking users to start a new conversation themselves |
| The same guidance behaves differently in the terminal and in an integration | State the rule on the channel each interface actually reads | Treating one surface's default context as if every surface supplied it |
| A requirement says an action must never be possible | A deterministic check that runs before the action | Stronger wording, more emphasis, or a better-written instruction file |
| Fetched or third-party content reaches the model | Deliver it as tool results, labelled, delimited, and screened before it is returned | Concatenating it into the standing instruction so the model definitely sees it |
| Two stages have different inputs, outputs and standards of success | Separate calls, each with its own contract and its own evaluation | One call for both, argued on token cost with quality left out |
| Downstream consumers keep breaking on well-formed output | Write the schema from what the consumer needs, and version it on the consumer's schedule | A schema describing a good answer, with parsing loosened until it passes |
| Regulated or sensitive data is in scope | Ask where it appears, including filenames, metadata and schema definitions | Protecting message bodies alone and treating configuration as out of scope |
| A behaviour changed and nobody can say which component moved | Pinned versions recorded before the change, giving a rollback target | Reproducing it, adding logging, or updating everything to current |
| Where processing physically happens is a requirement | The geography controls, chosen against a decision that may be unchangeable later | Treating placement as an operational detail settled after the build |
| Sessions are resumed on a different machine or worker | External session storage, keyed consistently, with identity selecting the session | Resuming by recency, or assuming a local transcript is reachable elsewhere |

**One habit that works past the table.** For every option, ask what would have to be true for the guarantee to hold. Then ask who checks it. If the answer to the second question is the model, the option is describing an improvement, not a control.

**ELI5.** Wrong answers sound sensible but fix only part of the problem. They ask the model nicely when you needed a locked door. Or they guard one gate when there are four. Always ask who really checks, and whether it is code or the model.

## What to Remember

- A **crossing rule** names three things: what may **cross**, which **component decides**, and what **happens to material that fails**. An edge with no rule is not an absent edge. It is one where **nothing is checked**, because no component believes the check is its own.
- **Interfaces differ in what already sits in context** before your text arrives. The **API is stateless** and supplies nothing. The **SDK defaults to a minimal prompt** covering tool calling, and the **coding preset** carries full style, safety and working-directory context. **Headless runs use that full prompt by default**. A rule the application depends on is **stated once per channel**.
- **Project instruction files load as conversation context**, **not as system prompt**, and they load by setting source, not by preset. Two switches, and neither implies the other.
- **Context shapes a decision**. A **deterministic gate removes one**. Instruction files and accumulated notes are **read as context, never as enforced configuration**. So blocking an action regardless of what the model decides needs a **hook or a check that runs first**.
- **Authority follows the channel content arrived** on. Third-party material belongs in **tool results, labelled and delimited**, with the policy stated in the system prompt. Your **own instructions do not belong in tool results**, because content there is treated as untrusted and may be ignored.
- **Content boundaries run outbound too**. Regulated data appears in **message content, attached files, and filenames and metadata**. It does **not** appear in workspace names, user contact details, billing or support tickets. **Schemas are compiled and cached separately** and do **not** carry the same protections, so no regulated value goes in a schema definition.
- **Geography is two settings**. One is a **per-request inference control** with a workspace default. The other is a **workspace location fixed at creation** that cannot be changed afterwards.
- A **schema is a contract** with the **model, the consumer, and the platform**. **Required properties are emitted first**, then optional ones. **Enum capitalisation is not guaranteed**, so compare case-insensitively. **SDK helpers strip unsupported constraints** and enforce them in your validation instead. **Strict tools, optional parameters and union types** share **one complexity budget** that fails the request when exceeded.
- **One call carries one output contract**. Stages judged by different standards of success need **separate calls with separate schemas**. The cost argument for merging them leaves out quality.
- **Continue resolves by recency**, **resume resolves by identifier**, and **fork copies a history** into a new identifier. In anything serving more than one conversation, **identity must select the session**, which only an identifier does.
- **Resuming restores content, not posture**. History, model and agent return. **Plan and bypass permission modes never** do, and **launch-time configuration must be passed again**. **Session files are local to the machine** that made them, so cross-host resumption needs an external store.
- **Three doors lead into a new conversation**: the **clock** (idle or absolute age), an **event** (logout, completion, role change, unrecoverable error), and **intent** (the application deciding the request is new work). **All three are required**, because each covers a path the other two leave open. A **rule that depends on the user acting** is **not a guarantee**.
- **Ending a session does not delete the transcript**. Retention runs on a **documented default measured in years**, or on the organisation's configured period.
- An **unpinned dependency tracks latest**, so upstream releases change what is running with **no action and no record**. **Constraints intersect** across everything that declares them, and a **conflict is reported, not silently resolved**.
- **Attribution requires a record made before the change**. Pinning creates it, **rollback is what it buys**, and an unpinned component removes the ability to prove what broke.

**ELI5.** Your app has a border, and you must guard it on purpose. Write down what may cross and who checks. Use real locks for "never" and signs for "please". Ask for conversation folders by name, clear the desk in three ways, and write down which tool versions you tested.

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
