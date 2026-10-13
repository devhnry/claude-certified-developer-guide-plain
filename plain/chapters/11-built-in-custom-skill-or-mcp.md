# Chapter 11: Four Mechanisms, Decided by What Must Execute

**Summary**: *A new capability arrives and four mechanisms (four ways to package it) are offered. At least three of them would work. That is the difficulty. Any rule that starts "always prefer" has stopped reading the requirement. What fits is decided by the thing being packaged, never by a ranking of the packages. Two questions decide nearly every case. Does the work have to reach a live system? And how many consumers are there? This chapter teaches those two questions, what each mechanism costs, and the loading rules that decide whether a package runs on somebody else's machine. The picture to hold is a restaurant kitchen: the recipe card (the Skill), the appliance the landlord runs (the built-in tool), your own gadget (the custom tool), and the shared supplier counter (the protocol server).*

## Four proposals arrive for one capability, and none of them is absurd

**First, the idea.** Four sensible mechanisms are offered for the same job. You cannot rule any out by spotting something silly. So the chapter teaches how to tell them apart by what the job needs.

**The picture: a restaurant kitchen.** You run a kitchen. A new dish has to come out the same way every time. These are the four ways to deliver it:
- A **Skill** (a recipe card). It tells the cook how to make the dish. It does not fetch ingredients.
- A **built-in tool** (an appliance the landlord already installed and runs). You just press the button.
- A **custom tool** (a gadget you build and keep in your own kitchen). Only your kitchen uses it.
- A **protocol server** (a shared supplier counter that several restaurants order from). It takes effort to set up and keep running.

**The example.** The **month-end reconciliation write-up** has to come out the way the **finance team produces** it. **Fixed section order**. **Wording nobody improvises**. A checklist run before it goes anywhere.

**Four proposals reach** the meeting:
- Reach for a **built-in tool**, since Anthropic already ships one that runs code.
- Define a **custom tool** in the application, since that is where every other capability lives.
- Package the whole procedure as a **Skill**.
- Stand up a **protocol server**, since **two other teams** will want this by spring.

Every one of those is **real engineering**, and somebody **shipped** each of them this quarter. Ruling options out as **obvious nonsense** returns nothing here. All four **survive a first read**. That is why the material is worth a chapter.

What separates them is **fit**. Fit is decided by two **properties of the capability**. Neither is a property of the mechanisms.

**ELI5.** Four people each offer you a way to make the same dish. All four ways work in some kitchen. So you don't ask "which way is best?" You ask what this dish needs.

## The execution question comes first, because it removes two options at once

**First, the idea.** Before you compare anything, ask one thing. Does this capability have to **reach a live system**, or is it just **knowledge** about how to do the work? The answer sorts the options.

**The execution question.** Does this capability have to **reach a system** that holds **live state** and **authenticates its callers** (checks who is asking)? Or is it **knowledge** about how work gets done?

**Procedure is the knowledge kind.** A section order, a template, a house convention, a review checklist, the three things humans always forget. **None of it calls anything**. It is **expertise written down**, like a recipe card. The mechanism built to carry that is a **Skill**. A Skill is a directory holding:
- a **`SKILL.md` file** with **YAML frontmatter** (a small header block of settings at the top of the file)
- a body of instructions
- whatever **templates and scripts** the procedure needs beside it<sup>[1]</sup>

**Live access is the other kind.** A balance that changed this morning. A record only certain callers may read. A write that has to land. A recipe card cannot go and get today's ingredients. In the same way, **prose describing an endpoint** (an address a program can call) cannot **make a request** to it. It also **drifts from the endpoint**, and nothing in the system can notice.

**The mirrored error.** The reverse mistake is more tempting. It is to serve a **procedure over a protocol**. Standing a server in front of static instructions is like building a supplier counter just to hand out recipe cards. It buys a **network hop** (an extra trip over the network) and no capability the instructions did not already have.

**A nuance that keeps the rule honest.** A Skill may **bundle executable scripts**, and the runtime does run them.<sup>[1]</sup> But that does not give the Skill **reach**. Through the API a Skill runs inside the **code execution container**. That container is sandboxed, with **no network access** and **no runtime package installation**.<sup>[1]</sup> So a bundled script is **deterministic local work** (the same result every time, done on the spot). It is not a route to a production system.

**ELI5.** Is the job "follow these steps" or "go and get something real"? Steps go on a recipe card. Getting real things needs a way to reach the shop. A recipe card, even a clever one, cannot walk to the shop.

## A built-in tool is capability Anthropic already operates

**First, the idea.** Once something has to execute, **three mechanisms are left**. The cheapest definition is the one you never write, so check what **already exists** first.

**Built-in is not one thing.** The split matters more than the label. **Tools differ by where the code runs**:
- **Server tools** include web search, web fetch, code execution and tool search. They **run on Anthropic's infrastructure** (the landlord's own appliance). The call and its result both arrive in the response. **No handler** (no code of yours) in the application executes anything.<sup>[2]</sup>
- Other built-ins, **bash and the text editor** among them, come with a **schema Anthropic publishes** (a written description of the tool's inputs) and trains Claude against. But the **application still runs** the operation and returns the result.<sup>[2]</sup> Anthropic wrote the manual. You still do the cooking.

**What you give up: ownership.** A built-in **buys a definition**, and sometimes an implementation. What it costs you is **ownership**. Chapter 9 put validation, the approval gate and the audit record at dispatch (the moment a tool call is handed off to run). For a **server-executed tool** there is **no dispatch** on a machine you control. That is the tradeoff to carry into a scenario. A built-in is right where the capability is **generic** and the **governance** (who approves it and who can check it) is not the point. It is wrong the moment a **human has to answer** for what ran.

**The anti-pattern: wrapping a built-in to make it shareable.** The failure is specific. The wrapper **lives inside one application**. So other teams reach neither the wrapper nor the reason it was written.

**ELI5.** Some appliances are already in the kitchen and the landlord runs them. They are free to use. But if the health inspector asks who did what, you cannot answer for work you never saw.

## The consumer count decides between a private function and a protocol

**First, the idea.** **Two mechanisms remain**, a custom tool and a protocol server. They do the same kind of thing. The question that separates them is **not technical**. It is **how many applications need it**.

**One application: a custom tool.** You have **one application**, a **narrow operation**, and an **input contract** (the exact inputs it takes) you already know. That is a **custom tool**, defined where the application lives. In the **Agent SDK** it has **four parts**:
- a name
- a description
- an input schema
- the handler that runs

The server carrying it **runs inside your application** rather than as its own process.<sup>[3]</sup> So there is **no deployment**, **no transport** decision (how messages travel), and **no second thing** to version. It is a gadget in your own kitchen.

**Several applications: a protocol server.** You have **several applications**, released on **schedules none of them share**. That is a **protocol server**. Chapter 10 covered what one exposes and where it runs. What belongs here is the arithmetic. A server is **machinery for reuse**. The machinery **gets paid** for whether or not anybody reuses it. You pay for:
- a process to deploy
- a transport to pick
- an interface to hold still while its callers move

Buy that for **one consumer** and the **bill arrives** with nothing on the other side of it.

**The same arithmetic, the other way.** Run it in the opposite direction and **two comfortable answers** stop working:
- **The copied implementation.** The operation goes inside each **team's application**. That **reads as independence** and **produces divergence**. Every team now **owns a variant**. The next change to the underlying system has to happen in as many **repositories as there are teams**.
- **A shared library.** It looks better but **moves the same cost** by a step. Every consumer **still integrates** it. Every consumer still has to upgrade before the fix reaches anybody.

| What the capability needs | Who needs it | What fits | What you are signing up for |
|---|---|---|---|
| Nothing executed; procedure, templates, conventions (a recipe) | Anyone whose task matches its description | A Skill (recipe card) | Writing a description precise enough to load, and keeping the body portable |
| Generic execution Anthropic already runs (a landlord's appliance) | Whoever is on the request | A built-in tool | Governance you do not own, on work you do not see run |
| A private operation with a known input contract (your own gadget) | One application | A custom tool | Nothing shared; a second consumer means doing this again |
| Live, authenticated access with its own release cycle (a shared supplier counter) | Several applications, several teams | A protocol server | A deployment, a transport, and an interface that outlives its first caller |

Read the rightmost column as the price list. Most wrong answers in this material are correct choices from the wrong row. The cue that tells you which row a scenario sits in is always stated in the scenario.

**ELI5.** If only your kitchen needs a gadget, build it right there. If many restaurants need the same supplier, set up one shared counter. Copying the gadget into every kitchen means fixing it in every kitchen later.

## A Skill costs about a hundred tokens until somebody needs it

**First, the idea.** A long procedure belongs in a Skill, and not in the instructions every session already carries, because of **arithmetic**. The arithmetic is called **progressive disclosure** (showing only as much as is needed, when it is needed). Tokens are small chunks of text, and the budget for them is limited.

**How a Skill loads, in stages.** Think of a recipe box where only the card titles are out on the counter.
- A Skill's **name and description** sit in the **system prompt** from startup. That costs roughly **a hundred tokens** each.
- The body of `SKILL.md` reaches context only when a **request matches that description**. It stays under **five thousand tokens**.
- **Bundled reference files** cost **nothing** until something reads them.
- Bundled scripts contribute **only their output**, not their source.<sup>[1]</sup>

Because the agent never has to read a whole Skill to use part of it, what a Skill can carry is **effectively unbounded**.<sup>[4]</sup>

**The wrong answer it exposes.** The alternative is the **always-on procedure**, written into a **project instruction file** or a system prompt. It is **paid for on every request**, including the overwhelming majority that have nothing to do with it. Claude Code documents the same contrast directly. A skill body **loads only when used**, so long reference material **costs almost nothing** until somebody needs it.<sup>[5]</sup>

**The field that carries the weight: the description.** The **description is not documentation**. It is the **matching criterion** (what Claude checks a request against). It has to say what the **Skill** does *and* when to **reach** for it.<sup>[1]</sup> A **vague description** does not degrade gracefully. It simply **never loads**, in every runtime equally. The failure looks like a Skill that was **never installed**.

**ELI5.** Keep only the titles of the recipe cards on the counter. Pull out a full card only when a customer orders that dish. If you stuck every card on the wall all day, you could not see the counter. And if a card's title is vague, nobody ever picks it.

## One file, several runtimes, and discovery changes in each

**First, the idea.** The same **`SKILL.md`** runs in three places: the **interactive terminal**, the **API**, and the **SDK**. What changes is how the **runtime finds** it and what it is **allowed to touch**. So "runs everywhere" is something you design for. It does not come free.

**How each place finds a Skill:**
- **Claude Code.** **Skills are files**. Personal ones live in **`~/.claude/skills/`**. Project ones live in **`.claude/skills/`**. When names clash, enterprise definitions **override personal** and **personal overrides project**.<sup>[5]</sup>
- **The SDK.** It **discovers** the same **filesystem locations** through its setting sources. It also takes a **`skills` option** naming which of them a session may invoke.<sup>[6]</sup>
- **The API.** A custom Skill is **uploaded to the workspace** instead. It is addressed by identifier alongside the code execution tool. Production requests **pin a version**, so an update to the Skill cannot quietly change deployed behaviour.<sup>[7]</sup>

**That last difference generalises.** The **file ports** (moves from place to place). The **distribution does not**. **Custom Skills do not sync** between surfaces on their own. A Skill wanted on three surfaces is managed on three surfaces.<sup>[1]</sup>

**The failure everybody meets once.** A **packaged workflow installs cleanly** on every machine in the team and **runs on exactly one**. The reason is that **installation copies files**, while **execution resolves** what those files point at. Think of a recipe card that says "use the oven in my kitchen." Copying the card is easy. The oven stays behind. The **author's-machine assumption** is the named form. It is invisible to the author by construction. It has three **usual shapes**:

| What the author's machine supplied | Why the install still succeeded | What the package should have carried |
|---|---|---|
| An absolute path into a home directory (e.g. a path starting at the author's own folder) | A path is plain text until something resolves it | A path relative to the Skill, written with forward slashes |
| A tool or command available in the local shell | Nothing in the package declares a shell dependency | Steps confined to what the runtime guarantees, or the dependency stated |
| An environment variable set months ago | The variable is read at the step that needs it, not at install | Required packages and variables named in the body |

**Two more constraints on the same list:**
- A Skill referring to protocol tools **names them fully**, **server prefix** included. Otherwise the **lookup misses** when several servers are connected.<sup>[8]</sup>
- A **subagent starts clean** rather than **inheriting** what its parent had loaded. So a Skill the parent depended on is **listed for the subagent** explicitly.

**Packaging sits on top, not beside.** A **plugin bundles Skills**, agents, hooks and protocol servers into one versioned, **installable unit**.<sup>[9]</sup> That is how a chosen set travels to a team. It is **distribution machinery**, **not a fifth answer** to the execution question. A **guardrail** the author relied on locally travels only if the **bundle actually contains** it.

**ELI5.** A recipe card can be copied to every kitchen. But if it says "use my oven," it only works in the author's kitchen. So write the card so it carries everything it needs. And if you want it in three kitchens, you hand it to each one.

## How wrong answers are built on this material

**First, the idea.** Wrong answers here **name mechanisms that work**. Every one is **somebody's shipped architecture**. That is why they read as reasonable, and why **four assumptions** are worth memorising.

**The four wrong assumptions:**
- **A universal preference stated as a rule.** "**Prefer a Skill** for anything procedural." "**Standardise on servers**." A **statement that holds** names something true of the **work being packaged**. A **statement that fails crowns one mechanism** regardless of what the requirement said. **Cost claims** are the common disguise. A claim that **one mechanism is always cheaper** has **priced nothing** in the scenario.
- **Instructions offered where execution was required.** Examples are documentation of an API, a procedure describing the query to run, or a **Skill standing in for a call**. Ask what the option would **actually invoke**. A **package that reaches nothing** cannot **substitute for a capability** that must **reach something**. It also **drifts from the system** it describes, with **nothing able to detect** the drift.
- **Reuse machinery bought for one consumer, or per-consumer copies bought for many.** It is the same **misread in both directions**. A **private function** does not need a deployment. **Four teams** do not need **four implementations**. A **shared library keeps the coupling**, because it makes every consumer **integrate and upgrade**.
- **A recurring cost accepted for an occasional need.** Examples are a **long procedure** loaded on **every request**, or a **nightly copy** of data standing in for **live access**. Both **trade** something the requirement asked for, **freshness or context**, for **convenience**.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| A documented internal procedure with templates, conventions and a checklist, and nothing to call | A Skill, loaded when a request matches its description | A schema, which names fields and validates them but carries no conventions |
| Several applications on different teams need one live system, released independently | One protocol server, connected by each application | The same integration repeated per application, or documentation of the endpoints |
| One application, one narrow operation, an input contract already known | A custom tool where that application lives | Server overhead bought for reuse that never happens |
| The capability is generic and Anthropic already runs it | The built-in, taken as it comes | A private reimplementation, or a wrapper nobody else can reach |
| A capability must be usable independently by teams that do not share a codebase | One maintained artifact many consumers invoke | Copying it per team, or a library every consumer must upgrade |
| The procedure must be absent from unrelated requests | On-demand loading, paid for at the description | Always-on instructions, paid for on every request |
| A packaged workflow installs everywhere and runs only for its author | Environment assumptions removed from the package | Treating a clean install as evidence the package works |

**A habit that works past the table.** Before comparing options, answer the **two questions** from the **scenario's own words**. What has to **execute**? How many **consumers** were named? An option that would be correct under a **different answer** to either question is the one **placed there to catch** you.

**ELI5.** Wrong answers are real kitchen setups, just for a different kitchen. So first ask two things. Does this dish need something fetched from outside? And how many restaurants need it? Then pick the setup that matches.

## What to remember

- What **fits is settled by the capability**, never by a **ranking of mechanisms**. Any claim that **one mechanism always wins**, on cost or on anything else, has **ignored the requirement** it was asked about.
- The **execution question sorts first**. Does the capability **reach a live, authenticated system**, or is it **knowledge** about how work is done? Procedure with **templates, conventions and checklists** is what a **Skill packages**.
- **Consumer count sorts second**. **One application** with a **known input contract** gets a **custom tool defined** in that application. **Several applications** on **independent release cycles** get a **protocol server**. A server is **reuse machinery you pay** for whether or not the reuse happens.
- A built-in is **capability Anthropic already ships**, split by where code runs. **Server tools execute** on **Anthropic's infrastructure** with **no handler** in your application. **Bash and the text editor** carry **Anthropic's schema** and still **execute locally**. What you give up is **governance at dispatch**.
- **Skills load in stages.** **Name and description** are always loaded, at about a **hundred tokens** each. The body loads only on a **description match**, under **five thousand tokens**. **Bundled files and scripts** cost **nothing** until **read or run**. That is why a **long procedure** belongs in a Skill rather than in **always-on instructions**.
- The **description is the matching criterion**, not documentation. It states what the **Skill does and when to use** it. A **vague one never loads** in any runtime.
- One **`SKILL.md` runs across surfaces**, but **discovery differs**. Claude Code and the SDK use **filesystem directories**. The API uses an **uploaded workspace Skill** with a **pinned version** in production. **Custom Skills do not sync** between surfaces on their own.
- A **clean install proves nothing** about execution. **Absolute paths**, **local commands** and **environment variables** baked into a package **install everywhere** and **run only for the author**. **Subagents inherit no Skills** from a parent.
- A **plugin bundles Skills**, agents, hooks and servers into one **versioned installable unit**. It **distributes a choice already made** rather than making one. A **guardrail left out of that bundle** reaches nobody.

**ELI5.** First ask whether the job is steps to follow or something to fetch. Steps go on a recipe card (Skill). Fetching from a shared supplier needs a shared counter (protocol server). A gadget for one kitchen is a custom tool. A landlord's appliance is a built-in. And a recipe card must not say "use my oven," or it only works for you.

## Endnotes for this chapter

1. Skills are reusable, filesystem-based resources that load on demand rather than requiring guidance to be repeated across conversations; each Skill is a directory containing a `SKILL.md` file whose YAML frontmatter requires `name` and `description`, with the description stating both what the Skill does and when Claude should use it, because it is what Claude matches a request against; content loads in levels, with metadata always loaded at startup at roughly 100 tokens per Skill, the `SKILL.md` body loaded when the Skill is triggered at under 5k tokens, and bundled resources consuming nothing until accessed, where reference files load when read and scripts run through bash with only their output entering context; Skills may bundle instructions, executable scripts and reference resources; custom Skills in Claude Code are filesystem-based, placed in `~/.claude/skills/` or `.claude/skills/`; Skills on the API run in a sandboxed container with no network access and no runtime package installation; and custom Skills do not sync across surfaces, so they are managed and uploaded separately for each surface. Anthropic, *Agent Skills* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

2. Tools differ primarily by where the code executes: client tools, including user-defined tools and tools with Anthropic-defined schemas such as `bash` and `text_editor`, run in your application, which executes the operation and returns a `tool_result`; server tools such as `web_search`, `web_fetch`, `code_execution` and `tool_search` run on Anthropic's infrastructure, with results visible directly and no handler code in the application. For tools with Anthropic-defined schemas, Anthropic publishes the schema and trains Claude on it while the application still executes each call. Anthropic, *Tool use with Claude* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

3. A custom tool is defined by four parts, a unique name, a description Claude reads to decide when to call it, an input schema, and an async handler that receives the validated arguments and returns result content; tools are registered on an SDK MCP server that runs in-process inside the application rather than as a separate process. Anthropic, *Give Claude custom tools* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/custom-tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)

4. Skills are presented as composable resources that complement Model Context Protocol servers by teaching agents workflows involving external tools, and because an agent with a filesystem and code execution does not need to read the entirety of a Skill into its context window for a given task, the amount of context that can be bundled into a Skill is effectively unbounded. Anthropic, *Equipping agents for the real world with Agent Skills* (Anthropic Engineering, accessed 2026-09-09), [https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

5. Unlike CLAUDE.md content, a skill's body loads only when it is used, so long reference material costs almost nothing until it is needed; where a skill is stored determines who can use it, and when skills share a name Claude Code resolves the conflict by source, with enterprise overriding personal and personal overriding project. Anthropic, *Extend Claude with skills* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

6. In the Agent SDK, skills are filesystem artifacts created as `SKILL.md` files in their own directories, loaded from the filesystem locations governed by the setting sources, discovered at startup as metadata with full content loaded when Claude invokes the skill, invoked either by the model autonomously or by the user directly, and scoped through a `skills` option accepting a list of names, all, or none. Anthropic, *Extend agents with skills* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/skills](https://code.claude.com/docs/en/agent-sdk/skills)

7. Skills integrate with the Messages API through the code execution tool, with the Skill referenced by `skill_id` and `version` in the `container` parameter; custom Skills are uploaded through the Skills API and shared workspace-wide; a new version is a complete snapshot rather than a delta; and the documented production guidance is to pin a specific version so that Skill updates never change deployed behaviour. Anthropic, *Using Agent Skills with the API* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/skills-guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)

8. Skill authoring guidance: use forward slashes in file paths rather than backslashes; do not assume packages are available, and state the required installation explicitly; and always use fully qualified tool names in the form `ServerName:tool_name` when a Skill uses MCP tools, because without the server prefix Claude may fail to locate the tool, especially when multiple MCP servers are available. Anthropic, *Skill authoring best practices* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

9. Plugins extend Claude Code with skills, agents, hooks and MCP servers bundled into a single installable unit, and plugin skills are always namespaced with the plugin's name to prevent conflicts when several plugins ship a skill of the same name. Anthropic, *Create plugins* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
