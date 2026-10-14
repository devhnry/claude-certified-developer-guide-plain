# Chapter 22: One Credential: What It Reaches, and for How Long

**Summary**: *Think of a house key. You cut spares, and each opens some doors until the lock is changed. A secret is a crowd of such copies. Three numbers set the price of a leak, and each practice here moves one. How many copies exist. What a copy allows the moment someone holds it. How long it works for that stranger. A fourth question is whether you would ever learn of it. It has no symptom if the answer is no.*

## The Value Is Shown Once and Then Comes to Rest Wherever It Was Needed

You make an API key in the Console. The full secret is shown once, at creation. A lost key cannot be shown again.<sup>[1]</sup> The platform keeps nothing to read back, so every later copy exists because a person made it.

Follow that key for a week. You paste it into a shell profile so a local run works. A deployment configuration takes a copy. Someone pastes it into a message for a stuck colleague. A runner caches it. A backup captures the runner. That makes six copies. Each was reasonable when made. No inventory lists them.

That leaves the question that sets what a leak costs. What can one of those six copies open, and for how long?

**ELI5.** Make spare keys and soon you cannot name who holds one.

## Three Measurements Decide the Damage, and Each Practice Moves One

The **copy set** is the list of spares: each place the value has come to rest, plus the access that place carries. Three measures act on it. **Count** means how many copies exist, and who can read each. **Reach** means what a single copy allows on arrival, the doors the key opens. **Life** means how long a copy works once someone else has it, the days before the lock is changed.

| Practice | Which measurement it moves | What it leaves standing |
|---|---|---|
| Referencing the secret instead of putting it in the file | Count | Reach and life of the remaining copies |
| A managed store read while running | Count, plus a record of each read | Reach |
| Separate credentials with narrow rights for each environment and service | Reach goes down | Count goes up |
| Setting an expiration at creation, and rotating on a schedule | Life | Count and reach |
| Access records and usage alerts | None of the three | All three |

Start with the right-hand column. Every practice leaves something alone. An answer naming one row and stopping answers a smaller question than a credential review asks.

**ELI5.** Fewer spares, fewer doors, shorter life: three separate jobs. Do all three.

## A Value Written Into a Tracked File Survives Its Own Deletion

A teammate commits a file with the key typed in, then types over it. Today's file is clean. History still holds the key, and so does every clone made before the fix.

So a config file should point to a secret and never contain it. This is **separation**. A tracked, cloned, reviewed or backed-up file spreads its contents to all those places, and overwriting edits only the newest version. Treating an overwrite as a removal is the classic anti-pattern. A credential once written inline is exposed and must be replaced.

The secret still needs a home. An **environment variable** injected when the program runs suits a secret that is local and short-lived: one process, one run, nothing on disk. A **managed secret store** suits a secret several services use. It gathers the copies into one place and logs who asked.<sup>[1]</sup>

Better still, keep the secret out of the workload. A proxy outside the agent's boundary adds credentials to outgoing requests. A vault swaps an opaque placeholder for the real secret on the way out. Subprocess environments can have provider credentials removed. The worker never holds the value.<sup>[4]</sup><sup>[7]</sup><sup>[8]</sup>

**ELI5.** Erasing a secret from a notebook fails if people copied the page.

## Three Properties Are Fixed at Creation and Changed Only by Issuing Another Key

Two things set reach: how many things a key serves, and what it may do.

Say one key serves development, staging and production. You split those apart on purpose. A shared key joins them again, so one theft hits all three. It also cannot be replaced in one place without being replaced in all. A shared key across environments buys simplicity and pays in isolation and rotation. A separate credential per environment and per service raises the count on purpose. Each is worth far less to a thief.

A key's workspace, expiration and any scopes you may pick are locked in at creation. To alter one, issue a different key.<sup>[1]</sup><sup>[2]</sup><sup>[3]</sup> Console **Admin API keys** offer no scope choices. Each has full access to every endpoint accepting it, and a key from one organization cannot manage another.<sup>[3]</sup> So issuing one is the whole authorisation decision, and approval belongs at issue time. Only an organization admin can create an admin credential. A requester with no permission in that workspace cannot use the create control.<sup>[1]</sup><sup>[3]</sup>

**ELI5.** A key is cut for set doors. Want different doors? Cut a new key.

## Rotation Is the Only Repair, and Expiry the Only Version That Runs Unattended

A leaked value cannot be made secret again. The one fix is a new key and revoking the old one. Anthropic's advice on both surfaces: use a secrets manager, rotate keys periodically, and revoke any key that may have leaked.<sup>[2]</sup><sup>[5]</sup>

Rotating on a timetable and rotating on a hunch do different jobs. The timetable caps how long a leak goes unnoticed. The hunch is emergency response. It gets cheaper with fewer copies, because code that looks up a name need not change when the value behind it does. One habit ruins both: put the new key back into the file the old one leaked from, and the error stops while the exposure returns.

Expiry works with nobody remembering. You pick it at creation. After it passes, requests fail and the key cannot be reactivated. It limits a stolen credential's usable life but does not stand in for storage or rotation.<sup>[2]</sup>

**Federation** deletes the durable value instead. A workload trades a trusted provider's identity token for a short-lived access token. Nothing static is minted, shared or rotated. The chain is only as sound as that provider's setup.<sup>[2]</sup>

**ELI5.** You cannot take copies back. You change the lock, or use keys that expire.

## An Asserted Identity Is a Claim Until Something Verifies the Signature

Sessions in a self-hosted environment carry a **signed token** your own services can check. A valid token proves Anthropic issued it, that it belongs to one session in one environment, and how that session began. It does not say which process is showing it. The token sits in an environment variable, so any code in the session can read it.<sup>[6]</sup> 

Checking is mechanical. Match the signature to the published key set. Reject an unexpected algorithm. Compare the audience claim with your own environment identifier. The check is also offline. A verified token stays good until it expires, whatever the session does later, and no revocation feed exists.<sup>[6]</sup>

The trap is **identity accepted as authorisation**: a verified caller gets whatever it can reach elsewhere. The token names the human who started the session, but that human did not sign in. Credentials made from it should cover one session's job and end when the token does.<sup>[6]</sup>

**ELI5.** A real badge proves a name. It should open only one job's rooms.

## Nobody Outside Your Organization Can Tell You a Key Has Leaked

From the platform side, odd usage patterns can be spotted. Whether one given key was compromised cannot.<sup>[5]</sup> Only your own records can tell you, and three kinds help. A managed store logs who read a value, which shrinks the copy set later. The Admin API lists each key with its expiration. It shows a redacted hint and never the secret, so you can audit and rotate before expiry.<sup>[1]</sup><sup>[2]</sup> Where work runs under a derived credential, record the session identifier beside the human identity. A question about one action then leads to one session, not a busy person.<sup>[6]</sup>

The anti-pattern is the **credential nobody watches**, and it fails silently. Other controls show themselves when they block something. Without monitoring, things look like success.

**ELI5.** A lost key makes no sound. Only a log and a key list tell you.

## How Wrong Answers Are Built on This Material

The wrong options here describe real practices. Each helps with something, so none is obvious nonsense.

- Fixing one measurement only. A key moves into plaintext build settings. A shared credential is rotated on a timetable but stays shared. Both beat the old state and leave the copy set as wide. They win for what to fix first, and lose for the strongest posture.
- Selling the shared credential as a plus. One credential everywhere is easier: one item to keep, one to swap. That ease is the flaw. Ask what one replacement costs and how many environments one compromise crosses.
- Acting after the value has left. Removing the committed value, limiting which networks may use the key and stricter review shrink no copies already made and shorten no stolen copy's life.
- Treating a verified identity as permission. A caller with a good token gets all it holds elsewhere. Verification says who is asking, not what is allowed.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Credential handling is reviewed across several environments | Move every measurement: split, narrow scopes, central storage, rotate on schedule and on suspicion | Calling one practice enough, or praising a single credential for simplicity |
| A credential sits in a tracked config file | Count it as exposed, replace it, and put a reference where the value was | Typing over it in a later change, as if history forgot |
| One key covers development, staging and production | Separate credentials per environment and per service | Rotating the shared key more often, or accepting the crossover as a fair trade |
| Several services need keys; where should they live? | A managed store, or config outside source control, loaded at runtime | A handy spot with a permanent copy nobody can revoke |
| A request shows up with a signed session token | Check signature, issuer and audience, then allow only what that session needs | Giving the session the named user's standing access |
| Someone asks if a credential was misused | Records: who read the value, which session acted, the key inventory | Assuming the platform would have raised it |

One habit works on any option. Name the measurement it moves and the one it leaves. The best answer usually needs all three.

**ELI5.** Tricky answers fix one thing. Pick the one that covers all three.

## What to Remember

- A credential is a copy set: the places its value came to rest plus the access each carries. Damage depends on count of copies, reach of one, and life before it stops working.
- A secret committed to a tracked file enters history, and a later overwrite changes only the current version. Treat any inline credential as exposed and replace it, since every clone taken before the repair keeps it.
- Configuration holds a reference, never a value. An environment variable fits one process for one run. A managed store fits several consumers, or auditing, because it gathers scattered copies into one and records who read it.
- Isolation needs distinct credentials per environment and per service. A shared key is a path between environments kept apart on purpose, so replacing it is an outage everywhere.
- Rotation is the only repair after exposure, since a leaked value cannot be made secret again. Rotate on a schedule to bound an undetected leak and at once on suspicion. Writing the replacement back into the file it leaked from recreates the problem. Expiry bounds a leaked credential's usable life and replaces neither storage nor rotation.
- A key's workspace, expiration and any scopes are set at creation and change only by issuing another key. So approval belongs at issue time. Console Admin API keys have no selectable scopes and full access to every endpoint that takes them, which makes issuing one the whole authorisation decision.
- Federation removes the durable secret instead of shortening its life. A workload swaps a provider-issued identity token for a short-lived access token, so nothing static is minted, distributed or rotated. It is as strong as the identity provider's configuration.
- Verified identity is authentication, not authorisation. A signed session token shows who created the session, not which process presented it. Verify signature, issuer and audience. Scope derived credentials to that session's task, with life bounded by the token's expiry.
- Use of a credential is visible only if somebody recorded it. The platform can detect anomalous usage but cannot know a key was compromised. Read logs, key inventories and session identifiers turn assumed access into evidence.

**ELI5.** Count spares, shrink what each opens, make each expire. Keep a log.

## Endnotes for this chapter

1. The Claude Console displays a new API key's full value only once, at creation, and a lost key cannot be viewed again, so a replacement must be created; a key can be scoped to a workspace and given an expiration at creation, and the recommended storage is a secrets manager. The Admin API includes endpoints for managing an organization's API keys programmatically, which require a separate Admin API key and never return a key's secret value, only a partially redacted hint. Anthropic, *Get your Claude API key* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/get-api-key](https://platform.claude.com/docs/en/get-api-key)

2. API keys are static secrets passed on every request, and Anthropic directs that they be stored in a secrets manager, rotated periodically, and revoked whenever a key is suspected of having leaked. Expiration is chosen at key creation from a preset, a custom duration, or Never, and cannot be changed afterwards; after a key expires, requests return a `401` authentication error and expired keys cannot be reactivated; the Admin API reports each key's `expires_at` so keys can be audited and rotated before expiry; and expiration limits the lifetime of a leaked credential but is not a substitute for secret hygiene. Workload Identity Federation lets a workload exchange a short-lived identity token issued by a trusted identity provider for a short-lived Claude API access token, so there is no static key string to mint, distribute or rotate; federation shrinks the blast radius of a leaked credential but does not on its own guarantee end-to-end security, because the trust chain is only as strong as the identity provider's configuration and a long-lived secret one hop upstream can still undermine it. Anthropic, *Authentication* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/manage-claude/authentication](https://platform.claude.com/docs/en/manage-claude/authentication)

3. Only organization members with the admin role can create Admin API keys; Claude Console Admin API keys do not have selectable scopes and every such key carries full access to all endpoints that accept Admin API keys; a key created in one organization cannot be used to manage a different organization; where scopes are selectable they are fixed at creation, and adding a scope later requires creating a new key; and the full secret is displayed only once and should be stored in a secrets manager. Anthropic, *Create an Admin API key* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/manage-claude/admin-api-keys](https://platform.claude.com/docs/en/manage-claude/admin-api-keys)

4. A security boundary separates components with different trust levels, and sensitive resources such as credentials can be placed outside the boundary containing the agent; the recommended approach is a proxy running outside that boundary which injects credentials into outgoing requests, so the agent never sees the actual credentials and credentials are stored in one secure location rather than distributed to each agent. Anthropic, *Securely deploying AI agents* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/agent-sdk/secure-deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

5. The environment service key must be stored in a secrets manager rather than in environment files or sandbox images, and rotated immediately if exposure is suspected; the key is scoped to one environment's work queue, so provisioning a separate workspace and environment per trust boundary limits each key to a single user's sessions instead of a shared pool; Anthropic can detect anomalous usage patterns but cannot know that a customer's key was compromised, so a suspected leak must be revoked and replaced by the customer; and revocation is validated on every request, so it takes effect on the worker's next call. Anthropic, *Security model* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security)

6. A valid session token proves that Anthropic issued it for a specific session in a specific environment and how the session was created, and deliberately does not prove which process on the runner host presents it, since the token sits in an environment variable that any code Claude runs and any tool or MCP server the session starts can read and present. Services must verify the signature against Anthropic's published key set, reject tokens whose algorithm header is not the expected one, and verify the audience claim against their own environment identifier to reject tokens issued to another organization's environment. Verification is offline, so a token that verifies stays valid until its expiry whatever has happened to the session since, and Anthropic does not publish a revocation feed for session tokens. Credentials derived from the token should be limited to what one coding session should reach rather than everything the creating user holds, bounded in lifetime to the token's expiry or shorter, and audited by recording the session identifier and token identifier alongside the user identity. Anthropic, *Verify session identity in self-hosted environments* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/self-hosted-environments-identity](https://code.claude.com/docs/en/self-hosted-environments-identity)

7. Vault credentials of the environment-variable category are keyed by the environment variable name and stored in the sandbox as an opaque placeholder; when the agent initiates an outbound request the placeholder is substituted with the real secret at egress, and the agent never sees the secret value. Anthropic, *Authenticate with vaults* (Claude Platform Docs, accessed 2026-09-10), [https://platform.claude.com/docs/en/managed-agents/vaults](https://platform.claude.com/docs/en/managed-agents/vaults)

8. `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips Anthropic and cloud provider credentials from subprocess environments including the Bash tool, hooks and MCP stdio servers, so the parent Claude process keeps those credentials for its API calls while child processes cannot read them, reducing exposure to prompt injection attempting to exfiltrate secrets through shell expansion. Anthropic, *Environment variables* (Claude Code Docs, accessed 2026-09-10), [https://code.claude.com/docs/en/env-vars](https://code.claude.com/docs/en/env-vars)
