---
name: reach-check
description: Before a plan runs, convert it to steps that name what they call, have a second agent challenge it with questions backed by evidence, then have the author rewrite it or say STOP, tagging every change as ours to fix or the provider's. Returns one verdict without the user in the loop. Use for "reach check", "check this plan", "can this plan work", "review the plan before we spend", "is this goal reachable", or before any delegation that will cost more than a few dollars.
---

# reach-check

A gate between a plan and its execution. It exists because an agent will follow a plan for a goal it cannot reach until the budget is gone, and because the user's approval of that plan makes it worse: in one measured case, an agent read an instruction to keep going until the work was ready as an order never to stop, and worked five hours past the fact that should have stopped it.

The gate runs on its own and comes back with one of three things: GO with a stop card, STOP with the reason, or a restated goal with the unreachable part dropped and named. It never comes back with questions for the user.

Measured on the plan from that case, over 38 worker runs: with the packets below, two chains out of two named the real blocker and restated the goal without it, at an opus-low reviewer and an opus-medium author, at a few dollars per chain. With the packets as first drafted, 15 reviewers across five models missed it and the gate said GO twice.

## Roles

Four contexts. The main session is the courier; nothing passes between agents except through files it writes.

| Role | Tier | Sees | Returns |
|---|---|---|---|
| Converter | capable plan-writing worker | goal, the plan as given, the project | the plan as steps that name what they call |
| Questioner | low-cost evidence-finding worker, with tools | converted plan and the tool list only | the kill observation, the boundary answer, 3 to 5 questions, each with evidence |
| Author | capable plan-writing worker, fresh context or the original author's context | converted plan plus questions | revised plan with every step marked and tagged, or STOP |
| Judge (tests only) | low-cost blind judge, blind | replies plus the answer key | scores |

In the measured trials, sonnet-low did not work in the questioner seat (five false or empty claims in three cells). Opus-high and another tested model at low and medium effort cost more and found nothing more. Pooling three opus-low questioners widened coverage of cheap findings and did not reach the blocker. These are historical test results; choose available models for the generic roles above.

## Procedure

1. **Convert.** Spawn the converter with the goal and the plan. Every step becomes an action that names the tool, function, API, file, service, credential or permission it needs, and for any library or SDK call, the exact function, class or option. Every name must come from a file the converter read; the first converter that was not told this invented a class and a script. Outcomes ("prove X") become the step that would prove X and what it calls. Nothing is dropped and nothing is judged. Save to `docs/reach-check/<plan-name>.md` under `## Plan`.

   Why this step exists: on the original wording, "prove resume" named no call, so "do we have it?" was never asked. Once it read "call `resume`, assuming it restores children", four cheap questioners in a row attacked the assumption.

2. **Question.** Spawn the questioner with the converted plan and the tool list. Three parts, in order:
   - The kill question: "What one observation would show this goal is out of reach with what we have?" Named to a step or assumption, looked for, reported whether it holds or not.
   - The boundary question: for any step that resumes, restores, reattaches or reconnects across a restart, a disconnect or an expiry, "what happens to the thing on the other side of that boundary, and which function would find it again, and what does that function actually do?" Ask about the process or connection itself, not the records of it. Evidence about restoring records is fixable, and an author will fix it; evidence about a process that was killed is not. If the only evidence found is about records, the questioner says so and looks again for what happens to the process. Measured: three chains on the same case, two with process evidence dropped the claim, the one with record evidence strengthened it.
   - 3 to 5 questions, each naming one step or assumption, each with one piece of evidence (command plus output, file plus line, or URL plus quote), each of one of two kinds: "can this step happen at all with what we have?" or "what happens to the plan if this assumption is false?".
   A 'no match' claim needs a second method before it counts, and the second method must not rest on the same assumption as the first. If the first assumed one record per row, the second must be one that finds the record even when that assumption is false, such as searching the whole folder for the number itself. No verdict, no score, no rewrite. Paste under `## Questions`.

   The file handed to the questioner holds the plan and nothing else: no coordinator notes, no scores, no answer keys. When the gate is being tested, the packets name the folders that hold the keys and forbid them; two reviewers found the answer in a note beside the plan before this rule existed.

3. **Answer.** Spawn the author with the converted plan and the questions, and quote the user's original instruction and approval in the packet. The gate has to hold against the approval, not in its absence. The author re-runs any claim it changes a step on or decides STOP on, and says which claims it took as given. It returns the plan with every step marked `[unchanged]`, `[changed]`, `[new]` or `[removed]`, and for every step changed, added or kept because of a reviewer claim, one tag: `[our code]` if the fix is inside this repository, `[provider]` if it needs a change from a third party, with evidence for the choice. A `[provider]` tag on the kill observation, or on any step the definition of done depends on, means STOP or a restated goal that drops that step. A `[provider]` step cannot be kept as work.

   The original author's context may answer instead of a fresh one. Measured at opus-medium: same input, two heads, same output, no defending.

4. **Decide.** The main session writes `## Result`:
   - A question is resolved when the step it attacked changed, or the author withdrew it with re-run evidence.
   - The kill observation counts as a question. If it holds and the author's tag is `[provider]`, or the author dropped the step it lives in, the result is STOP or the restated goal, and that is the verdict.
   - A question with an unchanged step and a prose reply is unresolved.
   - Two or more unresolved: STOP, the questions are the reason.
   - One unresolved: back to step 2 once, with only that question. Still unresolved: STOP.
   - All resolved and nothing dropped: GO. The evidence lines become the stop card.
   - A claim taken as given on a step that changed because of it is flagged in the result. It does not block, but the judge scores it.

5. **Carry the stop card.** Every delegation packet that follows gets this block:

```
budget:        <dollars or tokens; harness cap where available>
stall rule:    3 steps with no new evidence = stall. 1 stall = replan once.
               stall again = stop and report.
kill question: "if X is true, this goal is out of reach". X = <from the questioner>
progress is:   <a file changed, a test that now passes, a fact we did not have>
               Re-reading is not progress.
```

6. **Log it.** If you keep a field log, append one row for each check on real work. Lab experiments do not need a row.

```
python3 <path-to-log_check.py> \
  --tool <tool-name> --project "<project path>" --goal "<one-line goal>" \
  --verdict GO|STOP|RESTATED --cost <cost or -> \
  --kill "<one-line kill observation>" --dropped "<what the check removed, or ->"
```

   The row links the session to the check. A compatible report tool can later compare checked and unchecked runs. If no logger is available, skip this step; the check itself remains usable.

## Packet templates

Converter:

```
Do not implement anything and do not edit or create any file outside <scratch dir>. You may read files and run read-only commands. What went wrong last time: steps were written as outcomes to prove ("prove resume") without naming what each one calls, so nobody could check whether the call existed; and a previous converter invented two names that exist nowhere, so every name you write must be one you have seen in a file.
You are the planner. Rewrite the plan below as, under 500 words: 1. Steps, numbered; each an action, not an outcome; each names the concrete tool, function, API, file, service, credential or permission it needs, and for any library or SDK call the exact function, class or option, using only names you have confirmed exist by reading the file. Where the plan says "prove X", write the step that would prove X and what it calls. 2. Assumptions: things you believe true but did not verify. 3. Definition of done: one check that can fail.
Do not judge feasibility and do not drop items.
Goal: <goal>. Context: <paths, tools, credentials the run will have>.
Check yourself against this number: every step names at least one concrete thing it calls, and every name appears in a file you read.
```

Questioner:

```
Do not edit or create any file outside <scratch dir>. Do not run anything that starts a model or a provider. Read-only commands only. Do not rewrite the plan. Do not give a verdict, a score or a recommendation. What went wrong last time: the reviewer reached its target number of findings that were cheap to prove and never examined the one capability the whole goal depended on.
First, answer this one question in writing, with evidence: "What one observation would show this goal is out of reach with what we have?" Name the step or assumption it lives in, go and look, and report what you found whether it holds or not.
Second, for any step that resumes, restores, reattaches or reconnects across a restart, a disconnect or an expiry, answer with evidence: what happens to the thing on the other side of that boundary? Which function in the code or the library would find it again, and what does it actually do? Answer about the process or connection itself, not the records of it; if the only evidence you find is about records, say so and look again for the process.
Then check the rest of the plan's steps and assumptions and return 3 to 5 questions addressed to the plan's author. Each names the one step or assumption it attacks; attaches the evidence you found (command + output, file + line, or URL + quote); and is one of two kinds only: "can this step happen at all with what we have?" or "what happens to the plan if this assumption is false?". Nothing about style, structure or nice-to-haves. A 'no match' claim needs a second method before it counts, and the second method must not rest on the same assumption as the first. If the first assumed one record per row, the second must be one that finds the record even when that assumption is false, such as searching the whole folder for the number itself.
Check yourself against this number: every question carries exactly one piece of evidence.
=== PLAN === ... === END PLAN ===
```

Author:

```
Do not edit or create any file outside <scratch dir>. Do not run anything that starts a model or a provider. You may read files and run read-only commands. What went wrong last time: the author took a reviewer's claim as given, changed the plan because of it, and the claim was wrong.
You are the author of the plan below. The user's instruction that produced it was "<instruction>", and the user approved it. A reviewer sent the kill observation, the boundary answer and the questions below, with evidence. Re-run any claim you change a step on or decide STOP on; say which claims you took as given.
One rule: for every step you change, add, or keep because of a reviewer claim, write one tag after its mark: [our code] if the fix is a change inside this repository, or [provider] if it needs a change from a third party, and attach the evidence for that choice. A [provider] tag on the kill observation, or on any step the definition of done depends on, means STOP or a restated goal that drops that step. A [provider] step cannot be kept as work to do.
Respond with the revised plan as a full numbered list with every step marked [unchanged], [changed], [new] or [removed] and tagged where the rule applies, plus an Assumptions list and one Definition of done that can fail; or the word STOP and the reason, with a restated goal if one exists. Then a Claims section: the kill observation, the boundary answer, and each question, RE-RUN (with your command and output) or TAKEN AS GIVEN.
Check yourself against this number: every step carries exactly one mark.
```

## What this does not do

It does not watch the run once it starts. That is the stall checker, not yet written. It does not cap money; use the harness cap (`--max-budget-usd` in Claude Code, Codex `rollout_budget` once enforced) or a wrapper outside the harness.

## Known limits

- An author that sees a real seam will call it fixable when the evidence is about records rather than processes. The boundary question exists for that; it has been tested on one case.
- Authors reach the restated goal by narrowing what they claim under `[our code]` more often than by tagging `[provider]`. The outcome is the same; the judge scores the goal, not the tag.
- One author in two took a library claim as given after changing a step on it. The rule is in the packet; the result flags it.
- Tested on three goals of two kinds (data plumbing on one machine, a multi-agent backend), with opus-low questioners and opus-medium authors. The case that matters was the run that spent the budget.
