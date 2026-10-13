# Chapter 21: A Rule in a Prompt Is Not Enforcement

**Summary**: *A control counts as a guardrail only if it still works on a run where the model (the worker) has already decided wrongly. That one test sorts this whole skill. It also demotes most of what teams actually write down. Sort each control twice. First, does it need the model to cooperate? Second, does it run before the effect lands? Hooks (the door guards), permission rules (the locked doors), identity scope (the keycard) and OS isolation (the building walls) pass both questions. A rule agreed in a meeting and typed into a prompt (a sign on the wall) passes neither. Nobody finds that out on a quiet day.*

## The Rule Was Agreed by Everyone and Refused by Nothing

**First, the idea.** Writing a rule down is not the same as enforcing it. Think of an office building. The model is a **worker** inside it. A rule in a prompt is a **notice on the wall**. A real guardrail is a **locked door**, which stops the worker even if the worker ignores the notice.

**The story.** A team decides their agent writes into **one output directory** and nowhere else. The sentence goes into the **standing instruction** (the notice on the wall) and into the project's **context file** (a second notice in the hallway). It gets reviewed, agreed and shipped.

Months later a **write lands** somewhere else.

**What went wrong?** Nothing failed. No **component threw** an error. The rule had been addressed to the only part of the system whose job is to **weigh sentences against other sentences**. On that run, a **different sentence won**. Anthropic states it plainly. **Permission rules are enforced by Claude Code** rather than by the model. Instructions in a prompt or a **context file** shape what Claude tries to do. They do not change what the **runtime allows**.<sup>[1]</sup>

**The missing piece.** Call it the **point of refusal**. It is the **moment in the sequence** where something other than the model can still **stop the action**. In the building, that is a locked door. A control with no point of refusal is advice. Good advice, often. But advice.

**ELI5.** Imagine a sign on a door that says "please don't go in". A kind worker obeys it. A worker who got tricked, or who just made a mistake, walks right in. A locked door stops both of them. Only the locked door counts as a guardrail.

## Two Questions Sort Every Control You Are Offered

**First, the idea.** Every control you are offered can be sorted with two questions. Both start from the same assumption: the worker has already made the wrong call.

**The assumption.** Begin from the assumption that costs nothing and settles everything. The **model has already decided wrongly** on this run. A **planted instruction** (a trick hidden in content the agent reads) and an **ordinary mistake** change nothing about what follows. Anthropic's threat model names the **two routes** together for that reason.<sup>[4]</sup>

**The two questions.** Ask both of any control before you count it as a layer:
- Does it **need the model to cooperate**? (Does it rely on the worker choosing to obey?)
- Does it run **before the effect lands**? (Does it act before the door is already open and the damage done?)

| Control | Needs cooperation | Runs before the effect | What it produces on a steered run |
|---|---|---|---|
| A rule in the standing instruction or context file (a notice on the wall) | Yes | Not applicable | Intent, with no refusal underneath it |
| The model asked to confirm its own proposal (the worker checking their own work) | Yes | Yes | A second opinion from the first opinion |
| A `PreToolUse` hook (a guard at the door) | No | Yes | A refusal, and a reason returned to the model |
| A permission deny rule (a locked door) | No | Yes | A refusal the settings own |
| The scope of the identity the agent acts as (the keycard) | No | Yes | An operation that was never reachable |
| OS-level sandboxing around the process (the building walls) | No | Yes | A limit no rule had to name in advance |
| A `PostToolUse` hook, or an audit record (the logbook) | No | No | Evidence of what already happened |

"A steered run" means a run where the model has been pushed into the wrong decision.

**Which rows count?** The bottom five rows are **layers**. The top two are the **guarded process doing its own guarding**. That adds a step and no independence, because the worker is checking the worker.

**How to read the table.** Read the **last column** rather than the first. **Two rows reach refusal** by different routes. The bottom row earns its place for a reason unrelated to **prevention**: it leaves a record.

**ELI5.** Ask two things about any safety measure. Does it need the worker to behave? Does it work before something bad happens? A locked door needs no help from the worker and works first. A logbook works only afterwards, so it tells you what happened but cannot stop it.

## A Layer Earns the Name by Failing Without Taking Its Neighbours Down

**First, the idea.** **Layering** means several controls that fail separately. It does not mean several controls. Counting them is not the same thing.

**The problem with counting.** Three controls resting on **one dependency** behave as one control **drawn three times**. The drawing is what makes a review feel finished. Picture three notices on three walls. They all depend on the same worker choosing to read them.

**What does hold?** The arrangement that holds puts a control at **three positions that fail separately**:
- what **reaches the model** (who gets in the front door)
- what the **model produces** (what the worker carries out)
- what a **privileged action is allowed** to do (what the vault door permits)

Screening decides how often something lands. The hard limit on the action decides how bad it gets when screening misses. Neither substitutes for the other. Anthropic's hardening guidance lists **isolation, network restriction, filesystem control and proxy validation** as options to combine rather than choose between.<sup>[4]</sup>

**The anti-pattern: the stack that shares a failure.** The **stack that shares a failure** is built out of sensible parts. An instruction to refuse, a reminder to self-check and a closing prompt to summarise are **three sentences read by one reader**. Chapter 20 sorts screening in detail. Carry one property from it: a probabilistic control (one that works most of the time) **sets a rate** and **never a floor**.

**The independence test.** It is short enough to run while you read a scenario. Name one failure that **removes two** of them at once. If you can, the **count was wrong**.

**ELI5.** Three locks on one door that all open with the same key are really one lock. Real layers are different kinds of protection, so one broken thing cannot open them all. If you can find one thing that breaks two of your protections at once, you have fewer protections than you thought.

## What the Identity Permits Bounds Everything a Steered Agent Can Do

**First, the idea.** The strongest limit is what the agent was never given. In the building, this is the **keycard**. The keycard opens only the doors the worker needs. This is **scope** (what the identity the agent acts as is allowed to do).

**Why scope is different.** Every other control in this chapter can be missing, misconfigured, or never written for the path your agent actually took. **Scope** is different, because a **capability that was never granted** cannot be reached by a **route nobody predicted**. Anthropic states the design rule: restrict the agent to only the **capabilities its specific task requires**.<sup>[4]</sup> This is **least privilege** (give only what the job needs).

**What it buys: lower severity.** **Severity** is what this buys. An agent whose **identity can write anywhere** turns one steered decision into an **incident**. The same decision, made by an identity holding **one writable directory**, ends as a **denied call** and a line in a log.

**Four mechanics.** **Four mechanics decide** whether the scope you wrote is the scope that runs.

| What you write | What it does to the capability | What can widen it |
|---|---|---|
| A rule in the prompt or the context file (a notice) | Nothing at all | Any sentence weighed against it |
| A scoped deny rule such as one naming a command pattern (a lock on one door) | Leaves the tool present, blocks matching calls | Nothing below the scope it sits in |
| A bare tool-name deny rule (the door removed from the map) | Removes the tool from context, so Claude never sees it | Nothing below the scope it sits in |
| A deny rule in managed settings (the landlord's lock) | Same, organisation-wide | Nothing on the machine, command-line flags included |

**Two consequences.**
- **Deny beats allow at every scope.** So a deny rule cannot carry an **allowlist exception**. The **narrow allow** is the rule you write.<sup>[1]</sup>
- A **grant needs trust** where a restriction does not. A project's allow rules and additional directories apply only after the **workspace trust dialog** is accepted. Its **deny and ask rules** take effect regardless, because they only ever restrict.<sup>[1]</sup>

**The anti-pattern: the broad deny with a carve-out.** The **broad deny with a carve-out** is the anti-pattern the first consequence kills. You cannot lock everything and then poke an exception through the lock, because deny wins.

**A quieter rule underneath.** Whatever can **edit the scope holds the scope**. So changing permission configuration is itself a **privileged action**. Your administrator's copy has to win. That makes a **managed rule** that no local setting or flag can override a **security property** rather than an inconvenience.<sup>[1]</sup>

**Rules versus isolation.** Credentials sit one layer further out and belong to chapter 22. **Command parsing** checks a shell command against permission rules. It asks for approval when it cannot parse cleanly or **matches no allow rule**. Anthropic labels that machinery a **permission gate rather than a sandbox**, because it does not reason about what a **command's target path** would actually do.<sup>[4]</sup> **Rules cover** what you thought to name. **Isolation covers** the rest. Sandboxing (the building walls) is the complementary layer. It restricts the **filesystem and network reach** of shell commands at the **operating-system level**. That holds even where an injection got past the model's own decision-making.<sup>[1]</sup>

**ELI5.** Give a worker a keycard that opens only the one room they need. Then even a tricked worker can only reach that room. A rule can only lock the doors you remembered. Thick walls around the whole building stop the rest.

## A Hook Chooses Where the Refusal Sits in Time

**First, the idea.** A **hook** (a small program that runs at a set point in the agent's loop) is a guard standing at one spot in time. Some spots come before the action, so the guard can still say no. Some come after, so the guard can only write it down.

**Where hooks fit.** Chapter 13 built the hook and covered its precedence. Safety needs one thing from it. Hook events **divide the loop** into places that can **still refuse** and places that can **only report**. A **`PostToolUse` hook fires** after a tool has **already executed successfully**, so it cannot undo the action.<sup>[2]</sup><sup>[3]</sup>

**A scenario worth recognising.** A policy has to be applied to **every privileged action**. A **compliance record** also has to exist for a human reviewer, whether or not the action was permitted. Those are **two requirements at two vantage points**.
- **Denial** is available only while the **call is still pending**.
- A **truthful record** is possible only once the call has resolved.

So you need a **pair of hooks** rather than one clever one. A check at **session start** has no specific action in front of it. A sweep once the **session has closed** arrives **too late** to have refused anything.

**Position also buys transformation.** Refusal is not the only thing position buys. Sometimes a **deterministic transformation** (a fixed rule, not a judgement) has to happen before the model reasons over a value. Anthropic documents the **two seats** for it. Intercept at **`PreToolUse` for outbound tool inputs**. Intercept at **`PostToolUse` for inbound tool results**, where a returned field **replaces the result** the model goes on to read.<sup>[3]</sup> Suppose tool results arrive in **incompatible formats**. They get **canonicalised** (converted to one standard form) there. The fix is not an instruction to remember which service uses which.

**The anti-pattern: the deterministic rule handed back to the model.** The **deterministic rule handed back to the model** wears rigour well. Prompt-based hooks exist. They put a model in the decision seat deliberately. That suits a **judgement call** and not an **absolute rule**.<sup>[2]</sup>

**Two documented behaviours.**
- A **`PreToolUse` hook fires** before any **permission-mode check**, in every mode. A deny from it blocks the tool even in **bypass mode**. That is what lets policy survive a user changing their own settings.
- The reverse does not hold. A **hook returning allow** does not defeat a **deny rule**. So **hooks tighten and never loosen**.<sup>[2]</sup>

**Scope them where the consequence lives.** Hooks on every action buy you **latency** (waiting time) on the ones that could not hurt anybody. The repairs that look adjacent all **remove enforcement** instead of aiming it. These are **turning hooks off** during a rework, running the agent less often, or **relocating the rule** into the prompt. Keep hooks on **destructive operations and sensitive access**.

**Two limits keep an aimed hook honest.**
- A **matcher names the tool, not the effect**. Claude can **rewrite a file** by running a **shell command**. A hook matching the **file-editing tools** does not fire when that happens. This is why compliance scanning uses a **`Stop` hook** that inspects the working tree once per turn.<sup>[2]</sup><sup>[3]</sup>
- The **argument-level filter** keeps a hook from spawning on irrelevant calls. It **fails open** (it runs the hook anyway) when a command cannot be parsed. This is why the documentation directs a **hard allow or deny** to the permission system instead.<sup>[2]</sup>

Scope with the **best-effort filter**. Enforce with the layer that does not **fail open**.

**ELI5.** A guard at the door can stop you before you go in. A guard who only writes your name in a book after you leave cannot. If you need both a stopped door and a written record, you need two guards. And a guard who only watches the front door misses the person who climbs through the window.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers on this topic are not silly. They describe real controls that real teams build. Each one fails the same test: the worker has already made the wrong call.

**The shape of a wrong answer.** Wrong answers here describe **controls that exist**, that experienced humans build, and that appear in **real deployments**. Each **fails one test**, and it is always the same run: the model has already **decided wrongly**.

- **Instruction mistaken for enforcement.** A **system prompt**, a **context file**, a **refusal policy**, a **rule naming the directories** that are off limits. Each **shapes what gets attempted** and none **changes what the runtime permits**. So all are **absent on the one run** a guardrail exists for. They become correct where the question asks how to make an **attempt rarer**.
- **Recording offered where refusal was available.** **Logging the action**, **alerting** on it, **reviewing it later**, **reversing it afterwards**. Each needs the effect to have **happened first**. They are correct where **evidence is the requirement**. They are the wrong half of any question naming both **prevention and a record**.
- **The guarded process asked to guard itself.** **Self-confirmation**, a **second pass by the same model**, an instruction to **double-check before acting**. This adds a step and **no independence**, because a run that **decided wrongly the first time** is the run doing the checking.
- **Enforcement traded away** while appearing to tune it. **Suspending controls** during a rework, **narrowing the hours** the agent runs, **swapping a deterministic check for guidance**. Each answers a **real complaint about cost** by **removing the control**. None of them points the control at the **actions that carry consequence**.

**The scenario table.**

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Write access to production, and which controls are genuinely independent | Scoped credentials, a deterministic check before execution, and validation of proposed actions before dispatch | Any option addressed to the model that is being guarded |
| A rule must hold and a record must exist whether or not the action proceeded | Two events: refuse before the call, record after it | One check doing both, or a check at session start or session end |
| The entire safety approach is one screening step or one instruction | Independent layers on input, on output, and on the privileged action | Objections about transport security, billing, or instructions being forgotten |
| Controls fire on every action and the run has become slow | Keep them on destructive operations and sensitive access, drop the rest | Suspending them, restricting when the agent runs, or moving the rule into a prompt |
| Values must be normalised before the model reasons over them | Convert in the gap after a tool returns and before its result is read | Asking the model to remember each format, or repairing the wording afterwards |
| A restriction must survive the person it constrains | Managed settings, which no local file or flag overrides | A documented convention, or a rule in files the constrained party can edit |

**One habit that transfers.** For any control offered, **describe the run** where the **model has already been steered**. Then say what that control still does on it. An answer that stops at making the **attempt rarer** has told you where the control belongs, which is **above the floor** rather than at it.

**ELI5.** Most wrong answers are real safety measures that only work if the worker behaves. So ask yourself one question every time. If the worker has already gone wrong, what does this measure still do? If the answer is "nothing", it is a notice on the wall and not a lock.

## What to Remember

- A **guardrail holds** on a run where the **model decided wrongly**. **Sort every control** by two questions: does it **need the model's cooperation**, and does it **run before the effect lands**. Controls needing cooperation **set a rate**. Controls running after the effect **produce a record**.
- The **point of refusal** is the **moment** something other than the model can **stop the action**. **Permission rules are enforced by the runtime**, so a **prompt or context file** changes what is **attempted** and never what is **allowed**.
- **Layering means three controls that fail separately**: screening what **reaches the model**, screening what it **produces**, and a **hard limit on privileged actions**. Test it by naming one failure that **removes two** of them. If you can, the **count was wrong**.
- **Least privilege bounds severity**, because a **capability never granted** cannot be reached by a **route nobody predicted**. Write the narrow allow. **Deny beats allow at every scope** and a deny rule carries **no exceptions**.
- A **bare tool-name deny removes the tool** from context so Claude never sees it. A **scoped deny** leaves the tool and **blocks matching calls**. **Managed settings override every local file and flag**, which is what stops the constrained party **widening their own scope**.
- **Permission rules cover what somebody named**. **Sandboxing covers the rest**. Command matching is a **permission gate rather than a sandbox** and does not reason about what a command would do. **OS-level isolation limits filesystem and network reach** whatever the model decided.
- **`PreToolUse` refuses, `PostToolUse` reports**. A hook after the call **fires** only once the **tool has executed** and **cannot undo** it. So a requirement naming both a **policy check** and a **compliance record** needs **two hooks at two events**.
- **Hooks tighten and never loosen**. A `PreToolUse` deny holds in every **permission mode**, **bypass included**. A **hook returning allow** does not defeat a **deny rule**.
- **Scope enforcement** to where the **consequence lives**, keeping hooks on **destructive operations and sensitive access**. A **matcher names the tool, not the effect**: a **shell command** rewriting a file misses a hook matched to the **file-editing tools**.

**ELI5.** A sign on the wall only works on workers who read it. A locked door works on everyone. Give each worker a keycard for just their rooms, put a guard at the doors that matter, and keep a logbook for afterwards.

## Endnotes for this chapter

1. Permission rules are enforced by Claude Code rather than by the model, so instructions in a prompt or CLAUDE.md shape what Claude tries to do but do not change what Claude Code allows, and access is granted or revoked through permission rules, a permission mode or a PreToolUse hook; a deny rule blocks every matching call including calls that also match a narrower allow rule, so a deny rule cannot carry allowlist exceptions, and the same precedence applies between ask and allow; a bare tool name in a deny rule removes the tool from Claude's context entirely so Claude never sees it, while a scoped rule leaves the tool available and blocks matching calls; a hook that exits with code 2 stops the tool call before permission rules are evaluated so the block applies even when an allow rule would let the call proceed, while hook decisions do not bypass deny and ask rules; permission rules follow settings precedence with managed settings highest, so no other level including command line arguments can override a managed permission rule and a tool denied at any level cannot be allowed at another; permissions and sandboxing are complementary layers, with permissions controlling which tools, files and domains Claude Code can reach and sandboxing providing OS-level restriction of the Bash tool's filesystem and network access that prevents commands reaching resources outside defined boundaries even if a prompt injection bypasses Claude's decision-making; and a project's `permissions.allow` rules and `permissions.additionalDirectories` entries grant capability so they apply only after the workspace trust dialog is accepted, while deny and ask rules are unaffected since they only restrict. Anthropic, *Configure permissions* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)

2. Hooks are user-defined shell commands run at specific points in the lifecycle, giving deterministic control so that certain actions always happen rather than relying on the LLM to choose to run them; `PostToolUse` hooks cannot undo actions since the tool has already executed; `PreToolUse` hooks fire before any permission-mode check in every permission mode including `dontAsk`, and a hook returning `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`, which allows enforcement of policy that users cannot bypass by changing their permission mode, while the reverse is not true because a hook returning `"allow"` does not bypass deny rules from settings, so hooks can tighten restrictions but not loosen them past what permission rules allow; where a hook must see every file change, for compliance scanning or audit logging, a `Stop` hook that scans the working tree once per turn is recommended because Claude can also create or modify files by running shell commands; the `if` field filters hooks by tool name and arguments together but fails open, running the hook regardless of pattern, when the Bash command cannot be parsed, and because the filter is best-effort the documentation directs the use of the permission system rather than a hook to enforce a hard allow or deny; and `type: "prompt"` hooks exist for decisions that require judgment rather than deterministic rules, sending the prompt and the hook's input data to a Claude model to make the decision. Anthropic, *Automate actions with hooks* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)

3. `PostToolUse` hooks fire after a tool has already executed successfully, with input carrying both the arguments sent to the tool and the result it returned, and the event cannot block because the tool already ran; `updatedToolOutput` replaces the tool's result, and for redaction or transformation use cases the documented interception points are `PreToolUse` for outbound tool inputs and `PostToolUse` for inbound tool results; and Claude Code does not run a `PostToolUse` hook matching `Edit|Write` when a `Bash` command or a process outside Claude Code rewrites the same file. Anthropic, *Hooks reference* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)

4. Agents can take unintended actions due to prompt injection, meaning instructions embedded in content they process, or due to model error; command parsing for permissions parses bash commands into an AST and matches the result against permission rules, with commands that cannot be parsed cleanly or that do not match an allow rule requiring explicit approval and a small set of constructs always requiring approval regardless of allow rules, and this is described as a permission gate rather than a sandbox which, apart from built-in safety checks, does not infer whether a command is dangerous from its target path or effects; a security boundary separates components with different trust levels, so sensitive resources can be placed outside the boundary containing the agent; least privilege restricts the agent to only the capabilities required for its specific task; and defense in depth for high-security environments layers multiple controls, with the listed options being container isolation, network restrictions, filesystem controls, and request validation at a proxy. Anthropic, *Securely deploying AI agents* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/agent-sdk/secure-deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
