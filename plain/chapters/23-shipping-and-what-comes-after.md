# Chapter 23: Deploy Is a Phase Boundary, Not the End

**Summary**: *A release date ends the development work and nothing else. After go-live the system runs until someone switches it off. That brings three jobs the build never had: watching the numbers, answering when they move, and planning for a dependency that retires on a schedule your team does not set. This chapter covers the path a Claude application takes and the gates between its phases, where someone decides to move on or refuses.*

The analogy for this chapter: a restaurant. Building it ends. Running it does not. The health inspector who signs off before opening is a gate. A supplier who drops your key ingredient is a retiring model.

## Go-Live Closes One Calendar and Opens One With No End Date

The restaurant opens on Friday. The builders leave for the next site. Their job had a scope, a goal for "finished" and a deadline, and they hit all three. But the kitchen must run tomorrow and the day after, with none of those.

That open-ended stretch is the **standing phase** (the restaurant being open). It starts at go-live and covers operation and maintenance. It has no completion criterion, because a system people rely on always needs watching and moving forward.

On the exam you are placed at that hour and asked what comes next. Every option sounds true. One is a single task that happens after launch. One names who holds the system. One jumps to end of life. Only one follows the system's own clock.

**ELI5.** Building a toy box ends at the last nail. Playing with it never ends.

## A Gate That Cannot Refuse Anything Is Not a Gate

Between two phases, someone decides to go forward. That decision counts only if the answer can be no. The inspector can refuse because there is a real kitchen to look at.

Gates get skipped because a check costs a day the schedule lacked. That day is visible. The problem it would have caught is not.

| The gate checks | It blocks | Without the check, you ship |
|---|---|---|
| A constraint that has no named source | A platform picked out of habit | A deployment no one can defend in review |
| A build the current eval never scored | Promotion to production traffic | A regression with no traceable cause |
| A model reference that shifts with no change record | An unrecorded pin | An upstream release no one logged |
| Metrics not emitting, or an alert with no name on it | Go-live itself | A failure that a user reports first |
| A production finding tied to no requirement | Closing the ticket | Folklore in one person's head |

A skipped gate ships a system that works on launch day. Months later, people who were never in the room cannot reason about it.

The anti-pattern is treating deployment as a completion milestone. It is not laziness. People whose work finishes built the calendar, then handed it to people whose work does not.

**ELI5.** A bouncer who lets everyone in is just a doorway. A gate must be able to say no.

## The Standing Phase Holds Three Jobs, and Only One of Them Is Debugging

First comes instrumentation (the till and the kitchen thermometer). Nothing else works without it. On day one of production traffic, start emitting three numbers: cost of each call, time it takes, and how often it fails.

Cost telemetry is an estimate. The docs call Claude Code's exported cost metric an approximation. Official billing data comes from the API provider.<sup>[1]</sup> Watch its trend and set alerts. Do not use it for finance questions.

The failure count is worse, because it errs toward looking healthy. Picture a waiter saying "sorry, we can't make that" while the till logs a normal sale. A refusal is like that. It arrives on a successful response stream, not as an HTTP error, so the API error event does not fire. A separate refusal event exists so you can track refusal frequency at all.<sup>[2]</sup> Count only transport failures and your error rate stays flat while more responses give the caller nothing usable.

The second job is a named person who reacts when a number moves. An alert with no name is just a dashboard.

The third job is planned evolution (changing the menu). Teams under-plan it because a deployed setup looks still.

**ELI5.** A lemonade stand counts cups and spills. Someone must care when the numbers change. And the lemons may stop coming.

## Your Dependency Retires on Somebody Else's Calendar

Most dependencies stay put until you move them. A model does not.

A model ID names one pinned version, and the model behind it stays constant for the lifetime of that ID. The promise covers the ID, not the convenience aliases the API accepts for some earlier models.<sup>[3]</sup> So behaviour holds steady. Availability does not.

Like a supplier dropping your flour, Anthropic retires older models as newer ones launch. Customers with active deployments get at least 60 days' notice before retirement for publicly released models. Requests sent after the retirement date fail.<sup>[4]</sup> Partner-operated platforms set their own retirement schedules. So a model's status and dates on Amazon Bedrock or Google Cloud can differ from those on Anthropic-operated platforms.<sup>[4]</sup> Read the wrong calendar and you hold an expiry date nobody on the team has seen.

Assume it is frozen and the migration becomes an emergency, due on someone else's date. Instead, put it on the backlog with an owner and a date inside the notice window. Moving between current models is mostly drop-in. You check only a few things: features that are no longer available, changed thinking behaviour, and refusal behaviour that differs between targets.<sup>[5]</sup>

To know the replacement holds up, score an evaluation suite against the outgoing version's baseline. Chapter 19 covers building it. Chapter 18 covers pinning. Without both, you cannot say what a forced upgrade cost.

**ELI5.** Your favourite crayon will stop being made on a day someone else picked. They warn you early, so stock up calmly.

## A Finding That Never Reaches the Requirements Is Folklore

An open restaurant teaches what the test kitchen could not: which orders really come in, which menu line diners misread, where the money goes.

A finding has one good home, and the incident channel is not it. **Iteration** means the observation goes back to the requirement it contradicts. It then re-enters the arc as a change with a gate in front. Left in the channel, it lives in the head of whoever was on shift, until they move teams.

Retention clocks keep running after switch-off. Local session transcripts are stored for six years by default, or for an organization's custom conversation retention period where a finite one is set. Activity Feed data is retained for six years.<sup>[6]</sup> Decommissioning stops the traffic. It settles nothing already stored.

**ELI5.** Tell one cook the soup is too salty and it is lost when she leaves. Write it on the recipe.

## How Wrong Answers Are Built on This Material

Lifecycle distractors look reasonable. Each is something a good team really does, but it is the wrong kind of thing.

- **A single activity promoted to a phase.** Launch review, retrospective, load test, handover document. Each is real and each ends. A phase holds many activities over an open stretch. A completion date offered as the answer to "where does the system live now?" is the tell. It turns correct if the scenario asks what to schedule next week.
- **Ownership offered as lifecycle progress.** Handing it to a platform team, sharing it between two groups, hiring for it. These say who does the work, which stays the same. They fit only a question about responsibility, escalation or staffing.
- **The dependency assumed frozen.** The option treats the deployed setup as solid ground that changes only when the team chooses. Retirement dates and provider schedules move even if nobody touched the system. It turns correct only when the team alone controls the version in use.
- **A phase skipped because its evidence is not yet uncomfortable.** Shipping before an eval scores the build, going live before metrics emit, closing a finding unrouted. Each removes an answer someone needs later.

| Scenario | Usual answer | Usual trap |
|---|---|---|
| A system just went live and the question is what work comes next | The ongoing stretch from go-live: watch it, answer for it, plan its evolution | A finite task, a staffing arrangement, or end of life |
| A new version is ready and production is next | Score it against the baseline before promoting | Promote, then watch production for differences |
| Nobody knows what a live system costs or how often it fails usefully | Emit cost, latency and failure, and check what the failure count counts | The last load test, or a count missing refusals |
| A notice, retirement date or provider schedule shows up | Planned work with an owner and a date inside the notice window | Waiting until the date forces a rush |
| Production taught the team something | Send it back to the requirement it contradicts, as a change that faces a gate | Writing it in an incident record and calling it handled |
| A checkpoint is dropped to keep a date | Name what it would have refused | Believing the schedule argument, which always sounds stronger |

One more habit: ask whether each option ends. A task finishes. A staffing arrangement holds steady. A retirement closes the file. Exactly one item on a lifecycle list lasts as long as the system, and after a launch scenario that is the one it points at.

**ELI5.** "Throw a party" ends. "Stay open" keeps going. Pick the one that keeps going.

## What to Remember

- The **standing phase** begins at go-live, covers operation and maintenance, and has no completion criterion. A system in use needs watching, answering for and evolving until switched off. Development finishes; this does not.
- A **gate** is real only if it can refuse, and it refuses against a named artifact: the constraint with a source, the eval score against a baseline, the recorded pin, the live metric, the routed finding.
- A skipped gate throws no error. The system works on the day and cannot be reasoned about later. So schedule pressure wins wherever it is allowed to be an argument.
- From day one in production, instrument cost per call, latency and failures. Cost telemetry is an approximation, and official billing comes from the provider. Trend it, never reconcile against it.
- Refusals are not HTTP errors. They arrive on a successful stream, so a count of transport errors stays flat as usable responses drop. Track refusals separately.
- Pinning a model ID fixes the model for that ID's lifetime. It does not cover the convenience aliases accepted for some earlier models. Behaviour stays steady; availability does not.
- Anthropic sets the retirement schedule: at least 60 days' notice for publicly released models, then requests fail. Partner platforms have their own dates, so Bedrock or Google Cloud means a different calendar.
- Migrating between current models is mostly drop-in. Check removed features, changed thinking behaviour and refusal behaviour. An eval against the outgoing baseline shows what the swap cost.
- Iteration sends a production finding to the requirement it contradicts, back in as a gated change. Left in an incident record, it is knowledge held by one person on one shift.
- Retention outlives the application. Local session transcripts last six years by default, or an organization's configured retention period. Activity Feed data lasts six years. Switching off stops traffic, not stored data.

**ELI5.** Opening day starts a long job. Check, count, expect change, write down what you learn.

## Endnotes for this chapter

1. The exported cost metric supports usage-trend tracking, identification of high-usage sessions and attribution of spend, but cost metrics are approximations and official billing data comes from the API provider (Claude Console, Amazon Bedrock, or Google Cloud's Agent Platform). Anthropic, *Monitoring* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)

2. The API error event is logged when an API request to Claude fails and carries an HTTP status code, which is absent for non-HTTP failures such as connection errors. A refusal returns `stop_reason: "refusal"` and arrives on a successful response stream rather than as an HTTP error, so the API error event does not fire for it; a separate refusal event exists to let refusal frequency be tracked and grouped. Anthropic, *Monitoring* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)

3. Each Claude model ID identifies a pinned version of the model, and the underlying model remains constant for the lifetime of that ID; the guarantee covers model IDs and not the convenience aliases that the Claude API accepts for some earlier models. Anthropic, *Model IDs and versioning* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)

4. Anthropic regularly retires older models as newer ones launch, notifies customers with active deployments and provides at least 60 days' notice before retirement for publicly released models, and requests to models past the retirement date will fail. The dates published apply to Anthropic-operated platforms; partner-operated platforms (Amazon Bedrock and Google Cloud) set their own retirement schedules, so a model's lifecycle status and dates can differ. Anthropic, *Model deprecations* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/about-claude/model-deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)

5. Migration to the current models is mostly drop-in, using the same Messages API and tool use patterns, and the key changes to check are the features that are no longer available and thinking output, plus safety classifier refusals where the migration target has them and the previous model did not. Anthropic, *Migration guide* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/about-claude/models/migration-guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)

6. Local session transcripts from Cowork and Claude Code on users' machines are stored for six years by default, or for the organization's custom conversation retention period where a finite one is set, and Activity Feed data is retained for six years. Anthropic, *API and data retention* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/manage-claude/api-and-data-retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)
