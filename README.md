# Claude Certified Developer Guide, plain-English edition

A rewrite of [vkorost/claude-certified-developer-guide](https://github.com/vkorost/claude-certified-developer-guide) that is easier to read.

Each chapter keeps every fact, number, `code term` and citation from the original. What changed:

- The idea comes first, then the detail.
- One analogy per chapter, with the real exam term in bold next to every analogy word.
- Short sentences and everyday words.
- An "explain like I'm 5" box at the end of each section.

## Where things are

- `plain/chapters/` has the rewritten chapters. Start here.
- `book/chapters/` has the original chapters, untouched, so you can compare.
- `ERRATA.md` lists places where the original contradicts itself.
- `STYLE.md` has the rules the rewrite followed.
- `tools/check_facts.py` flags any number, `code term` or citation in the original that is missing from a rewrite.

## Known limits

- The original contradicts itself in a few places (for example a heading that says "three" over a list of four). The rewrite keeps the original claim as written.
- The analogies and ELI5 boxes are new text. Check anything that matters for the exam against the original chapter.

## Credit and license

Original book by V. Korostyshevskiy, licensed CC BY-NC-SA 4.0. This adaptation is shared under the same license, for non-commercial use. See `LICENSE`.
