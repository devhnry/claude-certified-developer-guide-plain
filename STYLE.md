# Style guide v2: rewrite, don't annotate

The first pass copied the original's sentences and added labels. That is not a rewrite. The test: someone who has never seen the original should find every paragraph easy on first read.

## Never change
- Every number, default, limit, price, version and date.
- Every `code term`, parameter, endpoint, header and model name, spelled exactly.
- Every citation marker like `<sup>[1]</sup>`, kept next to the claim it supports.
- Every table row and column (simplify the cell wording only).
- Chapter number and title, section order, and the endnotes (copy those verbatim).
- Original claims, even when the original contradicts itself. Keep the claim and flag it in your report.

## How to rewrite a paragraph
1. Read the paragraph. Close it. Say what it means to a friend who is smart but new to this.
2. Write that, from scratch. Do not edit the original sentence. If your sentence looks like the original with words swapped, start again.
3. One idea per sentence. About 15 words on average, 25 at most.
4. Concrete first. Start with a small example or a picture, then give the rule.
5. Say the plain thing. "The model picks the wrong tool" beats "tool selection degrades".

## Analogy
- One analogy per chapter, brought in only where it explains something that is hard. Not every paragraph needs it.
- When the analogy is used, the real term follows straight away, so the exam word sticks: "a locked door (a deny rule)".
- The analogy must never change what the real mechanism does. If it would, drop it for that paragraph.

## ELI5
- One short ELI5 per major section, 2 to 4 sentences, a child could follow. Not after every sub-part.

## Language
- Everyday words: "use", "fix", "so". No "leverage", "utilize", "robust", "seamless", "comprehensive", "ensure", "enhance", "streamline".
- Explain jargon in a few words the first time it appears.
- Bold ONLY an exam term at the place it is defined. Never for emphasis. Far fewer bold marks than the original.
- No em-dash chains. No padding ("it should be noted", "basically").
- Do not add facts that are not in the original.

## Hard limits (tools/check_similarity.py enforces these)
- At most 25% of sentences may closely match an original sentence.
- The chapter body must be shorter than the original body, so aim for 70 to 85% of its length.
- Bold marks must be under half the original's count.
