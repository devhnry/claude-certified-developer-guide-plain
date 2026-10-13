# Coverage Map

**Summary:** *This map lists every skill on the published blueprint (the exam's official list), how much it is worth, and the chapter that covers it. Use it to find the chapter behind a weak spot, so you don't have to read in order. The blueprint publishes a weight for each skill, not just each domain. That is more detail than most exams give you. Spend an evening looking at the weights before you decide where the rest of your evenings go.*

## Domain 1: Agents and Workflows

**How to read this table:** find a skill, check its weight, then go to the chapter in the last column.

| Skill | Weight | Owned by |
|---|---|---|
| **1.1** Agent Architecture | 4.5% | Chapter 12, *Known Steps Take a Chain; Unknown Ones an Agent* |
| **1.2** Agent Construction with Claude | 5.3% | Chapter 13, *The Loop, the Harness, and What You Stop Owning* |
| **1.3** Agent Patterns and Frameworks | 4.9% | Chapter 12, *Known Steps Take a Chain; Unknown Ones an Agent* |

## Domain 2: Applications and Integration

**How to read this table:** same layout as above. Each skill points to the one chapter that owns it.

| Skill | Weight | Owned by |
|---|---|---|
| **2.1** Understanding Requirements | 3.4% | Chapter 15, *The Constraints Nobody States Decide the Design* |
| **2.2** Systems Life Cycle | 2.8% | Chapter 23, *Deploy Is a Phase Boundary, Not the End* |
| **2.3** Claude API Mechanics | 6.8% | Chapter 3, *Messages, Streaming, Batches: Who Is Waiting Decides* |
| **2.4** Software Engineering Foundations | 7.4% | Chapter 17, *REST, Versioning, Review: the Exam Beyond Claude* |
| **2.5** Claude Application Design | 8.6% | Chapter 16, *Boundaries, Sessions, and Where Instructions Land* |
| **2.6** Configuration Management | 4.1% | Chapter 18, *An Unpinned Version Is an Untracked Change* |

## Domain 3: Claude Code

**How to read this table:** same layout. This domain has just one skill.

| Skill | Weight | Owned by |
|---|---|---|
| **3.1** Claude Code Operation | 3.1% | Chapter 14, *Permission Modes and Where the Human Gate Goes* |

## Domain 4: Eval, Testing, and Debugging

**How to read this table:** same layout. This domain also has just one skill.

| Skill | Weight | Owned by |
|---|---|---|
| **4.1** Debugging and Error Handling | 2.6% | Chapter 19, *A Test Says It Broke; a Trace Says Where* |

## Domain 5: Model Selection and Optimization

**How to read this table:** same layout again.

| Skill | Weight | Owned by |
|---|---|---|
| **5.1** LLM Fundamentals | 5.2% | Chapter 1, *What This Exam Tests That an Interview Does Not* |
| **5.2** Technical Fundamentals | 6.1% | Chapter 2, *Four Parts to Every Call, and Three Places It Breaks* |
| **5.3** Model Selection and Tradeoffs | 2.7% | Chapter 4, *A Model Choice Is Three Numbers You Were Not Given* |
| **5.4** Cost and Token Management | 2.8% | Chapter 8, *Cost Follows What You Resend, Not What You Ask* |

## Domain 6: Prompt and Context Engineering

**How to read this table:** same layout again.

| Skill | Weight | Owned by |
|---|---|---|
| **6.1** Context Engineering | 3.8% | Chapter 7, *The Window Is a Budget, and Everything Competes* |
| **6.2** Prompt Engineering | 4.6% | Chapter 5, *Instruction Placement Is a Trust Decision* |
| **6.3** Output Handling | 2.6% | Chapter 6, *Schema-Valid Is Not the Same as Correct* |

## Domain 7: Security and Safety

**How to read this table:** same layout. Skills 7.2 and 7.3 share one chapter.

| Skill | Weight | Owned by |
|---|---|---|
| **7.1** AI Application Security | 3.2% | Chapter 20, *The Attack Arrives as Content You Asked For* |
| **7.2** Guardrails and Safe Deployment | 2.3% | Chapter 21, *A Rule in a Prompt Is Not Enforcement* |
| **7.3** Claude Hooks | 1.0% | Chapter 21, *A Rule in a Prompt Is Not Enforcement* |
| **7.4** Identity, Secrets, and Key Management | 1.6% | Chapter 22, *One Credential: What It Reaches, and for How Long* |

## Domain 8: Tools and MCPs

**How to read this table:** same layout again.

| Skill | Weight | Owned by |
|---|---|---|
| **8.1** Tool Implementation | 4.4% | Chapter 9, *The Description Is the Input, Not the Documentation* |
| **8.2** MCP Server Development | 2.1% | Chapter 10, *One Server, Many Clients, Transport by Locality* |
| **8.3** Agentic Customization | 4.1% | Chapter 11, *Four Mechanisms, Decided by What Must Execute* |

## Where the Weight Is

The chapters follow the order in which you meet the decisions, not the order of the blueprint. So one domain is spread across the book instead of sitting in one place. If you are short on time, let these numbers decide where it goes. Domain 2 is worth thirteen times Domain 4.

**How to read this table:** each row is a whole domain. The weight is the sum of its skills, and the last column lists every chapter that covers it.

| Domain | Weight | Chapters covering it |
|---|---|---|
| 1 Agents and Workflows | **14.7%** | 12, 13 |
| 2 Applications and Integration | **33.1%** | 3, 15, 16, 17, 18, 23 |
| 3 Claude Code | **3.1%** | 14 |
| 4 Eval, Testing, and Debugging | **2.6%** | 19 |
| 5 Model Selection and Optimization | **16.8%** | 1, 2, 4, 8 |
| 6 Prompt and Context Engineering | **11.0%** | 5, 6, 7 |
| 7 Security and Safety | **8.1%** | 20, 21, 22 |
| 8 Tools and MCPs | **10.6%** | 9, 10, 11 |

## Every Chapter, in Order, With What It Owns

This is the same map the other way round. Use it when you know which chapter you are in and want to know which skills it is responsible for.

**How to read this table:** find your chapter number. The row shows its title, the skills it owns, and the exam weight of those skills together.

| Ch | Title | Skills | Exam weight |
|---|---|---|---|
| 1 | What This Exam Tests That an Interview Does Not | 5.1 | 5.2% |
| 2 | Four Parts to Every Call, and Three Places It Breaks | 5.2 | 6.1% |
| 3 | Messages, Streaming, Batches: Who Is Waiting Decides | 2.3 | 6.8% |
| 4 | A Model Choice Is Three Numbers You Were Not Given | 5.3 | 2.7% |
| 5 | Instruction Placement Is a Trust Decision | 6.2 | 4.6% |
| 6 | Schema-Valid Is Not the Same as Correct | 6.3 | 2.6% |
| 7 | The Window Is a Budget, and Everything Competes | 6.1 | 3.8% |
| 8 | Cost Follows What You Resend, Not What You Ask | 5.4 | 2.8% |
| 9 | The Description Is the Input, Not the Documentation | 8.1 | 4.4% |
| 10 | One Server, Many Clients, Transport by Locality | 8.2 | 2.1% |
| 11 | Four Mechanisms, Decided by What Must Execute | 8.3 | 4.1% |
| 12 | Known Steps Take a Chain; Unknown Ones an Agent | 1.1, 1.3 | 9.4% |
| 13 | The Loop, the Harness, and What You Stop Owning | 1.2 | 5.3% |
| 14 | Permission Modes and Where the Human Gate Goes | 3.1 | 3.1% |
| 15 | The Constraints Nobody States Decide the Design | 2.1 | 3.4% |
| 16 | Boundaries, Sessions, and Where Instructions Land | 2.5 | 8.6% |
| 17 | REST, Versioning, Review: the Exam Beyond Claude | 2.4 | 7.4% |
| 18 | An Unpinned Version Is an Untracked Change | 2.6 | 4.1% |
| 19 | A Test Says It Broke; a Trace Says Where | 4.1 | 2.6% |
| 20 | The Attack Arrives as Content You Asked For | 7.1 | 3.2% |
| 21 | A Rule in a Prompt Is Not Enforcement | 7.2, 7.3 | 3.3% |
| 22 | One Credential: What It Reaches, and for How Long | 7.4 | 1.6% |
| 23 | Deploy Is a Phase Boundary, Not the End | 2.2 | 2.8% |

Total skills: **25**, and each one is owned by exactly one chapter. The weights add up to **100.0%**.

**ELI5.** This chapter is a map of the whole exam. Every topic has a price tag showing how many points it is worth, and a note saying which chapter teaches it. Look at the big price tags first, then go read those chapters.
