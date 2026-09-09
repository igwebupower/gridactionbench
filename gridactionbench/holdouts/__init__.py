"""Private-seed holdout generation infrastructure. See docs/benchmark/PUBLIC_PRIVATE_POLICY.md.

Public: the generator code in this package (and the templates it draws from,
gridactionbench/scenarios/generator.py). Private: the seed value used to draw official
holdout instances (gridactionbench/holdouts/private_seed.py), and the instances
themselves once generated (written to a gitignored directory, never committed).
"""
