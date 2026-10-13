# Preface

## Software Wrote This

**First, the idea.** A language model wrote this book. So you should treat it like a trail guide (**the book**) written by a surveyor who walked the ground with a very good notebook, but who does not always know where the notebook runs out. Your job is to check the signposts (**the numbered references**).

A language model wrote this book. Every chapter, every table, every sentence.

That belongs at the front, not in a note at the back, because it changes what you should do with what follows. **Check things.** Every claim taken from Anthropic's documentation carries a numbered reference (a signpost) to the page it came from. Those references are there so you can open them. They are not there to make a paragraph look well dressed. A book written by software that asks to be believed is asking for something it has not earned.

**What software is good at.** The job this book needed done was this:
- reading a large body of documentation closely
- holding all of it at once
- noticing where two pages say different things

There are places in here where they do say different things. Where that happened, this book says so and names which page it followed. It does not pick the tidier page and move on.

**What software is bad at.** It does not know where its own knowledge ends. That is what the references are for. It is also why one instruction outranked every other rule this book was written under: **no invented specifics**. That means:
- no company
- no customer
- no incident
- no benchmark
- no measurement that is not in a source you can go and read

Where a scenario appears, it is openly made up. Where a figure appears, it came from somewhere named.

**ELI5.** A robot wrote this guide, and robots can be wrong without knowing it. So every important fact has a signpost showing where it came from. Walk over and read the signpost yourself.

## Who This Is For

**First, the idea.** This book has one reader in mind: the person facing the exam (**the mountain**). Every choice about what to include was settled by asking what that person needs.

You have the exam booked, or you are deciding whether to book it. That is the only reader considered here.

**The exam in numbers.**
- **53 items in 120 minutes**.
- The items are multiple choice and multiple response. Each item tells you how many answers to select.
- It is scored 100 to 1,000. **720 passes**.
- Behind it sits a published blueprint (the official list of what is tested) of **8 domains and 25 skills**. A weight is given for each skill, not only for each domain. That is finer detail than most certifications hand out.

This book is organised around that blueprint. The back matter has a coverage map (**the trail map**) that maps every skill to the chapter that owns it.

**The one writing rule.** Every paragraph had to **earn its place against something the exam tests**. It did not have to be interesting. It did not have to be complete. It did not have to sound thorough. A passage that would not help you answer something you would otherwise miss is not in here.

**Why it is this long.** There is good writing on building with these models. Almost none of it is arranged around what you will be asked. So this is not a survey. It is roughly **72,000 words** aimed at 25 named skills. That is a weekend to read and an evening to skim again. The length is a decision, not an accident: **a book you finish beats a book you admire**. The ground is wide enough that a complete treatment would never be read by the person who most needs it.

**ELI5.** This book is only for people taking this one test. If a page would not help you answer a test question, it was left out. It is short enough that you will actually finish it.

## What the Exam Is Actually Like

**First, the idea.** Two things about the exam (**the mountain**) shape the whole book. You should know both before chapter 1.

**Nearly every wrong answer is a mechanism that works.** Wrong options are not made of nonsense. They are made from real features used one step out of place. For example:
- a Skill where a server was needed
- a context file where a hook was needed
- a retry where the failure was permanent

So knowing that a mechanism exists is worth very little here. Knowing what it is for is worth almost everything. It is like a path that really exists but leads to the wrong summit.

**A third of it is not about Claude.** Domain 2 alone is **33.1%**. It covers REST semantics, versioning, review discipline and application boundaries. Domain 4 covers evaluation, testing and debugging. It is **2.6%**. That is a thirteen-fold spread. If you plan study time by how interesting a topic is, you will spend your evenings in the wrong place. The coverage map at the back prints every weight, so you can spend your time on purpose.

**ELI5.** The wrong answers on this test are real tools used in the wrong place. So learn what each tool is for, not just that it exists. Also, a lot of the test is about ordinary web building, not about Claude, so do not skip it because it feels boring.

## How a Chapter Is Built

**First, the idea.** Every chapter is laid out the same way, in the same order. That way you can drop into any chapter without having read the ones before it, like joining a trail at any marked stop.

Each chapter has these parts:

- **An italic summary.** It says what decision the chapter settles, and what getting it wrong costs.
- **Sections whose headers state their point.** There are no teasers. A header that means nothing until you have read the section under it is dead weight in a book somebody revises from. If you find one, it is a defect.
- **Tables wherever the material is parallel.** A table does in forty words what prose needs four hundred for. There is a lot of ground here.
- **Named failure shapes, in bold.** These carry more than they look. Wrong answers are built out of plausible mistakes. A mistake you can name is one you can spot in an option list you have never seen.
- **A section called How Wrong Answers Are Built on This Material.** It lists the families of assumption that wrong answers rest on. Then it has a table with three columns: what the scenario says, what the answer usually is, and what the trap usually is. The rows are written as **cues rather than cases**. So they still work on a scenario set in an industry this book never mentions.
- **A closing list called What to Remember.** It is marked densely. Every line is written so it stands up with the chapter shut, because that is the one condition under which anybody reads such a list.

**ELI5.** Every chapter looks the same: a short summary, clear headings, tables, named mistakes, a list of tricks the wrong answers use, and a list to remember. Because they all look alike, you can jump into any one.

## How to Read It

**First, the idea.** There are three ways to use the book, depending on how much time you have. Pick the one that matches your situation.

- **With time**, read in order. The chapters follow the order in which you meet the decisions when you build something. So each one leans on the last.
- **Without time**, read the closing lists first. There are twenty-three of them. Then read the chapters behind any line you could not defend on your own. The book was built to survive being used this way.
- **Chasing one weakness**, go to the coverage map, find the skill, and read the chapter that owns it.

**One honest caveat.** **Anthropic's documentation moves.** Numbers change, features ship, and pages get reorganised. Everything cited here was read on the dates in the references. Some of it will have changed by the time you read this. The reasoning lasts longer than the figures, which is why the reasoning is where the pages went. When a number matters to your answer, follow the link.

Now go and be wrong cheaply, here, rather than expensively, in an exam room.

**ELI5.** If you have lots of time, read from the start. If you have little time, read the short lists at the end of each chapter first, then read more only where you got stuck. If you know your weak spot, go straight to it. Facts online change, so check the link for any number you rely on.
