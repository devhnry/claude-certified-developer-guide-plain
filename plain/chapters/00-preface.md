# Preface

## Software Wrote This

Think of this book as a packing list for one trip, the exam. A language model wrote it. Every chapter, every table, every sentence.

I say so up front because it changes how you should read. Check things. Each claim from Anthropic's documentation has a numbered reference to the page it came from. Open them. Software has not earned your trust.

Software reads a huge pile of documentation closely and spots where two pages disagree. Sometimes they do. Then the book says so and names the page it followed.

Software cannot tell where its own knowledge ends. So one rule beat every other: **no invented specifics**. No made-up company, customer, incident, benchmark or measurement. If you cannot read it in a source, it is not here. Any scenario is openly hypothetical.

**ELI5.** A robot wrote this book, and robots can be wrong without noticing. So each fact points to its source. Look before you believe.

## Who This Is For

You have the exam booked, or you are deciding. You are the only reader I wrote for.

The exam has **53 items in 120 minutes**. Some are multiple choice, some are multiple response, and each item tells you how many answers to pick. Scores run from 100 to 1,000, and **720 passes**. A public blueprint sits behind it with **8 domains and 25 skills**. Each skill has its own weight, not just each domain. The book follows this blueprint, and the back matter maps every skill to its chapter.

One rule shaped each paragraph. It had to earn its place in the bag, meaning it had to match something the exam tests. Being interesting, complete or thorough did not count. If a passage would not help you answer a question you might miss, I cut it.

Little writing on these models follows the exam. This is not a survey. It is roughly 72,000 words aimed at 25 named skills. That is a weekend to read and an evening to skim again. I chose the length on purpose. A book you finish beats a book you admire.

**ELI5.** This book is for you, taking the exam. A page that would not help you answer a question is not in it.

## What the Exam Is Actually Like

Two facts shape the whole book. Learn them before chapter 1.

First, nearly every wrong answer is a mechanism that works. The wrong options are real features used in the wrong spot. A Skill might be offered where you needed a server. A context file might be offered where you needed a hook. A retry might be offered when the failure can never succeed. Knowing what a feature is for beats knowing it exists.

Second, a third of the exam is not about Claude. Domain 2 alone is 33.1%. It covers REST semantics, versioning, review discipline and application boundaries. Domain 4 covers evaluation, testing and debugging, and it is only 2.6%. That is a thirteen-fold gap. Split study time by interest and you will study the wrong things. The coverage map at the back prints every weight, so you can pack on purpose.

**ELI5.** Wrong answers are real tools used in the wrong place. Some topics are worth far more points than others.

## How a Chapter Is Built

Every chapter has the same parts in the same order. So you can jump into any one without reading the ones before.

1. An italic summary. It says what decision the chapter settles and what a wrong choice costs.
2. Sections whose headers state their point. A header should tell you something before you read the text under it. One that does not is a defect.
3. Tables wherever the material runs in parallel. A table says in forty words what prose needs four hundred for.
4. Named failure shapes, in bold. Wrong answers are built from believable mistakes. If you can name a mistake, you can spot it in an option list you have never seen.
5. A section called How Wrong Answers Are Built on This Material. It lists the assumptions wrong answers lean on. Then a table gives, per row, what the scenario says, what the answer usually is, and what the trap usually is. The rows are **cues rather than cases**, so they still work in an industry this book never mentions.
6. A closing list called What to Remember. Each line is written to make sense with the chapter closed, because that is the only time anyone reads such a list.

**ELI5.** Every chapter is laid out the same way, like identical lockers. You always know where to look.

## How to Read It

With time, read in order. The chapters follow the order you meet each decision when you build something, so each leans on the last.

Without time, read all twenty-three closing lists first. Then read the chapter behind any line you could not defend yourself.

Chasing one weakness? Open the coverage map, find the skill, and read the chapter that owns it.

One honest warning. Anthropic's documentation moves. Numbers change and pages move. I read everything cited here on the dates in the references, and some of it will be out of date by now. The reasoning lasts longer than the figures, so that is where most of the pages went. If a number matters to your answer, follow the link.

Now go and make your mistakes here, where they are cheap. The exam room is where they cost you.

**ELI5.** With lots of time, read front to back. With little, read the end-of-chapter lists first.
