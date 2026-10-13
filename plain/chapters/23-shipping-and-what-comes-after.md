# Chapter 23: Deploy Is a Phase Boundary, Not the End

**Summary**: *A release date is a completion criterion for the development work and for nothing else. What opens at go-live runs until the system is switched off (the restaurant stays open every night). It holds three jobs the build phase never had. The first is watching the numbers. The second is answering when they move. The third is planning around a dependency that retires on a schedule nobody on the team sets. This chapter covers the arc a Claude application moves through and the gates between its phases (the inspections before each step). A gate is where a decision to proceed gets made and, occasionally, refused.*

## Go-Live Closes One Calendar and Opens One With No End Date

**First, the idea.** Launching a system ends the building work. It does not end the work. Think of opening a restaurant. The **release** is opening night (**go-live**). The fitting-out of the building is done. Running the restaurant has just started, and it never has a finish date.

**What happens at launch.** The **release goes out**. Internal teams pick it up the same week. The **board empties**, the build channel goes quiet, and the humans who wrote the thing get **assigned somewhere else**. The builders pack up and leave.

**What ended.** Something genuinely ended there. Development had a **scope, a definition of done and a date**, and all three were satisfied. What started in the same hour has **none of the three**. It runs for as long as the system is in use.

**What the new thing is called.** Call it the **standing phase** (the restaurant being open for business). It is the stretch that **opens at go-live**, **covers operation and maintenance**, and carries **no completion criterion**. It has no finish line because a system humans depend on never stops needing to be watched, answered for and moved forward.

**How the exam asks about it.** A scenario will put you at exactly that hour and ask what your **next stretch of work** is. Every option will describe something real:
- One names a **single activity** that genuinely happens after a launch.
- One describes who **holds the system** rather than what happens to it.
- One skips to the end of its life.
- Only one of the four **runs on the system's clock**.

**ELI5.** Opening night is not the end of a restaurant. It is the start of the part that never stops. Cooking, cleaning and serving go on every day. The people who built the room have gone home, but the restaurant is still open.

## A Gate That Cannot Refuse Anything Is Not a Gate

**First, the idea.** Between any two phases sits a **decision to move forward**. Call it a **gate** (the inspection before the restaurant can open or change its menu). It is worth having only when you are allowed to answer no. No is available only where **something concrete is being checked**.

**Why gates get skipped.** A **checkpoint costs** you a day the schedule did not carry. The **day is visible**. What the checkpoint would have caught is not. So the day loses the argument.

| What the gate looks at | What it refuses to let through | What ships when nobody looks |
|---|---|---|
| A constraint with no named source behind it | A platform chosen on familiarity | A deployment nobody can defend at review |
| A build the current eval has never scored | Promotion to production traffic | A regression nobody can attribute to anything |
| A model reference that moves without a change record | An unrecorded pin | An upstream release nobody logged |
| Metrics not emitting, with no name attached to the alert | Go-live itself | A failure whose first reporter is a user |
| A production finding with no requirement it contradicts | Closing the ticket | Folklore held by whoever was on shift |

**The right-hand column is the real subject.** A **skipped gate ships a system** that works on the day. Months later it **cannot be reasoned about**, by humans who were never in the room.

**The anti-pattern.** **Deployment treated as a completion milestone** is the mistake this chapter sits against. It is not laziness. It is a calendar built by people whose **work genuinely does finish**, handed to people whose work does not. In restaurant terms, it is a plan that stops at the ribbon cutting.

**ELI5.** A gate is like a health inspector. The inspector is only useful if they can say "not yet". People skip the inspection because it costs a day today. Nobody sees the food poisoning it would have stopped.

## The Standing Phase Holds Three Jobs, and Only One of Them Is Debugging

**First, the idea.** Once the restaurant is open, three jobs start. The first is keeping the books (**instrumentation**, which means measuring what the system does). The second is having a named person who answers when the numbers move. The third is changing the menu as the world changes (**planned evolution**).

**Job 1: instrumentation comes first.** Nothing else in the phase is possible without it. From your first day of production traffic, **emit three quantities** (record them on every call):
- what **each call costs**
- how long it takes
- how often it fails

**Cost telemetry is an estimate.** Claude Code's exported cost metric is documented as an approximation. **Official billing data** comes from the API provider, not from the exporter.<sup>[1]</sup> So trend it and alert on it. Do not **settle a finance question** against it. Think of it as the till's running tally, not the bank statement.

**The failure count is worse.** It under-reports in the direction that looks like health. A **refusal arrives on a successful response stream** instead of as an HTTP error (a failure code from the server). So the **API error event does not fire** for one. A **separate refusal event** exists so refusal frequency can be tracked at all.<sup>[2]</sup> An error rate built from **transport failures stays flat** while a growing share of responses return nothing the caller can use. It is like counting only the plates that smash, while more and more dishes go back to the kitchen untouched.

**Job 2: somebody answers.** The second job is that somebody **answers when a number moves**. Instrumentation with **no name attached** is a dashboard. A dashboard only records what went wrong.

**Job 3: planned evolution.** The third job is **planned evolution**. It is **under-planned** because nothing in a **deployed configuration** looks like it is moving.

**ELI5.** After opening, you need to write down what each meal costs, how long it takes and how often it goes wrong. Someone must be named to act when the numbers change. And you must plan menu changes ahead, even when everything looks still.

## Your Dependency Retires on Somebody Else's Calendar

**First, the idea.** Most **dependencies sit still** until you move them. A model does not. Think of a supplier who one day stops making your main ingredient. You did not choose the date.

**What the pin gives you.** The pin is real, and it is worth knowing exactly what you get. A **model ID identifies a pinned version**. The underlying model stays constant for the **lifetime of that ID**. The guarantee attaches to the ID, not to the **convenience aliases** the API accepts for some earlier models.<sup>[3]</sup> That **holds the behaviour steady**. It does not hold the model available.

**What the supplier does.** Anthropic **retires older models** as newer ones launch. It notifies customers with active deployments at least **60 days before retirement** for publicly released models. It **fails requests sent after the retirement date**.<sup>[4]</sup>

**Two calendars.** **Partner-operated platforms** set their own retirement schedules. So a model's status and dates on **Amazon Bedrock or Google Cloud** can differ from the ones governing Anthropic-operated platforms.<sup>[4]</sup> Read one calendar while deployed against the other and you hold an expiry date nobody on the team has seen.

**The failure to avoid.** The **dependency assumed frozen** produces a specific failure. It is a migration **run as an incident**, on a deadline set elsewhere, in the week it turns urgent. The alternative is a planned backlog item with an **owner and a date** inside the notice window.

**What to check when you migrate.** Migration between current models is **mostly drop-in**. What you check is narrow:
- **features no longer available**
- **changed thinking behaviour**
- **refusal behaviour** that differs between targets<sup>[5]</sup>

**How you know the replacement holds.** An **evaluation suite scored against the baseline** (the scores) set by the **outgoing version** answers that. Building it is chapter 19's material. Pinning is chapter 18's. A team that built neither cannot say what a **forced upgrade** cost it.

**ELI5.** Your supplier will stop selling your main ingredient one day, and they pick the date. A pin keeps the ingredient the same while it lasts. It does not keep it on the shelf. So put the switch-over in your plan with a name and a date, before the supplier forces it.

## A Finding That Never Reaches the Requirements Is Folklore

**First, the idea.** Once the restaurant has real customers, you learn things the test kitchen could not tell you. Those lessons have to go back into the recipe book. If they only live in someone's head, they are folklore.

**What production tells you.** Production tells you things the test set could not:
- Which **inputs actually arrive**.
- Which instruction **humans read differently** from how it was written.
- Where the **cost concentrates**.

**Where findings should go.** Those findings have one useful destination, and an **incident channel** is not it. **Iteration** means a production observation **travels back to the requirement it contradicts**. It then re-enters the arc as a change with a gate in front of it. Left where it landed, it becomes knowledge held by **whoever was on shift**. It survives until that person changes team.

**Retention outlives the switch-off.** The end of the arc carries an obligation that outlives the switch-off. Retention clocks run on their own terms:
- **Local session transcripts** are stored for **six years by default**, or for an **organization's custom conversation retention period** where a finite one is set.
- **Activity Feed data** is retained for six years.<sup>[6]</sup>

Decommissioning stops the traffic and **settles nothing already stored**. Closing the restaurant does not empty the filing cabinet.

**ELI5.** When a customer shows you a problem, write it in the recipe book, so the fix is checked before it goes live. If you only tell the person on shift, it is gone when they leave. Even after the restaurant closes, the old paperwork is still in the cabinet.

## How Wrong Answers Are Built on This Material

**First, the idea.** Lifecycle distractors (the wrong options) are **unusually reasonable**. Almost every one names something a **competent team** really does, often in the same week the scenario is set. What makes one wrong is a **category error** about what **kind of object** it is.

**The four wrong patterns:**
- **A single activity promoted to a phase.** A **launch review, a retrospective**, a **load test, a handover document**: **all real, all finite**. A phase (the restaurant being open) is a **container holding many activities** across an **open-ended stretch**. The tell is a **completion date offered** as the answer to a question about where the system now lives. It becomes correct where the scenario **asks what to schedule next week**.
- **Ownership offered as lifecycle progress.** **Transferring the system to a platform team**, **splitting it across two groups**, hiring for it. All three answer who does the work, and the **work is unchanged** by every one of them. It becomes correct where the question is about **responsibility, escalation or staffing**.
- **The dependency assumed frozen.** This is any option treating the **deployed configuration as stable ground**, with **change arriving only when the team chooses** it. **Retirement dates and provider schedules** move underneath a **system nobody touched**. It becomes correct only where the version in use is under the **team's sole control**.
- **A phase skipped because its evidence is not yet uncomfortable.** Examples are **shipping before an eval scores the build**, **going live before metrics emit**, and **closing a finding** without routing it. Each is defensible in the moment. Each removes an answer somebody needs later.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| A system has just entered production use and the next stage of work is in question | The ongoing stretch that opens at go-live: watch it, answer for it, plan its evolution | A finite activity, a staffing arrangement, or the end of its life |
| A new version is ready and production traffic is the next step | Score it against the baseline before promoting it | Promoting first and watching production for the difference |
| Nobody can say what a live system costs or how often it fails usefully | Emit cost, latency and failure, and check what the failure count counts | Reasoning from the last load test, or from a count that omits refusals |
| A notice, a retirement date or a provider schedule appears anywhere | Planned work with an owner and a date inside the notice window | Deferring until the date forces an unplanned migration |
| Something learned in production needs to go somewhere | Back into the requirement it contradicts, as a change that faces a gate | Logging it in an incident record and considering it handled |
| A checkpoint is being skipped to hold a date | Name what it would have refused | Accepting the schedule argument, which always sounds stronger |

**A habit that works past the table.** Ask of each option **whether it terminates**. An **activity finishes**. An **ownership arrangement holds steady**. A retirement closes the file. Exactly one thing on a lifecycle list **runs as long as the system** does. Whenever a scenario has just described a launch, that is what it points at.

**ELI5.** Wrong answers describe real jobs that end, like a launch party or a staff handover. The right answer is the one that keeps going while the restaurant is open. When you read an option, ask "does this ever finish?".

## What to Remember

- The **standing phase opens at go-live**, covers **operation and maintenance**, and has **no completion criterion**. A system in use needs **watching, answering for and evolving** until it is **switched off**. Development finishes; this does not.
- A **gate is a decision** to proceed that is only real if it can **refuse**. It refuses against a **named artifact**: the **constraint with a source**, the **eval score against a baseline**, the **recorded pin**, the **live metric**, the **routed finding**.
- **Skipping a gate raises no error**. It ships a system that **works on the day** and **cannot be reasoned about later**. That is why **schedule pressure wins** wherever it is allowed to be an argument.
- **Instrument three quantities** from **day one** of production: **cost per call**, **latency**, **failures**. Cost telemetry is an **approximation** and official **billing comes from the provider**. So trend it, and **never reconcile** against it.
- A **refusal never surfaces** as an **HTTP error**. It arrives on a **successful response stream**. So a failure count built on **transport errors reads flat** while **usable responses fall**. Track **refusals separately**.
- A **model ID pins the model** for the **lifetime of that ID**. The guarantee covers IDs rather than the **convenience aliases** accepted for **some earlier models**. Pinning holds **behaviour steady**, not **availability**.
- **Models retire on Anthropic's schedule**, with at least **60 days' notice** for publicly released models and requests **failing after the retirement date**. **Partner platforms** publish their own dates, so a deployment on **Bedrock or Google Cloud** reads a **different calendar**.
- Migration between **current models is mostly drop-in**. Check **removed features**, **changed thinking behaviour**, **refusal behaviour**. An eval scored against the **outgoing baseline** tells you whether the swap **cost anything**.
- **Iteration** means a production finding **reaches the requirement it contradicts** and re-enters the arc as a **gated change**. A finding **left in an incident record** is knowledge held by **one person on one shift**.
- **Retention outlives the application**. Local session **transcripts keep for six years** by default, or for an organization's **configured retention period**, and **Activity Feed data** for six years. Switching a system off **stops traffic** and **settles nothing already stored**.

**ELI5.** Opening night starts the real work. Keep the books, name someone to act on them, and plan for your supplier to change. Never skip an inspection just to hit a date. Write every lesson back into the recipe book. Even after you close, the old paperwork is still there.

## Endnotes for this chapter

1. The exported cost metric supports usage-trend tracking, identification of high-usage sessions and attribution of spend, but cost metrics are approximations and official billing data comes from the API provider (Claude Console, Amazon Bedrock, or Google Cloud's Agent Platform). Anthropic, *Monitoring* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)

2. The API error event is logged when an API request to Claude fails and carries an HTTP status code, which is absent for non-HTTP failures such as connection errors. A refusal returns `stop_reason: "refusal"` and arrives on a successful response stream rather than as an HTTP error, so the API error event does not fire for it; a separate refusal event exists to let refusal frequency be tracked and grouped. Anthropic, *Monitoring* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)

3. Each Claude model ID identifies a pinned version of the model, and the underlying model remains constant for the lifetime of that ID; the guarantee covers model IDs and not the convenience aliases that the Claude API accepts for some earlier models. Anthropic, *Model IDs and versioning* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)

4. Anthropic regularly retires older models as newer ones launch, notifies customers with active deployments and provides at least 60 days' notice before retirement for publicly released models, and requests to models past the retirement date will fail. The dates published apply to Anthropic-operated platforms; partner-operated platforms (Amazon Bedrock and Google Cloud) set their own retirement schedules, so a model's lifecycle status and dates can differ. Anthropic, *Model deprecations* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/about-claude/model-deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)

5. Migration to the current models is mostly drop-in, using the same Messages API and tool use patterns, and the key changes to check are the features that are no longer available and thinking output, plus safety classifier refusals where the migration target has them and the previous model did not. Anthropic, *Migration guide* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/about-claude/models/migration-guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)

6. Local session transcripts from Cowork and Claude Code on users' machines are stored for six years by default, or for the organization's custom conversation retention period where a finite one is set, and Activity Feed data is retained for six years. Anthropic, *API and data retention* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/manage-claude/api-and-data-retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)
