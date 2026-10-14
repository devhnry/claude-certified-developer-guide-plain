# Chapter 21: A Rule in a Prompt Is Not Enforcement

**Summary**: *Ask one question of any control: does it still work on a run where the model has already made the wrong call? If yes, it is a guardrail. If no, it is advice. Sort each control with two checks. Does it need the model to cooperate? Does it run before the effect lands? Hooks, permission rules, identity scope and OS isolation pass both tests. A rule typed into a prompt passes neither. Nobody finds that out on a quiet day.*

## The Rule Was Agreed by Everyone and Refused by Nothing

Picture a team that wants its agent to write into one output folder and nowhere else. They put that sentence in the standing instruction. They put it in the project's context file too. Everyone reviews it and agrees.

Months later, a file shows up in the wrong place.

Nothing crashed. There was no error. The rule was only a sentence, and Claude weighs sentences against other sentences. On that run, a different sentence won.

Here is the fact to remember. Claude Code enforces permission rules. The model does not. A prompt or a context file changes what Claude *tries* to do. It does not change what Claude is *allowed* to do. <sup>[1]</sup>

What was missing is a **point of refusal**. That is a moment where something other than the model can still stop the action. Without one, a control is only advice. Maybe good advice. Still advice.

Here is the one analogy for this chapter. A "keep out" sign is a rule in a prompt. A locked door is a permission rule. The sign works on people who read it and agree. The door works on everyone.

## Two Questions Sort Every Control You Are Offered

Assume the worst. On this run, the model has already decided wrongly. Maybe someone hid an instruction in a document it read. Maybe it just slipped. Either way, what follows is the same. Anthropic's threat model lists both causes together for that reason.<sup>[4]</sup>

Before you call something a layer, ask two things. Does it need the model to cooperate? Does it run before the effect lands?

| Control | Needs the model's help | Acts before the damage | What you get when the run is steered |
|---|---|---|---|
| A rule written in the standing instruction or context file | Yes | Not applicable | A wish, with nothing behind it to say no |
| The model asked to confirm its own proposal | Yes | Yes | The first opinion asked for a second opinion |
| A `PreToolUse` hook | No | Yes | A no, and the reason is handed back to the model |
| A permission deny rule | No | Yes | A no that lives in the settings |
| What the agent's identity is allowed to touch | No | Yes | A step the agent has no way to take |
| OS-level sandboxing around the process | No | Yes | A wall nobody had to write a rule for |
| A `PostToolUse` hook, or an audit record | No | No | A receipt for something already done |

Only the bottom five rows count as layers. The top two are the guarded process guarding itself. That adds a step but no independence.

Look at the last column first. Two rows can actually refuse, by different routes. The bottom row is useful too, but not for prevention.

## A Layer Earns the Name by Failing Without Taking Its Neighbours Down

Three locks that open with one key are really one lock. Drawing it three times just makes a review feel finished.

**Layering** means controls at three places that fail on their own. They sit on what reaches the model, what the model produces, and what a privileged action may do. Screening controls how often a bad thing gets through. A hard limit controls the damage when screening misses. One cannot stand in for the other. Anthropic lists isolation, network restriction, filesystem control and proxy validation. You combine them. You do not pick one.<sup>[4]</sup>

The classic mistake is a stack that shares one failure. Say it holds an instruction to refuse, a reminder to self-check, and a closing prompt to summarise. That is three sentences, read by one reader. Chapter 20 covers screening. Take one idea from it. A control that works by probability sets a rate. It never sets a floor.

Use the independence test. Try to name one failure that knocks out two of your controls at once. If you can, your count of layers was wrong.

## What the Identity Permits Bounds Everything a Steered Agent Can Do

Any other control here can be missing, set up wrong, or written for a different path than the one your agent took. Scope is different. If a capability was never given, no route can reach it, even one nobody expected. Anthropic's design rule is simple. Give the agent only the capabilities its task needs.<sup>[4]</sup>

The payoff is lower severity. Say the agent's identity can write anywhere. One bad decision becomes an incident. Say it can write to one folder. The same decision ends as a denied call and a line in a log.

Four mechanics decide if the scope you wrote is the scope that actually runs.

| What you write | Effect on the capability | What can make it bigger |
|---|---|---|
| A rule in the prompt or context file | None | Any competing sentence |
| A scoped deny rule, for example one naming a command pattern | Tool stays, matching calls are blocked | Nothing at a lower level |
| A bare tool-name deny rule | Tool is taken out of context, so Claude never sees it | Nothing at a lower level |
| A deny rule in managed settings | Same result, across the organisation | Nothing on that machine, even command-line flags |

Two things follow.

First, deny beats allow at every scope. So no allow rule can carve an exception out of a deny rule. Write the narrow allow instead.<sup>[1]</sup> A broad deny with a carve-out does not work.

Second, giving access needs trust. Limiting access does not. A project's allow rules and extra directories apply only after you accept the workspace trust dialog. Its deny and ask rules apply either way, because they only restrict.<sup>[1]</sup>

One quieter rule sits underneath. Whoever can edit the scope owns the scope. So changing permission settings is itself a privileged action. Your administrator's copy has to win. That is why a managed rule, which no local setting or flag can override, is a security property and not an annoyance.<sup>[1]</sup>

Credentials sit one layer further out. Chapter 22 covers them. Command parsing checks a shell command against permission rules. It asks for approval when it cannot parse the command cleanly or finds no allow rule. Anthropic calls this a permission gate, not a sandbox. It does not work out what a command would do to its target path.<sup>[4]</sup> Rules cover only what you thought to name. Isolation handles everything else. Sandboxing limits what shell commands can reach on the filesystem and network, at the operating-system level. That holds even when an injection got past the model's own decision.<sup>[1]</sup>

## A Hook Chooses Where the Refusal Sits in Time

Chapter 13 already built the hook and its precedence. For safety, one point is enough. Hook events split the loop into moments that can still refuse and moments that can only report. A `PostToolUse` hook fires after a tool has already run successfully. It cannot undo anything.<sup>[2]</sup><sup>[3]</sup>

That solves a common exam scenario. A policy must be checked on every privileged action. A compliance record must also exist for a human reviewer, whether or not the action was allowed. These are two needs at two moments. You can deny only while the call is pending. You can record the truth only once it has finished. So you need a pair of hooks, not one clever hook. At session start there is no action to check yet. After the session closes, nothing is left to refuse.

Position buys more than refusal. Sometimes a value must be changed in a fixed way before the model reasons about it. Anthropic documents two places. Use `PreToolUse` for inputs going out to a tool. Use `PostToolUse` for results coming back, where a returned field replaces the result the model reads next.<sup>[3]</sup> Say two services return dates in different formats. Convert them there. Do not ask the model to remember which service uses which.

Handing a fixed rule back to the model is the mistake to watch for. It looks careful. Prompt-based hooks do exist. They put a model in the decision seat on purpose. That suits a judgement call. It does not suit an absolute rule.<sup>[2]</sup>

Two more documented behaviours finish the picture. A `PreToolUse` hook fires before any permission-mode check, in every mode. If it denies, the tool is blocked even in bypass mode. So policy survives a user changing their own settings. The reverse is false. A hook that returns allow does not beat a deny rule. Hooks tighten and never loosen.<sup>[2]</sup>

Aim hooks at where the damage can happen. A hook on every action adds delay to calls that could never hurt anyone. People often cure that delay by removing enforcement. They turn hooks off during a rework, run the agent less often, or move the rule into the prompt. Do none of these. Put them on destructive operations and sensitive access.

An aimed hook has two limits.

First, a matcher names the tool, not the effect. Claude can rewrite a file by running a shell command. A hook matched to the file-editing tools stays silent then. That is why compliance scanning uses a `Stop` hook, which inspects the working tree once per turn.<sup>[2]</sup><sup>[3]</sup>

Second, the argument-level filter, which stops a hook starting on irrelevant calls, fails open when a command cannot be parsed. Failing open means the hook runs anyway. So the documentation sends you to the permission system for a hard allow or deny.<sup>[2]</sup> Use the best-effort filter to scope. Use a layer that does not fail open to enforce.

## How Wrong Answers Are Built on This Material

Wrong answers here describe controls that really exist. Experienced people build them. Each fails the same test: the model has already decided wrongly.

- **Instruction mistaken for enforcement.** Think of a system prompt, a context file, a refusal policy, or a rule that names banned directories. Each shapes what gets attempted. None changes what the runtime permits. They are the right pick only if the question is about making an attempt rarer.
- **A record offered instead of a refusal.** Logging, alerting, later review, reversal. All of them wait for the damage. They fit when evidence is the need. They are the wrong half of an answer that asks for prevention and a record.
- **The guarded process checking itself.** The model confirms its own plan, runs a second pass, or gets told to double-check. A run that decided wrongly the first time is the one doing the checking.
- **Enforcement traded away.** Pausing controls while reworking, limiting when the agent may run, replacing a fixed check with advice. Each fixes a real cost complaint by removing the control. Point it at the actions that carry real consequences instead.

| If the scenario says | Usual answer | Usual trap |
|---|---|---|
| Write access to production, and which controls are truly independent | Scoped credentials, a fixed check before execution, and checking proposed actions before they are sent | Any option aimed at the model that is being guarded |
| A rule must hold, and a record must exist even if the action was blocked | Two events: refuse before the call, record after it | One check doing both jobs, or a check at session start or end |
| The whole safety plan is one screening step or one instruction | Independent layers on input, on output, and on the privileged action | Objections about transport security, billing, or instructions being forgotten |
| Controls run on every action and things got slow | Keep them only for destructive operations and sensitive access | Turning them off, restricting agent hours, or moving the rule to a prompt |
| Values must be put in one format before the model thinks about them | Convert after the tool returns, before the model reads the result | Telling the model to remember each format, or tidying the wording later |
| A restriction must hold against the person it limits | Managed settings, which no local file or flag can override | A team convention, or a rule in files that person can edit |

One habit works beyond the table. For any control, picture the run where the model was already steered. Then say what the control still does. If the answer is only "it makes the attempt rarer," the control sits above the floor, not at it.

## What to Remember

- A real guardrail still works when the model got it wrong. Two questions sort controls. Does it need the model? Does it run before the effect? Controls that need the model set a rate. Controls that run afterwards give a record.
- The point of refusal is a moment when something besides the model can say no. The runtime enforces permission rules. A prompt or context file changes what is attempted, never what is allowed.
- Layering means three independent controls. One guards input, one guards output, one puts a hard limit on privileged actions. If a single failure removes two, you miscounted.
- Least privilege caps severity. A capability never granted cannot be reached by an unexpected route. Write the narrow allow. Deny beats allow at every scope, with no exceptions.
- A bare tool-name deny removes the tool from context, so Claude never sees it. A scoped deny keeps the tool and blocks matching calls. Managed settings beat every local file and flag. That stops people widening their own scope.
- Permission rules cover what somebody named. Sandboxing covers the rest. Command matching is a permission gate, not a sandbox. OS-level isolation limits filesystem and network reach whatever the model decided.
- `PreToolUse` refuses. `PostToolUse` reports. It fires only after the tool has run and cannot undo it. A policy check plus a compliance record needs two hooks at two events.
- A hook can only make things stricter. A `PreToolUse` deny holds in every permission mode, bypass included. A hook returning allow does not beat a deny rule.
- Use hooks on destructive operations and sensitive access. A matcher names the tool, not what happens. A shell command can rewrite a file and slip past a hook matched to the file-editing tools.

## Endnotes for this chapter

1. Permission rules are enforced by Claude Code rather than by the model, so instructions in a prompt or CLAUDE.md shape what Claude tries to do but do not change what Claude Code allows, and access is granted or revoked through permission rules, a permission mode or a PreToolUse hook; a deny rule blocks every matching call including calls that also match a narrower allow rule, so a deny rule cannot carry allowlist exceptions, and the same precedence applies between ask and allow; a bare tool name in a deny rule removes the tool from Claude's context entirely so Claude never sees it, while a scoped rule leaves the tool available and blocks matching calls; a hook that exits with code 2 stops the tool call before permission rules are evaluated so the block applies even when an allow rule would let the call proceed, while hook decisions do not bypass deny and ask rules; permission rules follow settings precedence with managed settings highest, so no other level including command line arguments can override a managed permission rule and a tool denied at any level cannot be allowed at another; permissions and sandboxing are complementary layers, with permissions controlling which tools, files and domains Claude Code can reach and sandboxing providing OS-level restriction of the Bash tool's filesystem and network access that prevents commands reaching resources outside defined boundaries even if a prompt injection bypasses Claude's decision-making; and a project's `permissions.allow` rules and `permissions.additionalDirectories` entries grant capability so they apply only after the workspace trust dialog is accepted, while deny and ask rules are unaffected since they only restrict. Anthropic, *Configure permissions* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)

2. Hooks are user-defined shell commands run at specific points in the lifecycle, giving deterministic control so that certain actions always happen rather than relying on the LLM to choose to run them; `PostToolUse` hooks cannot undo actions since the tool has already executed; `PreToolUse` hooks fire before any permission-mode check in every permission mode including `dontAsk`, and a hook returning `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`, which allows enforcement of policy that users cannot bypass by changing their permission mode, while the reverse is not true because a hook returning `"allow"` does not bypass deny rules from settings, so hooks can tighten restrictions but not loosen them past what permission rules allow; where a hook must see every file change, for compliance scanning or audit logging, a `Stop` hook that scans the working tree once per turn is recommended because Claude can also create or modify files by running shell commands; the `if` field filters hooks by tool name and arguments together but fails open, running the hook regardless of pattern, when the Bash command cannot be parsed, and because the filter is best-effort the documentation directs the use of the permission system rather than a hook to enforce a hard allow or deny; and `type: "prompt"` hooks exist for decisions that require judgment rather than deterministic rules, sending the prompt and the hook's input data to a Claude model to make the decision. Anthropic, *Automate actions with hooks* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)

3. `PostToolUse` hooks fire after a tool has already executed successfully, with input carrying both the arguments sent to the tool and the result it returned, and the event cannot block because the tool already ran; `updatedToolOutput` replaces the tool's result, and for redaction or transformation use cases the documented interception points are `PreToolUse` for outbound tool inputs and `PostToolUse` for inbound tool results; and Claude Code does not run a `PostToolUse` hook matching `Edit|Write` when a `Bash` command or a process outside Claude Code rewrites the same file. Anthropic, *Hooks reference* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

4. Agents can take unintended actions due to prompt injection, meaning instructions embedded in content they process, or due to model error; command parsing for permissions parses bash commands into an AST and matches the result against permission rules, with commands that cannot be parsed cleanly or that do not match an allow rule requiring explicit approval and a small set of constructs always requiring approval regardless of allow rules, and this is described as a permission gate rather than a sandbox which, apart from built-in safety checks, does not infer whether a command is dangerous from its target path or effects; a security boundary separates components with different trust levels, so sensitive resources can be placed outside the boundary containing the agent; least privilege restricts the agent to only the capabilities required for its specific task; and defense in depth for high-security environments layers multiple controls, with the listed options being container isolation, network restrictions, filesystem controls, and request validation at a proxy. Anthropic, *Securely deploying AI agents* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/agent-sdk/secure-deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
