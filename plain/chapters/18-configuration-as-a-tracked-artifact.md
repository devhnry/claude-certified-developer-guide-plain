# Chapter 18: An Unpinned Version Is an Untracked Change

**Summary**: *Your system broke. Three things moved since it last worked. None was committed. The fix is to make every input a value someone picked and wrote down: the canonical model identifier, not the drifting pointer; a named prompt version a rollback can reach; plugin dependencies held in a tested range; each setting in the file whose reach fits who needs it. Skip it and the bill comes later: a regression you cannot assign, and nothing to roll back to.*

## Nobody Can Name the Change That Caused the Regression

Picture a kitchen whose recipe card says only "tomato sauce, pasta, cheese". The dish tastes off one day and nobody knows why. Unrecorded inputs make a system that kitchen.

A **summarisation service** begins emitting output that the **downstream parser cannot read**. It worked in March. Six weeks of release log are empty, so nothing seems to have changed.

Three things did change. Someone fixed a formatting complaint by editing the system prompt where the live service reads it. A plugin took the marketplace's newest release overnight. And the model identifier in the call was a **convenience pointer**. It moved to a newer snapshot on a timetable set outside your building.

All three alter the output. None left a commit. So four people sit in a review and guess. No earlier state can be restored, and nothing says which change came first.

Call that gap the **unattributable window**. It is the stretch between the last state you can reproduce and today's state, filled with changes nobody logged. Configuration management (a full recipe card) keeps it empty. It earns nothing on a normal day. On a regression day it is the only help.

Every input is either a value someone chose or a variable nobody declared. The second kind is silent. Five follow.

| What moves | Why nothing was committed | The pinned version of it |
|---|---|---|
| The model | A pointer shifts to a newer snapshot by itself | Canonical ID kept in a file under version control |
| The prompt | Somebody edits it in the spot the live system reads | A reviewed, named version, with the old one retained |
| A plugin | Auto-update grabs the latest marketplace release | A stated range, resolved from a tag |
| Team configuration | The file sits on one laptop only | Committed next to the code it governs |
| The measurement | The test set stays put while real traffic changes | A dated set, rebuilt from current traffic |

**ELI5.** If a cake tastes odd and you never wrote down the flour, you can't find why. A written list lets you go back.

## A Model Identifier Names One Snapshot; a Convenience Pointer Names Whatever Is Newest

Compare "flour from aisle 3" with "Brand X, 1 kg bag, batch 41". Only the second stays put. A model ID is the second kind. Each **Claude model ID** is a **pinned version**. The model beneath it never changes while that ID exists.<sup>[1]</sup>

From the 4.6 generation on, IDs have no date. That dateless ID is the **canonical** ID for the release. It points at one snapshot that is never changed in place, and a newer version gets a new ID. Anthropic calls it a common misconception that a dateless ID points at the latest or best version. Older models have a snapshot date in the ID. On the Claude API they also get short aliases that track the newest dated snapshot for their minor version.<sup>[1]</sup>

The format changed, not the habit. Write the ID the docs call canonical, never the short alias beside it. The alias is handy because it advances. Check the model page for the current convention. It already changed once.

A pin has two limits. The weights stay fixed for an ID. The serving setup around them does not. Routing, safety classifiers and sampling logic can change. Now and then an infrastructure update nudges observable behaviour on an ID that stood still.<sup>[1]</sup> So pinning cuts the suspects down but not to zero.

Every ID has its own deprecation and retirement schedule.<sup>[1]</sup> Partner platforms set their own dates too, so one model can be at a different lifecycle stage depending on where you run it.<sup>[2]</sup> A pin is a promise with a date. Chapter 17 has the migration work due then.

The anti-pattern is the pointer that made it into production. It never looks like a choice. It is quick to type and works that day. Later the output shape shifts, the old snapshot was never written down, and the fix is a hotfix to your parser. Keeping the prior identifier is half the value of pinning, and teams skip that half.

**ELI5.** "The newest one" means something different each week. A full name and number always means the same thing. Use it, and keep the old one for going back.

## A Prompt Version Is the Only Thing an Incident Timeline Can Point At

Chapter 17 covers where prompt text lives and its gate. A version adds a name, and the name does two jobs. An incident timeline can say which text produced the bad output. A rollback has a place to land. Without a name, both mean digging through editor history.

A version reaches production like a new model. It handles a slice of traffic first. Its score is compared with the current version's baseline, and that number decides: promote or revert. Anthropic says criteria must be specific and measurable first, and that grading trades speed for nuance. Code-based grading is the fastest and most reliable. Model-based grading is flexible once you have tested how reliable it is. Human grading is the most flexible and the slowest.<sup>[3]</sup> Chapter 19 builds the evaluation set. Here it works as a gate.

A prompt differs from a pinned model in one way: it has consumers. Skipping that check bets that no consumer depends on what this version changes. Three near-misses live in that gap. Warning downstream owners puts the change on their calendar and learns nothing about its effect. A clean staging run proves only what staging covers. Shipping to the checked consumers first leaves one application answering under two prompt versions. That is a second unattributable difference.

The anti-pattern is the prompt with no version number. The tell: the team shows you today's text and cannot produce yesterday's.

**ELI5.** A prompt is a note you hand the cook. Label the notes "version 1", "version 2", and you can hand back the old one.

## Four Configuration Surfaces, and the Reach That Picks Between Them

Some recipe cards hang on the shared wall. Others sit in one cook's apron. One rule settles most scenarios: match the file's reach to the people who need the setting.

| File | What it carries | Who it reaches |
|---|---|---|
| `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project-wide standing instructions | Anyone who clones the repo, via version control |
| `CLAUDE.local.md` | Notes for your own copy only | Your machine; not committed |
| `.claude/settings.json` | Permissions, hooks, telemetry and enabled plugins | Teammates and cloud sessions after it is committed |
| `.claude/settings.local.json` | Your own exceptions for this project | Your machine; excluded from commits automatically |
| `.mcp.json` in the project root | Servers the project must have to work | Anyone who clones the project |
| `managed-settings.json` and its console equivalent | Policy set by the organisation | All machines the organisation rolls it out to |

These reaches are in the docs. A project settings file arrives in a teammate's clone or a cloud session only after you commit it. The local file beside it goes into your global git excludes the first time Claude Code writes it.<sup>[4]</sup> Project instructions travel the same route, so that file carries team standards, not personal taste.<sup>[5]</sup> Of the three server scopes, only `.mcp.json` at the repository root reaches other people. Local and user scope both write to `~/.claude.json`.<sup>[6]</sup> Organisation policy is placed in a system path on each machine.<sup>[7]</sup>

If two cards disagree, the highest level that sets a key wins. The order runs managed settings, command line arguments, project local, shared project, then user settings. List keys, like the permission arrays, merge across files. Each file adds entries and none replaces another.<sup>[4]</sup>

The anti-pattern is a shared dependency left in personal configuration, and its owner cannot see the fault. Say every session needs a server, registered at user scope on the laptop where it was first tried. It works there and nowhere else. The workarounds are worse: a README setup procedure, which makes correctness depend on each person following it identically, or a sync step that copies personal files between machines. The reverse also fails. Commit an experiment nobody asked for to the project file, and now it is everyone's.

Instruction files are read into the context window at the start of each session. Claude treats them as context, not as enforced configuration.<sup>[5]</sup> A rule there steers Claude. It guarantees nothing.

**ELI5.** A card on the wall is read by the whole kitchen. A card in your apron is read by you.

## A Plugin Dependency Follows the Newest Release Until Somebody Constrains It

A supplier who swaps your tomatoes for each new brand unannounced is how a plugin dependency behaves by default. It follows the latest version. An upstream release can change what runs under your plugin, with no warning and nothing done on your side.<sup>[8]</sup> A declared version constraint holds it in a range you tested until your team chooses to move.

You declare constraints in the `dependencies` array of a plugin's `.claude-plugin/plugin.json`. They resolve against git tags on the repository that hosts the dependency. Each release is tagged `{plugin-name}--v{version}`. If several installed plugins constrain the same dependency, the ranges intersect. Resolution then takes the highest version that satisfies all of them, so auto-update keeps working within the range.<sup>[8]</sup> Which plugins are on is a separate key, `enabledPlugins`, keyed by plugin name and marketplace and settable in any settings file.<sup>[9]</sup>

With no version on record, the team cannot say where a regression began or freeze the working version, and has nothing to return to. So the repair must create the record.

The confident wrong answer is an upgrade schedule mistaken for a record. A monthly jump to the newest release feels tidy but only speeds up unattributed change. Waiting for authors to announce breaking changes fails too, since the record stays with them.

**ELI5.** A shop that quietly swaps your ingredients changes your dish overnight. A rule of "only these brands" keeps it the same until you decide.

## Environments Differ on Purpose, and the Difference Has to Be Declared Somewhere

Development, staging and production may each use a different model identifier, prompt version and plugin set. That alone is fine, since staging exists to hold something production lacks. The defect is that nobody can list the differences, so a deliberate one and an accident look alike.

Keep one tracked place with the same keys for every environment. A difference becomes a declaration. Each one is either in the file, because someone chose it, or it is drift.

Two fixes sound similar and are wrong. Forcing every environment to match, to end drift, wipes out differences that have a reason, including staging's whole purpose. Unpinning until they agree drops a control you need and moves behaviour changes outside the commit history again. A third fix fails too: moving the values into application code ties every configuration change to a release, though configuration and code change on unrelated schedules.

**ELI5.** A test kitchen and a main kitchen can cook different dishes on purpose. Trouble starts when nobody knows why.

## Restoring Measurability Comes Before Improving Anything

A feature has run for a year. Its builders have left. Prompts were edited in place more than once, the evaluation set dates from launch, and the model identifier was never fixed. Someone proposes a newer model. That is the wrong first move, for a mechanical reason. It stacks one more change on a system whose current behaviour was never recorded, so the result is as unattributable as the rest.

```
1  Pin the moving inputs      canonical model ID, plugin ranges, configuration in one tracked place
2  Give the prompts as they stand a version, whatever anyone thinks of the wording
3  Rebuild the measurement from recent production traffic rather than from the launch assumptions
4  Change one thing, and compare it against what steps 2 and 3 recorded
```

Step 2 draws objections. The current prompts hold a year of lessons, in edits no one documented. A wholesale rewrite erases those lessons and the baseline that would show what the rewrite broke. Step 3 tempts the opposite error. Deleting the stale evaluation set removes a weak measurement and offers no substitute, so you hold less than before. An old set tells you about launch. Rebuilt from current traffic, it tells you about now.

**ELI5.** Before fixing a messy kitchen, write down how it runs today. Then change one thing at a time.

## How Wrong Answers Are Built on This Material

Wrong options here describe what careful teams really do. One bad assumption separates each from the right answer. Four cover nearly everything.

- **A routine offered instead of a record.** A setup guide, a monthly upgrade, a promise that authors will warn you, a hand-kept change log. Each needs a person to get it right every time, and none gives you two states to compare. Ask what you could look up six weeks later.
- **A control removed to quiet the symptom.** Unpinning so environments agree, deleting the stale evaluation set, or dropping the part that broke. The complaint ends. So does your ability to trace the next failure. Ask whether you now declare fewer variables.
- **Talking where testing was needed.** Notifying downstream owners, booking a window, staging the rollout, or deferring consumers nobody has examined. All four handle a change well without ever assessing it. Ask whether the option teaches you what the change does, or only when it lands.
- **Improving before there is a baseline.** Upgrading the model, rewriting prompts, adding a capability, on an unmeasured system. It looks like initiative, so it survives elimination. Ask what you would compare the result with.

Match on what the scenario does, not the parts it names.

| If the scenario describes | Usually right | Usually the trap |
|---|---|---|
| A regression, with several things moved since the last good state | Version and pin the inputs so the change can be traced and undone | Upgrading faster, or removing the part that broke |
| A whole team relying on settings held on one person's machine | Put them in the project file that travels with the repo | A written manual setup step, or a copy in every personal file |
| A private experiment mixed with a shared requirement in one spot | Split by reach: shared goes with the project, the experiment stays with the user | Merging them, or syncing personal files across machines |
| Prompts edited in place, with an evaluation set older than current traffic | Pin inputs and capture today's behaviour before touching anything | Upgrading first, rewriting prompts, or deleting the old set |
| Every environment on its own model, prompt and plugins | Gather them into tracked configuration that declares the differences | Making environments identical, or unpinning to match them |
| A prompt change reaching several downstream consumers | Test the effect on each consumer, then coordinate on what you find | Announcing it, or reading a clean staging run as the test |
| A dependency moved overnight while the repo stayed still | A stated version range, resolved from a tag | Hoping release notes arrive before the breakage |
| Instruction and settings files for a new project | Version them alongside the code they govern, reviewed the same way | Copying them per environment, or storing them in a separate repo |

One habit outlives the table. For each option, ask what you could read back in six weeks, and where. If an option just asks people to be careful, there is nothing to read.

**ELI5.** A wrong answer says "tell everyone to be careful". A right answer leaves a record you can look up next month.

## What to Remember

- The **unattributable window** is the gap between the last reproducible state and now, full of unrecorded changes. Configuration management keeps it empty. It pays off when something regresses.
- Each input is a chosen value or an undeclared variable. Five move: model identifier, prompt text, plugin versions, team configuration, and the evaluation set that traffic drifts away from.
- A Claude model ID identifies a pinned version that does not change while the ID lives. From 4.6 onward the dateless ID is canonical and maps to a single fixed snapshot. A newer version gets a new ID. Earlier models carry a snapshot date; their shorter API aliases advance to the newest snapshot of that minor version.
- Pinning shrinks the unknowns, not removes them. Weights are fixed per ID. Routing, safety classifiers and sampling logic can still change, so observable behaviour may shift under an ID that did not.
- Every model ID has a retirement schedule of its own. Partner platforms set their own dates. So a pin is a dated commitment, and one model can have a different lifecycle status depending on where it runs.
- Keep the old pinned identifier. Without it, a regression means a hotfix, not a rollback. That is half the value of pinning, and the half teams skip.
- A prompt version lets a timeline name the text and a rollback land somewhere. Promote on a score against the current baseline, not on a read-through of the new text.
- Several consumers of one prompt mean several sets of expectations. Announcing, scheduling and staging are not assessment. Shipping to some consumers first leaves one application answering under two versions.
- Scope follows reach. Project instructions and `.claude/settings.json` reach teammates once committed. `CLAUDE.local.md` and `.claude/settings.local.json` stay on one machine. `.mcp.json` in the repository root holds the servers the project requires. User-scope servers in `~/.claude.json` reach nobody else.
- Settings precedence: managed, command line, project local, shared project, user. The top level that sets a key wins. List keys merge across files and do not override.
- Instruction files load as context. They are not enforced configuration. A rule written there steers Claude and guarantees nothing, so a scenario that demands a guarantee needs another mechanism.
- By default a plugin dependency tracks the newest release, so an upstream tag can change behaviour without any commit. A version constraint in `plugin.json` holds it to a tested range, resolved against tags named `{plugin-name}--v{version}`. Several constraints intersect, giving the highest version that meets all.
- No recorded version causes three failures at once: you cannot locate the regression, cannot hold the working version, and have nothing to roll back to. A regular upgrade cadence records nothing and speeds up unattributed change.
- Environments differ on purpose. Consolidate them into tracked configuration that declares each difference. Never make them identical or unpin until they agree. Configuration kept in application code means a release for each settings change.
- On an untracked system, restore measurability first. Pin the inputs, version the prompts as they stand, and rebuild the evaluation set from recent traffic. Rewriting the prompts discards what the feature learned. Deleting the stale set leaves you with less than nothing.

## Endnotes for this chapter

1. Each Claude model ID identifies a pinned version of the model, and the underlying model remains constant for the lifetime of that ID; starting with the Claude 4.6 generation model IDs use a dateless format, and the dateless ID is the canonical model ID for that release, mapping to a single fixed model snapshot whose weights and configuration Anthropic does not update, with an updated version shipping under a new model ID. Anthropic identifies the belief that dateless IDs behave as evergreen pointers routing to the latest or best-performing version as a common misconception. Models before the 4.6 generation include a snapshot date in the ID and, on the Claude API, also have shorter aliases that point to the most recent dated snapshot for that minor version. Every model ID, dated or dateless, has its own distinct deprecation and retirement schedule. Model weights are fixed for a given ID, but the serving infrastructure around the model, including the request router, safety classifiers and sampling logic, can change, and infrastructure updates occasionally produce minor differences in observable behaviour even when the model ID and weights have not changed. Anthropic, *Model IDs and versioning* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)

2. The retirement dates published by Anthropic apply to Anthropic-operated platforms; partner-operated platforms set their own retirement schedules, so a model's lifecycle status and dates can differ. Anthropic, *Model deprecations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/model-deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)

3. Success criteria should be specific and measurable, using quantitative metrics or well-defined qualitative scales; when choosing a grading method, code-based grading is the fastest and most reliable and extremely scalable but lacks nuance for complex judgements, LLM-based grading is fast, flexible and scalable and suitable for complex judgement provided its reliability is tested before scaling, and human grading is the most flexible and highest quality but slow and expensive. Anthropic, *Define success criteria and build evaluations* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/test-and-evaluate/develop-tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

4. A project's `.claude/settings.json` reaches a teammate's clone and a cloud session only if it is committed to version control, and committing it gives everyone who clones the repository the same permissions, hooks, telemetry and plugins; `.claude/settings.local.json` holds one person's settings for that project and is added to the user's global git excludes the first time Claude Code writes it. When the same key appears in more than one place, Claude Code uses the value from the highest level that sets it, in the order managed settings, command line arguments, project local settings, shared project settings, user settings; list keys such as `permissions.allow` are combined across files instead of one file's value replacing another's. Anthropic, *Claude Code settings* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)

5. CLAUDE.md files give Claude persistent instructions and are loaded into the context window at the start of every session; Claude treats them as context rather than enforced configuration. A project CLAUDE.md can be stored in either `./CLAUDE.md` or `./.claude/CLAUDE.md`, holds instructions that apply to anyone working on the project, and is shared with the team through version control, so it should carry project-level standards rather than personal preferences. A `CLAUDE.local.md` at the project root loads alongside CLAUDE.md and is treated the same way, and should be added to `.gitignore` so it is not committed. Anthropic, *How Claude remembers your project* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

6. MCP servers are registered at one of three scopes: `local`, stored in `~/.claude.json` under the entry for the current project and available only to you in that project; `project`, stored in `.mcp.json` in the project root and available to everyone who clones the project; and `user`, stored under the top-level `mcpServers` key in `~/.claude.json` and available only to you across all projects. `.mcp.json` is the file most worth writing by hand because it is checked into the repository. Anthropic, *Connect to MCP servers* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/mcp-quickstart](https://code.claude.com/docs/en/mcp-quickstart)

7. Managed settings are deployed by an organisation as a `managed-settings.json` file placed in the system directory for each operating system, as an MDM policy, or as server-managed settings from the claude.ai console. Anthropic, *Deploy managed settings* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/managed-settings](https://code.claude.com/docs/en/managed-settings)

8. By default a plugin dependency tracks the latest available version, so an upstream release can change the dependency under your plugin without warning; version constraints let you hold a dependency at a tested version range until you choose to move. Dependencies are listed in the `dependencies` array of a plugin's `.claude-plugin/plugin.json`, and Claude Code resolves version constraints against git tags on the repository hosting the dependency, each release tagged as `{plugin-name}--v{version}`. When several installed plugins constrain the same dependency, Claude Code intersects their ranges and resolves to the highest version satisfying all of them, and auto-update fetches the highest tag satisfying every installed plugin's range rather than the marketplace's latest version. Anthropic, *Constrain plugin dependency versions* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/plugin-dependencies](https://code.claude.com/docs/en/plugin-dependencies)

9. The `enabledPlugins` setting turns individual plugins on or off, keyed by `plugin-name@marketplace-name`, and can be set in any settings file. Anthropic, *Claude Code settings reference* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/settings-reference](https://code.claude.com/docs/en/settings-reference)
