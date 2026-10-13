# Chapter 15: The Constraints Nobody States Decide the Design

**Summary**: *Every system you are asked to change already has properties nobody put in the request. Say you drop a cache into a multi-tenant authorization path. It can break one of those properties quietly, months later, once. This chapter covers the two sets of requirements that stand between a business direction and a design you can defend. The first set is the behaviours somebody can mark pass or fail. The second set is the deployment constraints that only show up because somebody went and asked. Get the second set late and the repair is a migration, not a setting.*

## The Request Describes the Change and the System Describes the Constraints

**First, the idea.** A request tells you what to change. The system you are changing already has rules of its own. Those rules decide the design, and nobody wrote them in the request. Think of renovating an old house. The **request** (the work order) says "add a door here". The **system** (the house) has pipes and wiring inside the walls. The work order never mentions them.

**The ticket.** A **ticket lands**. Put a **cache in front** of the **authorization module**, because the checks are slow and the page waits on them.

Read it twice and you still find **nothing missing**. There is a **component**, a **symptom**, a **mechanism** and an **owner**.

**The system.** Now read the system instead of the ticket. **Several customers share** that deployment. Every **access decision** the module makes is written to a **log somebody audits**. The invalidation already in place (the way old cached answers get thrown out) does not behave the same way on **every path**. The team knows this and has never written it down.

None of that was put there for the benefit of this change. It was true last quarter and it will be true after the cache ships. Call it a **standing constraint** (the hidden pipes in the wall): a **property of the environment** that **predates the request**, appears in **nobody's description** of the work, and **decides the design** anyway.

**Why this is dangerous.** A **functional gap announces itself** the first time somebody runs the feature. A standing constraint violated by a cache is different. It announces itself when **one tenant** (one customer sharing the system) is served **another tenant's decision**. That happens months later, once. **Silent, rare and expensive** is the exact profile of a defect that iteration never catches. Iteration (try, look, fix, repeat) **needs a signal**, and this defect gives none until it gives a very large one.

**What to do.** Your first move on a change of that shape is **neither code nor a design**. It is a **set of targeted questions** (the walk through the house before you cut the wall):
- what has to **stay true**
- what **invalidates an entry**
- what the **audit trail** must record
- how the module behaves when the **cache is wrong**

Anthropic makes the general form of the point about Claude itself, which needs the same thing for the same reason. Going straight to code produces code that **solves the wrong problem**, so exploration and planning are **separated from execution**.<sup>[1]</sup>

**ELI5.** Someone asks you to put a new door in a wall. They do not tell you there is a water pipe inside it. If you cut first, the pipe bursts and nobody notices for months. So you look inside the wall and ask questions before you cut.

## A Goal You Cannot Fail Is Not Yet a Requirement

**First, the idea.** A goal is a direction. A requirement is something you can check. In the house, "make the kitchen nicer" is a goal. "The sink drains in under a minute" is something an **inspector** (the reviewer) can mark pass or fail.

**Goals are not requirements.** A **business problem** is a direction. Get invoices approved sooner. Stop the compliance team reading every document. **Both sentences** are **worth having**, and you can **neither build nor check** a system against either one.

**What a functional requirement is.** A **functional requirement** says what the system must do, in enough detail that somebody can **mark it pass or fail**. **Deriving them turns** one direction into **several checkable behaviours**:
- flag each document as needing review or not
- quote the clause that triggered a flag
- leave a flagged document unapproved until a named reviewer clears it

Each of those can be **run and scored**. The **direction cannot**.

**The test.** The **test is mechanical**, and it is the only one you need. Read the statement, then ask yourself what **observation would show it had been broken**. If nothing would, the statement is a **preference**.

**Anthropic's examples.** Anthropic sets the same discipline for **success criteria**, and the worked pairs are the fastest way to learn it. "Good performance" becomes "**accurate sentiment classification**". "Safe outputs" becomes fewer than **0.1% of outputs across 10,000 trials** flagged by the **content filter**.<sup>[2]</sup> The second version of each is **longer**, but length is not what you are buying. It **bought a line** the system can be held to at review.

**The anti-pattern: the requirement nobody can fail.** It is **seductive** because it is **agreeable**. Everybody signs off on fast, accurate and secure. **Nothing has been agreed**. Two people read one sentence and **build different pictures** from it. They find the difference at the review, when one of them says this is not what was asked for.

**ELI5.** "Make it nice" cannot be wrong, so it cannot be checked. "The sink drains in one minute" can be checked. Turn every wish into something a person could say "yes" or "no" to.

## The Second Set of Requirements Sits on Other People's Desks

**First, the idea.** Behaviour requirements come to you. **Infrastructure requirements** (the rules about where and how the system runs) do not. In the house, these are the rules held by other people: the city office, the power company, the neighbours. You have to go and ask each one.

**Behaviour comes by itself.** **Functional requirements arrive** on their own, near enough. Whoever wants the feature knows what it should do and will **tell you unprompted**.

**Infrastructure is different.** **Infrastructure requirements bound the deployment** rather than the behaviour. They say nothing about what the system produces. They say everything about the **conditions** under which producing it is **acceptable**. Hardly any of them are anywhere in the business problem. They come out by **interrogation rather than by reading**, because each one is **obvious** to the human holding it and therefore **never said out loud**. **Four questions** cover most of the ground.

| The question | Who actually holds the answer | What a late answer costs |
|---|---|---|
| How fast, measured where the user is | Whoever owns the experience, and whoever runs the region | A model, a platform or a topology chosen against the wrong number |
| What volume, and what the peak looks like | Operations, plus whoever keeps the historical figures | Capacity and rate limits sized for the average |
| Processed where, stored where, under which regulation | Legal, compliance, the data protection function | A rebuild, because some of these settings are fixed at creation |
| Acting under whose credentials, auditable how | Security, and the owner of the system being acted upon | An audit trail that cannot answer the question it exists for |

**Why this belongs at the start.** The third column is the reason. Four questions **cost you a conversation**. Their answers, **arriving late**, **cost you a migration**. What gets traded against a latency figure once you hold one is chapter 4's material. Getting the figure at all is this chapter's.

**A trap that looks like diligence.** A **latency budget** (how fast it must be) tells you nothing whatsoever about which **tenant** may see which **record**. Performance targets and correctness rules are different kinds of statement. **Correctness inferred from a performance target** is **guessing** with a spreadsheet open.

**ELI5.** Some rules are held by other people and nobody tells you them. You have to go and ask four questions: how fast, how many, where, and who is allowed. Asking costs a chat. Finding out late costs rebuilding.

## A Residency Rule Removes Options and Never Weighs Against Them

**First, the idea.** Some constraints are just one factor among many. A **residency rule** (a rule about which country the data may be processed or stored in) is not. Think of **zoning law** on the house plot. It does not make a design a bit worse. It makes some designs illegal before you start.

**Different kinds of constraint.** **Latency, scale, residency and identity** decide a deployment more often than anything else does. They do not all behave the same way once **design starts**.

A **latency target** is a **threshold**. Candidate designs get measured against it. Some clear it, and the ones that clear it are then compared on other grounds. A **residency rule** is **not a threshold** at all. It **strikes candidates off the list** before any comparison begins. Whatever survives is compared as though the rule had **never come up**.

**Two separate settings.** Where **inference runs** and where **data is stored** are two **independent settings**.
- The first travels on the request. `inference_geo` takes `"us"` or `"global"`. It can be set **per call** or as a **workspace default**. It is supported from **Claude 4.6 onward** and returns a `400` on earlier models. US inference is priced at 1.1 times the standard rate.
- The second does not travel at all. **Workspace geo is fixed at creation** and cannot be changed afterwards.<sup>[3]</sup>

**Retention bites harder.** Retention (how long data is kept) has the same shape. **Zero data retention** is arranged **per organization** through an account team. Enabling it for one organization does **not extend** it to another under the same account. **HIPAA readiness** needs a **signed agreement**. Once enabled, the **configuration is permanent** and **no administrator** can switch it off. A request carrying a feature the arrangement does not cover **fails** with a `400` rather than **degrading quietly**.<sup>[4]</sup> Partner platforms move the ground as well. On Amazon Bedrock and Google Cloud the **cloud provider** is the **data processor**, so their **retention documentation** is the one that governs.<sup>[4]</sup>

**The standard wrong answer.** **Residency treated as one factor to balance** is the **standard wrong answer** on this material. It always arrives dressed as engineering judgement: a faster region, a cheaper platform, a simpler integration. None of the three is an argument. A constraint of that kind decides which **options are admissible** at all. The three being weighed had **stopped being options** before anybody weighed them.

**ELI5.** Some rules are like a "no building here" sign. You do not weigh the sign against a nicer view. You cross those plots off the map first. Then you choose among the plots that are left.

## The Record Exists Because the Reviewer Was Not in the Room

**First, the idea.** You write the requirements down because the person who checks your work was not there when you gathered them. In the house, this is the **permit file** (the written record). The inspector reads the file, not your memory.

**Why write it down.** **Requirements get written down** for one reason that survives contact with a busy team. Whoever **reviews a deployment choice** was not in the conversation where its **constraints came out**. The review is where the choice has to be defended.

**What goes in the record.** A short record does the job:
- the **behaviours the system must exhibit**
- the **infrastructure constraints**
- which **regulation** or which **owner** each constraint came from

With it, your **platform choice** reads as a **consequence** of the requirements. Without it, it reads as **familiarity**, and familiarity is what a reviewer **pushes** on.

**Keep it current.** That record has to **stay current**, because **configuration does not retro-fit** itself (it does not change what already exists). **Permission policies** show this cleanly. Tightening a policy on an agent governs **sessions created after the change**. Sessions already running **keep the configuration** they started with.<sup>[5]</sup> Running your own infrastructure has the same gap. Once session content reaches a **self-hosted worker** it is retained, redacted or deleted under the **operator's own policies**. Anthropic has no visibility into what happens to it after delivery.<sup>[6]</sup>

**Do not do this for every ticket.** None of this scales down to every ticket. Pretending it does is how the discipline gets abandoned wholesale. Anthropic's calibration is a good one to borrow. **Planning earns its overhead** when the approach is **uncertain**, when the change touches **several files**, or when the code is **unfamiliar**. A change whose **diff fits in one sentence** should skip it.<sup>[1]</sup> **Multiple tenants**, an **audit obligation** and **behaviour nobody describes** the same way twice clear that bar three times over.

**ELI5.** The person who checks your work was not in the room. So you keep a file that says what the house must do, what the rules are, and who gave each rule. When the rules change, you update the file. Small jobs do not need a big file.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here **describe good engineering**. Prototyping, staged rollout, monitoring and reuse are all things **competent teams** do, which is why they survive a first read. What makes one wrong is what it **assumes has already been established**.

**The four wrong assumptions:**
- The **unstated property assumed absent**. The option **treats the system** as though the only **things true** of it are the ones the **request mentioned**. Iterating toward a fix, shipping behind a flag and building a small version first all **belong to a system whose invariants are known** (the rules that always hold). **Each becomes correct** once the **change is reversible** and the **damage is loud and contained**.
- **Discovery relocated to after the build**. Monitoring, incident review and a canary release (a rollout to a small group first) do **find constraints**. They find them by **violating one**. It is a **fair trade** when a failure is **cheap, quick and visible**. It is a **bad trade** when it is **silent, rare and consequential**. That is the profile every **tenancy and audit scenario** is built on.
- A **constraint inferred instead of elicited** (guessed instead of asked for). This means **reading correctness rules** off a performance target, off a neighbouring module's implementation, or off what the previous team wrote. **Copying an approach imports its assumptions** along with its **structure**. An **authorization path** is where an **imported assumption does the most damage**.
- A **hard constraint weighed as a preference**. This is a **regulation**, a **jurisdiction** or a **retention obligation** offered as **one input to a tradeoff** against cost, latency or effort. Constraints of that kind **produce the candidate list**. They **never compete** inside it.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Properties the request never mentioned: several tenants, an audit trail, behaviour that varies by path | Elicit the invariants, the invalidation rules, the audit obligation and the failure modes first | Iterating, prototyping or shipping behind a flag, all of which learn the same facts from an incident |
| A goal stated as faster, better, accurate or seamless | Convert it into behaviours somebody can mark pass or fail | Accepting the goal as the requirement and moving on to mechanism |
| A regulation, a jurisdiction or a retention obligation anywhere in the setup | Treat it as the filter that produces the candidate list | Balancing it against latency or cost as though every input were commensurate |
| Functional behaviour fully specified and a platform decision due | Obtain latency, volume, residency and identity, then decide | Choosing on familiarity, existing tooling, or what shipped last time |
| Somebody proposes copying an approach from a neighbouring system | Check which of that system's assumptions actually hold here | Reuse justified by similarity of shape rather than shared invariants |
| A design is defensible inside the team and opaque outside it | Write the record, naming the source of every constraint | Documenting the decision without the constraints that forced it |

**A habit that works past the table.** For each option, ask what it **needs you to know already**. Then check whether the scenario said that thing was **settled** or said that **nobody had established** it.

**ELI5.** Wrong answers sound like good building habits: try it and see, fix it later, copy the house next door. They fail because they pretend you already know what is inside the walls. If nobody checked, you do not know.

## What to Remember

- A **standing constraint** is a **property of the environment** that **predates the request**, appears in **no description** of the work, and **decides the design** regardless. **Multiple tenants**, an **audit obligation** and **inconsistent existing behaviour** are the three that recur.
- **Elicit before implementing** wherever a mistake would be **silent, rare and expensive**. Iteration **needs a signal**. A **tenancy or authorization defect emits none** until it emits a large one.
- A **functional requirement** names the **behaviour the system must exhibit**, written so somebody can **mark it pass or fail**. Test it by asking what **observation would prove it broken**. If none exists, it is a **preference, not a requirement**.
- **Infrastructure requirements bound the deployment**, not the behaviour. They fix the **conditions** under which producing the output is **acceptable**. They are **obtained by asking**, never by reading, because **each is obvious** to whoever **holds** it. The four: **latency measured at the user**, **volume at peak**, **processing and storage location** under a **named regulation**, and whose **credentials act**, with what **audit record**.
- A **residency, retention or identity rule** decides which options are **admissible**. **Speed, cost and familiarity** order what survives the rule and **never overturn** it.
- Where **inference runs** and where **data is stored** are **separate settings**. `inference_geo` is **per request** or **per workspace default**. **Workspace geo is fixed at creation** and cannot be changed, so a residency answer **arriving late costs a rebuild** rather than a config change.
- A **performance target** implies **no correctness rule**. A **latency budget** says nothing about which **tenant** may see which **record**, and **inferring one from the other** is guessing.
- **Requirements are recorded** because whoever **reviews the decision** was **absent** when the **constraints were gathered**. The record holds the **behaviours**, the **constraints**, and the **source of each constraint**. That is what turns a **platform choice into a consequence** rather than a **habit**.

**ELI5.** Before you change a house, look inside the walls and ask the people who know the rules. Turn wishes into things you can check. Cross off the plots the law forbids. Write it all in a file for the inspector.

## Endnotes for this chapter

1. Letting Claude jump straight to coding can produce code that solves the wrong problem, so plan mode separates exploration from execution; planning is most useful when the approach is uncertain, when the change modifies multiple files, or when the code being modified is unfamiliar, and a change whose diff could be described in one sentence should skip the plan. Anthropic, *Best practices for Claude Code* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

2. Good success criteria are specific and measurable: "good performance" is replaced by "accurate sentiment classification", and "safe outputs" by less than 0.1% of outputs out of 10,000 trials flagged for toxicity by the content filter. Anthropic, *Define success criteria and build evaluations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/develop-tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

3. Two independent settings govern where data is processed and stored. The `inference_geo` parameter accepts `"us"` or `"global"`, can be sent on a request or set as a workspace default, is supported on Claude 4.6 and later models and returns a `400` error on earlier ones, and US inference is priced at 1.1 times the standard rate across all token pricing categories. Workspace geo is set when a workspace is created and cannot be changed afterwards. Anthropic, *Data residency* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/data-residency](https://platform.claude.com/docs/en/manage-claude/data-residency)

4. Zero data retention is enabled per organization by an account team, and enablement does not automatically extend to other organizations under the same account. HIPAA readiness requires a signed business associate agreement, and once enabled the configuration is permanent and cannot be disabled by an administrator; a request that uses a feature outside the arrangement returns a `400` error. On Amazon Bedrock and Google Cloud's Agent Platform the cloud provider is the data processor, and those platforms' own retention and compliance documentation applies. Anthropic, *API and data retention* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/manage-claude/api-and-data-retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)

5. Permission policies are set in the agent's tools configuration and can be changed later by updating the agent; running sessions keep the toolset configuration they were created with, and updates apply to sessions created afterwards. Anthropic, *Permission policies* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/permission-policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)

6. Under the shared responsibility model for self-hosted sandboxes, conversation content and tool outputs pass through the operator's worker and stay in the operator's environment, which makes retaining, redacting or deleting that data in line with the operator's own policies their responsibility; Anthropic has no visibility into what a worker does with session content once it has been delivered. Anthropic, *Security model* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security)
