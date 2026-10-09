# Evidence behind the six rules

Each rule, the named sources, the numbers, and what the source does not support. Read this
when a rule is being argued with, extended, or applied to a case it does not obviously cover.

---

## R1 — one question per artifact

Six formats, six questions, no overlap. None of them substitutes for another.

| Format | The one question it answers | Source |
|---|---|---|
| Hill chart (Basecamp / Shape Up) | Are the unknowns gone? | https://basecamp.com/shapeup/3.4-chapter-13 |
| Amazon Weekly Business Review | Are the numbers on track? | https://commoncog.com/the-amazon-weekly-business-review/ |
| ADR (Nygard 2011) | Why is it like this? | https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions |
| Postmortem (Google SRE, PagerDuty, Cloudflare) | What broke, and what changes? | https://sre.google/sre-book/postmortem-culture/ |
| Changelog (Keep a Changelog) | What changed in the product? | https://keepachangelog.com/en/1.1.0/ |
| RFC / RFD / six-pager | What should we decide? | https://rust-lang.github.io/rfcs/ · https://rfd.shared.oxide.computer/rfd/0001 |

The WBR refuses its fourth question explicitly: strategy and problem-solving discussion are
banned in the room. That refusal is the mechanism, not an accident of scope.

**How short the top of a real one is.** Google's example postmortem (SRE book, Appendix D)
opens with a 28-word Summary and a 15-word Impact, and the timeline table is at the *bottom*.
https://sre.google/sre-book/example-postmortem/

**Measured on the author's pages.** A long recap the reader rejected ran 2,224 words. 711 of them
answered the question the reader had opened it for; 1,513 (68%) answered five questions
nobody had asked, and nothing said which was which until the end.

---

## R2 — the skeleton never changes

Seven organisations froze a shape independently, without copying each other.

| Who | What is frozen | Count |
|---|---|---|
| Statuspage | Investigating / Identified / Monitoring | 3 |
| ADR | Context, Decision, Status, Consequences | 4 |
| PagerDuty | Draft / In Review / Reviewed / Closed | 4 |
| Cloudflare postmortem | apology, impact, mechanism, remediation, timeline | 5 |
| Keep a Changelog | Added, Changed, Deprecated, Removed, Fixed, Security | 6 |
| Oxide RFD | prediscussion, ideation, discussion, published, committed, abandoned | 6 |
| Amazon WBR | chart design, palette, time periods, charts per page | not a count |

Nobody freezes more than six parts. Amazon is the outlier that proves the point: what it
holds constant is the presentation itself, so the only thing that differs between two
meetings is the data.

Sources: https://support.atlassian.com/statuspage/docs/incident-communication-tips/ ·
https://response.pagerduty.com/after/post_mortem_process/ ·
https://blog.cloudflare.com/18-november-2025-outage/ · the ADR, changelog, RFD and WBR
links above.

---

## R3 — status is a shape or a named state

**Basecamp, Shape Up ch. 13.** Percent-done is rejected outright because "to-do lists
actually grow as the team makes progress", so the number moves in the direction that
flatters. The replacement is a position on a hill — still figuring it out, or now just doing
it — and "a dot that doesn't move is effectively a raised hand."
https://basecamp.com/shapeup/3.4-chapter-13 · https://basecamp.com/hill-charts

**Oxide** gives an RFD a named state, not a completion figure.

**Kanban Guide** defines Work Item Age and Cycle Time — elapsed-time facts, not estimates.
https://kanbanguides.org/english/

**Spotify's squad health check** attaches a trend arrow to each colour, so direction carries
as much as level. Its own authors warn that used as a ranking it makes teams hide problems.
https://engineering.atspotify.com/2014/09/squad-health-check-model

### What happens when status is a single compressed judgement

**Watermelon reporting.** Green outside, red through. The stated cause is price, not
dishonesty: honesty has been "made personally expensive."
https://www.cultivatedmanagement.com/watermelon-reporting/

**Keil, Smith, Iacovou & Thompson, MIT Sloan Management Review, Spring 2014**, drawing on 14
studies over 15 years. In one study of 56 experienced software project managers, managers
wrote biased reports **60% of the time**, and the bias was more than twice as likely to be
optimistic as pessimistic. Companion paper (JAIS 15:12, 2014) is grounded theory over 118
interviews across 9 IT projects.
http://marketing.mitsmr.com/PDF/MITSMR-The-Pitfalls-of-Project-Status-Reporting.pdf

**Burn-down charts** fail because the estimate is made when least is known and the chart
assumes an end date ongoing products do not have (Allan Kelly).
https://www.allankelly.net/archives/902/burn-down-charts-good-bad-and-ugly-and/

---

## R4 — show the thing, 450 words

**The 450 comes from two pages by one author, and the wider field has no study of it.** The two pages: the worst
picture-free stretch was 453 words on the page the reader accepted and 1,491 on the page the
reader rejected. 450 is the ceiling that number produces, and the grader FAILs above it.

**Words per picture.** The accepted reference page runs 85 words per picture, 14
screenshots, and zero blocks of quoted source. Rejected pages ran 221 words per
picture with 8 to 40 `<pre>` blocks. So 85 is the grader's WARN line; its FAIL line, 150,
has no source beyond sitting between those two measurements.

**Text plus diagrams is the strongest finding in the multimedia literature.** Cromley & Chen
(2025), *Educational Research Review* 49:100730 — meta-analysis of Mayer's corpus, 92
articles, 181 studies, 591 effects, 1990–2022. Overall g = 0.37, and: "Large, consistent
effects were found for text + diagrams across factual, inferential and transfer outcomes."
Animation, games and simulations were inconsistent; virtual reality had no significant
effect. https://www.sciencedirect.com/science/article/pii/S1747938X25000673

**Pictures instead of words is not what the evidence says.** Learning styles do not survive
testing (Pashler et al. 2008/2009; Rogowsky et al. 2015, 121 adults, no significant
preference-by-method relationship; Massa & Mayer 2006, no attribute-by-treatment
interaction). The support is for words *and* pictures together, for everybody.
https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/Pashler_McDaniel_Rohrer_Bjork_2009_PSPI.pdf

**One distinctive picture beats five similar ones.** Higdon et al. 2025 attribute picture
superiority to distinctiveness rather than dual coding, and the effect reverses under fast
presentation — a picture needs dwell time to pay off.
https://journals.sagepub.com/doi/10.1177/17470218241235520

**The mark is the evidence.** A raw crop with a caption underneath is weaker than the same
crop with an amber band over the region and a caption naming the band. This came from the
user's own page, not from the literature.

**Seductive details** — the decorative screenshot, the interesting aside — reliably harm
recall and comprehension. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10176302/

---

## R5 — draw only what was measured

No external citation. The rule comes from the failure it prevents: a drawing is the one
element on the page a reader accepts without checking, so an invented drawing is worse than
an absent one. It is the local form of the finding in §XAI below — an explanation that is
satisfying and vacuous is indistinguishable from the inside.

**Placebic vs actionable explanations.** Participants given actionable explanations
significantly outperformed others on objective measures of their mental model, and rated
placebic explanations **equally satisfying**. https://arxiv.org/abs/2512.06591

**The evaluation critique.** Subjective satisfaction cannot distinguish meaningful from
vacuous explanation; expert users experienced an illusion of understanding from insufficient
explanations. https://arxiv.org/pdf/2511.03730

**Illusion of explanatory depth.** Rozenblit & Keil 2002: people rate their understanding
high, fail to produce the causal steps, then revise downward — and the illusion is
*strongest* where the environment supports real-time explanation with visible mechanisms,
which is exactly a diagram. https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog2605_1

Practical consequence: state the alternative that was rejected and what would have to be
true for it to win. A counterfactual is the form that lets a reader contest rather than
accept. https://arxiv.org/pdf/2204.10152

---

## R6 — a page nobody must open is dead

**Cockburn, *Agile Software Development* ch. 3 (2001).** Two criteria for a working display:
the information changes, and it costs very little energy to look at. His verdict:
"Hallways qualify very nicely as good places for information radiators. Web pages don't",
because accessing the page costs more effort than people will spend "and so the information
stays hidden."
https://athena.ecs.csus.edu/~buckley/CSc231_files/ACockburn_Agile_SW_Development_Ch3.pdf

**BARC, 214 companies, April 2022.** 25% of employees actively use BI tools, with "minimal
growth in the past seven years we've been tracking this metric."
https://barc.com/news/new-study-identifies-drivers-of-bi-and-analytics-adoption-in-companies-today/
The often-quoted "60–70% of dashboards go unused, per Gartner" traces to a LinkedIn post,
not a Gartner publication. Use the BARC figure.

**What survived, and the obligation welded to each.**

- Amazon WBR: every metric owner must speak for their own graph and may not skip one.
- Toyota andon: the operator may pull the cord and stop the line.
- ThoughtWorks corridor poster: it is in the corridor, so looking costs nothing.
- The one web page that worked (Fowler, via Cockburn): it rebuilt every 15 minutes and
  emailed the named people whose tests failed.
- Google SRE: refuses to have anyone watch a screen at all; alerts carry the obligation.
  https://sre.google/sre-book/monitoring-distributed-systems/

**Wording decides whether a radiator is read.** Cockburn: a board headed "Things we did
wrong last increment" was ignored; "Things to work on this increment" was referred to often.
Same data, opposite fate.

---

## Why the dense chip grid is banned

**Search is serial.** Nothing in a grid of identical labelled tiles is preattentive — hue,
luminance, orientation, size and motion are; words are not. Preattentive search is flat in
set size at 200–250ms; text search is linear. 32 chips at ~230ms each is about 7 seconds
before the reader has learned anything, against a page budget of roughly 25 seconds plus
4.4 seconds per 100 words. https://ics.uci.edu/~majumder/vispercep/preattentiveproc.pdf ·
https://search.bwh.harvard.edu/new/pubs/StevensHndbk_VisualSearch_Wolfe_2018.pdf

**Crowding.** In a dense display a nearest-neighbour rule governs: only the chip at fixation
is legible, and every other chip on screen is texture — a summary-statistic representation
that knows something text-like is there and cannot read any of it.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8284675/ ·
https://journals.sagepub.com/doi/full/10.1177/2041669520913052

**Gestalt works against the content.** Equal spacing, identical styling and identical
bounding boxes assert that all items are equals. If 8 of 32 are blocked on the reader, the
strongest visual signal on the page contradicts the most important fact in the document,
and grouping is perceived before labels are read.

**Legends.** Every house style in the field says delete the key and label directly — Urban
Institute ("When possible, directly label the data in the chart and omit the legend"),
Datawrapper ("remove the color key and directly label your categories"), BBC bbplot, the
Economist, FT Visual Vocabulary. A 32-chip index is a legend at document scale, sitting
screens away from what it decodes. https://urbaninstitute.github.io/graphics-styleguide/ ·
https://www.datawrapper.de/blog/text-in-data-visualizations

**Stacked bars.** Cleveland & McGill's ranking (replicated by Heer & Bostock 2010) puts
length third and colour last; a stacked bar makes the reader use both. Six small integers
written as numerals are exact and need no legend. https://dl.acm.org/doi/10.1145/1753326.1753357

---

## Titles: what is measured, and what is folklore

**The ceiling on concreteness.** Aubin Le Quéré & Matias, *Scientific Reports* 2025 — 8,977
Upworthy tests, 35,910 headline instances, concreteness scored against Brysbaert's 40,000-word
norms (validated r = 0.61 against 176 human raters). Interaction −0.058, p < 0.001. Where a
test was low in concreteness (8.7% of tests) more concreteness *raised* CTR 5.5% relative;
where it was already high (50.9% of tests) more concreteness *lowered* it 9.9% relative. An
inverted U. https://pmc.ncbi.nlm.nih.gov/articles/PMC11704130/

**The tease is penalised.** Facebook 2014 defined clickbait as a headline that "encourages
people to click to see more, without telling them much information about what they will
see", reported 80% of surveyed users preferred headlines that helped them decide before
clicking, and demoted on dwell time and click-to-like ratio. In 2016 it added a trained
classifier. https://about.fb.com/news/2014/08/news-feed-fyi-click-baiting/ ·
https://about.fb.com/news/2016/08/news-feed-fyi-further-reducing-clickbait-in-feed/

**Clickbait costs credibility.** Molyneux & Coddington, *Journalism Practice* 14(4) 2019:
clickbait headlines lowered perceived credibility and quality. A ~200-participant experiment
(IEEE TTS 2021) found clickbait reduced credibility and was *not* significantly clicked more.

**The hooky title wins the click and loses the follow-through.** Jamali & Nikzad,
*Scientometrics* 2011, ~1,900 PLoS articles: question-format titles were downloaded more and
cited less. http://eprints.rclis.org/19669/1/Jamali_title.pdf

**Front-load.** NN/g 2009, 80 participants, links truncated to 11 characters: comprehension
of the destination ranged 85% (plainly named) to 0% (a link starting "Introducing"); 35% of
links left users unable to say where they led.
https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/

**Questions vs statements as headings: no difference.** Hartley & Trueman, *British Journal
of Educational Psychology* 53, 205–214 (1983) — a summary of nine experiments. GOV.UK
forbids question headings and plainlanguage.gov recommends them; neither cites an
experiment, and the one measurement found no overall difference.

### Do not cite these

- **"80% read the headline, 20% read the body" / "five times as many read the headline."**
  Ogilvy, *Confessions of an Advertising Man*, 1963, with no study, sample or citation. The
  80% almost certainly mutated from his separate line about spending eighty cents of the
  dollar on the headline — a claim about *budget*, not readership. The chain ends at the
  1920s Starch magazine recognition survey.
- **Miller 7±2.** About recall of chunks from short-term memory, and Miller treated the
  number as a rhetorical device. Cowan (2001) revised it to 3–5, still about items held in
  memory rather than items visible on a screen. A sorted list of 500 items works fine because
  the reader indexes into it. The chip grid fails because it is unsorted and offers no
  guiding feature, not because 32 > 4.
- **Hick's law.** Holds when the reader can anticipate where a target sits in an *ordered*
  set; Landauer & Nachbar got logarithmic response times over up to 4,096 ordered candidates.
  Where the reader must visually scan and evaluate each option, the relationship is linear in
  n. https://www.csse.canterbury.ac.nz/andrew.cockburn/papers/paper191-cockburn.pdf
- **Data-ink ratio as a maximisation target.** Contested; embellished charts were found no
  less accurate and better recalled. The narrow claim that does survive: a chart encoding six
  small integers less precisely than typing them, while adding a legend, is a loss.
- **"60–70% of dashboards go unused (Gartner)."** Traces to a LinkedIn post.
- **The Standish CHAOS failure rates.** Eveleens & Verhoef reproduced the method over 5,457
  forecasts across 1,211 projects and found the definitions "misleading, one-sided" — it
  measures estimation accuracy and calls it success.
  https://www.cs.vu.nl/~x/the_rise_and_fall_of_the_chaos_report_figures.pdf

---

## Type sizes

APCA ties minimum size to contrast rather than giving a flat number.
https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html

- **Lc 90**, preferred for fluent body text: no smaller than 18px/300 or 14px/400;
  non-body text no smaller than 12px/400.
- **Lc 75**, the minimum for columns of body text: 24px/300, 18px/400, 16px/500, 14px/700.
- **Lc 60**, minimum for content text that is not body or column text: 24px/400, 21px/500,
  18px/600, 16px/700.

12px/400 is the floor for *incidental* text at the highest contrast level. It was used for 32
items of primary navigation on a rejected page. Urban Institute's own chart-label minimum —
the most compressed text in the discipline — is 12px for axis labels and 14px for legends.

Datawrapper's rule when text does not fit is the one to follow: "find another solution",
rather than making it smaller or narrower.
