# Benchmark Gaming Risk vs Raw Coding Generalization in Frontier Coding Models

Run date: 2026-06-21

## Executive Summary

Highest benchmark-gaming risk in this review: DeepSeek, Moonshot/Kimi, Z.ai/Zhipu, MiniMax, and xAI. The common pattern is strong public or crowd-visible coding benchmark evidence with weaker same-model private repo-level evidence, larger scaffold variance, or missing disclosure about attempts, budget, and tools.

Strongest evidence of raw coding generalization: Anthropic, OpenAI, Meta, and Google DeepMind. These labs have stronger support from private or harder repo-level benchmarks such as Scale SWE-Bench Pro Private, Scale SWE-Bench Pro Public, SWE-bench Verified, Terminal-Bench, and CodeClash-style evaluations.

Biggest uncertainties: model identity drift, agent scaffold differences, inference-budget differences, hidden pass@k or retry policies, and missing private/live evidence for several frontier models. Arena and public leaderboard results are useful signals, but they are not substitutes for hidden-test private repo evaluations.

## Important Caveat

Benchmark-gaming risk is not proof of intentional cheating or any other misconduct. It is an evidence-based estimate from public-vs-private performance gaps, contamination risk, reporting practices, scaffold dependence, and leaderboard incentives. Public benchmark gaps are evidence of risk, not proof of misconduct.

## Benchmark Taxonomy

1. Saturated public coding puzzles: HumanEval, MBPP, HumanEval+, MBPP+, BigCodeBench-style public task sets.
2. Public competitive-programming datasets: APPS, CodeContests, historical Codeforces, LeetCode, and AtCoder snapshots.
3. Public repo-level patch benchmarks: SWE-bench Full, SWE-bench Lite, SWE-bench Verified, public SWE-Bench Pro.
4. Public agentic coding leaderboards: Aider Polyglot, Terminal-Bench public submissions, Arena/WebDev-style leaderboards.
5. Live/post-release contest benchmarks: newest-window LiveCodeBench, fresh Codeforces, AtCoder, and LeetCode contest problems.
6. Private/held-out repo-level software-engineering evals: SWE-Bench Pro Private, SWE-Bench Pro Held-out, private company-repo tasks.
7. Private enterprise-code or paid-task evals: proprietary enterprise repositories, SWE-Lancer-style paid freelance tasks, hidden tests with human verification.
8. Custom internal hidden-test evals: internal unreleased repositories, fixed tool budgets, multiple graders, private holdout rotation.

## Vulnerable Benchmarks

### Vulnerability Mechanism Matrix

| benchmark | age and public availability | contamination and saturation risk | reporting and scaffold inflation risk |
|---|---|---|---|
| HumanEval | Public since 2021; small 164-task set. | Very high: widely mirrored, discussed, and saturated. | Very high: frequently vendor-reported; pass@k, retries, and prompt tuning can move scores. |
| HumanEval+ | Public EvalPlus derivative of HumanEval. | High: stronger tests, same public task family. | High: public harness allows repeated tuning against known failure modes. |
| MBPP | Public since early code-generation benchmark work; about 1,000 entry-level Python tasks. | Very high: simple tasks, few original tests, broad exposure. | Very high: frequently reported; few-shot prompting and repair loops can inflate results. |
| MBPP+ | Public EvalPlus derivative of MBPP. | High: expanded tests reduce false positives but do not remove public exposure. | High: public harness and known task distribution remain optimizable. |
| APPS | Public 2021 competitive-programming benchmark. | High: old contest-style tasks and solutions are common online. | High: execution-based filtering, retries, and algorithmic scaffolds can materially help. |
| CodeContests | Public competitive-programming dataset. | High: contest problems and solutions are web-exposed; dataset was used in model training research. | High: sampling, execution selection, and contest-specific prompting can inflate results. |
| Historical Codeforces/LeetCode/AtCoder | Old public contest windows and archived solutions. | Very high for historical windows; lower for fresh post-release windows. | High: model teams often report contest-style scores; solution search space favors retries. |
| SWE-bench Full | Public real GitHub issue benchmark from 2023-2024 era work. | Medium-High: realistic but public and heavily studied. | High: agent scaffold, repository retrieval, patch selection, and test strategy matter. |
| SWE-bench Lite | Public 300-task subset. | High: smaller set enables faster iteration and saturation. | Very high: cheap iteration makes scaffold hillclimbing easier. |
| SWE-bench Verified | Public 500-task human-filtered subset. | Medium-High: better quality but highly visible and leaderboard-optimized. | High: bash-only vs tool-calling versions and mini-SWE-agent versions are not always comparable. |
| Public Aider Polyglot | Public 225-task Exercism-derived benchmark. | High: fixed tasks and public commands. | Very high: pass-rate-1 vs pass-rate-2, edit format, and retry strategy materially affect scores. |
| Public BigCodeBench/Hard | Public practical coding benchmark with full and hard splits. | Medium-High: stronger than tiny puzzles, but public and contamination-aware. | Medium-High: library use, task style, and calibrated pass@1 details matter. |
| WebDev Arena / LMArena coding | Public crowd-preference arena. | Medium-High: prompts are not a fixed public dataset, but leaderboard incentives are visible. | Very high: response style, model variant, UI, and crowd preference can dominate correctness. |

### HumanEval

- Description: 164 hand-written Python programming problems with unit tests from OpenAI's code-generation evaluation work ([HumanEval repo](https://github.com/openai/human-eval)).
- Vulnerability rating: Very High.
- Why vulnerable: public since 2021, small, widely reported, likely included in benchmark-aware training/evaluation workflows, and often reported with pass@k variants.
- Supporting evidence: the official repo exposes the task format and evaluation harness; the benchmark is small enough for repeated prompt/scaffold iteration.
- Non-intent over-optimization path: tune prompts, sampling, retries, or post-processing against the known task style and hidden-test distribution.

### HumanEval+

- Description: EvalPlus-expanded HumanEval with substantially more tests than the original ([EvalPlus](https://github.com/evalplus/evalplus)).
- Vulnerability rating: High.
- Why vulnerable: stronger tests reduce false positives, but the task set remains public, small, and derived from HumanEval.
- Supporting evidence: EvalPlus is explicit about evaluating HumanEval/MBPP variants with expanded tests.
- Non-intent over-optimization path: tune to EvalPlus harness behavior or common failure modes while still benefiting from public problem exposure.

### MBPP

- Description: about 1,000 crowd-sourced entry-level Python problems, each with a description, reference solution, and three tests ([MBPP repo](https://github.com/google-research/google-research/tree/master/mbpp)).
- Vulnerability rating: Very High.
- Why vulnerable: old, public, simple, and has very few visible tests per problem.
- Supporting evidence: the official README documents the dataset structure and splits.
- Non-intent over-optimization path: train or tune on similar simple Python snippets and optimize few-shot examples for the task style.

### MBPP+

- Description: EvalPlus-expanded MBPP evaluation ([EvalPlus](https://github.com/evalplus/evalplus)).
- Vulnerability rating: High.
- Why vulnerable: expanded tests improve correctness checking but do not make the public task set private or fresh.
- Supporting evidence: EvalPlus provides public evaluation commands and dataset variants.
- Non-intent over-optimization path: iterate prompts and repair loops against a public harness.

### APPS

- Description: 10,000 programming problems ranging from simple introductory tasks to algorithmic competition problems ([APPS paper](https://openreview.net/forum?id=sD93GOzH3i5)).
- Vulnerability rating: High.
- Why vulnerable: public since 2021, heavily used, and built from competitive-programming style tasks that may overlap with web training data.
- Supporting evidence: the benchmark paper describes public problem, solution, and test-case structure.
- Non-intent over-optimization path: optimize for competitive-programming statement patterns, input parsing, and common algorithms.

### CodeContests

- Description: DeepMind competitive-programming dataset used in AlphaCode work ([CodeContests repo](https://github.com/google-deepmind/code_contests)).
- Vulnerability rating: High.
- Why vulnerable: public competitive-programming problems are common in training data and leaderboard work.
- Supporting evidence: the official repository describes the dataset as competitive-programming problems from multiple sources.
- Non-intent over-optimization path: train or fine-tune on similar contest problems and use execution-based selection.

### Historical Codeforces, LeetCode, and AtCoder Snapshots

- Description: static historical contest/task snapshots used in many coding evaluations.
- Vulnerability rating: Very High for old static data; Medium to High for carefully windowed recent data.
- Why vulnerable: older contest tasks and discussions are widely mirrored online; solutions often appear in repositories, blogs, and forums.
- Supporting evidence: LiveBench and LiveCodeBench were created partly to avoid stale benchmark contamination through fresh monthly or contest-sourced tasks ([LiveBench](https://livebench.ai/), [LiveCodeBench](https://livecodebench.github.io/leaderboard.html)).
- Non-intent over-optimization path: train on public solutions or tune on known contest families without targeting any specific benchmark.

### SWE-bench Full

- Description: 2,294 real GitHub issue/PR tasks across Python repositories, requiring repository reasoning and patch generation ([SWE-bench paper](https://openreview.net/forum?id=VTF8yNQM66), [SWE-bench](https://www.swebench.com/)).
- Vulnerability rating: Medium-High.
- Why vulnerable: much more realistic than puzzle benchmarks, but public and heavily optimized since release.
- Supporting evidence: the benchmark is public, later variants such as Verified, Multilingual, and Pro exist partly to improve reliability and robustness, and newer dynamic benchmark papers such as SWE-rebench and SWE-MERA explicitly frame static SWE benchmarks as vulnerable to contamination or outdated task distributions ([SWE-rebench](https://arxiv.org/abs/2505.20411), [SWE-MERA](https://arxiv.org/abs/2507.11059)).
- Non-intent over-optimization path: optimize agent scaffolds, retrieval, patch validation, and retry loops against public repositories and issue styles.

### SWE-bench Lite

- Description: smaller SWE-bench subset designed for faster and cheaper evaluation ([SWE-bench Lite](https://www.swebench.com/lite.html)).
- Vulnerability rating: High.
- Why vulnerable: smaller public subset, easier to iterate on, and heavily used for quick leaderboard comparisons.
- Supporting evidence: official SWE-bench pages list Lite separately from Verified and Multilingual.
- Non-intent over-optimization path: repeatedly tune the agent scaffold and patch-selection strategy on the smaller task distribution.

### SWE-bench Verified

- Description: 500-instance human-filtered SWE-bench subset reviewed for task quality and solvability ([SWE-bench Verified](https://www.swebench.com/verified.html)).
- Vulnerability rating: Medium-High.
- Why vulnerable: stronger than Full/Lite in quality, but public, saturated, and sensitive to scaffolds, tool-calling versions, and run configuration.
- Supporting evidence: the Verified page documents bash-only and mini-SWE-agent settings and cautions that some versions are not directly comparable; SWE-rebench reports that some static SWE-bench-style performance may be inflated by contamination concerns ([SWE-bench Verified](https://www.swebench.com/verified.html), [SWE-rebench](https://arxiv.org/abs/2505.20411)).
- Non-intent over-optimization path: improve repository navigation, test selection, patch validation, and agent loops against a known public distribution.

### Public Aider Polyglot

- Description: 225 Exercism tasks across C++, Go, Java, JavaScript, Python, and Rust ([Aider leaderboard](https://aider.chat/docs/leaderboards/)).
- Vulnerability rating: High.
- Why vulnerable: public task set, public commands, edit formats, pass-rate-1/pass-rate-2 metadata, and two-attempt workflows.
- Supporting evidence: the leaderboard exposes command, date, edit format, reasoning effort, cost, and pass-rate details.
- Non-intent over-optimization path: tune edit format, retry strategy, and model settings to this fixed benchmark.

### Public BigCodeBench and BigCodeBench-Hard

- Description: practical programming benchmark with full and hard subsets, ranked by calibrated pass@1 ([BigCodeBench](https://bigcode-bench.github.io/)).
- Vulnerability rating: Medium-High.
- Why vulnerable: more practical than tiny puzzles, but public tasks and benchmark documentation enable repeated optimization.
- Supporting evidence: BigCodeBench explicitly discusses contamination concerns and public-data tradeoffs.
- Non-intent over-optimization path: tune for task style, library imports, and public harness constraints.

### WebDev Arena / LMArena-Style Coding Arenas

- Description: public crowd-preference coding arenas such as Arena's coding leaderboard ([Arena coding](https://arena.ai/leaderboard/text/coding)).
- Vulnerability rating: Medium-High.
- Why vulnerable: rankings are visible, preference-driven, and sensitive to response style, UI, prompt mix, and model variants.
- Supporting evidence: Arena reports model rankings from crowd votes rather than hidden correctness tests.
- Non-intent over-optimization path: optimize conversational coding style, verbosity, and visible user preference patterns.

## Robust Benchmarks

### Robustness Mechanism Matrix

| benchmark or eval type | privacy/freshness | task source and realism | hidden tests, tools, scaffold, reproducibility |
|---|---|---|---|
| SWE-Bench Pro Private | Private proprietary code; not publicly accessible. | 276 instances from 18 commercial codebases. | Hidden/private tasks; evaluator-run; strong robustness but not fully externally reproducible. |
| SWE-Bench Pro Held-out | Held-out split not used as the public leaderboard set. | 858 professional-repository tasks described by Scale. | Strong holdout value; outside auditability is limited. |
| SWE-Bench Pro Public | Public, but newer and harder than classic SWE-bench subsets. | 731 professional-repository tasks with multi-file patches. | Public leaderboard remains optimizable; harness notes and cost/turn limits matter. |
| SWE-Lancer private/closed splits | Private or partially closed; public Diamond split is weaker. | Real Upwork freelance software tasks with monetary payouts. | End-to-end tests and human verification are strong; full private access and reproducibility are limited. |
| Newest-window LiveCodeBench | Fresh contest windows reduce training exposure. | LeetCode, AtCoder, and Codeforces problems. | Hidden contest tests are useful; competitive programming is narrower than repo work. |
| Fresh post-release contests | Live after model release or cutoff. | Codeforces, AtCoder, and LeetCode contests. | Strong anti-contamination signal; requires strict date control and no solution leakage. |
| Private CodeClash-style arenas | Can be private or public depending on arena. | Multi-round codebase evolution and goal completion. | Evaluates long-horizon degradation; public arena details and model coverage can limit confidence. |
| Terminal-Bench 2.0 | Public leaderboard; task set and harness constrain terminal-agent behavior. | Terminal-based tool workflows. | Strong tool-use signal; agent scaffold differences remain a major confounder. |
| Private enterprise-repo evals | Private repos and hidden tests. | Real company codebases, debugging, features, tests, and maintenance. | Very robust if budgets and graders are fixed; often unauditable. |
| Custom internal hidden-test evals | Private rotating holdouts. | Unreleased repos or internal tasks. | Strong if independently governed; weak if methodology is undisclosed. |

### SWE-Bench Pro Private

- Description: 276 proprietary-code tasks from 18 private commercial codebases ([Scale SWE-Bench Pro Private](https://labs.scale.com/leaderboard/swe_bench_pro_private)).
- Robustness rating: Very High.
- Why harder to game: private repositories are not publicly accessible and are unlikely to appear in training data.
- Remaining weaknesses: evaluator-controlled and not fully reproducible by outside researchers; results may depend on mini-SWE-agent or similar harness settings.

### SWE-Bench Pro Held-out

- Description: held-out SWE-Bench Pro split described by Scale as 858 tasks across professional repositories ([Scale SWE-Bench Pro Public](https://labs.scale.com/leaderboard/swe_bench_pro_public)).
- Robustness rating: Very High.
- Why harder to game: held-out tasks reduce direct public optimization.
- Remaining weaknesses: outside parties cannot fully audit unreleased task composition or scoring.

### SWE-Bench Pro Public

- Description: 731 public professional-repository tasks with larger patches than SWE-bench Verified and stronger realism claims ([Scale SWE-Bench Pro Public](https://labs.scale.com/leaderboard/swe_bench_pro_public)).
- Robustness rating: High.
- Why harder to game: harder, more realistic multi-file software tasks than public puzzles or SWE-bench Lite; average reference solution is over 100 LOC across multiple files.
- Remaining weaknesses: public leaderboard and public tasks remain optimizable over time.

### SWE-Lancer Private or Closed Splits

- Description: real freelance software-engineering tasks with monetary payout framing and human verification ([SWE-Lancer repo](https://github.com/openai/SWELancer-Benchmark), [SWE-Lancer paper](https://arxiv.org/abs/2502.12115)).
- Robustness rating: High to Very High for closed/private splits; Medium for public split.
- Why harder to game: paid real-world tasks and human verification are closer to practical engineering value than isolated coding puzzles.
- Remaining weaknesses: public split can be trained against; private/full evaluation access may be limited.

### Newest-Window LiveCodeBench

- Description: fresh coding problems from LeetCode, AtCoder, and Codeforces contests, continuously updated ([LiveCodeBench](https://livecodebench.github.io/leaderboard.html), [Artificial Analysis](https://artificialanalysis.ai/evaluations/livecodebench)).
- Robustness rating: High.
- Why harder to game: recent post-release problems reduce training contamination and memorization risk.
- Remaining weaknesses: competitive programming is narrower than repo-level software engineering.

### Fresh Post-Release Codeforces, AtCoder, and LeetCode Contests

- Description: contest problems sourced after model training or release.
- Robustness rating: High.
- Why harder to game: solutions are unavailable before contest completion, and post-release timing reduces direct training exposure.
- Remaining weaknesses: still favors algorithmic puzzle skill over long-horizon repo maintenance.

### Private CodeClash-Style Arenas

- Description: goal-oriented, multi-round software-engineering tournaments where models evolve codebases over rounds ([CodeClash](https://codeclash.ai/)).
- Robustness rating: Medium-High.
- Why harder to game: multi-round codebase evolution and competitive goals expose degradation and long-horizon weaknesses.
- Remaining weaknesses: public benchmark details and limited model coverage make it less definitive than private enterprise-code evals.

### Terminal-Bench 2.0

- Description: terminal-agent benchmark with leaderboard submissions, model attribution, and restrictions on modifying timeouts/resources ([Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Robustness rating: High.
- Why harder to game: evaluates tool-using terminal workflows rather than isolated puzzle completion.
- Remaining weaknesses: results are strongly scaffold-dependent, and agent differences can dominate base-model differences.

### Private Enterprise-Repo Evals and Hidden-Test Company Tasks

- Description: unreleased company repositories, hidden tests, fixed tool budgets, and independent grading.
- Robustness rating: Very High when standardized.
- Why harder to game: private code, hidden tests, and realistic maintenance work reduce direct memorization and prompt tuning.
- Remaining weaknesses: often unauditable publicly and may not be reproducible.

### Custom Internal Hidden-Test Evals

- Description: internal held-out repositories, rotating tasks, hidden tests, fixed budget, and independent graders.
- Robustness rating: Very High when rigorously governed.
- Why harder to game: task rotation and private holdouts resist leaderboard hillclimbing.
- Remaining weaknesses: results are only credible if methodology, sampling, and grader independence are disclosed.

## Top 10 Lab/Model Scorecard

| rank | lab | model | benchmark-gaming risk | raw coding generalization | confidence | short rationale |
|---:|---|---|---:|---:|---:|---|
| 1 | DeepSeek | DeepSeek V3.2 / V3.2 Speciale | 75 | 60 | 68 | Strong public and live-contest evidence; weak Scale Pro public result and no same-model private result found. |
| 2 | Moonshot / Kimi | Kimi K2.5 / K2.6 | 68 | 64 | 66 | Strong SWE-bench/Arena evidence; sparse private evidence and lower Pro public support. |
| 3 | Z.ai / Zhipu | GLM-5 / GLM-5.1 | 65 | 68 | 64 | Strong public SWE-bench and Arena results; no current same-model private Pro result found. |
| 4 | MiniMax | MiniMax M2.5 / M2.7 | 64 | 68 | 62 | Very strong public SWE-bench result; private evidence missing and terminal results less dominant. |
| 5 | xAI | Grok 4.20 Reasoning / Grok 4 | 60 | 58 | 58 | Public/crowd evidence and one stronger terminal setup, but large scaffold variance and no private repo result found. |
| 6 | Alibaba / Qwen | Qwen3-Coder / Qwen3.7 Max Preview | 52 | 58 | 63 | Mixed evidence: solid Pro public, weaker terminal, no private result found. |
| 7 | Meta | Muse Spark | 49 | 82 | 76 | Strong Scale Pro private/public results; sparse model disclosures and lab-level reporting caution keep risk moderate. |
| 8 | Google DeepMind | Gemini 3.1 Pro / Gemini 3 Pro / Gemini 3 Flash | 45 | 80 | 80 | Strong live contest, private Pro, and terminal evidence; variant normalization caveats remain. |
| 9 | OpenAI | GPT-5.4 xHigh / GPT-5.3-Codex / GPT-5.5 | 39 | 88 | 85 | High public results are backed by strong Scale Pro, Terminal-Bench, and CodeClash evidence. |
| 10 | Anthropic | Claude Opus 4.6 / 4.7 | 35 | 89 | 86 | Strong public scores are matched by top private Pro and strong terminal evidence. |

## Lab-by-Lab Analysis

### DeepSeek

- Best current coding model: DeepSeek V3.2 / V3.2 Speciale.
- Public benchmark evidence: SWE-bench Verified lists DeepSeek V3.2 high reasoning at 70.0%; Artificial Analysis LiveCodeBench lists DeepSeek V3.2 Speciale at 89.6% ([SWE-bench](https://www.swebench.com/), [Artificial Analysis](https://artificialanalysis.ai/evaluations/livecodebench)).
- Robust/private/live evidence: Scale SWE-Bench Pro public lists deepseek-v3p2 at 15.56%; Terminal-Bench lists Terminus 2 DeepSeek-V3.2 at 39.6% ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Higher-risk pattern: strong public/live contest evidence does not carry through to stronger Pro public and terminal settings.
- Evidence against concern: LiveCodeBench is fresher and less contamination-prone than historical puzzles, so the live-contest result still supports real algorithmic ability.
- Unknowns: no same-model Scale Pro private result found; Speciale vs standard model relationship is unclear; scaffold and inference-budget details differ.
- Final score: benchmark-gaming risk 75; raw coding generalization 60; confidence 68.

### Moonshot / Kimi

- Best current coding model: Kimi K2.5 / Kimi K2.6.
- Public benchmark evidence: SWE-bench Verified lists Kimi K2.5 high reasoning at 70.8%, SWE-bench Multilingual lists Kimi K2.5 at 67.3%, and Arena coding lists Kimi K2.6 near the top public crowd-preference tier ([SWE-bench](https://www.swebench.com/), [SWE-bench Multilingual](https://www.swebench.com/multilingual-leaderboard.html), [Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Scale SWE-Bench Pro public lists Kimi K2 Instruct at 27.67%; Terminal-Bench lists Kimi K2.5 at 43.2% ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Higher-risk pattern: public SWE-bench performance is much stronger than Pro public and terminal results.
- Evidence against concern: Kimi has meaningful repo-level and terminal evidence; this is not a puzzle-only profile.
- Unknowns: no Scale Pro private result found; K2 Instruct, K2.5, and K2.6 are not directly interchangeable.
- Final score: benchmark-gaming risk 68; raw coding generalization 64; confidence 66.

### Z.ai / Zhipu

- Best current coding model: GLM-5 / GLM-5.1.
- Public benchmark evidence: SWE-bench Verified lists GLM-5 high reasoning at 72.8%, SWE-bench Multilingual lists GLM-5 at 69.7%, and Arena coding lists GLM-5.1/GLM-5.2 max in the top public tier ([SWE-bench](https://www.swebench.com/), [SWE-bench Multilingual](https://www.swebench.com/multilingual-leaderboard.html), [Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Terminal-Bench lists GLM 5 at 52.4%; Scale Pro public lists GLM 4.6 at 9.67%, but that is not the current GLM-5 model ([Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0), [Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public)).
- Higher-risk pattern: strong public leaderboard evidence with missing same-model private Pro support.
- Evidence against concern: terminal performance is mid-strong, suggesting some tool-using generalization beyond public SWE-bench.
- Unknowns: no current GLM-5 private Pro result found; GLM 4.6 Pro public result should not be treated as GLM-5 evidence.
- Final score: benchmark-gaming risk 65; raw coding generalization 68; confidence 64.

### MiniMax

- Best current coding model: MiniMax M2.5 / M2.7.
- Public benchmark evidence: SWE-bench Verified lists MiniMax M2.5 high reasoning at 75.8%; SWE-bench Multilingual lists MiniMax 2.5 at 68.3% ([SWE-bench](https://www.swebench.com/), [SWE-bench Multilingual](https://www.swebench.com/multilingual-leaderboard.html)).
- Robust/private/live evidence: Scale Pro public lists MiniMax 2.1 at 36.81%; Terminal-Bench lists MiniMax M2.5 variants around 42-43% ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Higher-risk pattern: extremely strong SWE-bench Verified result with weaker harder-eval support and no same-model private result found.
- Evidence against concern: Multilingual SWE-bench and terminal evidence show broader coding ability than one benchmark.
- Unknowns: M2.1, M2.5, and M2.7 comparisons are imperfect; no Scale Pro private result found for the current model.
- Final score: benchmark-gaming risk 64; raw coding generalization 68; confidence 62.

### xAI

- Best current coding model: Grok 4.20 Reasoning / Grok 4.
- Public benchmark evidence: Aider Polyglot lists Grok-4 high at 79.6% pass-rate-2; BigCodeBench lists Grok-3-Beta near older frontier results; Arena coding lists Grok 4.20 multi-agent beta near the top tier ([Aider](https://aider.chat/docs/leaderboards/), [BigCodeBench](https://bigcode-bench.github.io/), [Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Terminal-Bench lists Grok 4.20 Reasoning at 57.3% in one CLI setup, but other Grok 4 agent setups are much lower; no Scale Pro private result found ([Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Higher-risk pattern: evidence is unusually scaffold-sensitive and public/crowd-heavy.
- Evidence against concern: a 57.3% Terminal-Bench result is meaningful tool-using evidence.
- Unknowns: no private repo-level result found; Grok 4, Grok 4.20, and multi-agent variants are not directly comparable.
- Final score: benchmark-gaming risk 60; raw coding generalization 58; confidence 58.

### Alibaba / Qwen

- Best current coding model: Qwen3-Coder 480B-A35B / Qwen3.7 Max Preview.
- Public benchmark evidence: SWE-bench Verified lists Qwen3-Coder 480B/A35B at 55.4%; Arena coding lists Qwen3.7 Max Preview in a high public crowd-preference tier ([SWE-bench](https://www.swebench.com/), [Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Scale Pro public lists Qwen3-Coder 480B/A35B at 38.70%; Terminal-Bench lists Qwen 3 Coder 480B at 23.9%; CodeClash lists Qwen3 Coder below the leading closed models ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0), [CodeClash](https://codeclash.ai/)).
- Higher-risk pattern: public leaderboard and model-family evidence outpaces terminal and goal-oriented evidence.
- Evidence against concern: Scale Pro public score is relatively solid compared with several other open-weight or open-ish models.
- Unknowns: no Scale Pro private result found; Qwen3-Coder and Qwen3.7 Max Preview are different model identities.
- Final score: benchmark-gaming risk 52; raw coding generalization 58; confidence 63.

### Meta

- Best current coding model: Muse Spark.
- Public benchmark evidence: Arena coding lists Meta Muse Spark in the top crowd-preference tier ([Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Scale Pro public lists Muse Spark at 55.00%; Scale Pro private lists Muse Spark at 44.70%, second in the observed private comparison ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Scale private](https://labs.scale.com/leaderboard/swe_bench_pro_private)).
- Higher-risk pattern: sparse model documentation and public leaderboard exposure; prior Llama 4 reporting controversy creates a lab-level disclosure caution, not direct Muse Spark coding evidence ([The Verge](https://www.theverge.com/meta/645012/meta-llama-4-maverick-benchmarks-gaming)).
- Evidence against concern: strong private Pro performance is a strong counterweight against public-benchmark-only explanations.
- Unknowns: Muse Spark release details and model-card-level coding disclosures are sparse; the private result is not independently reproducible by outside users.
- Final score: benchmark-gaming risk 49; raw coding generalization 82; confidence 76.

### Google DeepMind

- Best current coding model: Gemini 3.1 Pro / Gemini 3 Pro Preview / Gemini 3 Flash.
- Public benchmark evidence: Artificial Analysis LiveCodeBench lists Gemini 3 Pro Preview high at 91.7% and Gemini 3 Flash Preview Reasoning at 90.8%; SWE-bench Verified lists Gemini 3 Flash high reasoning at 75.8% ([Artificial Analysis](https://artificialanalysis.ai/evaluations/livecodebench), [SWE-bench](https://www.swebench.com/)).
- Robust/private/live evidence: Scale Pro public lists Gemini 3.1 Pro thinking at 46.10%; Scale Pro private lists Gemini 3.1 Pro thinking at 32.20%; Terminal-Bench lists TongAgents Gemini 3.1 Pro at 80.2% ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Scale private](https://labs.scale.com/leaderboard/swe_bench_pro_private), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Higher-risk pattern: many Gemini variants and reasoning modes make exact attribution difficult.
- Evidence against concern: strong live-contest, private repo-level, and terminal evidence all point in the same direction.
- Unknowns: Gemini 3 Pro Preview, 3.1 Pro, and Flash are not identical; tool budgets and reasoning modes differ.
- Final score: benchmark-gaming risk 45; raw coding generalization 80; confidence 80.

### OpenAI

- Best current coding model: GPT-5.4 xHigh / GPT-5.3-Codex / GPT-5.5.
- Public benchmark evidence: SWE-bench Verified lists GPT-5-2 Codex at 72.8%; Aider lists GPT-5 high as a top public Polyglot result; Arena coding lists GPT-5.4/GPT-5.5 High in the top public tier ([SWE-bench](https://www.swebench.com/), [Aider](https://aider.chat/docs/leaderboards/), [Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Scale Pro public lists GPT-5.4 xHigh at 59.10%; Scale Pro private lists GPT-5.4 xHigh at 43.40%; Terminal-Bench lists GPT-5.5 and GPT-5.3-Codex systems around 75-85%; CodeClash lists GPT-5 second among tested models ([Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Scale private](https://labs.scale.com/leaderboard/swe_bench_pro_private), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0), [CodeClash](https://codeclash.ai/)).
- Higher-risk pattern: many Codex, CLI, and reasoning variants make model-vs-scaffold attribution hard.
- Evidence against concern: strong private Pro, public Pro, terminal, and goal-oriented results reduce the public-benchmark-overfit explanation.
- Unknowns: exact availability dates, tool policies, and inference budgets vary across GPT-5.x/Codex variants.
- Final score: benchmark-gaming risk 39; raw coding generalization 88; confidence 85.

### Anthropic

- Best current coding model: Claude Opus 4.6 / Claude Opus 4.7.
- Public benchmark evidence: SWE-bench Verified lists Claude Opus 4.6 at 75.6% and Claude Opus 4.5 high reasoning at 76.8%; Arena coding lists multiple Claude Opus 4.6/4.7 variants at the top public crowd-preference tier ([SWE-bench](https://www.swebench.com/), [Arena](https://arena.ai/leaderboard/text/coding)).
- Robust/private/live evidence: Scale Pro private lists Claude Opus 4.6 thinking at 47.10%, the top observed private result; Scale Pro public lists Opus 4.6 thinking at 51.90%; Terminal-Bench lists Opus 4.7/4.6 systems around 75-80% ([Scale private](https://labs.scale.com/leaderboard/swe_bench_pro_private), [Scale public](https://labs.scale.com/leaderboard/swe_bench_pro_public), [Terminal-Bench](https://www.tbench.ai/leaderboard/terminal-bench/2.0)).
- Higher-risk pattern: thinking-mode and agent-scaffold differences complicate direct comparisons.
- Evidence against concern: private Pro, public Pro, terminal, SWE-bench, and Arena evidence are broadly consistent.
- Unknowns: exact inference-budget and tool-use settings differ by evaluator and agent.
- Final score: benchmark-gaming risk 35; raw coding generalization 89; confidence 86.

## Cross-Benchmark Gap Analysis

Models that dominate public benchmarks but lack comparable private/live support: DeepSeek, Moonshot/Kimi, Z.ai/Zhipu, MiniMax, and xAI. The risk signal is strongest when public SWE-bench, LiveCodeBench, or Arena performance is high but same-model Scale Pro Private evidence is absent and Terminal-Bench or Pro Public results are much lower.

Models that perform consistently across public and private/live evaluations: Anthropic, OpenAI, Google DeepMind, and Meta. They have visible public strength and strong evidence on harder repo-level or terminal evaluations.

Models with strong scaffold-dependent results: OpenAI, Anthropic, Google, xAI, MiniMax, and several open or open-ish model families. Terminal-Bench and SWE-bench agent submissions are useful, but the agent scaffold, tool budget, and retry policy must be treated as part of the result.

Models with unusually sparse disclosures: Meta Muse Spark, xAI Grok 4.20, MiniMax M2.x, Z.ai GLM-5, Moonshot Kimi K2.x, and DeepSeek V3.2 variants. Sparse disclosure is a confidence penalty, not evidence of intent.

## Final Ranking

### Highest Benchmark-Gaming Risk

1. DeepSeek - 75
2. Moonshot / Kimi - 68
3. Z.ai / Zhipu - 65
4. MiniMax - 64
5. xAI - 60
6. Alibaba / Qwen - 52
7. Meta - 49
8. Google DeepMind - 45
9. OpenAI - 39
10. Anthropic - 35

### Strongest Raw Coding Generalization

1. Anthropic - 89
2. OpenAI - 88
3. Meta - 82
4. Google DeepMind - 80
5. Z.ai / Zhipu - 68
6. MiniMax - 68
7. Moonshot / Kimi - 64
8. DeepSeek - 60
9. Alibaba / Qwen - 58
10. xAI - 58

## Failure Modes

- Benchmark contamination is hard to prove from public evidence alone.
- Model release dates, training cutoffs, and benchmark exposure windows may be unclear.
- Labs and evaluators use different agent scaffolds, tool access, context lengths, retries, and inference budgets.
- Private evaluations are harder to game but may be unauditable by outside researchers.
- Public leaderboards can be noisy, preference-driven, or sensitive to response style rather than correctness.
- Real-world coding value includes debugging, code review, product judgment, tests, maintainability, and collaboration, not only benchmark score.
- Benchmark-gaming risk is not intent. It is a risk estimate based on observable gaps and incentives.

## Recommendations

- Use private repositories.
- Use hidden tests.
- Use post-release tasks.
- Fix scaffold and tool budgets.
- Require pass@1 or clearly separate pass@1 from pass@k.
- Disclose attempts, retries, sampling, temperature, patch selection, and inference budget.
- Separate base-model capability from agent-scaffold capability.
- Include multiple programming languages.
- Include debugging, feature work, refactors, tests, code review, and maintenance tasks.
- Rotate tasks frequently.
- Maintain private holdout sets.
- Audit contamination and benchmark exposure.
- Require independent replication before treating a result as strong evidence of generalization.
