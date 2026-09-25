---
name: research-defense-ppt
description: Structure, refine, or review scientific presentation decks and defense scripts, especially Chinese graduate research/transfer-PhD PPTs. Use when the task is to organize or optimize a research talk around a clear narrative such as background -> requirements -> scheme -> design -> testing -> optimization -> iteration, adapt explanations to mixed physics/electronics audiences, or turn technical slides into natural oral scripts.
---

# Research Defense PPT

Use this skill for research-report, thesis-defense, transfer-PhD, or stage-review PPT work where the core job is not just editing slides, but building a convincing scientific narrative from the actual research process.

## Core workflow

Start from the research logic, not the slide order:

1. Clarify the scene
2. Identify audience background and likely concerns
3. Extract the real project backbone
4. Map that backbone onto the existing PPT
5. Tighten transitions and evidence
6. Rewrite for oral delivery if needed

For mixed committees, especially "mostly physics, some electronics":

- Physics-facing explanations: give the correct high-level physical reason, then return to your real boundary.
- Electronics-facing explanations: answer why the design was chosen, how it was verified, and what the current limits are.

## Default narrative spine

For most scientific engineering decks, prefer this progression:

`Background -> Requirements -> Scheme -> Design -> Testing -> Optimization -> Iteration`

Do not force every project into identical proportions. The backbone stays the same, but emphasis shifts by deck type.

## How to apply the spine

### 1. Background

Goal: explain why the problem matters and what physical / engineering context defines it.

Good background answers:

- What is the object or phenomenon?
- Why is it worth measuring / controlling / building?
- What application scenarios matter?
- Why does this problem naturally lead to this type of detector or control system?

Avoid:

- Long textbook exposition with no connection to the later design
- Listing options without explaining why the final route is chosen

For this user's muon-imaging PPT, strong background means:

- Explain where muons come from and why they are usable
- Distinguish application scenarios
- Explain why those scenarios lead to specific detector-readout constraints
- Explain why the project settles on `plastic scintillator + SiPM`, not just that it does

### 2. Requirements

Goal: convert the scientific target into concrete engineering demands.

Good requirement slides answer:

- What must the system handle?
- What environmental or deployment constraints exist?
- What must be read out / stabilized / triggered / controlled?
- What are the shared demands across scenarios?

In this user's deck, the requirement layer is where:

- plastic scintillator arrays imply multi-channel readout
- SiPM implies gain sensitivity, bias management, and dark-noise-trigger issues
- different detector geometries imply packaging / deployment constraints

### 3. Scheme

Goal: justify the chosen technical route before diving into implementation.

Good scheme slides compare alternatives and explain selection criteria:

- feasibility
- complexity
- deployment suitability
- maturity
- maintainability

Important: "scheme" is not yet board-level details. It is the bridge from requirements to architecture.

Example from this user's deck:

- compare gas detector / TPC / plastic scintillator routes
- explain why TPC has richer tracking information but higher field, gas, readout, and deployment complexity
- explain why plastic scintillator + SiPM better fits large-area and in-situ deployment

### 4. Design

Goal: show how the chosen route is concretely implemented.

Typical design layers:

- system architecture
- key device / ASIC selection
- front-end implementation
- backend / DAQ implementation
- trigger logic
- software / control path

Each design page should answer one implicit question:

- Why this partition?
- Why this chip or method?
- What function is implemented here?
- How does it connect to the next layer?

Avoid turning design pages into part lists.

### 5. Testing

Goal: prove the system actually works.

Testing should progress from component-level to system-level:

- calibration / pedestal / baseline
- linearity / dynamic range / noise
- detector-electronics integration
- long-run acquisition
- physics-relevant spectra or residuals

Do not just read plot labels aloud. Explain what the figure proves.

Useful pattern:

- what was tested
- what the figure shows
- what conclusion is justified

### 6. Optimization

Goal: show that the work is not static and that limitations are understood.

Optimization can include:

- threshold tuning
- gain compensation
- trigger tuning
- noise reduction
- structural refinement
- algorithm improvements

Be concrete. "Optimization" should not become a vague promise.

### 7. Iteration

Goal: show next-step logic, not just a wish list.

Strong iteration answers:

- what works already
- what remains limited
- what will be improved next
- why that next step follows naturally from current results

For transfer-PhD or proposal decks, this often becomes:

`Completed master's closed loop -> transferable capabilities -> doctoral research entry point`

## Special guidance for transfer-PhD decks

A common structure is:

- master's background and completed work
- accumulated capabilities
- transition page
- doctoral positioning
- research boundary
- phased plan
- relation to lab / national mission

The transition page is critical. It must show:

- not only what was built
- but what capability was formed
- and why the doctoral topic is a continuation in methods / control / system integration

For this user:

- completed loop: requirements -> architecture -> FEE -> DAQ -> trigger -> software -> integration validation
- formed abilities: electronics system design, FPGA control, hardware-software coordination, debugging and integration
- transition logic: move from detector readout control to precision frequency-control loops

## Script-writing rules

When rewriting a script from slides:

- write page by page
- keep one main point per page
- add explicit transitions
- sound like spoken explanation, not slide annotation
- reduce repetitive openers like "this page mainly shows"
- compress the front half if it is background-heavy
- make the doctoral / proposal half steadier and more deliberate

If the requested style is plain and direct:

- prefer declarative sentences
- reduce filler such as "the purpose is", "in other words", "as we can see"
- explain figures instead of paraphrasing every bullet

## Figure-explanation rule

For any important plot or schematic, answer three things:

1. What is this figure showing?
2. Why is it on this page?
3. What conclusion can be safely drawn?

Examples:

- cosmic-ray cascade figure: explains the origin of atmospheric muons and why muons reach ground level
- pedestal figure: shows baseline distribution and noise stability, not "negative charge deposition"
- Landau-like spectrum: shows separation of noise and muon events and supports valid event readout

## Q&A preparation rule

When generating likely committee questions:

- separate physics-heavy questions from electronics-heavy questions
- include "transfer-PhD / why this topic" questions
- include short, defensible answers
- for deep physics questions, answer at the right level and return to your boundary

Useful answer pattern:

`High-level correct statement -> system-level relevance -> your actual contribution / boundary`

## Common pitfalls

- Background too long, but still not answering "why this route"
- Requirement slides that list constraints without converting them into engineering demands
- Scheme slides that compare options without making a choice
- Design slides that become component descriptions instead of design reasoning
- Test slides that read figure labels without stating the conclusion
- Final summary that repeats content but does not close the argument

## Output checklist

Before finishing, verify:

- the deck follows a visible research logic
- each major section answers a different question
- key figures are interpreted, not recited
- route selection is justified
- test evidence supports the claims
- optimization and iteration are specific
- for transfer-PhD decks, the master's-to-PhD transition is explicit
