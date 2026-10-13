# Chapter 14: Permission Modes and Where the Human Gate Goes

**Summary**: *Claude Code gets configured before it gets trusted (the contractor gets their access set up before they start). Nearly every decision on this material is made once, then inherited by everybody afterwards. This chapter covers five things. First, which permission mode fits the risk of the work. Second, which file a setting belongs in so it reaches the people who need it. Third, why a standard that must hold everywhere is declared once instead of copied into each repository. Fourth, what each core component is for. Fifth, how an unattended run gets its output shape enforced instead of politely requested. Set the scope wrong and one afternoon's convenience becomes everybody's default.*

## The Mode Was Widened for One Refactor and Never Narrowed Again

**First, the idea.** Claude Code is like a contractor you let into your building. Before they start, you decide what they can do without asking you. That decision is made once and stays in place. If you forget about it, it keeps applying long after the job that needed it.

**The analogy for this chapter.** Claude Code is the **contractor** (the tool). The **permission mode** is the keycard the contractor carries. The **settings files** are the rule binders on the wall, kept at different levels. **`CLAUDE.md`** (the context file) is the briefing note handed over each morning. Where it fits, each part gets named in bold beside its real term.

**What happened.** A **rename across forty files** is unbearable one approval at a time. So somebody **widens the permission mode** (upgrades the keycard), finishes the rename, and moves on. That was correct for the rename. But **nobody sets it back**. The wider mode reaches the **project's settings file** (the binder on the wall), **gets committed** (the binder is copied to everyone), and a session opened to change one value now starts with the authority of a session that was going to rewrite a package.

**The term to know.** Call that a **standing grant**. It is **authority handed over once**, in a file, then **inherited by every later session**. Nobody asks whether the task in front of you needs it. Permission modes, settings files, context files and allow rules are all **standing grants**. Nearly every scenario in this chapter is one of them meeting work it was **never sized** for.

**ELI5.** Say you give a helper a master key to move all the boxes in one day. If you forget to take the key back, they keep it for every job after that. Even a job that only needed one small door.

## Plan Mode Separates Deciding Where to Change from Changing It

**First, the idea.** **Plan mode** lets Claude look around and make a plan before it is allowed to change anything. Deciding where to change something is a different job from changing it.

**The three phases.** Claude Code works a task through **three blended phases**: gather context, act, verify.<sup>[1]</sup> The recommended loop **walls the first off** from the second. **Enter plan mode**. Claude reads, searches and explores without **touching your source** (the contractor walks the building with a clipboard, but touches nothing). You approve a plan. Then the implementation runs.<sup>[2]</sup>

**The wall is real.** It is not just advice. Plan mode is itself a permission mode (a keycard level), and **edits stay blocked** until the approval.<sup>[3]</sup>

**A scenario shape.** A behaviour is **spread across several entry points**, and your earlier edits **kept landing** at the wrong one. Here is why the usual fixes fail:
- More **reading is unbounded**. There is no point where it is done.
- Following test failures assumes the tests cover every entry point. That coverage is the thing in doubt.
- One module per session guarantees that nothing sees the behaviour whole.

The fix is to **map the flows, compare the change points**, then edit.

**Gathering rewards the same precision.** A set defined by a **filename criterion** is selected exactly by a **path pattern**. **Content search** returns whatever mentions a word. It **misses the files** that never do.

**ELI5.** Before the helper starts fixing, they walk round with a clipboard and write a plan. They are not allowed to touch anything until you say yes. This stops them from fixing the wrong room.

## Six Permission Modes, Read by Who Decides the Actions They Do Not Cover

**First, the idea.** A **permission mode** is the keycard level for a session. The useful way to read the list is to ask who is left deciding about everything the card does not open.

**How to read it.** A **mode sets your session's baseline**. Read the list by who is **left holding the decision** on everything the mode does not cover. Do not read it by how much it lets through.<sup>[3]</sup>

| Mode | Runs with no prompt | Who decides the rest |
|---|---|---|
| `default`, labelled Manual | Reads | A person, at a prompt |
| `acceptEdits` | Reads, file edits, common filesystem commands such as `mkdir` and `mv` | A person, at a prompt |
| `plan` | Reads, plus classifier-approved commands where auto mode is available | A person, and edits wait for an approved plan |
| `auto` | Whatever a classifier model clears | A second model, reviewing each action before it runs |
| `dontAsk` | Only pre-approved tools | Nobody: anything that would prompt is denied |
| `bypassPermissions` | Everything | Nobody, which is why it belongs in a container |

**Two facts hold for every row.**
- **Deny rules apply in every mode** (a locked door no card opens), including the one that skips checks. **Allow rules stop meaning anything** in that mode.
- Writes to protected paths such as `.git` and `.claude` are never auto-approved outside it.<sup>[3]</sup>

**The anti-pattern.** A **mode widened to stop the prompting**. Prompt fatigue (being tired of being asked) is a real cost. But it is not a **risk assessment**. So size the mode to the **blast radius** (how much damage a wrong action could do). A deny rule at project or organisation scope closes what a mode leaves open.

**ELI5.** Each keycard opens some doors without asking. For every other door, someone has to decide. It might be a person, a second checker, or nobody at all. Pick the card by how bad it would be if a door opened that should not have.

## Configuration Scope Follows Who Has to Receive the Setting

**First, the idea.** A setting can live in several files. The file it sits in decides who gets it. So first ask who needs the setting, then pick the file.

**The files and their order.** Claude Code **reads settings from four files** plus whatever an organisation deploys, and the file a key sits in decides who gets it. **Precedence runs** in this order:
1. managed settings
2. command-line flags
3. `.claude/settings.local.json`
4. the committed `.claude/settings.json`
5. `~/.claude/settings.json`

List keys such as `permissions.allow` **merge across files rather than replacing** each other.<sup>[4]</sup>

**Read the stack as a question about audience.** Think of rule binders at different levels:
- **The committed project file** is the binder every worker on the project gets. A setting everyone on a project needs belongs here. It **travels with the checkout** (the copy of the project you download), it is reviewed like the code it governs, and your teammate's clone has it.
- **The user file** is your own binder. It **covers every project** on your machine and reaches nobody else.
- **The local file** is a **personal exception** inside one project.
- **Managed settings** are deployed centrally (the head office binder). **Nothing below overrides** them.

**Two named failures.**
- **Environment variables carrying a team decision.** They leave the value on one machine, **unreviewed and unversioned**.
- **Documentation offered as configuration.** That means a wiki page, or a preamble each developer pastes. It depends on humans repeating themselves exactly, and nothing loads it.

**ELI5.** Rules written in the shared binder reach everyone who joins the job. Rules in your own pocket reach only you. If everyone needs the rule, it goes in the shared binder.

## Context Files Layer Instead of Overriding, So a Standard Is Declared Once

**First, the idea.** `CLAUDE.md` is the briefing note Claude gets at the start of each session. Notes from different levels stack up. None of them cancels another.

**What it is.** `CLAUDE.md` is the **persistent instruction file**, **loaded at the start** of every session.<sup>[5]</sup> It can sit in these places:
- project scope, in `./CLAUDE.md` or `./.claude/CLAUDE.md`
- user scope, in `~/.claude/CLAUDE.md`
- as a managed policy file<sup>[6]</sup>

Run `/init` and Claude **drafts you a starter** from the repository itself.<sup>[7]</sup>

**The hierarchy.** This is what scenarios get built on. Every discovered file is **concatenated rather than overridden** (joined one after another, not swapped). They are **ordered from broadest scope down** to your working directory.<sup>[5]</sup> **Nothing displaces anything**. So you **declare a standard** that must hold everywhere once, at the **wide scope**. Then each repository's file carries what is true only of it.

**What goes wrong if you copy instead.** Copy that block into every repository and there are as many **copies as repositories, drifting apart**. A **central page** still needs a pointer in each repository, and somebody has to open it.

**Two limits travel with this.**
- **Size degrades adherence** (Claude follows long files less well). So keep the file **near `200` lines**. Move narrower guidance into `.claude/rules/`, where a **`paths` glob loads a rule** only when Claude reads a matching file.
- The file is **context rather than enforced configuration**. Blocking an action whatever the model decides is a hook. Hooks are owned by chapters 13 and 21.<sup>[5]</sup>

**ELI5.** Each morning the helper reads a stack of notes. The big boss's note comes first and your team's note comes after. Nothing gets crossed out. So you write the company-wide rule once, and each team only adds its own.

## Five Components, Separated by When They Load and Who Invokes Them

**First, the idea.** Claude Code has five main parts. What tells them apart is when each one enters Claude's context (what it can see) and who triggers it.

| Component | Where it lives | When it enters context |
|---|---|---|
| Rules | `.claude/rules/*.md` | Every session, or only when a `paths` glob matches a file being read |
| Skills | `.claude/skills/<name>/SKILL.md`, or under `~/.claude` | Descriptions at startup, the body when Claude judges it relevant or somebody types `/name` |
| Commands | `.claude/commands/*.md` | On invocation, by typing `/name` |
| Subagents | `.claude/agents/*.md`, or under `~/.claude` | A separate context window, on delegation |
| Agent memory | `~/.claude/projects/<project>/memory/` | The `MEMORY.md` index every session, capped at `200` lines or 25KB; topic files on demand |

**Skills are directories.** A **skill is a directory** (a recipe binder on the shelf), and that property decides a recurring scenario.<sup>[8]</sup> A procedure of **instructions plus support scripts** has somewhere to keep them. Its body **costs you no context** until it is used. Compare the same material inside a context file. It **loads every session** whether the procedure comes up or not, and the **scripts are still homeless**. Built as a library, it becomes something application code calls. But the requirement was that a session could reach it. Command files still work. **Skills are their successor**.<sup>[6]</sup>

**Subagents.** A **subagent** (a helper sent into another room) runs in its **own context window** with its **own tool access**. So a long exploration **returns a summary** and leaves the main conversation clean.<sup>[9]</sup>

**Agent memory.** This runs the other way. Claude writes it for itself (the contractor's own notebook). It is machine-local, so it **distributes nothing**.<sup>[5]</sup>

**ELI5.** Some notes are read every morning. Some are recipe binders that only come off the shelf when needed. Some helpers work in their own room and bring back a short report. And the helper keeps a private notebook that nobody else gets a copy of.

## An Unattended Run Needs Its Output Shape Enforced Rather Than Requested

**First, the idea.** Sometimes Claude Code runs with nobody watching, and a program reads what it says. In that case you must force the format of the answer, not ask nicely for it.

**How an unattended run starts.** Pass `-p` and Claude Code **runs one prompt and exits**. This used to be called **headless mode**.<sup>[6]</sup> The `--output-format` flag selects one of three outputs:
- plain text
- structured JSON
- `stream-json`, the newline-delimited form that **emits tokens as generated** when used with `--verbose` and `--include-partial-messages`

**The decisive flag.** `--json-schema` returns the result, alongside JSON output, in a **`structured_output` field**. It is checked against a schema **validated at startup**.<sup>[10]</sup> This is the contractor filling in a form with fixed boxes, not writing a free letter.

**What this settles.** A pipeline turns a review into inline comments. It needs **one finding per object** with fields it can index. Here is why the weak options fail:
- A **firmer instruction still only asks**.
- **Regular expressions** over markdown encode this week's formatting as a contract.
- A cleanup pass runs a second unconstrained generation over the first.

**Prose parsed in place of a contract** is the anti-pattern.

**Two mechanics finish it.**
- A `-p` run **starts in Manual** on every plan. So you **hand an unattended job its mode**. Use `dontAsk`, which denies anything outside the **pre-approved set** instead of waiting for input nobody supplies.<sup>[3]</sup>
- Adding `--bare` **skips auto-discovery** of hooks, skills, commands, subagents, plugins, MCP servers, memory and context files. So a run behaves the same on a **machine nobody configured**.<sup>[10]</sup>

**ELI5.** If a robot reads the helper's answer, a polite request is not enough. Give the helper a form with fixed boxes and refuse any form that is filled in wrong. And since nobody is there to answer questions, tell the helper up front what it may do.

## The Gate Belongs Where the Worst Case Is Expensive, Not Where the Habit Is

**First, the idea.** A **gate** is a point where a person must say yes. Modes and rules settle what runs unasked. The gate decides where you still have to look. Put it where a wrong call costs the most.

**The one input.** Modes and rules **settle what runs unasked**. They say nothing about where you still have to look. That decision has one input: what a **wrong call costs**, and how hard it is to **take back**.

**Sort actions by what undoes them.**
- An edit confined to the working directory is undone by a **checkpoint or a diff**. A gate there buys you **oversight nobody needed**.
- An action undone only by another action gets a pause by default. Examples are a destructive shell command or a write outside the working directory. It **deserves a pause**, and a **deny rule** makes that pause deterministic (always happens, no exceptions).
- An action nothing can take back **needs a human**. The **agent's own review** is an input, not a substitute.

**One judgement, seen twice.** Mode and gate are one **judgement seen twice**. A mode fixes a session's default posture (the keycard). A gate **lifts one action** out of it (a manager's signature for one door).

**ELI5.** Ask a person before the helper does something that cannot be undone. Don't ask about things you can easily fix, like a pencil mark you can rub out. Asking about everything just teaches people to click yes without reading.

## How Wrong Answers Are Built on This Material

**First, the idea.** The wrong options here describe **configurations real teams ship**. What makes one wrong is an **assumption underneath** it. Four assumptions cover almost everything.

**The four wrong assumptions:**
- **Convenience treated as a requirement.** A **mode is picked** because it **removes interruptions**, and the **risk of the work never enters** the comparison. The option becomes correct only where the scenario calls the work **low-stakes and reversible**.
- **State that does not travel** offered as **shared configuration**. Examples are machine-local environment variables, a pasted preamble, a wiki page, a spreadsheet. **Each holds the content**, but **none arrives with a checkout or loads** during a session.
- **Duplication chosen over a scope that already exists.** That means a **shared standard copied into every repository**, or linked from each one. **Layering already applies** the general and the local together. So a scenario naming two scopes of instruction **wants the layering**.
- **A shape requested where it had to be enforced.** That means **stronger wording, cleverer parsing**, or a **second generation** to tidy the first. All three leave a consumer depending on **formatting nothing promised**.

**Match** on what the **scenario** is doing. Never match on the **industry** it is **dressed** in.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Configuration must be identical for everyone working on a repository | The committed project settings file, versioned alongside the code | Per-machine environment variables, or a document somebody is asked to follow |
| Standards apply everywhere, with extra rules in some repositories | Declare the general once at the wide scope and keep local files local | Copying the block into each repository, or linking out to a page |
| A downstream program consumes the run's output | Constrain the shape at the interface and validate on receipt | A firmer instruction, a regex over markdown, or a cleanup pass |
| Edits keep landing at the wrong place in unfamiliar code | Map the flows and compare change points before editing | More reading, test-driven iteration, or one narrow session per module |
| A team procedure carries instructions plus support scripts | A skill directory the tool discovers and loads on demand | Inlining it into the context file, or shipping it as a library |
| The action is hard to undo or reaches beyond the repository | A pause for a human, backed by a deny rule | A mode carried over from whatever the last task needed |
| A job runs unattended and must behave the same on every machine | Pre-approved tools, a mode that never waits, a fixed output shape | A default that assumes somebody is at a prompt |

**A habit that works past the table.** One **habit transfers**. Before you compare options, ask what a fresh clone on a **machine nobody has configured** would inherit.

**ELI5.** Wrong answers often sound sensible. They pick the easy keycard, leave the rule in someone's pocket, copy the same note everywhere, or just ask nicely for a neat answer. Look at what the problem really is, not at the story around it.

## What to Remember

- A **standing grant** is **authority set once in a file** and **inherited by every later session** without anyone re-deciding it. **Permission modes**, **settings files**, **context files** and **allow rules** all qualify. Scenarios are built on one meeting work it was **never sized** for.
- **Six permission modes**:
  - `default` (labelled **Manual**, reads only)
  - `acceptEdits` (edits and **filesystem commands**)
  - `plan` (**edits blocked** until a plan is approved)
  - `auto` (a **classifier reviews each action**)
  - `dontAsk` (**pre-approved tools** only, **never waits**)
  - `bypassPermissions` (**containers only**)

  **Deny rules hold in every mode**. **Allow rules** mean nothing in the last.
- **Settings precedence**, highest first: **managed settings**, **command-line flags**, the **project-local file**, the **committed project file**, then **user settings** in your home directory. **List keys** such as `permissions.allow` **merge across files** rather than replacing each other.
- **Scope follows audience**. A rule everyone on the project needs goes in the **committed project file**, which is **versioned, reviewed and present** in a **fresh clone**. **Per-machine variables and written documents** reach nobody.
- **Context files concatenate**, **broadest scope first**, so **nothing overrides anything**. **Declare a cross-repository standard** once at the **wide scope** and let each repository's file carry only its own. Copying or linking **reintroduces drift**.
- `CLAUDE.md` is **context, not enforcement**, so an **absolute prohibition** belongs in a **hook**. Keep it **near `200` lines** and push narrow guidance into **`.claude/rules/` with a `paths` glob**.
- **Five components by load behaviour**:
  - **rules** load every session or on a path match
  - **skills** load their body on demand and **bundle scripts**, being **directories**
  - **commands** run when typed
  - **subagents** get their **own context window and tools**
  - **agent memory** is **written by Claude**, stored per repository, **machine-local**
- **`-p` runs one prompt and exits** and is the **former headless mode**. **`stream-json` streams events**. **`--json-schema` returns a validated `structured_output`**. An **unattended pipeline enforces the shape**, because **asking for a format** produces the intermittent behaviour already being reported. A **`-p` run starts in Manual** whatever the plan. **`--bare` skips discovery** of hooks, skills, commands, subagents, plugins, MCP servers, memory and context files.
- **Place the human gate by reversibility**: **no gate** where a **checkpoint or a diff** undoes it, a **pause plus a deny rule** where only another action can, and a **person** where nothing can. The **agent's own review is an input** to that decision, never the decision.

**ELI5.** Claude Code is a contractor with a keycard. Set the card once and it sticks, so size it to the job. Put shared rules in the shared binder and company rules at the top. Make robots read a fixed form. Ask a person only before things that cannot be undone.

## Endnotes for this chapter

1. Claude works a task through three blended phases, gathering context, taking action and verifying results, chaining tool calls and course-correcting until done. Anthropic, *How Claude Code works* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)

2. The recommended four-phase workflow of exploring in plan mode, asking for a detailed implementation plan, implementing after approval and committing, together with the guidance that planning is most valuable when the approach is uncertain, the change spans several files, or the code is unfamiliar. Anthropic, *Best practices for Claude Code* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

3. The available permission modes and what each runs without a prompt; the `default` mode being labelled Manual in the CLI, the extensions and the desktop app; plan mode blocking edits until a plan is approved; the auto-mode classifier reviewing actions before they run; `dontAsk` auto-denying every call that would otherwise prompt so the session never waits for input; `bypassPermissions` being restricted to isolated containers and VMs; deny rules blocking in every mode including `bypassPermissions` while allow rules have no effect there; the protected paths whose writes are never auto-approved outside that mode; and the built-in starting permission mode for `-p` runs being `default`. Anthropic, *Choose a permission mode* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/permission-modes](https://code.claude.com/docs/en/permission-modes)

4. The four settings files and the scope each reaches, including a committed project file reaching teammates' clones and a cloud session while user and local files stay on one machine; the precedence order from managed settings down through command-line arguments, project local, shared project and user settings; and list keys such as `permissions.allow` merging across files rather than overriding. Anthropic, *Claude Code settings* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)

5. CLAUDE.md files loading at the start of every session and being treated as context rather than enforced configuration, with a `PreToolUse` hook named as the mechanism for blocking an action regardless of what Claude decides; the project locations `./CLAUDE.md` and `./.claude/CLAUDE.md`; all discovered files being concatenated into context rather than overriding each other, ordered from the filesystem root down to the working directory; the guidance to target under `200` lines per file because longer files consume more context and reduce adherence; `.claude/rules/` holding modular instruction files that a `paths` glob scopes so they load only when Claude reads matching files; and auto memory being stored per repository under `~/.claude/projects/`, machine-local, with the first `200` lines or 25KB of `MEMORY.md` loaded at the start of every conversation and topic files read on demand. Anthropic, *How Claude remembers your project* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

6. Definitions of the core components and features: CLAUDE.md placed at project scope, at user scope in `~/.claude/CLAUDE.md`, or as managed policy; rules as modular instruction files in `.claude/rules/`; commands invoked by typing `/name` and definable as files in `.claude/commands/`, with skills named the recommended successor; skills as a `SKILL.md` file loaded automatically when relevant or invoked directly; subagents running in their own context window with their own tool access and permissions; sessions tied to a directory with transcripts under `~/.claude/projects/`; non-interactive mode invoked with `-p` and formerly called headless mode; and bare mode starting without loading hooks, skills, custom commands, subagents, plugins, MCP servers, auto memory or CLAUDE.md. Anthropic, *Glossary* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/glossary](https://code.claude.com/docs/en/glossary)

7. `/init` initialising a project with a generated CLAUDE.md guide. Anthropic, *Commands* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/commands](https://code.claude.com/docs/en/commands)

8. Skills as a directory containing `SKILL.md` plus optional supporting files and bundled scripts, discovered from `.claude/skills/` at project scope and `~/.claude/skills/` at personal scope, with the body loading only when the skill is used so long reference material costs almost nothing until needed. Anthropic, *Extend Claude with skills* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)

9. Subagents preserving context by keeping exploration out of the main conversation, enforcing constraints by limiting which tools they may use, and being defined as files in `.claude/agents/` for a project or `~/.claude/agents/` for every project on a machine. Anthropic, *Create custom subagents* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

10. Non-interactive runs with `-p`; `--output-format` accepting `text`, `json` and `stream-json`, the last being newline-delimited JSON used with `--verbose` and `--include-partial-messages` to receive tokens as they are generated; `--output-format json` combined with `--json-schema` returning the structured result in a `structured_output` field, with an invalid schema rejected at startup; and `--bare` skipping auto-discovery of hooks, skills, custom commands, subagents, plugins, MCP servers, auto memory and CLAUDE.md so a run behaves the same on every machine. Anthropic, *Run Claude Code programmatically* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)
