# Chapter 17: REST, Versioning, Review: the Exam Beyond Claude

**Summary**: *This is the third-heaviest skill on the paper, and it hardly mentions Claude. It asks about REST contracts, JSON that copes with a field you have never met, concurrency you cap yourself, prompts that get code-style review, a build that checks only what really breaks, and a migration that locks in behaviour first. Study only the model and these arrive as plain engineering questions you cannot answer. Missing one costs the same as missing a model question.*

## Seven Named Topics in This Skill, and None of Them Is About Claude

Picture a developer who knows every page about the model. Then a question describes forty call sites, a deprecated parameter and six months to fix it. That is a migration question. Claude is only the backdrop.

The blueprint names seven topics. **REST APIs**. **JSON**. **Asynchronous programming**. **Version control**. **Lifecycle integration**. **Code review**. **Refactoring**, both small and large. None is specific to Claude. A good engineer does all of them on a normal Tuesday.

Good practice does not change when a model is involved. What changes is the thing you call. Think of a supplier across town. You phone in orders, pay per delivery, and the supplier rewrites the catalogue on their own timetable. Call this a **model-shaped dependency**. It is remote, its answers vary, it bills per call, and its versions retire on a schedule you do not control. It can also fail while reporting success.

| Property | What it does to normal practice |
|---|---|
| Same input, different output on different runs | A test that demands an exact match gives you noise, not real failures |
| Each call costs money by size | Token spend can regress, just as latency can |
| The publisher retires versions on their calendar | Migration is planned work, not upkeep |
| A failure can look like a good answer | Checking only the status code leaves a gap |
| Behaviour lives in prose, not control flow | Prompt text is code and belongs where code lives |

Each section below is an ordinary habit with one of these rows mixed in.

**ELI5.** A friend sells you sandwiches. Each tastes a bit different. You pay every time. One day he stops making your favourite. You plan for that.

## A Contract Is What Is Promised Plus What Is Reserved

Chapter 2 covers the parts of a call. Chapter 3 covers the endpoints. Under both lies a sharper question that exams like. What does the publisher promise, and what did they keep the right to change? In the supplier picture, this is the small print on the order form.

The promises are plain. You reach Claude through a **RESTful API**. Requests and responses are JSON. Each response carries an identifier for that one call.<sup>[1]</sup> The service is stateless, which comes from REST and not from the model. It remembers nothing between calls. If you want continuity, your code must provide it.

The kept-back rights start with versions. Every request must send an `anthropic-version` header. Anthropic recommends the latest version. Older ones count as deprecated and may be closed to new users.<sup>[2]</sup> Pinning a version does not freeze the service. It only means any change was someone's decision.

Here is the part that decides questions. An error comes back as JSON holding a type, a message and a request identifier. The versioning policy says the values in those objects may grow over time.<sup>[3]</sup> Act on the values you know. Add a default branch for anything else. Log the identifier, not the wording.

Now the trap. A careful engineer writes a switch covering every error value in the docs. Nothing is left out, so the reviewer approves. But the list belongs to the publisher, who can add to it. The first new value hits a branch that is not there, and the bug appears far from its cause. Matching on message text breaks the same way, because wording is not part of the contract. The typed exception classes are.<sup>[3]</sup>

JSON follows the same rule in small. Read fields by name. Skip fields you do not know instead of failing on them. A field that is missing and a field that is null say different things, so keep them apart.

**ELI5.** The supplier says new kinds of problems may show up. So keep a catch-all for the ones you do not know.

## Concurrency Is a Property of Your Process, Not a Feature of the Service

"Asynchronous" means two unrelated things here, and questions pull them apart on purpose. One is a service that takes a big pile of work and hands results back later. Chapter 3 covers that. It earns a discount, not speed. The other is how your own code is written. This section is about that one.

A thread that waits on a network call does nothing while it waits. Non-blocking code instead fires off many calls, does other work in the gaps, and deals with each answer when it arrives. You phone in many orders without standing at the door for each. You are overlapping the waiting, not computing in parallel. That is why one process can have hundreds of calls out at once without hundreds of cores.

Four consequences matter.

One, you set the limit that actually applies. Suppose a loop starts ten thousand calls together. It meets the rate limit as a wall. Each rejected call then spends retry budget that the waiting calls also need. A **bounded pool of workers** turns a burst into a steady rate.

Two, answers do not come back in the order you sent them. Once work overlaps, a result has no built-in tie to its request. So give each job a key. The key returns with the result, and you match on it. If you match by position in a shared list instead, you may update the wrong customer and see no error at all.

Three, retries and concurrency multiply each other. The retry budget is one pool shared across the process. If every worker retries by itself against a limit they all caused, the limit stays tripped. Your logs then look like a service outage.

Four, a retried call must be harmless to repeat. Concurrency makes retries routine. Say a job saves a record, charges an account or sends a message. It needs a key the receiver can use to see it already handled that job. Without one, a correct client and a correct service still create the record twice. Neither log shows an error.

The named failure is unbounded fan-out, and nobody usually chooses it. Someone writes the sequential version and it is slow. Starting everything at once is the fix with the least typing. If volume is high and no one is waiting on a single answer, use the service's own asynchronous submission instead of writing concurrency yourself. High volume with no one waiting is the signal.

**ELI5.** Ten thousand calls at once jams the supplier's line. Use a few callers. Number each order. Make sure ordering twice does not bring two sandwiches.

## Version Control Holds Everything That Decides What Ships

One test does the work of any file-type list. If editing it changes what the live system does, it lives in the repository next to the code. It gets tracked and reviewed like code.

That test catches things you likely keep elsewhere.

| Artifact | Where it often sits | Why it belongs in the repo |
|---|---|---|
| Prompt text | In a string in a handler, or a database row no one diffs | It sets behaviour, so editing it changes behaviour with no commit |
| Model identifier | Written inline where the call is made | It sets capability, price and a retirement date, and shows up in many files |
| Tool and output schemas | Next to the code, normally | Downstream consumers were built against them |
| Evaluation sets and thresholds | A spreadsheet one person owns | A pass mark means nothing without a fixed set behind it |
| Credentials | Wherever they were first pasted | They do not belong there either, and chapter 22 says why |

People argue most about prompts, so take that head on. A prompt looks like documentation because it is prose. It is not documentation. It is code that defines behaviour. Run the same input through two prompt versions and you have two different systems. If one version skipped the commit, the deployment record cannot tell them apart. So a prompt needs one home, a tracked history, and review at least as strict as the code around it. A hand-written change log only matches reality while someone remembers to update it.

Claude Code's own settings follow this rule. A project settings file reaches a teammate's clone and a cloud session only when it is committed. The local one beside it is added to git excludes the first time it is written, so it stays out of commits.<sup>[4]</sup> Team settings are shared by committing them. Personal machine settings are kept out on purpose.

The anti-pattern is the prompt edited live in production. The tell is a team that cannot say what the system did last month.

**ELI5.** If changing something changes what the app does, store it with the code, with a history. A prompt counts. A password does not.

## A Pipeline Stage Earns Its Place on Two Conditions, and Most Fail One

Adding this work to an existing build comes down to a single question. What should the build check that it does not check now? Chapter 19 covers building evaluation sets and tests. Chapter 23 covers the phases. This section covers choosing.

A stage belongs only if both of these hold. It catches a regression that would otherwise ship. And it stays green when an answer comes back worded differently but is still right. Think of checking a delivery at the door: right goods, not the same box colour as last week. Three stages pass both tests on this kind of system.

| Stage | What it catches | Why it survives rewording |
|---|---|---|
| Scored evaluation against a versioned set | Quality dropping after a prompt, model or setting change | It uses a score threshold, not one required output |
| Contract tests over schemas and parsers | Tool schemas, output shapes and consumers drifting apart | It checks shape and fields, not wording |
| Token and cost regression check | A change that quietly multiplies tokens per request | It uses a budget with a stated tolerance |

Two stages tempt people. Each fails half the test.

Comparing output to a saved response, byte for byte, fails the second test straight away. Every fair rewording trips it. It raises alarms on good runs, so people turn it off within a week. The exact-match assertion is the anti-pattern. Turning it off is the sensible reaction.

Automatic remediation fails the first test, and less obviously. Say the pipeline rewrites the prompt when a score falls, then ships the rewrite unreviewed. It did not catch the regression. It erased the warning, along with the human judgement the warning existed to call.

There is a reproducibility trap under all this, worst when the pipeline runs Claude Code itself. A non-interactive run with `-p` loads the same context as a normal session. That means anything set in the working directory or the home directory. It also runs the project's hooks and connects its configured servers, with no trust dialog. Add `--bare` and all that discovery is skipped, so a scripted run gives the same result on every machine. Add `--output-format json` and you get a payload a script can branch on.<sup>[5]</sup> A build step that reads whatever the host has set up cannot be repeated. One runner passes and another fails with no code change, and nobody thinks to look at the machine.

Claude can run inside repository workflows. It can answer a mention on an issue or pull request, or take a prompt to run on any repository event. It signs in with a repository or organisation secret.<sup>[6]</sup> That plugs into the lifecycle you already have, not a new one.

**ELI5.** A good door check asks "is this the right stuff?" not "is it identical?" A check that cries wolf gets switched off. A fixer that changes things unasked removes the alarm.

## An Automated Reviewer Produces Findings; the Merge Gate Is Still Something You Build

The managed review service shows the exact split that questions test. It runs when a pull request opens or on each push. Findings land as inline comments on the lines they concern. A check run appears beside the other checks. That check run always ends neutral, so branch protection never uses it to block a merge. To gate on it, your own pipeline has to read the severity breakdown from the check run and decide.<sup>[7]</sup>

This is a general pattern. A reviewer, human or machine, makes findings. A gate is a rule about which findings stop a change. They are two separate things. Install the first and think you have the second, and you hold a review no one must act on.

Now the review itself. A teammate opens a pull request on your service. It works, but three things are missing. The prompt and model are hardcoded inline. No code handles an error from the remote service. And no tests cover the integration.

Do not rank them and let two go. Each breaks production alone, for its own reason.

- Hardcoded settings mean the prompt and model change only with a deploy, and no one reviews them as things that change.
- With no error handling, the first rate limit, timeout or overload becomes an unhandled exception. This dependency will certainly return errors.
- With no tests, no one can prove later that the first two were ever fixed.

So ask for all three before the merge. Any partial answer lets one through. Approving because the happy path works ships all three. Deferring the error path holds back the one gap that fails while users are watching. The tricky wrong answer is approving with a promise to fix it yourself, because it feels kind. It defeats the review, moves the work without finishing it, and leaves the author no better at the next one. The next request repeats it.

Behind those three sits what makes any change easy to review. It does one thing. An example shows it running. A test proves the behaviour, not just describes it. A short note states what the change assumes about its environment. A reviewer who must first work out the author's intent will leave the review until last. So a correct change can wait for weeks.

**ELI5.** A reviewer points at problems. A gate is a door that stays shut until they are fixed. Having a reviewer gives you no gate. And if a helper says "I'll just fix it for you," you never learn what you got wrong.

## Refactoring Splits by Whether Behaviour Has to Be Pinned First

Small-scale refactoring changes how code is laid out and leaves what it does alone. Pull a hardcoded value into configuration. Name a seam. Split a function that quietly took on a second job. It counts as correct if nothing observable moved. That makes it safe to do constantly and cheap to review, since a reviewer who trusts the claim just checks the shape.

That promise is also the value. It is why the two kinds of change need separate commits. Mix both and no one can tell later which half caused a bug. The mixed commit is the anti-pattern, and rushed people write it, not careless ones. Splitting it costs one more commit and lets you revert half the work.

Pulling out configuration is the small refactor this material asks for most. It fixes the review gap from the last section. The migration below also needs it first. A value you can change without a deploy can change one environment at a time.

Large-scale refactoring is a different job with the same name. One case keeps appearing on the exam. A deprecated parameter is used in dozens of places, with a deadline attached.

The deadline is real and written down. Customers with active deployments get at least sixty days' notice before a public model retires. Requests to a retired model simply fail. And an audit of API usage helps you find the places that still call the old thing.<sup>[8]</sup>

The deadline is not the danger. Meaning is.

Two documented migrations show it. The first is manual extended thinking with an explicit token budget. The newest models do not support it and return an error. That budget has no direct replacement. Thinking is adaptive, and the effort parameter controls the output, not a thinking budget.<sup>[9]</sup> The second is the sampling parameters. They were deprecated from a stated generation onward and return an error when set to a non-default value. One SDK dropped them entirely, so passing them raises a type error, not a quiet ignore.<sup>[8]</sup>

In both, the replacement is not a rename. It works on something else. So a mechanical swap across forty call sites changes behaviour at every one and warns you at none. It is like a supplier swapping your sandwich for a salad under the same item number.

So the order is fixed. Lock in the behaviour first, then change it. Write regression tests for what the parameter does today, while the old one still works, since afterwards there is nothing left to observe. Then migrate in batches small enough to trace a failure to one batch. Check each batch against those tests before starting the next.

Two named failures cluster here, and both answer a question nobody asked.

The compatibility wrapper keeps the old signature while the meaning shifts beneath it. Every call site still compiles and the diff is tiny. But the change in meaning now sits inside one function that no test watches. The parameter still vanishes on the published date.

The deadline-day migration is the honest form of the same dodge. All the work is booked for the last stretch. So every change in meaning lands in one unchecked push, when no time is left to recover.

Both trade a real risk for a tidier calendar.

**ELI5.** Before swapping a part, photograph how the old one works. Change a few things at a time and compare. Doing it all on the last day leaves no time to fix mistakes.

## How Wrong Answers Are Built on This Material

Wrong answers here are hard to rule out, because they describe things good teams do. Wrappers get written. Reviewers do sometimes fix small things themselves. Four habits of thought produce most of them.

- **Schedule risk standing in for meaning risk.** The option fixes when the work happens, not whether the change is safe. Examples are a wrapper, a batching plan or a later release. A quick test helps. Would it still be right if the deadline were a year off? If yes, it never touched the risk in the scenario. It is right only when the replacement is truly a drop-in rename.
- A check that cannot take rewording. Exact string equality, a fixed response length, a stored output compared literally. Each catches real changes. Each also fires on a right answer phrased another way, so it makes noise and gets turned off. Ask what a correct but reworded answer does to the check.
- Judgement taken out where judgement was the point. Examples: rewriting a prompt automatically on a low score, approving with a promise to fix it privately, and treating an automated reviewer as a merge gate. Each turns a signal for a person into an action by a machine. Ask which person was meant to decide, and whether the option leaves them anything to decide with.
- A partial fix chosen because it is biggest. Three separate gaps are listed. The option closes the largest. It is a real gain, so it passes a first read. When each gap breaks production alone, the answer is all of them. Covering two of three is wrong by the same rule as covering none.

Match on what the scenario does, not on the tool it names.

| If the scenario says | Usual answer | Usual trap |
|---|---|---|
| A parameter is deprecated and its replacement acts differently | Test current behaviour, then migrate in batches you can trace | A wrapper keeping the call shape, or a single swap on deadline day |
| A pipeline is planned for a Claude-backed service | Stages that catch real regressions and stay green when wording shifts | Comparing output literally, or auto-rewriting and deploying |
| A change hardcodes settings, skips error handling and has no tests | Ask for all three before merge, as each fails alone | Approving and fixing it yourself, or deferring the error path |
| One job must act the same on every machine | Load nothing the host happens to hold, and state the context | Assuming a scripted run sees what a developer's session sees |
| Prompts are hand-edited and nobody knows what changed when | One home, tracked history, review on the code's terms | A hand-kept log, or optional review for prose |
| Volume is high, jobs are independent, no one waits on one result | Bounded concurrency with a correlation key, or asynchronous submission | Starting every call at once, or a plain loop called simple |
| A retry fires and the same action landed twice | Make the job safe to repeat, with a key the receiver knows | More retries, fewer retries or backoff, none of which fix a repeat |
| An automated reviewer already comments on every pull request | Read its findings in your pipeline and decide what blocks a merge | Treating the reviewer being there as the gate |
| A response field gets a value the code never expected | Branch on known values and default the rest | A full switch, or matching on error message text |

One habit works past the table. For each option, say which of the five properties of a model-shaped dependency it covers and which it quietly ignores. Wrong options are nearly always good engineering aimed at a dependency that behaves better than this one.

**ELI5.** Wrong answers sound like things smart teams really do. Ask of each one: does it deal with the real danger, or just make the calendar look neat? Does a person still get to decide?

## What to Remember

- A model-shaped dependency has five properties: it varies between identical runs, bills by the call, retires on the publisher's schedule, fails while returning success, and has behaviour defined in prose. Practice stays the same. Each practice must absorb a property.
- A contract is what is promised plus what is reserved. Errors arrive as JSON with a type, a message and a request identifier. The versioning policy reserves the right to grow those value sets. So code branches on known values, defaults the rest, and skips message text.
- Every request needs an `anthropic-version` header. The latest version is recommended. Earlier ones are deprecated and may be closed to new users. Pinning makes any upgrade a deliberate decision.
- Concurrency means overlapping waiting, not parallel computation, so one process can hold many calls in flight. You set the limit that governs. Bounded workers turn a burst into a rate. Launching everything hits the rate limit as a wall and burns retry budget queued work needs.
- A retried call must be safe to repeat, since concurrency makes rare retries routine. Work that writes, charges or sends carries a key the receiver knows it already handled. Otherwise a correct client and a correct service create the record twice.
- Completion order is not submission order. Each unit of concurrent work carries a correlation key that returns with its result. Joining by position updates the wrong record silently.
- Anything that changes production behaviour when edited belongs in version control: prompt text, model identifiers, tool and output schemas, evaluation sets and thresholds. Credentials do not. Shared configuration is committed. Machine-specific settings are left out.
- A prompt is code that defines behaviour, so two prompt versions are two systems on one input. It needs one home, a tracked history, and a review gate as strict as the code around it. A hand-kept change log drifts from reality.
- A pipeline stage earns its place by two tests. It catches a regression that would otherwise ship, and its green result survives an answer that is reworded but correct. Literal output comparison fails the second and gets disabled. Automatic remediation fails the first and deletes the signal it was meant to raise.
- Three stages fit: a scored evaluation against a versioned set with a threshold, contract tests over schemas and downstream parsers, and a token and cost regression check.
- A scripted run that loads whatever the host has configured is not reproducible. Non-interactive Claude Code reads the working directory and home directory by default, including hooks and configured servers. A bare mode skips that, so every machine gives the same result.
- A reviewer produces findings. A gate decides which findings stop a change. The managed review posts inline comments and a check run that always ends neutral, so it never blocks a merge itself. Gating means reading its severity output yourself.
- Three gaps in a Claude-powered change each fail alone. Hardcoded configuration cannot change without a deploy. No error path turns the first rate limit into an unhandled exception. No tests leave both unproven. Ask for all three. Approving while fixing it yourself moves the work instead of resolving it.
- A change is easy to review when it does one thing, an example shows it running, a test proves the behaviour, and a short note states what it assumes about its environment. A reviewer who must rebuild the intent reviews last.
- Restructuring and behaviour change go in separate commits. Together, no one can say which caused a symptom. Splitting costs one extra commit.
- Small refactoring changes structure and nothing observable. Large refactoring changes semantics, so behaviour is pinned in tests before the change, and migration runs in batches small enough to trace a failure.
- A deprecated parameter whose replacement acts on something else is not a rename. Anthropic gives at least sixty days' notice before a public model retires, requests past retirement fail, and a usage audit finds remaining call sites. A compatibility wrapper keeps the signature and loses the meaning. The deadline-day migration packs every semantic change into one push with no slack behind it.

**ELI5.** Treat the model like a moody supplier across town. Expect surprises, limit your calls, keep your recipes in one tracked place, check deliveries for sense and not spelling, and test before you switch.

## Endnotes for this chapter

1. The Claude API is a RESTful API at `https://api.anthropic.com`, requires `content-type: application/json` on every request, and returns a `request-id` response header carrying a globally unique identifier for that request. Anthropic, *API overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/overview](https://platform.claude.com/docs/en/api/overview)

2. API requests must send an `anthropic-version` request header, for example `anthropic-version: 2023-06-01`; Anthropic recommends using the latest API version whenever possible, and previous versions are considered deprecated and may be unavailable for new users. Anthropic, *Versions* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/versioning](https://platform.claude.com/docs/en/api/versioning)

3. Errors are always returned as JSON with a top-level `error` object that always includes a `type` and a `message` value, alongside a `request_id` field; in accordance with the versioning policy the values within these objects may expand and the set of `type` values is expected to grow over time; the official SDKs raise typed exceptions rather than returning raw JSON, and the documented guidance is to catch those typed classes rather than string-matching error messages. Anthropic, *Claude API errors* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/api/errors](https://platform.claude.com/docs/en/api/errors)

4. A project's `.claude/settings.json` reaches a teammate's clone and a cloud session only if the file is committed to version control; until then it is a file on one machine's disk. The adjacent `.claude/settings.local.json` is added to the user's global git excludes the first time Claude Code writes it, so that it stays out of commits. Anthropic, *Claude Code settings* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)

5. Passing `-p` runs Claude Code non-interactively, loading the same context an interactive session would, including anything configured in the working directory or `~/.claude`, and running the hooks in a project's `.claude/settings.json` and connecting the servers in its `.mcp.json` with no workspace trust dialog and no per-server approval prompt. Adding `--bare` reduces startup time by skipping auto-discovery of hooks, skills, custom commands, subagents, plugins, MCP servers, auto memory and `CLAUDE.md`, and is described as useful for CI and scripts where the same result is needed on every machine. `--output-format json` returns structured JSON with the result, session ID and metadata. Anthropic, *Run Claude Code programmatically* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/headless](https://code.claude.com/docs/en/headless)

6. The Claude Code GitHub Action runs Claude Code inside a repository's workflows, responding to an `@claude` mention in a pull request or issue comment, or running automatically on any GitHub event when given a prompt, authenticating from a repository or organisation-level Actions secret. Anthropic, *Claude Code GitHub Actions* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/github-actions](https://code.claude.com/docs/en/github-actions)

7. Reviews trigger when a pull request opens, on every push, or on manual request; findings are posted as inline comments on the specific lines where issues were found, with a summary in the review body, and each review populates a check run alongside the repository's other CI checks. That check run always completes with a neutral conclusion, so it never blocks merging through branch protection rules; gating merges on findings requires reading the severity breakdown from the check run output in your own CI. Anthropic, *Code Review* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/code-review](https://code.claude.com/docs/en/code-review)

8. Once a model is deprecated all usage must be migrated to a replacement before the retirement date, and requests to models past the retirement date will fail; Anthropic notifies customers with active deployments and provides at least 60 days' notice before retirement for publicly released models; an audit of API usage is available to help locate remaining usage of deprecated models. The `temperature`, `top_p` and `top_k` parameters are deprecated from Claude Opus 4.7 onward and return a `400` error when set to a non-default value on those models, and the Python SDK from v1.0 removes them from its request types so that passing them raises a `TypeError`. Anthropic, *Model deprecations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/model-deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)

9. Manual extended thinking with an explicit `budget_tokens` value is not supported on the newest models and returns a `400` error; `budget_tokens` has no direct replacement because thinking is adaptive, and the effort parameter is a separate output-level control rather than a thinking budget. Anthropic, *Migration guide* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/migration-guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)
