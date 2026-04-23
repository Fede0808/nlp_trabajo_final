# The Story of This Repo

## The Opening Move

This repository does not tell the story of a sprawling product team. It tells the story of a focused academic build sprint. On **April 19, 2026**, the project appears almost fully formed in a sequence of seven commits, all authored by **Federico Blasco**, moving from scaffold to a CPU-aware NLP pipeline in a single day.

That compressed timeline matters. This is not a repo that grew over months of feature pressure. It is a repo that was assembled with a clear destination already in mind: a final assignment that needed technical rigor, reproducibility, and a convincing narrative.

## The Chronicles: A Year in Numbers

- **Total commits**: 7
- **Commits in the last year**: 7
- **Active months in the last year**: 1
- **Active month by volume**: 2026-04 with all 7 commits
- **Merge commits**: 0
- **Visible contributors**: 1

The numbers say this is a young repository, but not an accidental one. The lack of merges and the single-author history suggest an intentional solo effort rather than an evolving shared codebase.

## Cast of Characters

### Federico Blasco

Federico is effectively the entire cast, but the commit history still reveals changing roles:

- **Project framer** in `chore: initial project scaffold`
- **Assignment archivist** in `chore: add doc directory for assignment files`
- **Constraint setter** in `chore: add assignment prompt and context`
- **Process designer** in `chore: git hygiene and project management docs`
- **Builder** in `feat: add cpu-only nlp pipeline modules`
- **Narrator** in `docs: add project notebooks and progress tracking`
- **Environment custodian** in `chore: ignore local workspace settings`

That progression is telling: the repo begins with structure and rules before it earns its models. The author does not start by training. He starts by making the work legible.

## Seasonal Patterns

There is only one visible season here, and it is intense: **April 2026**.

Instead of a long arc with quiet months and bursts of delivery, this repository shows a concentrated build window. That often happens in academic projects: the timeline is external, the milestones are known ahead of time, and the repo is created when the work becomes concrete enough to need disciplined reproducibility.

In other words, this is less “product drift over time” and more “mission assembly.”

## The Great Themes

### 1. Constraints before ambition

The most important story in this repo is not “train a model.” It is “train something defensible on a normal CPU machine.” The project repeatedly encodes that constraint:

- conservative Torch thread settings
- RAM-aware sample sizing
- distilled Transformer choice instead of a larger BERT variant
- dynamic quantization for CPU inference

This repo treats hardware limits as a first-class design input, not an afterthought.

### 2. Shared preprocessing as a fairness contract

Another strong theme is fairness in comparison. The canonical `texto_limpio` column is more than a convenience; it is a methodological commitment. By ensuring that both the SVM and the Transformer consume the same cleaned text foundation, the repo protects the comparison from turning into an apples-to-oranges benchmark.

### 3. Academic narrative as architecture

Many codebases bolt documentation on later. This one bakes the course structure directly into the repo:

- `Fase 0` through `Fase 5`
- notebooks aligned to those phases
- planning documents in `doc/`
- a local API because the assignment requires something operational, not just analytical

The architecture reflects the rubric.

## Plot Twists and Turning Points

### Turning point 1: from scaffolding to rules

The first commits are chores, but they are not empty chores. They define the repo boundaries, the assignment framing, and the hygiene rules. This creates a project that knows what it is supposed to be before it contains much code.

### Turning point 2: the pipeline lands in one shot

The commit `feat: add cpu-only nlp pipeline modules` is the repo’s real act break. That is where the codebase stops being a prepared workspace and becomes a system:

- hardware helpers
- corpus preparation
- cleaning
- evaluation
- artifact storage
- API
- Transformer support

That single commit carries most of the operational identity of the repository.

### Turning point 3: the notebooks make it teachable

The later docs commit adds notebooks and progress tracking. That move transforms the repo from “engine” to “submission.” The code now has a guided tour, which matters in an academic setting where explanation is part of the deliverable.

### Turning point 4: the Transformer becomes a logistical problem

The current uncommitted work introduces a subtle but important shift. The Transformer phase is no longer just a modeling task; it becomes a logistics and reproducibility task centered on offline weight availability. The repo now explicitly distinguishes between:

- having the tokenizer cached
- having the actual model weights cached
- being able to complete the deep-learning phase offline

That is a mature move. It turns a vague blocker into a documented condition.

## The Current Chapter

Right now, the repository is in its “hardening for delivery” chapter.

The baseline path is strong:

- the SVM is trained and serializable
- the API serves the baseline
- the smoke test script produces metrics, confusion matrices, and class-level diagnostics

The deep-learning path is closer than before, but still conditional:

- the repo had a prepared Transformer workflow
- the local cache now includes tokenizer access
- the remaining question has been whether the model weights exist locally and can be used offline in a fully reproducible way

The latest layer of work pushes the repo toward something stronger than a technical experiment: a submission that can explain its own limits honestly. That may end up being the defining quality of the project. Not just that it compares SVM and Transformers, but that it does so under real-world CPU constraints, with explicit evidence, and without pretending the environment is more generous than it is.

## What This Repo Is Really About

On the surface, this is a text classification repository about Argentine real-estate listings.

Underneath, it is a repo about making an ambitious NLP assignment fit inside ordinary local hardware without losing methodological dignity. It is a small codebase with a very clear personality: practical, constrained, academically accountable, and increasingly self-aware about the difference between “the code exists” and “the result is truly reproducible.”
