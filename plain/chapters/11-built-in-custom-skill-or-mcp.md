# Chapter 11: Four Mechanisms, Decided by What Must Execute

**Summary**: *One new capability, four mechanisms offered, at least three that would work. That is the hard part. "Always prefer X" stops reading the requirement, because the thing being packaged decides the answer, not a ranking. Two checks decide almost everything. Does the work touch a live system? How many consumers need it? Below: those checks, the price of each mechanism, and why a package may work for you and fail for a teammate.*

## Four Proposals Arrive for One Capability, and None of Them Is Absurd

Picture a restaurant kitchen where one dish must taste the same every night.

Finance has that need. Finance needs a **month-end reconciliation write-up** in the house format. Fixed section order. Wording nobody improvises. A checklist before it goes out.

Four proposals reach the meeting:

- A **built-in tool**: Anthropic already ships one that runs code.
- A **custom tool**: write it in the application, like every other capability.
- A **Skill**: package the whole procedure.
- A **protocol server**: two other teams will want this by spring.

All four are real engineering, and somebody shipped each this quarter. None can be crossed off as nonsense. Fit decides, and fit comes from two properties of the capability, not from the mechanisms.

The kitchen will return. A Skill is a recipe card. A built-in is the landlord's appliance. A custom tool is a knife in your own kitchen. A protocol server is a supplier counter several restaurants share.

**ELI5.** Four helpers raise their hands for one job. Look at the job, not at who seems best.

## The Execution Question Comes First, Because It Removes Two Options at Once

Ask first. The **execution question**: must the capability reach a system with live state that checks who is calling? Or is it knowledge about how work gets done?

Section order, templates, house style, a review checklist: none of it calls anything. It is expertise on paper, which is what a **Skill** (the recipe card) carries. A Skill is a directory holding a `SKILL.md` file. The file has YAML frontmatter and a body of instructions. Templates and scripts sit beside it.<sup>[1]</sup>

Live access is different: a balance that changed this morning, a record only some callers may read. Text describing an endpoint cannot send a request to it, and it drifts from the real endpoint with nothing to flag it. The reverse is more tempting. A server wrapped around fixed instructions adds a hop and no ability.

One caveat. A Skill may bundle scripts, and they do run.<sup>[1]</sup> But that adds no reach. Through the API, a Skill runs in the code execution container, which is sandboxed, with no network access and no runtime package installation<sup>[1]</sup>. A bundled script is local, deterministic work, not a road into production.

**ELI5.** A recipe card gives steps but cannot phone the supplier. Need today's real stock? Someone must call. Only need steps? The card is enough.

## A Built-in Tool Is Capability Anthropic Already Operates

If something must execute, three options remain. Check what already exists first, since the cheapest definition is the one you never write.

"Built-in" splits by where the code runs. **Server tools** (web search, web fetch, code execution, tool search) run on Anthropic's infrastructure. The call and result both arrive in the response. Your application has no handler.<sup>[2]</sup> Bash and the text editor differ. Anthropic publishes their schema and trains Claude on it, but your application still runs the operation and returns the result.<sup>[2]</sup>

A server tool is the landlord's appliance (server-executed): press the button, never see it run.

A built-in hands you a definition, sometimes the implementation too. The cost is ownership. Chapter 9 put validation, the approval gate and the audit record at dispatch. A server-executed tool has no dispatch on your machine. The tradeoff: a built-in suits generic work with no governance stakes. It is wrong once a human must answer for what ran.

Wrapping a built-in to share it is an anti-pattern. The wrapper sits inside one application, so other teams never find it.

**ELI5.** Borrowing the landlord's oven saves buying one, but you can't inspect it. Fine for toast. Bad when someone must sign for the meal.

## The Consumer Count Decides Between a Private Function and a Protocol

Two options are left, and they do the same job. What separates them is not technical. Count the applications.

One app needs one narrow operation with known inputs? Use a **custom tool** (your own knife) in that app. In the Agent SDK it has four parts: name, description, input schema and handler. Its server runs inside your application, not as a separate process.<sup>[3]</sup> So you deploy nothing, pick no transport, and version nothing extra.

Several applications that release on their own schedules: a **protocol server** (the supplier counter). Chapter 10 covered what one exposes and where it runs. Here only cost matters. A server is reuse machinery, paid for whether or not anyone reuses it. You deploy a process, pick a transport, and hold an interface steady while callers change. For one consumer, that buys nothing.

Flip the arithmetic and two easy answers fail. Copying the code into each team's app looks independent but breeds divergence. Every team owns a variant, and each change to the underlying system lands in every repository. A shared library only moves the cost. Each consumer still integrates it and must upgrade before a fix reaches anyone.

| Need | Users | Pick | Cost to you |
|---|---|---|---|
| No execution: procedure, templates, conventions | Anyone whose task fits the description | A Skill | A description sharp enough to trigger loading, and a portable body |
| Generic execution that Anthropic runs | Whoever makes the request | A built-in tool | Governance you do not own over work you cannot watch |
| One private operation, inputs known | A single application | A custom tool | Nothing is shared, so a second consumer means redoing it |
| Live authenticated access, own release cycle | Many applications and teams | A protocol server | A deployment, a transport, and an interface that must outlast its first caller |

Read the last column as prices. Most wrong answers are right choices from the wrong row. The scenario states the cue for its row.

**ELI5.** One kitchen needs one knife, so buy it. Five restaurants needing one ingredient justify a shared counter. One restaurant does not.

## A Skill Costs About a Hundred Tokens Until Somebody Needs It

Think of a recipe binder: you see spine labels, and open a card only when someone orders that dish. A long procedure goes in a Skill, not in instructions every session carries, and the reason is arithmetic. It is called **progressive disclosure**.

It loads in stages.

- Name and description are in the system prompt from startup. Each takes roughly a hundred tokens.
- The `SKILL.md` body arrives only when a request matches that description. It stays under five thousand tokens.
- Bundled reference files cost nothing until read.
- Bundled scripts add only their output.<sup>[1]</sup>

The agent can use part of a Skill without reading all of it, so a Skill can hold effectively unlimited material.<sup>[4]</sup>

The alternative is a procedure in a project instruction file or system prompt. It is paid for on every request, even nearly all that never need it. Every recipe taped to the wall. Claude Code's docs make the same point: a skill body loads only on use, so long reference text is nearly free until then.<sup>[5]</sup>

One field carries the weight. The description is the matching criterion (the spine label), not documentation. It must say what the Skill does and when to reach for it.<sup>[1]</sup> A vague one never loads, in any runtime, and looks like a Skill nobody installed.

**ELI5.** A binder shows labels until you open a card. A clear label gets the right card pulled. A fuzzy one stays on the shelf.

## One File, Several Runtimes, and Discovery Changes in Each

One `SKILL.md` works in the terminal, through the API and under the SDK. Each finds it differently and allows different access, so "runs everywhere" takes design.

In Claude Code, Skills are files. Personal ones live in `~/.claude/skills/`, project ones in `.claude/skills/`. On a name clash, enterprise beats personal, and personal beats project.<sup>[5]</sup> The SDK looks in those same places via its setting sources. A `skills` option lists which ones a session may call.<sup>[6]</sup> On the API, you upload a custom Skill to the workspace instead. It is referenced by identifier next to the code execution tool. Production requests pin a version, so updates cannot quietly change deployed behaviour.<sup>[7]</sup>

The file ports; distribution does not. Custom Skills do not sync across surfaces: three surfaces, three copies to manage.<sup>[1]</sup>

Now the failure everyone meets once. A recipe card copied to every kitchen, but only one can cook from it. A workflow installs cleanly on every teammate's machine and runs on one. Installing copies files. Running resolves what they point at. This is the **author's-machine assumption**, invisible to the author. It takes three usual shapes.

| Hidden on the author's machine | Why install passed | Missing from the package |
|---|---|---|
| Absolute path under a home directory | Paths are plain text until used | Path relative to the Skill, forward slashes |
| A command in the local shell | The package never says it needs one | Only steps the runtime guarantees, or the dependency spelled out |
| An environment variable from months back | It is read when needed, not at install | Packages and variables listed in the body |

Two more rules. When a Skill uses protocol tools, write the full name with the server prefix. Without it, the lookup can miss when several servers are connected.<sup>[8]</sup> And a subagent starts clean, with nothing its parent loaded. List the parent's Skills for it explicitly.

A **plugin** sits on top. One versioned, installable unit holds Skills, agents, hooks and protocol servers<sup>[9]</sup>. That is how a team gets a chosen set. It is distribution, not a fifth answer to the execution question. A guardrail used locally travels only if the bundle holds it.

**ELI5.** "Use the big blue pot from my shelf" works in one kitchen. Copying the card doesn't copy the pot. Write down everything the cook needs.

## How Wrong Answers Are Built on This Material

Every wrong option works somewhere, so it sounds fine. Learn these four patterns.

- A favourite turned into a rule: "Prefer a Skill for anything procedural," "Standardise on servers." A true statement describes the work. A false one crowns a mechanism whatever the requirement says. "Always cheaper" is the usual cover, and it has priced nothing in the scenario.
- Text offered where a call was needed. Think API docs, a described query, a Skill acting as a call. Ask what it would really invoke. Something that reaches nothing cannot stand in for a system call, and it drifts out of date unnoticed.
- A server for one consumer, or copies for many. One misreading, two directions. A private function needs no deployment, four teams need not write four versions, and a shared library keeps the coupling because everyone must integrate and upgrade.
- An ongoing cost for a rare need. Examples: a long procedure in every request, or a nightly data copy instead of live access. Each trades away freshness or context for convenience.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| An internal procedure with templates, conventions and a checklist, and nothing to call | A Skill that loads when the description matches | A schema: it names and validates fields but has no conventions |
| Several applications on different teams need one live system, released independently | One protocol server each application connects to | The same integration repeated per application, or endpoint docs |
| One app, one small operation, inputs already known | A custom tool in that app | Paying for a server whose reuse never arrives |
| Generic capability that Anthropic runs already | Use the built-in as shipped | Rebuilding it privately, or a wrapper no one else can find |
| Teams with no shared codebase must each use the capability | One maintained artifact many consumers call | Copying it per team, or a library everyone must upgrade |
| The procedure should not appear in unrelated requests | Load on demand; you pay only for the description | Always-on instructions that cost something every request |
| Workflow installs on every machine but works only on the author's | Strip the environment assumptions from the package | Reading a clean install as proof it works |

One habit outlasts the table. Before comparing options, answer from the scenario's own words: what must execute, and how many consumers were named? Any option that fits a different answer to either question was put there as bait.

**ELI5.** Wrong answers are real tools in the wrong place. Ask first: must it call something live, and how many kitchens need it?

## What to Remember

- Fit comes from the capability, not from a league table of mechanisms. If someone says one always wins, on cost or otherwise, they skipped the requirement.
- Ask the execution question first. Does it reach a live, authenticated system, or is it know-how? Know-how such as templates, conventions and checklists is what a Skill packages.
- Consumer count second. One application with known inputs gets a custom tool inside it. Several applications on independent release cycles get a protocol server, reuse machinery you pay for even if no reuse happens.
- A built-in is capability Anthropic already ships, split by where code runs. Server tools execute on Anthropic's infrastructure with no handler in your application. Bash and the text editor use Anthropic's schema but still execute locally. The loss is governance at dispatch.
- Skills load in stages. Name and description are always loaded, about a hundred tokens each. The body loads only on a description match, under five thousand tokens. Bundled files and scripts cost nothing until read or run. Hence long procedures belong in Skills, not always-on instructions.
- Treat the description as the matching test. It must say what the Skill does and when to use it. If vague, it never loads, in any runtime.
- One `SKILL.md` works on every surface, yet it is found differently. Claude Code and the SDK read filesystem directories. The API uses a Skill uploaded to the workspace, with a pinned version in production. Surfaces do not sync custom Skills for you.
- Installing cleanly says nothing about running. Absolute paths, local commands and environment variables install everywhere but work only for the author. Subagents get no Skills from their parent.
- A plugin bundles Skills, agents, hooks and servers into one versioned installable unit. It spreads a choice already made rather than making one. Leave a guardrail out of the bundle and nobody receives it.

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
