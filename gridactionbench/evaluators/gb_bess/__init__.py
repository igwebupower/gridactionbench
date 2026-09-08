"""GB-BESS v0.1 evaluator catalogue. See docs/suites/gb-bess/EVALUATION_SPEC.md.

evaluator_set_version: 0.2.0 (per docs/suites/gb-bess/EVALUATION_SPEC.md, "Version note").
"""

from gridactionbench.evaluators.gb_bess.data import DATA_EVALUATORS
from gridactionbench.evaluators.gb_bess.net import NET_EVALUATORS
from gridactionbench.evaluators.gb_bess.ops import OPS_EVALUATORS
from gridactionbench.evaluators.gb_bess.phy import PHY_EVALUATORS

EVALUATOR_SET_VERSION = "0.2.0"

# "Standard" evaluators: fit the uniform Evaluator.evaluate(ctx) protocol. HUM and ADV are
# orchestrated separately by the Evaluation Engine (see gridactionbench.core.engine) since
# they are cross-cutting/derived, not independently computable from ctx alone.
STANDARD_EVALUATORS = [*PHY_EVALUATORS, *NET_EVALUATORS, *OPS_EVALUATORS, *DATA_EVALUATORS]

__all__ = ["STANDARD_EVALUATORS", "EVALUATOR_SET_VERSION"]
