# Chapter 1: What This Exam Tests That an Interview Does Not

**Summary**: *In an interview, you show you can build something. On this exam, you show you can choose the right tool. The wrong answers are real tools that suit some other problem, so you cannot just skim them. This chapter uses the smallest ideas in the syllabus: what a token is, what the window is, why the same request can come back different, and which dial controls what. Hold those four straight and many later questions get easy.*

One picture runs through the chapter. A request is an order handed to a cook. The cook works one scoop at a time, and the counter is only so big.

## The Same Request Twice Returns Two Different Answers, and Nothing Is Broken

Order the same dish twice, with the ticket byte for byte identical. The plates come out slightly different. A model does the same. The two responses often use different words. Sometimes the structure differs. Now and then one adds a caveat the other skips.

Most people open a ticket. They suspect a stray timestamp, a redeployed config, or two code versions behind a load balancer. Usually nothing changed. The model writes one token at a time, and it samples each choice. It does not look the answer up. So two runs can split at any step and stay split. Anthropic states it directly: identical inputs can produce different outputs even with temperature set to 0, on its own inference service and on third-party providers.<sup>[1]</sup> Temperature 0 does not turn the cook into a machine. It narrows the choices. It does not cut them to one.

A person hardly notices. A parser does, and so does any step that expected a field and got a sentence.

Here the exam leaves the interview behind. In an interview, "it varies, that is expected" ends the talk. Here, a scenario shows the variation, adds a believable defect, and asks what you tell the teammate. The scored answer names the mechanism, then says what the application does about it. Stopping at "that is expected" fixes nothing.

The application can validate the output, retry on failure, and use sampling settings when consistency matters more than variety. None of that makes the cook repeat a plate. It makes the restaurant cope when the plate changes.

Remember the shape: a fact about the technology, then the part of your system that absorbs it. Only the first half just describes the world. Only the second treats a permanent property as a bug.

**ELI5.** Ask a cook for the same soup twice. It tastes close, never identical. You do not scold the cook. You taste each bowl before it leaves the kitchen.

## A Token Is the Unit You Are Billed In, Limited By, and Debugging Against

A **token** is the smallest piece the model handles, like one scoop. It can be a word, part of a word, a character or a byte. It is not one word each. For Claude it is roughly 3.5 English characters, and that shifts with the language.<sup>[2]</sup>

Three things in the syllabus are counted in tokens. Miss that and they look like three topics.

| What is counted in tokens | Where it bites |
|---|---|
| What you send, every request | Your bill, and the room left in the window |
| What the model writes back | The bill at another rate, plus the output cap |
| What the model spends thinking first | A third charge, for work nobody reads |

The third row surprises people. It is why the effort setting exists.

**ELI5.** A token is one scoop of flour. The cook charges per scoop, and the kitchen caps the scoops. Even silent thinking uses scoops.

## The Window Is Capacity, and Temperature Is Selection

The **context window** is the counter. It limits what one request can carry. It is finite and acts as working memory, not storage. As it fills, accuracy and recall slip. Anthropic names this **context rot**.<sup>[3]</sup>

Here is a mix-up that keeps coming back, usually from a confident colleague. A transcript will not fit, and the colleague says to raise the temperature. That points at the wrong part. Temperature is how daring the cook is when choosing. It says nothing about counter size. Turn it up or down and the failure just reads differently.

| Dial | What it changes | What it cannot change |
|---|---|---|
| Temperature and sampling settings | Which token wins among the candidates | Input size, and cost |
| Context window | How much one request can hold and cross-check | How varied or repeatable the wording is |
| `max_tokens` | How long the response can run | Input size |
| Effort | Tokens spent reasoning before the answer | Input size |

These are four separate machines on one ticket. Mixing up capacity and selection is the named anti-pattern, and it fails in reverse too: trimming input does not fix inconsistent wording.

Say a scenario needs a long document kept whole, so a reference in section nine resolves against section two. Both sections must sit on the counter in the same request. That is capacity. No sampling setting, speed gain or output cap touches it.

**ELI5.** The counter is how much food the cook can lay out. The cook's mood is how daring the choices are. A bolder mood does not grow the counter.

## Reasoning Depth Is a Separate Setting From Model Choice

New developers often assume one dial says "how good do you want it", and that it is the model name. There are really three independent settings, and scenarios pull them apart on purpose.

The model sets the capability tier: which cook you hire. **Thinking** decides whether the model reasons in view before answering. **Adaptive thinking** lets it judge how much reasoning a request deserves. **Effort** sets how many tokens Claude spends responding, trading thoroughness for token savings on one model. It works on all supported models with no beta header.<sup>[4]</sup> **Fast mode** is another thing entirely. It gives up to 2.5 times higher output tokens per second on supported Opus models, at premium pricing.<sup>[5]</sup> That is a faster stove, not a better cook.

Two are quality dials, one is a speed dial, and they are priced differently.

| Setting | Buys you | Costs you |
|---|---|---|
| A larger model | Skill on harder work | More money per token, often more delay |
| Thinking, or adaptive thinking | Reasoning first, where the work needs it | Tokens the user never sees |
| Effort | A say in how much of that reasoning happens | Thoroughness, if you turn it down |
| Fast mode | More output tokens per second | Premium pricing, supported models only |

A mechanical trap sits underneath. Toggling thinking modes invalidates prompt caching.<sup>[6]</sup> Say a team pays to reuse a large stable prefix, then turns thinking on for some requests. The reuse is quietly gone.

**ELI5.** Hire a better cook, give the cook more thinking time, or buy a faster stove. These are separate choices. A faster stove does not make the cook smarter.

## Three Prompting Modes, Priced in Tokens

The last foundation is the cheapest technique in the book. People skip it because it seems too plain.

**Zero-shot** gives the task and no examples. **One-shot** gives one worked example. **Multi-shot** gives several. Each step up spends more tokens for closer adherence. A description states a rule and leaves its edges open. An example shows an edge already settled. Say the prose keeps getting capitalisation wrong. One settled case can fix what another paragraph of rules did not. The cost comes back every time, since the examples ride with each request.<sup>[7]</sup> It is a photo of the finished dish clipped to every ticket.

Watch for this. A team holds a few labelled examples of the output it wants. The options: put them in the prompt, store them in a database, train a custom model, or warn users off the hard cases. Putting them in the prompt is the shortest route, and nothing has to be built first.

Training a custom model on a few labelled cases looks like rigour. It is the same information sent down a pricier road, with a deployment to maintain.

**ELI5.** Want a dish plated a certain way? Show the cook a photo. Three photos help more. Sending the cook to a new school is a lot of work for the same photos.

## How Wrong Answers Are Built on This Material

Wrong answers are rarely silly. They name tools that work and get used weekly. One hidden assumption sinks each one. Three are worth memorising.

- A sampling setting offered for a capacity problem. Temperature, `max_tokens` and sampling shape how the response is made. None changes how much input fits. If material does not fit, any option naming a sampling parameter is wrong on mechanism, not on degree.
- Normal behaviour called a defect. Wording that drifts between runs of an unchanged request is just how generation works. An option that confirms a bug, files a ticket, or pins something to stop it accepts a false premise. The flip side counts too. An option that explains the mechanism and stops has not answered a question about what to do.
- A heavy tool picked over the one the material already fits. Training, retrieval infrastructure and separate apps show up as answers to problems a few prompt examples would settle. Cost is the clue. Ask what must be built before anyone can try the option.

Match on what the scenario is doing, not the industry around it.

| When the scenario says | The answer is usually | The trap is usually |
|---|---|---|
| Identical requests return differently worded responses | Name sampling, then say how the app validates, retries or constrains | Blaming request construction, or the model version |
| A document is too long, or references across it are lost | Capacity: one request, or split and carry state on purpose | A sampling parameter, faster responses, or a bigger output cap |
| A small set of labelled examples of the wanted output exists | Put them in the prompt | Training a custom model, or storing them where the model never reads |
| Quality is uneven on work that needs reasoning | Thinking or effort, weighed against what tokens buy | A larger model as the only quality dial |
| Speed is the stated problem and quality is fine | The speed mechanism, priced accordingly | Anything that changes what the model writes, not how fast |
| A stable prefix is reused across many requests | Keep the conditions the reuse needs | Toggling a setting that silently breaks it |

One habit beats the table. When two options look fine, ask which mechanism each acts on, then check which one the scenario named. The wrong option usually acts on a real mechanism the scenario never mentioned.

**ELI5.** Wrong answers are real kitchen tools on the wrong job. A whisk is great, but it will not enlarge the counter.

## What to Remember

- A token is the unit of billing, of the window, and of reasoning spend. In Claude it is about 3.5 English characters. Input, output and thinking all count, at different rates.
- Sampling picks each token, so one request run twice can differ, even at temperature 0. That is how generation works, not a flaw in the request.
- Temperature selects. The window holds. Neither fixes the other's problem.
- The window is working memory, not storage. Recall drops as it fills, which Anthropic calls context rot. Anything cross-referenced goes in the same request.
- Model, thinking and effort are three independent settings. Fast mode is speed, bought at premium pricing, not capability.
- Toggling thinking modes invalidates prompt caching.
- Zero-shot, one-shot and multi-shot trade tokens for adherence. If a team holds labelled examples, showing them to the model is the cheapest fit. Reaching past that is the standard wrong answer.

**ELI5.** The cook varies a little each time. The counter is only so big. Hiring, thinking time and stove speed are separate choices. When unsure, show the cook a photo before building a new kitchen.

## Endnotes for this chapter

1. Identical inputs can produce different outputs even with temperature set to 0, on Anthropic's own inference service and on third-party providers. Anthropic, *Glossary* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/glossary](https://platform.claude.com/docs/en/about-claude/glossary)

2. Tokens are the smallest individual units of a language model and can correspond to words, subwords, characters or bytes; for Claude a token approximately represents 3.5 English characters, varying by language. Anthropic, *Glossary* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/about-claude/glossary](https://platform.claude.com/docs/en/about-claude/glossary)

3. The context window functions as working memory rather than storage, and accuracy and recall degrade as the token count grows, a phenomenon Anthropic names context rot. Anthropic, *Context windows* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/context-windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)

4. The effort parameter controls how many tokens Claude spends when responding, trading response thoroughness against token efficiency on a single model, and is available on all supported models with no beta header required. Anthropic, *Effort* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/effort](https://platform.claude.com/docs/en/build-with-claude/effort)

5. Fast mode delivers up to 2.5 times higher output tokens per second from supported Claude Opus models, at premium pricing. Anthropic, *Fast mode* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/fast-mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode)

6. Toggling thinking modes invalidates prompt caching. Anthropic, *Thinking* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)

7. Prompting techniques including the use of worked examples are documented as a means of improving adherence to a required output shape. Anthropic, *Prompt engineering overview* (Claude Platform Docs, accessed 2026-09-09), [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
