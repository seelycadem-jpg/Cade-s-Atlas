# Meanwhile Atlas: house style and analytic standards (internal)

Internal to the project. The public About page carries only purpose, goal and the method in brief.

The full standards live in the doc "Meanwhile Atlas: Analytic Standards" (https://claude.ai/artifact/TcJD2axuTWXPd8fQWroQZk): foundations, logic diagram, tiering matrix, link taxonomy, confidence language, writing rules, QC flow, German-question pilot, voice, story methodology, themes. This file is the short form every session applies. Story methodology and anti-slop rules are in claude/story-method.md.

## Rule zero: the banned construction

The negation-then-reveal is banned in every register, including chat with the user: "It did not X. It Y'd." / "Not X, but Y." / "The question is not X but Y." State what a thing is or did, directly. A contrast is stated in one clause with "rather than" or "instead of", and only when the contrast is the point. Example: write "The law enforced itself through rewards rather than punishment", never "The law did not create a system of punishment. It rewarded those who followed the rules."

## Rule one: two registers

- The presidential daily brief, everywhere: event briefs, arrow notes, story chapters at every altitude, theme propositions, the About page, chat. Every sentence carries information or argument. Judgment first. No word that could be cut without loss. If the President would skim it, cut it. No questions; the reader is told.
- Cicero, in the themes layer only (the ten "Man and …" passages): the passage may ask questions and let them stand, build through them, and address the reader. It is the one place the atlas thinks aloud. Rule zero still applies. Every question must be real, one the theme page then answers with propositions and links; a question used to sound deep is sent back.

## Rule two: facts, no authorities (added 2026-10-28)

Product text names no historians, academics, books, schools of thought or data compilers. The reader is told the facts and the judgment, never who said it. Historical actors are named as actors (Luther argued, Bismarck dismissed); a modern author or scholar is never cited. Where two readings exist, write "one reading holds … the other holds …" and give each its evidence. Reading lists ("the shelf"), chart source lines and dataset names stay in the data for the editors and never render in the product; the About page alone may describe sources in general terms. Applies to briefs, arrow notes, story text, polity profiles, chart captions and chat.

## Rule three: the bottom line (added 2026-10-28)

Every event's bottom line is written in one shape: purpose, outcome, consequence. First what the actors were trying to do, in plain words ("Britain and France fought Russia to stop it taking Constantinople and the Straits"); then whether they got it and at what cost; then what it changed in the international, political or social order ("it broke the international system established at the Congress of Vienna"). Two or three sentences. The same shape governs a knot's first line and a profile's "now".

## Rule four: actors and pith (added 2026-10-28)

Actors carry their role and name on first mention: Russian Tsar Nicholas I, German Chancellor Olaf Scholz, British Prime Minister Lord Aberdeen; a bare surname is never the first mention. One idea per sentence; no sentence that could be cut without loss of information; no clause that restates. A draft that runs long is cut, never padded.

## Purpose

An analytic training set. The product is a reader who can grade a causal claim; history is the material. Links carry the argument; events are evidence. Inevitability is an error. Nothing ships without its objection.

## Foundations (for explaining the past)

- Pearl's ladder: every grade states its rung (1 association, 2 intervention, 3 counterfactual). Coincident = rung 1 mistaken for 3. The "pull an event" feature is rung 3 made visible.
- Mackie's INUS: Contributing means a necessary part of one sufficient set among several; the test is to name the set.
- Van Evera's tests: evidence is hoop, smoking gun, doubly decisive or straw-in-the-wind; Depth 3 is organised by tests. Straws only = Contributing at low confidence at most.
- Toulmin: the arrow note is claim, objection, warrant, verdict. The warrant is the general rule that licenses the inference; no warrant, no link.
- Tetlock: red-team survival rate by grade is tracked and published as the atlas's calibration curve.
- From intelligence tradecraft keep only: known vs assessed, key assumptions check per arc, red team, fixed confidence words.
These names are for the editors; by rule two none of them appears in product text.

## Four governing principles

1. Write forward: every brief from inside its moment, outcome unknown (counters hindsight bias).
2. One argument per screen, one tap to its evidence (three depths: verdict, argument, evidence; never mixed).
3. The reader generates before being told (guess the grade before the note opens).
4. The line is the argument: fixed visual language for grades everywhere; a chain of "and then" is a list, never a story.

## Voice: the blend (the brief register)

- The Economist: judgment first, compression, dry wit used sparingly.
- Financial Times: the economy is the spine; figures carry the argument.
- Martin Wolf: rigor and nerve; a wrong idea is called wrong, with the reason.
- Stratfor: constraints over intentions; geography, demography and position before ideology or character.
- Robert Kaplan: the long view and the map; terrain and distance as standing causes.
- Ian Bremmer: who gains, who loses, the odds; outcomes as distributions.
- Fareed Zakaria: synthesis for an intelligent general reader; the big pattern named plainly.

The themes register borrows from the classical essay. The blend describes the voice; none of these names is cited in product text.

## Rules

1. Lead with the verdict: the bottom line (rule three) opens every event, knot and profile.
2. Mechanism before motive; constraints first, ideology second, personality last.
3. Numbers argue: a figure appears only when it changes the judgment, always with its basis.
4. Name the objection in the same paragraph as the claim; draft it before the verdict.
5. Probabilities rather than prophecy: "made more likely", "narrowed the options"; never "inevitable", "destined", "had to".
6. Say it once; no closing restatement.
7. Plain words for big ideas; a term of art once, then what it means in this case.
8. No hero history: the situation gets the first sentence, the leader the second, and the leader's choice names the option declined.
9. Dry, never cold; irony never aimed at victims.
10. Written to be used: could a reader quote it in a meeting about today and be right?

## Structure

Four objects: Events, Stories (grouped into Arcs), Links, and Themes (ten, each holding propositions). Two content levels only; "theatre" is a label on a story-to-story link. Links may join any two events or stories. Themes are read off the links; an event belongs to a theme only through a link that supports or embarrasses one of its propositions. One link table, no nesting field. Polity profiles (periods per state: government, head, capital, religion, population, economy, now, how, next) sit behind the globe.

## Tiers (score 0-2 on each; 5-6 = Tier 1, 3-4 = Tier 2, 0-2 = Tier 3)

Reach across regions and domains · Irreversibility · Explanatory load for today. Fame and casualty counts do not score. Tier 1 must carry at least one cross-region link. Tiers are outputs of the link graph.

## Links

Type (one): Structural · Material · Ideological · Reactive · Enabling · Precedent.
Grade (one): Necessary · Sufficient · Contributing (default) · Contested · Coincident (kept).
Confidence (one): High · Moderate · Low.
One mechanism per hop; long chains are split. Necessary/Sufficient require a counterfactual sentence; Contributing names the set and A's rank; Contested states each reading ("one reading holds …") with its evidence, without naming its authors. Ideological links need evidence the actors read or invoked the idea.

## Arrow note (60-100 words)

Claim (verb matched to grade) · Objection (strongest, stated) · Warrant (the transferable rule) · Verdict (grade, defended) · Evidence tests (hoop / smoking gun / both / straws; required for Tier 1) · Meta (type, grade, confidence, hops, cross-region).

## Event brief (page order, agreed 2026-10-28, revised the same day)

The brief: Bottom line (rule three) · Why it matters (the consequences as mechanisms with their date range; never trivia).
In depth: What happened (the situation first, then the actors with role and name, facts without causal verbs) · Why (two or three drivers ranked, then the trigger in its own sentence) · What followed (changed conditions, dated, in order of weight) · By the numbers (basis on every figure; ranges where sources differ) · A common misreading · Places · Interesting fact (where firsts, anniversaries, legends and the telegraph go; kept, at the bottom).
Causes and effects: the trace · chains into the event, read as paths with the weakest arrow named · what caused this and what this caused, graded.
Dropped: the questions-an-analyst-asks block and the one-line rule; the lens stays in the data as an editorial note.

## Grade visual language

Necessary and Sufficient: solid. Contributing: dashed. Contested: dotted. Coincident: struck through, in the warning colour. Same everywhere: timeline, dossier, story page.

## Politics

Contested politics are described rather than adjudicated: the claim, who makes it, what the other side says, at equal length. Ongoing wars cite the source and date of every figure.

## Build order (agreed 2026-10-28)

1. Two hand-built pilots: German question (done, ten knots to 2022) and East Africa (Omani Zanzibar to Arusha). ~50 links, red-teamed.
2. Link data model; grade visuals; arrows on the timeline; "what caused this / what this caused" in the dossier; guess-the-grade beat. (done)
3. Counterfactual: pull a Necessary event, downstream greys out.
4. Front door: the arcs on one screen; timeline behind a click. (done: Atlas page with globe, cut, arcs)
5. Scale links to all events with AI proposing and red team checking; story-to-story layer; themes and propositions; then the quiz.
6. The full rewrite of every event brief to rules zero to four, in batches of forty by region, each batch through the pipeline's checks and published; Europe first. (agreed 2026-10-28; done the same day, all 781 events, briefcheck stage enforces it on every build)

## Working practice

The user likes a publish to the same artifact after each step. External images are blocked by the artifact CSP; no photos of real people. Build pipeline and test scripts are described in the session notes.

## The globe (rebuilt 2026-10-29)

Borders change year by year. From 1886: a dated record of every state and colony (maps/cs.json), evaluated at mid-year, with a ledger of changes generated from it. 1400-1885: survey maps of eleven years; every piece of land that changed hands between two surveys was dated where the year is known (maps/pieces.json, 153 dated) and hatched where it is not (91). Coastal gaps in the survey maps are merged into the neighbouring polity; large blank land stays "no state recorded". Physical layer: hillshade relief reprojected per pixel when the view settles, rivers and sea names that appear by zoom, mountain and desert names only when close. Pipeline: g2/build_maps.sh. Product text never names the data sources; the About page describes them in general terms.
