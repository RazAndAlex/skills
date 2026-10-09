---
name: design-round
description: "Visual work — a screen, page, chart, layout, logo or diagram — run as six gated phases: study real prior art, derive the acceptance question, build N options that differ in form, reject look-alikes, open every option in a browser, publish them side by side."
when_to_use: "Use when the user asks for a screen or page ('make the dashboard', 'questa pagina', 'redo the layout'), a logo or mark, a chart or visualisation, or options to choose between ('show me options'). For a small fix on a screen already accepted, go straight to the work instead."
---

# Design round

One round. Six phases. Each phase has a gate, and a phase that fails its gate repeats
instead of passing work forward.

This exists because rounds without gates are expensive. In the author's own work, seven
ungated rounds of one view ran for 43.5 hours before anything was accepted. The two gates
that were missing both times are phase 1 and phase 4.

## The rule that outranks the rest

**A screen the user has not looked at is an irreversible action.** The first screen goes
in front of the user, running, and their reaction is what releases the second. Acceptance
comes from the user; a green internal check is a hypothesis.

## Phase 1: study what already exists

Before drawing anything, find three real products that solve this problem and say what
mechanism each uses. Name them, link them, describe the mechanism in one line each.

If workers are available, delegate three parallel low-cost research scouts, one field each. Otherwise research the fields sequentially. Ask for pointers to existing work, never mockups.

- **Gate:** three named real products, each with its mechanism stated. A general
  description of the problem space does not pass.
- Concrete: `Linear's command palette anchors the active item with a left rail and dims
  siblings.` Vague: `modern apps use clean navigation.`

## Phase 2: derive the acceptance question

Write the single question every option will be judged against, before any option exists.
It must be answerable by looking, in under five seconds, without hovering, and it must
name what a person has to read to answer it. Every one of those things (labels, axis values,
the names beside marks, the words in a control) is part of the answer and is judged at the
same reading distance as the figure. An acceptance question about the figure alone lets
every label shrink to make room for it.

Use a high-judgment worker here if available; this method-setting step is where extra reasoning has paid off in measured runs. Otherwise use a capable worker and keep the gate.

Name the incumbent to beat, including the boring one. Prettier than the incumbent is not
a win.

- **Gate:** one question, one incumbent, both written down. Two questions means two rounds.

## Phase 3: build N options that differ in form

Three to five. Each is a **different form**, not a different parameter. One route,
switchable, throwaway: no tests, no persistence, no polish, no abstractions.

If workers are available, use capable implementation workers as a pipeline, one form each. Otherwise build the options in sequence. Give each builder the acceptance question from phase 2 and the prior art from phase 1.

- **Gate:** every option names its own form in one word or phrase.
- Concrete: `braid`, `elastic time`, `flight recorder`, `slice observatory`. Vague:
  `version A`, `variant 2`, `the improved one`.

## Phase 4: reject the look-alikes

Hand the N options to one low-cost independent judge, if available; otherwise ask the reader to compare the forms. Give this instruction: name the form of each, then say which pairs share a form. Any pair that shares a form is one
option, and one of them goes back to phase 3.

It was the cheapest gate in the measured setup, and its absence produced the most common
complaint: the options all looked the same.

- **Gate:** N distinct forms, judged by someone who did not build them.

## Phase 5: open every option

Launch each one and look at it. Screenshot it at 1536x770, the real viewport, not
1920x1080. Then walk the recorded decisions and confirm none has crept back. Record the
smallest text a person has to read and its contrast against what it sits on: nothing a
person must read sits below 13px, weight 400, APCA Lc 60 (about #b0b0b0 on #0b0b0d), and
no label is smaller or fainter than the thing it labels. Review scaffolding (measurements,
form labels, questions to the user) never appears inside the specimen in the product's own
tokens; it goes in the reply.

Reviews that read source agree with the implementer. Reviews that open the artifact
contradict it: one found a composer broken by nested buttons, a popover clipped 299px out
of view, and a "Show 3 more" control that did nothing, all three in demos labelled
working.

An implementer never checks its own option.

- **Gate:** one screenshot per option, plus a line per recorded decision saying it holds.

## Phase 6: publish them together

One artifact, all N side by side, each live and clickable, with a preview strip so the
options can be compared without being opened one at a time. If installed, use `artifact-design` for the artifact structure and `dataviz` for charts. If installed, use `unslop` for English prose. Otherwise apply the six gates and review the artifact directly.

- **Gate:** the user has the link. Nothing else closes this phase.

## After the user picks

Graft, do not restart. Take the winner as the base and pull the strongest single part of
each loser into it, then re-run phase 5 on the result. If `arena` is installed, use it for graft mechanics; otherwise graft the strongest single part of each loser into the winner yourself.

When the user says they like something, that is a direction and not a specification. Keep
the reason it worked; change everything else. Treating a preference as a fixed constraint
is what makes round six look like round five.

## Boundaries

- On the first round, show option one running and wait for the user's reaction before
  building the second.
- Deliver only options whose forms are distinct. A duplicate form goes back to phase 3.
- Name the products you studied inside the proposal itself.
- Open every option before delivery, including when the build succeeded. A build passing
  and a screen working are different facts.
- For a small fix on a screen the user has already accepted, go straight to the work.
