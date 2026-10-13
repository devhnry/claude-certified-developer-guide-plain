# Chapter 10: One Server, Many Clients, Transport by Locality

**Summary**: *One capability, four teams, and a vendor interface that changes when it likes. Wire that integration into each application and the same repair happens four times, late, in four codebases. A server (the shared shop) is the alternative: one implementation, several callers, released on a schedule of its own. This chapter covers four things. First, what a server exposes and who decides to use each part. Second, why transport (how the two sides talk) is settled by where the server runs. Third, which configuration scope shares a server and which keeps it private. Fourth, what changes when callers differ in privilege.*

## Four Applications, One Interface, and Four Copies of Every Breaking Change

**First, the idea.** When several applications need the same capability, you can build it once in a shared place instead of four times. Think of a **shop**. The shop is the **server** (a separately running process). Each application is a branch that sends someone to the shop's counter. That someone is the **client** (the part of an application that connects to a server).

**The problem.** Take an internal **analytics platform**. **Four applications** want to use it: a support assistant, a reporting agent, a developer tool, and something an external contractor uses. Each team **writes its own** schema, its own authentication and its own error handling. That is **four descriptions of one operation**. It is like four branches each building their own copy of the shop's service.

Then the platform ships a **breaking change** on a **release schedule** none of the four controls. That means **four repairs**, found at four different times.

**The fix.** That is the argument for a server. It is about **reuse rather than capability**. **Model Context Protocol** (MCP, the shared rulebook for how clients and servers talk) lifts the **tool definition** out of any single application. It puts it in a **separately running process** (the shop) that clients connect to.<sup>[1]</sup> **Build the operation once**. Every client you connect gets it.

**Where is the line?** The point where this starts to pay off has a name. The **reuse boundary** is where a capability **stops belonging** to one application and becomes a **separately released artifact** (a shop with its own opening hours) that several applications call. Two facts push a capability over it:
- **more than one consumer** (more than one branch)
- an interface that **moves independently** of all of them

With one consumer and a stable interface, the tool you wire directly **stays cheaper**. That is like a branch making the thing in its own back room. Chapter 11 covers that choice.

**ELI5.** Four shops each wanted the same machine. Instead of building four machines, you build one machine in a shared building. When it breaks or gets an upgrade, you fix it once. But if only one shop wants it, just keep it in that shop.

## Three Primitives, Separated by Who Decides to Use Them

**First, the idea.** A server can offer three kinds of things. They are called **primitives**. What separates them is not what they hold. It is **who decides to use them**.

A server **exposes tools, resources and prompts**. Accounts of them describe what each contains, which is the least useful thing about them. What decides which you reach for is **who initiates** (who starts the request).

In the shop, the three look like this:
- a **tool** is a service the shop does when someone asks, such as "run this report"
- a **resource** is a good on the shelf. The branch manager (the **host**, the application that runs the client) picks it up and puts it on the desk before work starts
- a **prompt** is a printed order form that a customer (a **person**) picks on purpose

| Primitive | Who initiates | What it holds | Reach for it when |
|---|---|---|---|
| Tool | The model, from the request and its context | An action with a schema, invoked, returning a result | The operation has to be chosen at runtime by whatever the work needs |
| Resource | The host application, which assembles context | Read-only data addressed by a URI | Known data belongs in context from the start of the turn |
| Prompt | A person, selecting it deliberately | A vetted instruction template, usually surfaced as a command | Exact wording beats whatever a human would type |

**In plain words:**
- Tools are **model-controlled**. The model invokes them on its **own reading** of the situation.<sup>[2]</sup>
- Resources are **application-driven**. The **host decides** how to bring them in.<sup>[3]</sup>
- Prompts are **user-controlled**. They are exposed so **somebody selects** one explicitly.<sup>[4]</sup>

**What a wrong choice costs.** Each **wrong choice costs** something specific.
- **Data published** as a tool spends a **round trip** (a trip to the shop and back) fetching what was never in doubt.
- **Wording published** as a tool leaves the **model deciding** whether to apply the phrasing. That phrasing was the whole point of packaging it.

**ELI5.** The shop has three kinds of things. Some are services Claude asks for when it needs them. Some are goods on a shelf that the manager hands over at the start. Some are order forms a person picks on purpose. Who picks tells you which kind it is.

## Transport Is Decided by Where the Server Runs, Not by Preference

**First, the idea.** **Transport** is the way the client and the server send messages to each other. The protocol offers two, and you choose by **where the server runs** compared with the client.

**The two standard transports.**<sup>[5]</sup> In shop terms, one is a walkie-talkie between two people in the same room. The other is a phone line to a shop across town.
- **stdio** (the walkie-talkie). The client starts the server as a **child process** (a program it launches itself). The two speak over that process's own **standard input and output**. It uses one JSON-RPC **message per line**. Standard error is free for logging. Nothing but valid messages is allowed on standard output.
- **Streamable HTTP** (the phone line). The server gives one endpoint path that answers both **POST and GET**.

**The rule: process locality decides.** The fact you need is where your **server runs** relative to its client. A child process already has its **pipes** (the walkie-talkie is built in). A deployment **shared by many users**, on a machine none of them own, is what a **network protocol** is for.

**Two anti-patterns.** Both sound like consistency.
- A **listening port on every workstation** gives a purely local tool a network surface nobody needed.
- A **subprocess per user of a shared deployment** fails the other way. It **multiplies server processes** with users. It gives up the single deployment that was the reason to build a server.

**Transport is chosen per deployment.** The protocol does not fix it. So one server can run over pipes locally and be **hosted over HTTP** for the shared case. A third shape **skips the process boundary**. The server is defined in your own application code and runs in-process.<sup>[6]</sup>

**How configuration shows it.** Configuration follows the same fact:
- An entry **carrying a command** is **stdio by default**.
- An entry carrying a `url` needs an **explicit type** of `http`, `sse` or `ws`.<sup>[7]</sup>

**ELI5.** If the helper sits in the same room, you can just talk through a tube. If the helper works across town for lots of people, you need a phone line. Look at where the helper is, then pick. Do not pick the same one for everything.

## The Host Owns the Client, and a Server Never Sees the Whole Conversation

**First, the idea.** MCP splits the work into three parts: **host, client, server**. In the shop, the branch manager is the host. The person sent to the counter is the client. The shop is the server.

**How the parts fit.**<sup>[1]</sup>
- The **host** application creates and manages client instances.
- Each **client** talks to **exactly one server**.
- The host **enforces the boundaries** between them.

**What this means for you as a server author.** Three consequences bind an author. A server:
- receives only what is sent to it
- **cannot read the conversation history**
- **cannot see into another server**

So nothing the server does may depend on context it was not passed. The composability that lets several servers combine comes out of that **isolation**. It is like the shop only knowing what the person at the counter tells it.

**Who writes what.** You **write the server**. You **rarely write the client**. Claude Code ships one. The **MCP connector** reaches a remote server straight from the Messages API with no separate client process.<sup>[8]</sup>

**ELI5.** The manager sends one person to each shop. The shop only knows what that person says. It cannot read the manager's notes or peek into the shop next door. So always tell the shop everything it needs.

## Configuration Scope Answers Who Loads the Server, Never What It Does

**First, the idea.** A **scope** says who gets a server's setup. It never changes what the server does. In shop terms, it is the list of branches that have the shop's phone number.

**The scopes.** Claude Code writes a definition at one of **three scopes**, with a fourth **deployed administratively**.<sup>[9]</sup>

| Scope | Where the definition lands | Who gets the server |
|---|---|---|
| `local` | `~/.claude.json`, under this project's entry. The default | One person, one project |
| `project` | `.mcp.json` at the repository root | Everyone who clones the repository |
| `user` | `~/.claude.json`, at the top level | One person, every project |
| Managed | An administered file deployed to the machine | Everyone in the organisation, with no individual setup |

**How to choose.** **Scope follows who needs the thing**.
- A dependency your team shares belongs in **version control** (the shared history of the code), reviewed and versioned with the code.
- A **personal experiment** stays personal.
- **Setup instructions in a README** is the anti-pattern that keeps winning arguments it should lose. It is unreviewable, unversioned and undistributable. It also splits apart the first time somebody reads step four differently.

**Four mechanics matter.**
- **Scope is fixed** when a server is added. So changing it means **removing the entry** and adding it again.
- Where one name is defined at more than one scope, the **highest-precedence definition** is **used whole**. There is **no merging across scopes**.<sup>[9]</sup>
- The first time Claude Code meets a project-scoped server it **asks for approval**. So a repository you cloned cannot start a process **without consent**.<sup>[10]</sup>
- A project-scoped stdio server runs from each **teammate's machine**. So every clone needs the **runtime installed** (the program that runs the server).

Chapter 22 owns credentials. One warning from it fits here: **commit history** keeps an **inline secret** long after the file stops carrying it.

**ELI5.** Some phone numbers are in your own notebook. Some are on the team's shared list that everyone gets. Some are given out by the boss. The list decides who can call the shop. It does not change what the shop does.

## A Server Reached by Callers of Differing Privilege Is a Trust Boundary

**First, the idea.** A **trust boundary** is a line where you can no longer assume the other side is friendly. Once a server is **genuinely shared**, your callers **stop being uniform**. In the shop, some customers are staff and some are outside visitors.

**The problem.** One of those four teams is contractors. Three decisions survive that. Each has a comfortable alternative that holds only while **every caller is honest**.

**1. Authenticate and authorise at the server boundary.** Work out who the caller is. Do not treat connected clients as equally privileged.
- An **identity the caller supplies** is an **assertion** (a claim) rather than a verification (a check).
- The specification puts the credential version as a prohibition. A **server must not accept a token** that was not issued for it. A server **forwarding unvalidated tokens** is a proxy an attacker can point at whatever sits behind it.<sup>[11]</sup>

**2. Choose tool granularity deliberately.**
- A small set of **purpose-scoped operations** can be **authorised one at a time**, per caller.
- A **thin passthrough to every underlying endpoint** cannot be authorised that way. Neither can one tool accepting an arbitrary query.
- That last one reads as flexibility. It is really **blast radius** (how much damage one mistake or attacker can do). A tool able to express any statement offers nothing to authorise separately.

**3. Return errors as structured results.** The model must be able to reason about them. They carry **no stack traces** and **no connection strings**. Chapter 9 made the general case for actionable errors. What is added here is that whoever reads this one sits **outside the team** that wrote it.

**Nobody does this for you.** **Nobody audits** any of this on an organisation's behalf. Anthropic **does not security-audit** the servers it lists. So an organisation needing a **fixed set** deploys one administratively.<sup>[12]</sup>

**ELI5.** When only your friends use the shop, you can trust them. When strangers can walk in, the shop must check who each person is. It should also offer small, specific services, not "do anything you like". And if something goes wrong, it should not hand over its secrets in the error message.

## How Wrong Answers Are Built on This Material

**First, the idea.** Wrong answers here describe **real engineering**: one transport standardised on, a server scoped to the team that asked first, a configuration **kept personal**. **Four assumptions** turn those into the **wrong answer**.

**The four wrong assumptions:**
- **One mechanism asserted to win everywhere**. Examples are "Prefer the **network transport**", "run it locally" and "support both". A **universal preference** has **ignored** the **deployment fact** the scenario supplied.
- A **design that holds only while callers are honest**. Examples are an **asserted identity accepted**, a **general query interface**, or internal detail in an error. The cue is any stated **difference in privilege** between consumers.
- The **interface scoped to the first consumer**. Examples are **building against one application** and extending on request, or deploying only to **developer machines**. Both **restore the coupling** a server exists to remove.
- **Scope chosen by convenience rather than by audience**. Examples are **personal configuration** for a shared dependency, or **manual steps** standing in for a committed file.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Several applications need one capability, released separately | One server, its interface defined independently of any consumer, hosted where all reach it | Per-application integration, or an interface built for the first consumer |
| A server is started as a local child process on one machine | Standard input and output | A network transport, a listening port, or running both |
| One server serves workstations and a shared hosted application | A transport per deployment: pipes locally, a network protocol for the shared case | One transport imposed on both, or a subprocess per user |
| Data is known in advance and needed at the start of the turn | A resource, addressed and fetched into context | A tool call spent retrieving what was never in doubt |
| Every teammate needs the same server after cloning | Project scope, committed to version control | Personal scope, or setup steps in a README |
| Consumers include somebody outside the team | Authenticate at the boundary, scope tools narrowly, keep internals out of errors | Trusting the connection, or a general query tool called flexible |

**A habit that works past the table.** One habit transfers past the table. Name the **deployment facts** the scenario stated: **how many consumers**, **where each runs**, how their **privileges differ**. Then check whether the option in front of you used them.

**ELI5.** Wrong answers pick one favourite way and use it everywhere, trust everyone, or build only for the first customer. Instead, read what the question tells you about who uses the shop and where. Then pick the answer that fits those facts.

## What to Remember

- A **server earns its place** on two facts: **more than one consumer**, and an **interface moving independently** of all of them. One consumer and a **stable interface** make a **directly wired tool cheaper**.
- **Tools, resources and prompts** differ by **who initiates**. The **model invokes a tool**. The **host application places a resource** (read-only data addressed by a URI) into context. A **person selects a prompt**, a **vetted instruction template** usually surfaced as a command.
- **Process locality decides transport**. A server started as a **child process** speaks over **standard input and output**, one JSON-RPC **message per line**. A **deployment shared** by many users needs a **network protocol**. Transport is **chosen per deployment**.
- The **host creates one client per server** and **enforces the boundaries** between them. So a server **never reads the conversation history** and never sees into another server.
- Configuration **scope names who loads a server**, nothing else. **`local`** is **private to one project**. **`project`** lives in a **committed `.mcp.json`** reaching everyone who clones. **`user`** is private **across every project**. Scope is **fixed at the moment** a server is added.
- A **shared server is a trust boundary**. **Resolve the caller's identity** there, because a **supplied identity** is an assertion. **Scope tools to named operations**, because one tool expressing any query offers **nothing to authorise** separately.

**ELI5.** Build one shared shop only when many branches need it and it keeps changing. Pick the walkie-talkie or the phone line by where the shop is. Put the team's phone list where everyone gets it. And when strangers can call, check who they are.

## Endnotes for this chapter

1. MCP follows a client-host-server architecture in which the host process creates and manages client instances, each client communicates with exactly one server, and the host enforces security policies and boundaries; servers expose resources, tools and prompts, operate independently with focused responsibilities, and may be local processes or remote services; servers cannot read the whole conversation nor see into other servers, with full conversation history staying with the host. Model Context Protocol, *Architecture* (accessed 2026-09-09), [https://modelcontextprotocol.io/specification/draft/architecture](https://modelcontextprotocol.io/specification/draft/architecture)

2. Tools in MCP are designed to be model-controlled, meaning the language model can discover and invoke them automatically based on its contextual understanding and the user's prompts. Model Context Protocol, *Tools* (accessed 2026-09-09), [https://modelcontextprotocol.io/specification/draft/server/tools](https://modelcontextprotocol.io/specification/draft/server/tools)

3. Resources allow servers to share data providing context to language models, such as files, database schemas or application-specific information, each uniquely identified by a URI; they are application-driven, with host applications determining how to incorporate context, whether through explicit selection in a UI element, user search and filtering, or automatic inclusion. Model Context Protocol, *Resources* (accessed 2026-09-09), [https://modelcontextprotocol.io/specification/draft/server/resources](https://modelcontextprotocol.io/specification/draft/server/resources)

4. Prompts allow servers to expose prompt templates providing structured messages and instructions; they are user-controlled, exposed with the intention that the user explicitly selects them, and are typically triggered through user-initiated commands in the interface such as slash commands. Model Context Protocol, *Prompts* (accessed 2026-09-09), [https://modelcontextprotocol.io/specification/draft/server/prompts](https://modelcontextprotocol.io/specification/draft/server/prompts)

5. The protocol defines two standard transport mechanisms: stdio, in which the client launches the MCP server as a subprocess, the server reads JSON-RPC messages from standard input and sends them to standard output, messages are delimited by newlines, the server may write UTF-8 strings to standard error for logging, and the server must not write anything to standard output that is not a valid MCP message; and Streamable HTTP, in which the server provides a single HTTP endpoint path supporting both POST and GET. Model Context Protocol, *Transports* (accessed 2026-09-09), [https://modelcontextprotocol.io/specification/latest/basic/transports](https://modelcontextprotocol.io/specification/latest/basic/transports)

6. Transport guidance for the Agent SDK: a server documented with a command to run uses stdio, a server documented with a URL uses HTTP or SSE, and tools built in the application's own code use an SDK MCP server that runs in-process rather than as a separate server process. Anthropic, *Connect to external tools with MCP* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/agent-sdk/mcp](https://code.claude.com/docs/en/agent-sdk/mcp)

7. A JSON entry with a `url` but no `type` is a configuration error, because Claude Code reads an entry with no `type` as a stdio server; it skips that server and reports that a `type` of `http`, `sse` or `ws` must be added. The `type` field also accepts `streamable-http` as an alias for `http`, the name the MCP specification uses for that transport, so configurations copied from a server's documentation work without modification. Anthropic, *Connect Claude Code to tools via MCP* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)

8. The MCP connector enables connecting to remote MCP servers directly from the Messages API without a separate MCP client. Anthropic, *MCP connector* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/agents-and-tools/mcp-connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)

9. MCP servers are configured at three scopes controlling which projects a server loads in and whether the configuration is shared: local scope is the default, stored in `~/.claude.json` under the project's path and private to one project; project scope stores the configuration in a `.mcp.json` file at the project root, checked into version control so the team gets the same servers; user scope is stored in `~/.claude.json` and is available across all projects while remaining private. Administrators can additionally deploy servers at the enterprise level through managed configuration. When the same server is defined in more than one place, the definition from the highest-precedence source is used in its entirety and fields are not merged across scopes. Anthropic, *Connect Claude Code to tools via MCP* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)

10. A server's scope is fixed when it is added, so changing scope means removing the entry and re-adding it at the new one; a local stdio server is a program Claude Code starts as a subprocess on the machine, registered with the command to run, while an HTTP server is registered with a URL; and the first time Claude Code sees a project-scoped server it asks for approval, a prompt that exists so a cloned repository cannot launch processes on the machine without consent. Anthropic, *Connect to MCP servers* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/mcp-quickstart](https://code.claude.com/docs/en/mcp-quickstart)

11. MCP servers must not accept any tokens that were not explicitly issued for the MCP server; a server that passes tokens through without validating their claims, including audience, lets an actor holding a stolen token use the server as a proxy for data exfiltration, and bypasses controls such as rate limiting, request validation and traffic monitoring that depend on the token audience. Model Context Protocol, *Security Best Practices* (accessed 2026-09-09), [https://modelcontextprotocol.io/specification/draft/basic/security_best_practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)

12. By default anyone running Claude Code can connect any MCP server they choose; Anthropic reviews connectors against its listing criteria before adding them to its directory but does not security-audit or manage any MCP server, and an administrator can restrict which servers run in the organisation, from deploying a fixed approved set through a managed configuration file to disabling MCP entirely, or filtering what users configure with allowlists and denylists. Anthropic, *Control MCP server access for your organization* (Claude Code Docs, accessed 2026-09-09), [https://code.claude.com/docs/en/managed-mcp](https://code.claude.com/docs/en/managed-mcp)
