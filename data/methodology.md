# Methodology: Benchmark Gaming Risk vs Raw Coding Generalization

Run date: 2026-06-21

This methodology estimates observable benchmark-gaming risk and raw coding generalization for frontier coding models. It does not infer intent. A high risk score means the public evidence is more consistent with public-benchmark over-optimization, contamination exposure, scaffold dependence, selective reporting, or weak private/live support.

## Definitions

- Vulnerable benchmark: public, old, saturated, widely discussed, likely present in training data, easy to tune against, easy to scaffold-optimize, or dependent on visible test cases.
- Robust benchmark: private, held-out, live, post-release, hidden-test, enterprise-code, realistic multi-file, independently run, or difficult to train directly against.
- Benchmark-gaming risk: the degree to which a model or lab appears to overperform on vulnerable public coding benchmarks compared with robust coding evaluations.
- Raw coding generalization: evidence that the model can solve unseen, realistic, multi-file, long-horizon, tool-using coding tasks across independent settings.
- Confidence: evidence support for a rating, accounting for source quality, reproducibility, date, independence, and whether results are public, private, live, or vendor-reported.

## Source Hierarchy

Sources were weighted in this order:

1. Benchmark papers, official benchmark documentation, and official benchmark repositories.
2. Independent leaderboards and evaluator-run results.
3. Reproducible GitHub repositories and public harnesses.
4. Vendor model cards, vendor blogs, and vendor-reported scores, labelled as such.
5. Credible journalism for reporting-practice controversies or disclosure concerns.

Vendor-reported claims were not used as sole support for a high confidence score.

## Model Selection

The top-10 lab/model set was selected for current frontier coding relevance using current public evidence from SWE-bench, Scale SWE-Bench Pro, Terminal-Bench, Artificial Analysis LiveCodeBench, Arena coding, CodeClash, Aider, and BigCodeBench. When a lab has several current coding-relevant models, the scorecard names the strongest current model family and notes model-variant uncertainty.

Labs selected:

1. Anthropic
2. OpenAI
3. Google DeepMind
4. Meta
5. MiniMax
6. Z.ai / Zhipu
7. Moonshot / Kimi
8. DeepSeek
9. Alibaba / Qwen
10. xAI

## Scoring Rubric

### Benchmark-Gaming-Risk Score, 0-100

- 30 points: public-vs-private/live performance gap.
- 20 points: unusually high performance on saturated public benchmarks relative to harder evaluations.
- 15 points: evidence of contamination, leakage, memorization, or benchmark exposure.
- 15 points: evidence of leaderboard hillclimbing, benchmark-specific variants, or repeated public leaderboard optimization.
- 10 points: selective reporting, missing scaffold details, missing pass@k/attempt counts, or unreproducible claims.
- 10 points: excessive dependence on agent scaffold, retries, context budget, or tool setup compared with base-model capability.

### Raw-Coding-Generalization Score, 0-100

- 35 points: strong private/held-out software-engineering evaluation performance.
- 25 points: strong live/post-release contest or coding-task performance.
- 20 points: strong agentic repo-level performance under standardized scaffold and budget.
- 10 points: consistency across independent evaluators.
- 10 points: real developer usefulness, adoption, or preference evidence where available.

### Confidence Score, 0-100

Start at 50, then adjust:

- +20 for multiple independent sources.
- +15 for private, held-out, or live evaluations.
- +10 for reproducible methodology.
- +10 for consistent results across benchmark types.
- -20 for mostly vendor-reported evidence.
- -15 for missing scaffold, tool, or budget details.
- -15 for sparse data.
- -10 for old data relative to current model releases.
- -10 for contradictory sources.

Caps:

- Cap confidence at 90 unless at least two independent robust evaluation sources support the rating.
- Cap confidence at 70 if most evidence is vendor-reported.
- Cap confidence at 60 if the best model identity is unclear.
- Cap confidence at 50 if private/live evidence is absent.

## Normalization Rules

- Separate lab, model, and agent scaffold.
- Do not compare base-model results with agent results without caveat.
- Do not compare pass@1 with pass@k without caveat.
- Do not compare single-attempt with multi-attempt results without caveat.
- Do not compare no-tool results with tool-using results without caveat.
- Penalize missing attempt counts, temperature, context length, inference budget, tool access, retry policy, pass@k, or patch-selection details.
- Penalize special benchmark-specific model variants when the relationship to generally available models is unclear.
- Date-normalize results when possible; newer models are not directly comparable with older benchmark entries.

## Applying the Scores

Scores are qualitative, evidence-weighted estimates rather than exact cross-benchmark normalizations. Coding benchmarks differ in task type, scaffold, hidden tests, tool budget, pass metric, and release timing. Public benchmark gaps are treated as evidence of benchmark-gaming risk, not proof of misconduct or intent.

Unknowns were scored conservatively. Missing private/live evidence raises benchmark-gaming-risk and lowers confidence. Strong private, held-out, live, or independently reproduced results lower benchmark-gaming-risk and raise raw-coding-generalization confidence.
