# Chapter 14: Permission Modes and Where the Human Gate Goes

**Summary**: *Set Claude Code up before you trust it: most choices are made once and inherited by everyone. It covers the right permission mode for the risk, the right file for each setting, why a shared standard is declared once, what each core component does, and how an unattended run gets its output shape enforced. Wrong scope turns one afternoon's shortcut into the team default.*

## The Mode Was Widened for One Refactor and Never Narrowed Again

Picture a key card that opens every door, made for an office move. Nobody wipes it afterwards, and it gets handed on.

Approving forty file edits one by one is painful. So someone **widens the permission mode** and finishes. Fine for the rename. But it lands in the committed project settings file. Now a session meant to change one value can rewrite a package.

Call this a **standing grant**: authority given once, in a file, and inherited by every later session. Permission modes, settings files, context files and allow rules are all standing grants (the card that stays programmed). Most scenarios here pair one with work it was never sized for.

**ELI5.** A key card made for one move still opens every door next month.

## Plan Mode Separates Deciding Where to Change from Changing It

Claude Code works in three phases that blend: gather context, act, verify.<sup>[1]</sup> The recommended loop puts a wall between the first two. In plan mode, Claude reads, searches and explores without touching your source. You approve a plan, then it works.<sup>[2]</sup> The wall holds: plan mode is a permission mode, so edits stay blocked until you approve.<sup>[3]</sup>

Suppose one behaviour has several entry points and your edits hit the wrong one. More reading never ends. Chasing test failures assumes tests cover every entry point, the very doubt. One module per session sees no whole. Trace the flows, compare candidate spots, then edit.

Be exact when gathering. For files matching a filename rule, use a path pattern. A content search finds files mentioning a word and misses those that never do.

**ELI5.** Look around the room first. Move furniture only after your plan is approved.

## Six Permission Modes, Read by Who Decides the Actions They Do Not Cover

A **mode** is the starting level for your session. Ask who makes the call on everything the mode leaves out, not how much it allows.<sup>[3]</sup> Each mode is a key card. Who stands at the doors it does not open?

| Mode | Runs with no prompt | Who decides the rest |
|---|---|---|
| `default`, labelled Manual | Reads | You, at a prompt |
| `acceptEdits` | Reads, edits, everyday filesystem commands like `mkdir` and `mv` | You, at a prompt |
| `plan` | Reads, and commands a classifier approves when auto mode is available | You. Edits wait for an approved plan |
| `auto` | What a classifier model clears | A second model, per action |
| `dontAsk` | Only pre-approved tools | No one. Prompts become denials |
| `bypassPermissions` | All of it | No one, so use it only in a container |

Two facts hold in every row. Deny rules work in every mode, even the one that skips checks, and allow rules mean nothing there. Outside it, writes to protected paths like `.git` and `.claude` always ask first.<sup>[3]</sup>

So the mistake is widening a mode to silence prompts. Prompt fatigue is real but is not a risk check. Fit the mode to the blast radius, the damage a wrong call can do. A deny rule at project or organisation scope closes the gaps.

**ELI5.** A deny rule is a lock that beats every key card.

## Configuration Scope Follows Who Has to Receive the Setting

Claude Code reads settings from four files, plus whatever an organisation deploys. Precedence runs: managed settings, command-line flags, `.claude/settings.local.json`, the committed `.claude/settings.json`, then `~/.claude/settings.json`. List keys such as `permissions.allow` add up across files rather than replacing.<sup>[4]</sup>

Ask who needs a setting. A setting the whole project needs goes in the committed project file. It travels with the checkout, gets reviewed like code, and sits in a teammate's clone. The user file covers all your projects and reaches no one else. The local file holds your personal exceptions inside one project. Managed settings are deployed centrally, and nothing below overrides them.

Two failures have names. A team decision in an environment variable lives on one machine, with no review or history. Documentation posing as configuration, like a wiki page or pasted preamble, relies on people repeating it exactly. Nothing loads it.

**ELI5.** A rule on the shared fridge reaches everyone. One in your pocket reaches you.

## Context Files Layer Instead of Overriding, So a Standard Is Declared Once

`CLAUDE.md` holds standing instructions that load at the start of each session.<sup>[5]</sup> At project scope it is `./CLAUDE.md` or `./.claude/CLAUDE.md`. At user scope, `~/.claude/CLAUDE.md`. It can also be a managed policy file.<sup>[6]</sup> Type `/init` and Claude drafts a first version from the repository.<sup>[7]</sup>

Claude joins every file it finds, and none overrides another. They run from the broadest scope down to your working directory.<sup>[5]</sup> So state a standard needed everywhere once, at the wide scope. Each repository's file then carries only what is true there. Copy the block into every repository and the copies drift apart. Link to a central page and each repository still needs a pointer someone must open.

Two limits. Long files are followed worse, so stay near `200` lines. Put narrower guidance in `.claude/rules/`, where a `paths` glob loads a rule only when Claude reads a matching file. And the file is context, not enforced configuration. To block an action whatever the model decides, use a hook (chapters 13 and 21).<sup>[5]</sup>

**ELI5.** A school sets big rules once. Each class adds its own sheet.

## Five Components, Separated by When They Load and Who Invokes Them

| Component | Where it lives | When it enters context |
|---|---|---|
| Rules | `.claude/rules/*.md` | At session start, or when a `paths` glob matches a file read |
| Skills | `.claude/skills/<name>/SKILL.md`, or under `~/.claude` | Descriptions at startup. Body when relevant or on `/name` |
| Commands | `.claude/commands/*.md` | When invoked as `/name` |
| Subagents | `.claude/agents/*.md`, or under `~/.claude` | Own context window, on delegation |
| Agent memory | `~/.claude/projects/<project>/memory/` | `MEMORY.md` index each session, up to `200` lines or 25KB. Topic files on demand |

A skill is a directory, and that settles a common case.<sup>[8]</sup> A procedure with instructions and helper scripts fits in one, and its body costs no context until used. In a context file it loads every session, needed or not, and the scripts have no home. A library is called by application code, but the need was for a session to reach it. Command files still work, but skills replaced them.<sup>[6]</sup>

Subagents get their own context window and tools. A long exploration returns as a summary, so the main chat stays clean.<sup>[9]</sup> Agent memory is the reverse. Claude writes it for itself, and being machine-local it shares nothing.<sup>[5]</sup>

**ELI5.** Some tools sit on the desk. Others wait in a drawer.

## An Unattended Run Needs Its Output Shape Enforced Rather Than Requested

Pass `-p` and Claude Code runs one prompt and exits, once called headless mode.<sup>[6]</sup> `--output-format` chooses plain text, structured JSON, or `stream-json`. The last is newline-delimited, and with `--verbose` and `--include-partial-messages` it emits tokens as they are generated. The key flag is `--json-schema`. Paired with JSON output, it returns the result in a `structured_output` field, matched to a schema validated at startup.<sup>[10]</sup>

A pipeline turns a review into inline comments. It needs one finding per object, with fields it can look up. Asking harder is still asking. Regexes over markdown make this week's formatting a contract. A cleanup pass adds a second unconstrained generation. Each parses prose where a contract was needed.

A `-p` run starts in Manual on every plan, so give an unattended job its mode. `dontAsk` denies anything outside the pre-approved set instead of waiting for input nobody will give.<sup>[3]</sup> Add `--bare` and Claude skips auto-discovery of hooks, skills, commands, subagents, plugins, MCP servers, memory and context files. The run then acts the same on a machine nobody configured.<sup>[10]</sup>

**ELI5.** A form with labelled slots can't be filled in wrong. A schema is that form.

## The Gate Belongs Where the Worst Case Is Expensive, Not Where the Habit Is

Modes and rules decide what runs unasked. Where you still look depends on what a wrong call costs and how hard it is to take back.

Sort actions by how they get undone. A checkpoint or diff reverses an edit inside the working directory, so a gate there is oversight nobody needed. Other actions need another action to reverse them, like a destructive shell command or a write outside the working directory. They deserve a default pause, and a deny rule makes it certain. An action nothing can reverse needs a human. The agent's own review feeds that choice, never replaces it.

Mode and gate are one judgement at two sizes. The mode sets the session default. The gate lifts out one action.

**ELI5.** If you can erase it, let the kid draw. If it can never be fixed, a grown-up decides.

## How Wrong Answers Are Built on This Material

Wrong options are setups real teams ship. A hidden assumption sinks each, and four cover almost all.

- **Convenience treated as a requirement.** Someone picks a mode to cut interruptions and never weighs risk. Right only for work stated as low-stakes and reversible.
- **State that does not travel**, offered as shared configuration: machine-local environment variables, a pasted preamble, a wiki page, a spreadsheet. Each holds the content. None comes with a checkout or loads in a session.
- **Duplication chosen over a scope that already exists.** Copying a shared standard into each repository, or linking from each. Layering already combines general with local, so when a scenario names two scopes of instruction, pick layering.
- **A shape requested where it had to be enforced.** Firmer wording, cleverer parsing, or a second pass to tidy the first. The consumer still trusts a format nobody promised.

Match on what the scenario does, not its industry.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Everyone on a repository needs the same configuration | The committed project settings file, versioned with the code | Per-machine environment variables, or a document to follow |
| Standards apply everywhere, with extras in some repositories | Declare the general part once at the wide scope. Local files stay local | Pasting the block into each repository, or linking out |
| Another program reads the run's output | Fix the shape at the interface. Validate when it arrives | A firmer instruction, a regex over markdown, or a cleanup pass |
| Edits land in the wrong place in unfamiliar code | Trace flows, compare change points, then edit | More reading, test-driven loops, one session per module |
| A team procedure has instructions and scripts | A skill directory loaded when needed | Putting it in the context file, or a library |
| An action is hard to undo or leaves the repository | A human pause, plus a deny rule | A mode inherited from the last task |
| An unattended job must behave the same everywhere | Pre-approved tools, a mode that never waits, a fixed output shape | A default that assumes a person at a prompt |

One habit outlasts the table: ask what a fresh clone on an unconfigured machine would inherit.

**ELI5.** Wrong answers feel easy. The right one works when you aren't watching.

## What to Remember

- A **standing grant** is authority written once in a file and inherited by all later sessions. Permission modes, settings files, context files and allow rules all count. Scenarios pair one with work it was never sized for.
- Six permission modes. `default` (labelled Manual) reads only. `acceptEdits` adds edits and filesystem commands. `plan` blocks edits until a plan is approved. `auto` has a classifier review each action. `dontAsk` runs pre-approved tools only and never waits. `bypassPermissions` is for containers only. Deny rules hold in every mode. Allow rules mean nothing in the last.
- Precedence, strongest first: managed settings, command-line flags, the project-local file, the committed project file, then user settings in your home directory. List keys such as `permissions.allow` add up across files.
- Scope follows audience. Whatever the project needs lives in the committed project file, which is versioned, reviewed and in every fresh clone. Per-machine variables and documents reach nobody.
- Context files are joined, broadest first, and none overrides another. Declare a cross-repository standard once at the wide scope, with each repository's file holding only its own. Copying or linking brings drift back.
- `CLAUDE.md` is context, not enforcement, so a hard ban goes in a hook. Keep it near `200` lines. Narrow guidance goes in `.claude/rules/` with a `paths` glob.
- Five components by load behaviour. Rules load every session or on a path match. Skills are directories, so they bundle scripts and load on demand. Commands run when typed. Subagents get their own context window and tools. Agent memory is written by Claude, stored per repository, machine-local.
- `-p` runs one prompt and exits, the former headless mode. `stream-json` streams events. `--json-schema` returns a validated `structured_output`. Unattended pipelines enforce the shape, because asking for a format gives the flaky behaviour already reported. A `-p` run starts in Manual whatever the plan. `--bare` skips discovery of all of: hooks, skills, commands, subagents, plugins, MCP servers, memory, context files.
- Put the human gate by reversibility. No gate where a checkpoint or a diff undoes it. A pause plus a deny rule where only another action can. A person where nothing can. The agent's own review informs the decision and never makes it.

**ELI5.** Set rules once where everyone finds them. Lock the important ones.

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
