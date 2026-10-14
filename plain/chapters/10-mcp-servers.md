# Chapter 10: One Server, Many Clients, Transport by Locality

**Summary**: *Four teams need one capability, and the vendor's interface keeps changing. If each team builds its own link, every change costs four fixes in four repos. A server is built once, called by several apps, and released on its own timeline. This chapter covers what a server offers, why its location picks the transport, which scope shares it, and what changes when callers differ in privilege.*

## Four Applications, One Interface, and Four Copies of Every Breaking Change

An internal **analytics platform** has four users: a support assistant, a reporting agent, a developer tool and a contractor's tool. Each writes its own schema, login and error handling.

Then the platform makes a **breaking change**. Each team finds out separately and patches alone.

Our analogy is a factory tool room. One room stores the drill and teams borrow it. The room is the server. The teams are the clients.

A server is about reuse, not extra power. **Model Context Protocol** (MCP) lifts the tool definition out of one app. It lives in its own running process, and clients connect to it.<sup>[1]</sup> Build the operation once and each client gets it.

The **reuse boundary** is where a capability stops being one app's code and is released separately. Two facts carry it across: more than one consumer, and an interface that changes independently. With one consumer and a steady interface, a directly wired tool costs less. Chapter 11 covers that choice.

**ELI5.** Four kids each buy scissors, then the design changes. All four must repair theirs. One shared pair is fixed once.

## Three Primitives, Separated by Who Decides to Use Them

A server offers **tools, resources and prompts**. Who starts each one tells them apart.

| Primitive | Who initiates | What it holds | Reach for it when |
|---|---|---|---|
| Tool | The model, judging from the request | A callable action that returns a result | The job picks the operation at runtime |
| Resource | The host application, building the context | Data to read, found by a URI | The data is known and needed at turn start |
| Prompt | A person, choosing on purpose | A tested instruction template, often a command | Exact wording matters more than a human's typing |

In the tool room, a tool is a drill the worker (the model) grabs mid-job. A resource is a binder the foreman (the host) hands over at shift start. A prompt is a work order a person takes off the rack.

Tools are **model-controlled**.<sup>[2]</sup> Resources are **application-driven**: the host chooses how they arrive.<sup>[3]</sup> Prompts are **user-controlled**: somebody selects one.<sup>[4]</sup>

Wrong picks cost something. Data offered as a tool burns a round trip on something never in doubt. Wording offered as a tool lets the model decide whether to use it at all.

**ELI5.** Some things you grab, some a helper hands you, some you pick from a menu. Who picks tells you the kind.

## Transport Is Decided by Where the Server Runs, Not by Preference

The protocol defines two standard **transports**, meaning ways to carry messages.<sup>[5]</sup> With **stdio**, the client launches the server as a child process. They swap JSON-RPC messages over its standard input and output, one per line. Logs go to standard error. Standard output holds only valid messages. **Streamable HTTP** uses one endpoint path for both POST and GET.

Choose by where the server sits relative to its client. A child process already has pipes, like a hatch between two rooms. A shared deployment on a machine no user owns needs a network protocol, like the post between buildings.

Two tidy habits fail. A port on every workstation gives a local tool a network surface it never needed. A subprocess per user of a shared deployment grows with users and drops the single deployment you wanted.

The choice is per deployment. One server can use pipes on a laptop and HTTP when shared. A third option drops the process boundary: the server sits in your own app, in-process.<sup>[6]</sup> Config reflects this. An entry holding a command defaults to stdio. An entry holding a `url` must state its type: `http`, `sse` or `ws`.<sup>[7]</sup>

**ELI5.** A friend next door gets notes through a hatch. A friend across town gets a letter. Where they live picks the method.

## The Host Owns the Client, and a Server Never Sees the Whole Conversation

Roles: host, client, server. The host app makes the clients. Each client speaks to exactly one server. The host keeps the walls up.<sup>[1]</sup>

Picture the factory office sending one runner per tool room. Like a server, a runner knows nothing about other rooms. It cannot read the conversation history or look into a neighbour. So it can never lean on context it was not handed. That isolation lets servers combine.

You build the server, rarely the client. Claude Code ships one. The **MCP connector** also reaches a remote server straight from the Messages API, with no client process.<sup>[8]</sup>

**ELI5.** A runner fetches from one room and knows only what the slip says.

## Configuration Scope Answers Who Loads the Server, Never What It Does

Claude Code stores a definition at one of three scopes. A fourth is rolled out by administrators.<sup>[9]</sup>

| Scope | Where the definition lands | Who gets the server |
|---|---|---|
| `local` | `~/.claude.json`, under this project. The default | You, this project only |
| `project` | `.mcp.json` in the repository root | Anyone who clones the repository |
| `user` | `~/.claude.json`, top level | You, in all projects |
| Managed | A file admins place on the machine | The whole organisation, no individual setup |

Pick by audience. A team server goes in version control, reviewed with the code. A private experiment stays private. README setup steps are the bad habit: nobody reviews them, and people read step four differently.

Four details apply. Scope is locked when you add the server. To change it, delete the entry and add it again. If a name appears at several scopes, the highest-precedence definition wins whole, with no merging.<sup>[9]</sup> Claude Code asks approval the first time it sees a project-scoped server, so a cloned repo cannot launch anything unasked.<sup>[10]</sup> And a project-scoped stdio server runs on each teammate's machine, so everyone needs the runtime. Chapter 22 owns credentials. Git history keeps an inline secret after the file drops it.

**ELI5.** A note on the fridge is read by the household. A note in your pocket is read by you.

## A Server Reached by Callers of Differing Privilege Is a Trust Boundary

On a really shared server, callers are not equal. One of our four teams is the contractors. Three decisions matter. Each has an easy alternative that works only if everyone is honest.

First, **authenticate and authorise** at the server's edge. A stated identity is a claim, not proof. The specification bans one thing outright: a server must not accept a token issued for something else. One that forwards unchecked tokens becomes a relay an attacker points at whatever it guards.<sup>[11]</sup>

Second, set **tool granularity** on purpose. Narrow single-job tools can be permitted caller by caller. A thin wrapper over every endpoint cannot, and neither can one tool that runs any query. That looks flexible but is blast radius. If a tool can say anything, nothing is left to permit separately.

Third, return errors as structured results the model can act on, with no stack traces or connection strings. Chapter 9 argued for actionable errors. Here the reader may be an outsider.

Nobody audits this for you. Anthropic does not security-audit the servers it lists, so an organisation needing a fixed set deploys one administratively.<sup>[12]</sup>

**ELI5.** The clerk checks every badge and lends only what that person may take.

## How Wrong Answers Are Built on This Material

Wrong answers sound like good engineering. Four assumptions break them.

- **One mechanism that wins everywhere.** "Prefer the network," "go local," "do both." It ignores the deployment facts.
- **A design that needs honest callers.** Trusting a stated identity, a free-form query tool, internals in errors. Watch for differing privilege.
- **An interface cut to the first consumer.** Building for one app, or shipping only to developer laptops. Both restore the coupling.
- **Scope picked for ease.** Personal config for a shared dependency, or hand-run steps instead of a committed file.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Many apps need one capability shipped separately | One server, hosted where all reach it | An integration per app, or an interface shaped by the first user |
| A server starts as a local child process | Standard input and output | A network transport, a listening port, or both |
| One server feeds workstations and a shared hosted app | Transport per deployment: pipes locally, network when shared | One transport for both, or a subprocess per user |
| Data is known up front, needed when the turn begins | A resource, loaded into context | A tool call fetching what was never uncertain |
| All teammates need the same server after cloning | Project scope, committed to version control | Personal scope, or README steps |
| Some consumers sit outside the team | Authenticate at the edge, narrow tools, no internals in errors | Trusting the connection, or a general query tool called flexible |

One habit outlasts the table. List the deployment facts: how many consumers, where each runs, how privileges differ. Then see which option used them.

**ELI5.** A wrong answer ignores a clue in the story. Collect the clues first.

## What to Remember

- A server pays off with several consumers and an interface that moves. Otherwise wire the tool directly.
- The model starts a tool. The host loads a resource (read-only data with a URI). A person selects a prompt, a vetted instruction template.
- Location decides transport. A child-process server uses standard input and output, one JSON-RPC message per line. A deployment shared by many users needs a network protocol. Pick per deployment.
- One client per server, with walls enforced by the host. A server never reads the conversation history or sees another server.
- Scope only says who loads a server. `local` is private to one project. `project` sits in a committed `.mcp.json` for everyone who clones. `user` is private across all projects. Scope is fixed when you add it.
- A shared server is a trust boundary. Resolve the caller there, since a supplied identity is a claim. Scope tools to named operations, since a tool that can express any query leaves nothing separate to approve.

**ELI5.** Build one tool room and let everyone borrow. Hatch or post depends on where it is. Check badges at the counter.

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
