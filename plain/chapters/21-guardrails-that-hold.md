# Chapter 21: A Rule in a Prompt Is Not Enforcement

**Summary**: *Ask one question of any control: does it still work on a run where the model has already made the wrong call? If yes, it is a guardrail. If no, it is advice. Two checks sort it. Does it need the model to cooperate? Does it run before the effect lands? Hooks, permission rules, identity scope and OS isolation pass both. A rule typed into a prompt passes neither. Nobody finds that out on a quiet day.*

## The Rule Was Agreed by Everyone and Refused by Nothing

Picture a team that wants its agent to write into one output folder and nowhere else. They put that sentence in the standing instruction and the project's context file. All agree.

Months later, a file lands in the wrong place. Nothing crashed. The rule was only a sentence, and Claude weighs sentences against each other. Another one won.

Claude Code enforces permission rules. The model does not. A prompt or a context file changes what Claude *tries* to do, not what it is *allowed* to do. <sup>[1]</sup>

What was missing is a **point of refusal**. That is a moment where something other than the model can still stop the action. Without one, a control is advice.

The analogy for this chapter: A "keep out" sign is a rule in a prompt. A locked door is a permission rule. The sign works on people who read it and agree. The door works on everyone.

**ELI5.** A sign says "please don't come in." Polite people obey it. A lock asks no one. A prompt rule is the sign. A permission rule is the lock.

## Two Questions Sort Every Control You Are Offered

Assume the model has already decided wrongly. Maybe someone hid an instruction in a document it read, or it just slipped. Anthropic's threat model lists both causes together.<sup>[4]</sup>

Before you call something a layer, ask two things. Does it need the model to cooperate? Does it run before the effect lands? A sign needs the reader to cooperate. A lock does not.

| Control | Needs the model's help | Acts before the damage | What you get when the run is steered |
|---|---|---|---|
| A rule in the standing instruction or context file | Yes | Not applicable | A wish, with nothing behind it |
| The model asked to confirm its own proposal | Yes | Yes | The same opinion, asked twice |
| A `PreToolUse` hook | No | Yes | A no, with the reason sent back |
| A permission deny rule | No | Yes | A no kept in the settings |
| What the agent's identity may touch | No | Yes | A step it cannot take |
| OS-level sandboxing around the process | No | Yes | A wall with no rule to write |
| A `PostToolUse` hook, or an audit record | No | No | A receipt for what is done |

Only the bottom five rows count as layers. The top two are the guarded process guarding itself. The bottom row helps, but not for prevention.

**ELI5.** Ask two things about a safety rule. Does it need the robot's help? Does it act before the mess? A lock needs no help and acts first. A camera only shows the mess.

## A Layer Earns the Name by Failing Without Taking Its Neighbours Down

**Layering** means controls at three places that fail on their own: what reaches the model, what it produces, and what a privileged action may do. Think of an office building: a front desk screens visitors, each floor has a badge reader, and the server room has its own lock. Screening controls how often a bad thing gets through. A hard limit controls the damage when screening misses. Neither replaces the other. Anthropic lists isolation, network restriction, filesystem control and proxy validation. Combine them.<sup>[4]</sup>

The classic mistake is a stack that shares one failure: an instruction to refuse, a reminder to self-check, and a closing prompt to summarise. That is three signs on one wall, read by one reader. Chapter 20 covers screening. Its lesson here: a control that works by probability sets a rate, never a floor.

Test independence: name one failure that knocks out two controls. If you can, your count was wrong.

**ELI5.** Three doors with the same key are really one door. Real safety needs locks that break differently. If one thing breaks two, you had one.

## What the Identity Permits Bounds Everything a Steered Agent Can Do

Any other control can be missing, set up wrong, or written for a different path than your agent took. Scope is different. A capability never given cannot be reached by any route. A badge that never opens the server room opens it on no path. Anthropic's design rule: give the agent only the capabilities its task needs.<sup>[4]</sup>

The payoff is lower severity. If the identity can write anywhere, one bad decision is an incident. If it can write to one folder, it is a denied call and a log line.

Four mechanics decide whether your written scope is the scope that runs.

| What you write | Effect on the capability | What can make it bigger |
|---|---|---|
| A rule in the prompt or context file | None. It is only a sign. | Any competing sentence |
| A scoped deny rule, for example a command pattern | Tool stays, matching calls blocked | Nothing at a lower level |
| A bare tool-name deny rule | Tool removed from context, so Claude never sees it | Nothing at a lower level |
| A deny rule in managed settings | Same, across the organisation | Nothing on that machine, even command-line flags |

Two things follow. First, deny beats allow at every scope, so no allow rule can carve an exception out of a deny rule. Write the narrow allow instead.<sup>[1]</sup>

Second, giving access needs trust, and limiting access does not. A project's allow rules and extra directories apply only after you accept the workspace trust dialog. Its deny and ask rules apply either way, since they only restrict.<sup>[1]</sup>

Whoever can edit the scope owns the scope, so changing permission settings is itself a privileged action. If a tenant can swap the building's locks, they are not locks. The administrator's copy has to win. That is why a managed rule, which no local setting or flag can override, is a security property.<sup>[1]</sup>

Credentials belong to chapter 22. Command parsing checks a shell command against permission rules and asks for approval when it cannot parse the command cleanly or finds no allow rule. Anthropic calls this a permission gate, not a sandbox. It does not judge what a command does to its target path.<sup>[4]</sup> Rules cover only the doors you named. Isolation is the walls around the building. Sandboxing limits what shell commands can reach on the filesystem and network, at the operating-system level, even when an injection got past the model's own decision.<sup>[1]</sup>

**ELI5.** Give a helper a key to one room only. Even a tricked helper can only enter that room. A "no" on one door misses other doors, so you also build walls.

## A Hook Chooses Where the Refusal Sits in Time

Chapter 13 built the hook and its precedence. Hook events split the loop into moments that can refuse and moments that can only report. A `PostToolUse` hook fires after a tool has already run successfully. It cannot undo anything.<sup>[2]</sup><sup>[3]</sup> A guard at the door can stop you. One reading the log next morning cannot.

This solves a common exam scenario. A policy must be checked on every privileged action. A compliance record must also exist for a human reviewer, whether or not the action was allowed. You can deny only while the call is pending. You can record the truth only once it has finished. So you need a pair of hooks. A session start has nothing to check yet. A session end has nothing left to refuse.

Position buys more than refusal. Sometimes a value must be changed in a fixed way before the model reasons about it. Anthropic documents two places for that. Use `PreToolUse` for inputs going out to a tool. Use `PostToolUse` for results coming back, where a returned field replaces the result the model reads next.<sup>[3]</sup>

Prompt-based hooks do exist. They put a model in the decision seat on purpose, which suits a judgement call, not an absolute rule.<sup>[2]</sup>

A `PreToolUse` hook fires before any permission-mode check, in every mode. If it denies, the tool is blocked even in bypass mode, so policy survives a user changing their own settings. The reverse is false. A hook that returns allow does not beat a deny rule. Hooks tighten and never loosen.<sup>[2]</sup>

A hook on every action slows harmless calls. People often cure that by removing enforcement: hooks off, the agent run less often, or the rule moved into the prompt. That swaps a lock for a sign. Put hooks on destructive operations and sensitive access.

An aimed hook has two limits. First, a matcher names the tool, not the effect. Claude can rewrite a file by running a shell command, and a hook matched to the file-editing tools stays silent. That is a lock on the front door with the back door open. So compliance scanning uses a `Stop` hook, which inspects the working tree once per turn.<sup>[2]</sup><sup>[3]</sup>

Second, the argument-level filter, which stops a hook starting on irrelevant calls, fails open when a command cannot be parsed. Failing open means the hook runs anyway. The documentation sends you to the permission system for a hard allow or deny.<sup>[2]</sup> Scope with the filter. Enforce with a layer that does not fail open.

**ELI5.** A guard can stop you only before you walk in. After that, the guard can only write down what you did. So you need both, and the guard must watch every door.

## How Wrong Answers Are Built on This Material

Wrong answers here describe real controls. Each fails the same test.

- **Instruction mistaken for enforcement.** A system prompt, a context file, a refusal policy, or a rule naming banned directories. Each is a sign. None changes what the runtime permits. They fit only for making an attempt rarer.
- **A record offered instead of a refusal.** Logging, alerting, later review, reversal. All wait for the damage. They fit when evidence is the need, not when prevention is.
- **The guarded process checking itself.** The model confirms its own plan or is told to double-check. A run that decided wrongly the first time is the one checking.
- **Enforcement traded away.** Pausing controls while reworking, limiting when the agent may run, replacing a fixed check with advice. Each fixes a cost complaint by removing the control. Aim it at risky actions.

| If the scenario says | Usual answer | Usual trap |
|---|---|---|
| Write access to production, and which controls are truly independent | Scoped credentials, a fixed check before execution, and checking proposed actions before sending | Any option aimed at the model being guarded |
| A rule must hold, and a record must exist even if blocked | Two events: refuse before the call, record after | One check doing both jobs, or a check at session start or end |
| The whole safety plan is one screening step or one instruction | Independent layers on input, output, and the privileged action | Objections about transport security, billing, or forgotten instructions |
| Controls run on every action and things got slow | Keep them for destructive operations and sensitive access | Turning them off, limiting agent hours, or moving the rule to a prompt |
| Values must be in one format before the model thinks about them | Convert after the tool returns, before the model reads it | Telling the model each format, or tidying the wording later |
| A restriction must hold against the person it limits | Managed settings, which no local file or flag overrides | A team convention, or a rule in files that person can edit |

One habit works beyond the table. Picture the steered run and say what the control still does. If the answer is only "it makes the attempt rarer," the control is a sign, not a lock.

**ELI5.** Tricky answers offer a sign, a camera, or a helper checking its own work. None can stop the helper. Ask what still works if the helper already chose wrong.

## What to Remember

- A guardrail holds on a run where the model decided wrongly. Sort every control by two questions: does it need the model's cooperation, and does it run before the effect lands. Controls needing cooperation set a rate. Controls running after the effect produce a record.
- The point of refusal is the moment something other than the model can stop the action. The runtime enforces permission rules, so a prompt or context file changes what is attempted, never what is allowed.
- Layering means three controls that fail separately: screening what reaches the model, screening what it produces, and a hard limit on privileged actions. Name one failure that removes two of them. If you can, the count was wrong.
- Least privilege bounds severity, because a capability never granted cannot be reached by a route nobody predicted. Write the narrow allow: deny beats allow at every scope, and a deny rule has no exceptions.
- A bare tool-name deny removes the tool from context, so Claude never sees it. A scoped deny leaves the tool and blocks matching calls. Managed settings override every local file and flag, which stops the constrained party widening their own scope.
- Permission rules cover what somebody named. Sandboxing covers the rest. Command matching is a permission gate, not a sandbox, and does not reason about what a command would do. OS-level isolation limits filesystem and network reach whatever the model decided.
- `PreToolUse` refuses, `PostToolUse` reports. A hook after the call fires once the tool has run and cannot undo it, so a requirement naming both a policy check and a compliance record needs two hooks at two events.
- Hooks tighten and never loosen. A `PreToolUse` deny holds in every permission mode, bypass included, and a hook returning allow does not defeat a deny rule.
- Scope enforcement to where the consequence lives: destructive operations and sensitive access. A matcher names the tool, not the effect, so a shell command rewriting a file misses a hook matched to the file-editing tools.

**ELI5.** A lock beats a sign, because it works even when the helper chooses badly. Use different locks, give only the keys needed, and keep a notebook.

## Endnotes for this chapter

1. Permission rules are enforced by Claude Code rather than by the model, so instructions in a prompt or CLAUDE.md shape what Claude tries to do but do not change what Claude Code allows, and access is granted or revoked through permission rules, a permission mode or a PreToolUse hook; a deny rule blocks every matching call including calls that also match a narrower allow rule, so a deny rule cannot carry allowlist exceptions, and the same precedence applies between ask and allow; a bare tool name in a deny rule removes the tool from Claude's context entirely so Claude never sees it, while a scoped rule leaves the tool available and blocks matching calls; a hook that exits with code 2 stops the tool call before permission rules are evaluated so the block applies even when an allow rule would let the call proceed, while hook decisions do not bypass deny and ask rules; permission rules follow settings precedence with managed settings highest, so no other level including command line arguments can override a managed permission rule and a tool denied at any level cannot be allowed at another; permissions and sandboxing are complementary layers, with permissions controlling which tools, files and domains Claude Code can reach and sandboxing providing OS-level restriction of the Bash tool's filesystem and network access that prevents commands reaching resources outside defined boundaries even if a prompt injection bypasses Claude's decision-making; and a project's `permissions.allow` rules and `permissions.additionalDirectories` entries grant capability so they apply only after the workspace trust dialog is accepted, while deny and ask rules are unaffected since they only restrict. Anthropic, *Configure permissions* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)

2. Hooks are user-defined shell commands run at specific points in the lifecycle, giving deterministic control so that certain actions always happen rather than relying on the LLM to choose to run them; `PostToolUse` hooks cannot undo actions since the tool has already executed; `PreToolUse` hooks fire before any permission-mode check in every permission mode including `dontAsk`, and a hook returning `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`, which allows enforcement of policy that users cannot bypass by changing their permission mode, while the reverse is not true because a hook returning `"allow"` does not bypass deny rules from settings, so hooks can tighten restrictions but not loosen them past what permission rules allow; where a hook must see every file change, for compliance scanning or audit logging, a `Stop` hook that scans the working tree once per turn is recommended because Claude can also create or modify files by running shell commands; the `if` field filters hooks by tool name and arguments together but fails open, running the hook regardless of pattern, when the Bash command cannot be parsed, and because the filter is best-effort the documentation directs the use of the permission system rather than a hook to enforce a hard allow or deny; and `type: "prompt"` hooks exist for decisions that require judgment rather than deterministic rules, sending the prompt and the hook's input data to a Claude model to make the decision. Anthropic, *Automate actions with hooks* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)

3. `PostToolUse` hooks fire after a tool has already executed successfully, with input carrying both the arguments sent to the tool and the result it returned, and the event cannot block because the tool already ran; `updatedToolOutput` replaces the tool's result, and for redaction or transformation use cases the documented interception points are `PreToolUse` for outbound tool inputs and `PostToolUse` for inbound tool results; and Claude Code does not run a `PostToolUse` hook matching `Edit|Write` when a `Bash` command or a process outside Claude Code rewrites the same file. Anthropic, *Hooks reference* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

4. Agents can take unintended actions due to prompt injection, meaning instructions embedded in content they process, or due to model error; command parsing for permissions parses bash commands into an AST and matches the result against permission rules, with commands that cannot be parsed cleanly or that do not match an allow rule requiring explicit approval and a small set of constructs always requiring approval regardless of allow rules, and this is described as a permission gate rather than a sandbox which, apart from built-in safety checks, does not infer whether a command is dangerous from its target path or effects; a security boundary separates components with different trust levels, so sensitive resources can be placed outside the boundary containing the agent; least privilege restricts the agent to only the capabilities required for its specific task; and defense in depth for high-security environments layers multiple controls, with the listed options being container isolation, network restrictions, filesystem controls, and request validation at a proxy. Anthropic, *Securely deploying AI agents* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/agent-sdk/secure-deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
