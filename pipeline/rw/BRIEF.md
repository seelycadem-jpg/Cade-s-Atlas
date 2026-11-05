# Rewrite brief for one batch of Meanwhile Atlas event briefs

You are rewriting the text of history events for an analytic atlas. The product is a reader who can grade a causal claim; history is the material. Your output is one Python file, `/home/claude/anNN.py` (NN given in your task), in exactly this shape:

```python
# <region> batch (<years>): every brief rewritten to rules zero to four.
OVERRIDE = True
A = {
"<event id>": dict(
 bluf="...",
 now="...",
 story="...",
 why="...",
 trig="...",      # optional
 then="...",
 myth="...",      # optional
 fact="..."),
...
}
```

Read `/home/claude/an35.py` first, in full. It is the worked standard; match its register, length and shape exactly. Then read your batch file `/home/claude/rw/bNN.txt`: one block per event with the id, year, title, actors, place and the current text of every field. Rewrite every event in the batch. Keep every event id exactly as given.

## The fields

- `bluf` — the bottom line, 2 or 3 sentences, 40 to 90 words, in one fixed shape: **purpose → outcome → consequence**. First what the actors were trying to do, in plain words ("Britain and France fought Russia to stop it taking Constantinople and the Straits"). Then whether they got it and at what cost. Then what it changed in the international, political or social order ("it broke the international system established at the Congress of Vienna"). For an event with no purposeful actor (an earthquake, a plague, a discovery) open with the situation, then the outcome, then the consequence.
- `now` — "Why it matters": the political or social consequence, stated as mechanism with its date range, 1 or 2 sentences. Never trivia, never "is still remembered", never a museum or a holiday (those go in `fact`). If the current `now` already does this well, keep it verbatim.
- `story` — "What happened": the situation first, then the actors with role and name, then the facts in order, without causal verbs. 3 to 5 sentences. Keep every date and figure from the current text; add none you are unsure of.
- `why` — the drivers, two or three, ranked, each its own sentence. 1 to 3 sentences.
- `trig` — the trigger, one sentence, only where there is a datable trigger. Omit otherwise.
- `then` — "What followed": changed conditions, dated, in order of weight. 2 to 4 sentences.
- `myth` — "A common misreading": include only where there is a widely held wrong reading worth killing. Two sentences: the misreading stated flat, then the correction. Optional.
- `fact` — "Interesting fact": one or two sentences; the memorable detail, the first, the legend, the number (the Armada lost more ships to storms than to guns; the Crimean War was the first covered by telegraph). Give every event one. Keep the current `fact` if it is good.

## The rules (all enforced; a linter runs on your file)

- **Rule zero**: no negation-then-reveal, ever. Never "It did not X. It Y'd." Never "not X, but Y", "not only X but Y", "not because X but because Y". State what a thing is or did. A contrast is one clause with "rather than" or "instead of", used only when the contrast is the point.
- **Rule one**: presidential-daily-brief register. Judgment first. Every sentence carries information. No questions. No throat-clearing, no "it is worth noting", no "arguably". No adjectives of scale ("huge", "massive", "dramatic", "pivotal"): give the number instead.
- **Rule two**: name no historians, scholars, academics, economists, books about the event, schools of thought, "studies" or "the consensus". Historical actors are named as actors. Where two readings exist write "one reading holds … the other holds …" and give each its evidence. The words historian/scholar/economist/academic/according to are banned even in their everyday sense; find another word.
- **Rule three**: the bottom line shape above, every event.
- **Rule four**: actors carry role and name on first mention in each field: "Russian Tsar Nicholas I", "German Chancellor Olaf Scholz", "Ottoman Grand Vizier Kara Mustafa", "Mainz goldsmith Johannes Gutenberg", "Cossack Hetman Ivan Mazepa". A bare surname is never a first mention. One idea per sentence. No sentence that could be cut. A draft that runs long is cut, never padded.
- Probabilities rather than prophecy: "made more likely", "narrowed the options"; never "inevitable", "destined", "had to", "paved the way", "changed everything", "watershed", "sent shockwaves".
- Numbers only when they change the judgment, with their basis; ranges where sources differ.
- Contested present-day politics (Israel and Palestine, Kashmir, Taiwan, Ukraine, Rwanda, Xinjiang, coups since 2000): describe rather than adjudicate. State each side's claim at equal length; attribute every figure for an ongoing war to the source type and year ("UN count, 2024"). Stay evenhanded; the atlas has readers on every side.
- Accuracy over colour. Preserve every fact, date and figure already in the current text unless you know it to be wrong, in which case fix it. Add a date, name or number only when you are certain of it. A plain sentence beats a wrong detail.
- British spelling (centralise, honour), numerals for dates and figures, "per cent", no Oxford comma needed, straight quotes inside the Python strings must be escaped or avoided: use single quotes inside the text (the Python strings use double quotes). No em dashes; use commas, semicolons or full stops.

## Process

1. Read `/home/claude/an35.py` and your `/home/claude/rw/bNN.txt`.
2. Write `/home/claude/anNN.py` with every event in the batch.
3. Run `cd /home/claude && python3 lint_an.py anNN.py`. Fix every reported problem and rerun until it prints 0 problems. The linter checks rule zero, banned phrases, authorities, missing fields and bottom-line length; it cannot check facts, so check those yourself.
4. Reply with: the file path, the event count, the linter result, and a list of any event where you changed or dropped a fact from the current text and why. Nothing else.
