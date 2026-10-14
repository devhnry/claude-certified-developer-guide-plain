# Chapter 15: The Constraints Nobody States Decide the Design

**Summary**: *The system you are changing has traits nobody wrote in the ticket. Add a cache to a multi-tenant authorization path and you may break one of them, quietly, once, months on. Two kinds of requirement sit between a vague business aim and a design you can defend. One is behaviour someone can mark pass or fail. The other is a set of deployment limits you only learn by asking. Learn the second kind late and the fix is a migration, not a setting.*

## The Request Describes the Change and the System Describes the Constraints

Say you ask a contractor to knock out a kitchen wall. Inside it sit a gas pipe and wiring you never mentioned. A good contractor asks before swinging the hammer.

Now take a ticket. The authorization module is slow, the page waits on it, so add a cache in front. The ticket has a component, a symptom, a fix and an owner. It looks complete.

Look at the system instead. Several customers share this deployment. Each access decision lands in a log that someone audits. The old cache-clearing rule (invalidation) works differently on different paths. The team knows, and has never written it down.

Those are the pipes in the wall. They held last quarter. They will hold after the cache ships. Call each one a **standing constraint**. It is a fact about the environment. It was there before the request, nobody mentions it when describing the work, and it still decides the design.

A missing feature shows itself the first time someone runs it. A cache that breaks a standing constraint hides. Months later, once, one tenant gets another tenant's decision. Silent, rare and expensive: iteration cannot catch that, because iteration needs a signal and this gives none until it gives a huge one.

So do not open with code or a design. Open with questions. What must stay true? What invalidates an entry? What must the audit trail record? What happens when the cache is wrong? Anthropic says Claude needs the same step. Jumping straight to code can solve the wrong problem, so exploring and planning are kept apart from doing.<sup>[1]</sup>

**ELI5.** Before cutting into a wall, ask what is inside it. Pipes are there even if no one said so.

## A Goal You Cannot Fail Is Not Yet a Requirement

"Get invoices approved sooner." "Stop the compliance team reading every document." Good wishes, but you cannot build or test against them. "Make the kitchen nicer" has the same flaw.

A **functional requirement** says what the system must do. It is sharp enough for a reviewer to give a pass or a fail. To get these, split one direction into several checkable behaviours. Flag each document as needing review or not. Quote the clause behind each flag. Keep a flagged document unapproved until a named reviewer clears it. You can run and score each one. The direction itself you cannot.

The test is mechanical. Read the statement. Ask what you could observe that would show it was broken. If nothing, it is a preference.

Anthropic's own success criteria follow this rule.<sup>[2]</sup> It swaps "good performance" for "accurate sentiment classification". It swaps "safe outputs" for a count: under 0.1% of outputs, over 10,000 trials, flagged by the content filter.

The requirement nobody can fail is the trap, because everyone agrees with it. Fast, accurate, secure: all sign. Nothing was agreed. Two people picture two systems and find out at review.

**ELI5.** "Make it nice" can never be wrong, so no one can check it. "The door closes with no gap" can be checked. A good requirement is one you can fail.

## The Second Set of Requirements Sits on Other People's Desks

Nobody has to dig for functional requirements. The person who wants the feature tells you what it should do.

Infrastructure requirements fence in the deployment instead of describing behaviour. They say little about what the system produces and plenty about when producing it is acceptable. You get them by asking, not reading, because the holder finds each one obvious and never says it. Like building codes: nobody mentions them, but the inspector will. Most of the ground is covered by four questions.

| The question | Who holds the answer | What a late answer costs |
|---|---|---|
| How fast, measured where the user is | The experience owner, and whoever runs the region | A model, platform or topology picked against the wrong number |
| What volume, and what the peak looks like | Operations, plus keepers of historical figures | Capacity and rate limits sized for the average |
| Processed where, stored where, under which regulation | Legal, compliance, data protection | A rebuild, since some settings are fixed at creation |
| Acting under whose credentials, auditable how | Security, and the owner of the system acted upon | An audit trail that cannot answer its own question |

The last column shows why this work goes first. Asking the four costs a conversation. Answers that come late cost a migration. Trading off a latency figure once you hold it is chapter 4's topic. Getting the figure is this chapter's.

One trap looks like diligence. A latency budget tells you nothing about which tenant may see which record. Speed targets and correctness rules are different statements. Deriving a correctness rule from a performance target is guessing with a spreadsheet open.

**ELI5.** Some rules live in one person's head and never get said. So you ask four things: how fast, how much, where, and who. Asking is cheap. Learning late is not.

## A Residency Rule Removes Options and Never Weighs Against Them

Latency, scale, residency and identity decide most deployments. They do not all act alike.

A latency target is a bar. Test every design against it, then compare whichever clear it. A residency rule is more like a zoning law: it bans some plans before any comparison starts. What is left is compared as if the rule never existed.

Two settings are independent: where inference runs, and where data is stored. The first travels with the request. `inference_geo` takes `"us"` or `"global"`, set per call or as a workspace default. It works from Claude 4.6 onward, and earlier models return a `400`. US inference costs 1.1 times the standard rate. The second does not travel. Workspace geo is chosen when the workspace is created. After that it cannot be changed.<sup>[3]</sup>

Retention bites harder. Zero data retention is set per organization through an account team. Enabling it for one organization does not extend it to another on the same account. HIPAA readiness needs a signed agreement. Once on, it is permanent and no administrator can switch it off. A request using a feature outside the arrangement fails with a `400` and does not quietly degrade.<sup>[4]</sup> On Amazon Bedrock and Google Cloud, the cloud provider is the data processor, so their retention documentation governs.<sup>[4]</sup>

The standard wrong answer treats residency as one factor to balance. It comes dressed as judgement: a faster region, a cheaper platform, a simpler integration. None of these is an argument. Residency decides which options are admissible at all, and those three had stopped being options before anyone weighed them.

**ELI5.** A zoning law says "no tall buildings here." It does not compete with "tall is cheaper." It removes tall plans from the pile. Then you pick from what remains.

## The Record Exists Because the Reviewer Was Not in the Room

Why write requirements down? The person who reviews the deployment choice was not there when the constraints came out, and the review is where you defend it.

A short record does it. List the behaviours the system must show, the infrastructure constraints, and the regulation or owner behind each. Then your platform choice reads as a consequence. Without it, the choice reads as familiarity, which is what reviewers push on.

Keep the record current, because configuration does not update itself. Permission policies show it. Tighten a policy on an agent and it governs sessions created after the change. Sessions already running keep their old configuration.<sup>[5]</sup> Self-hosting has a similar gap. Once session content reaches your worker, your own policies decide whether it is retained, redacted or deleted. Anthropic cannot see what happens after delivery.<sup>[6]</sup>

Do not apply this to every ticket. Anthropic's rule: planning pays off when the approach is uncertain, when the change touches several files, or when the code is unfamiliar. If the diff fits in one sentence, skip it.<sup>[1]</sup> Our cache ticket has several tenants, an audit duty and uneven behaviour. It clears the bar three times.

**ELI5.** Write down why you built it this way and who said so. Someone who wasn't there can read it later. When the rules change, change the paper too.

## How Wrong Answers Are Built on This Material

Wrong answers here describe sound engineering. Prototypes, staged rollouts, monitoring and reuse are all normal good practice, so they pass a quick read. The flaw is in what each one assumes you already know.

- Unstated property assumed absent. The option treats the request as the whole truth about the system. Iterating, flags and a small first version suit a system whose invariants are known. Each is right once you can undo the change and any damage is loud and contained.
- Finding out after the build. Monitoring, incident review and canary releases do surface constraints, but only by tripping over one. That works when failure is cheap, quick and visible. It fails when failure is silent, rare and costly, the shape of every tenancy and audit scenario.
- Constraint inferred, not elicited. Someone reads correctness rules off a performance target, a neighbouring module, or the previous team's work. Copying an approach copies its assumptions with its structure. Authorization paths are where a borrowed assumption hurts most.
- A hard limit scored like a preference. A regulation, jurisdiction or retention duty is put on the scale against cost, latency or effort. Limits like these write the shortlist. They never compete on it.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Properties the request never mentioned: several tenants, an audit trail, behaviour that varies by path | Ask first: invariants, invalidation rules, audit duty, failure modes | Iterate, prototype or use a flag, which learns the same facts from an incident |
| Goal is "faster", "better", "accurate" or "seamless" | Rewrite as behaviours that can pass or fail | Accept the goal as the requirement, then pick tools |
| A regulation, jurisdiction or retention duty appears anywhere | Use it to filter the shortlist | Trade it against latency or cost as if they were equals |
| Behaviour is fully specified and a platform must be chosen | Get latency, volume, residency and identity first | Choose by habit, current tooling, or the last project |
| Someone wants to copy a neighbouring system's approach | Check which of its assumptions hold here | Defend reuse because it looks alike, not because the invariants match |
| Team can defend the design, outsiders cannot follow it | Write the record, with each constraint's source | Record the decision but not the constraints that forced it |

One habit outlasts the table. For each option, ask what it needs you to know already. Then check whether the scenario called that settled or said nobody had established it.

**ELI5.** A wrong answer can sound smart. Ask what it quietly assumes. If it assumes something nobody checked, like the hidden pipe, it is wrong.

## What to Remember

- A standing constraint is a fact about the environment that came before the request, shows up in no description of the work, and shapes the design anyway. Three recur: multiple tenants, an audit obligation, and inconsistent existing behaviour.
- Where a mistake would be silent, rare and expensive, ask before you build. Iteration runs on signals. A tenancy or authorization bug gives none until it gives a huge one.
- A functional requirement is a behaviour the system must show, worded for a pass or fail mark. To test one, ask what you could observe that proves it broken. Nothing? Then it is a preference, not a requirement.
- Infrastructure requirements fence the deployment and say nothing of behaviour. They define when producing the output is acceptable. Get them by asking, never reading, since the holder finds each obvious. The four are latency measured at the user, volume at peak, processing and storage location under a named regulation, and whose credentials act, with what audit record.
- Residency, retention and identity rules settle which options are even allowed. Speed, cost and familiarity rank the survivors. They never overturn the rule.
- Inference location and data storage are separate settings. `inference_geo` is per request or a workspace default. Workspace geo is fixed at creation and cannot change, so a late residency answer costs a rebuild, not a config edit.
- A performance target never implies a correctness rule. A latency budget is silent on which tenant sees which record. Deriving one from the other is guessing.
- Write requirements down because the reviewer missed the conversation where the constraints surfaced. The record holds the behaviours, the constraints, and the source of each constraint. That turns a platform choice into a consequence rather than a habit.

**ELI5.** Ask about the hidden pipes before you cut. Turn wishes into things you can check. Treat the law as a filter, not a vote. Write down why.

## Endnotes for this chapter

1. Letting Claude jump straight to coding can produce code that solves the wrong problem, so plan mode separates exploration from execution; planning is most useful when the approach is uncertain, when the change modifies multiple files, or when the code being modified is unfamiliar, and a change whose diff could be described in one sentence should skip the plan. Anthropic, *Best practices for Claude Code* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

2. Good success criteria are specific and measurable: "good performance" is replaced by "accurate sentiment classification", and "safe outputs" by less than 0.1% of outputs out of 10,000 trials flagged for toxicity by the content filter. Anthropic, *Define success criteria and build evaluations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/develop-tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

3. Two independent settings govern where data is processed and stored. The `inference_geo` parameter accepts `"us"` or `"global"`, can be sent on a request or set as a workspace default, is supported on Claude 4.6 and later models and returns a `400` error on earlier ones, and US inference is priced at 1.1 times the standard rate across all token pricing categories. Workspace geo is set when a workspace is created and cannot be changed afterwards. Anthropic, *Data residency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/data-residency](https://platform.claude.com/docs/en/manage-claude/data-residency)

4. Zero data retention is enabled per organization by an account team, and enablement does not automatically extend to other organizations under the same account. HIPAA readiness requires a signed business associate agreement, and once enabled the configuration is permanent and cannot be disabled by an administrator; a request that uses a feature outside the arrangement returns a `400` error. On Amazon Bedrock and Google Cloud's Agent Platform the cloud provider is the data processor, and those platforms' own retention and compliance documentation applies. Anthropic, *API and data retention* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/api-and-data-retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)

5. Permission policies are set in the agent's tools configuration and can be changed later by updating the agent; running sessions keep the toolset configuration they were created with, and updates apply to sessions created afterwards. Anthropic, *Permission policies* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/permission-policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)

6. Under the shared responsibility model for self-hosted sandboxes, conversation content and tool outputs pass through the operator's worker and stay in the operator's environment, which makes retaining, redacting or deleting that data in line with the operator's own policies their responsibility; Anthropic has no visibility into what a worker does with session content once it has been delivered. Anthropic, *Security model* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security)
