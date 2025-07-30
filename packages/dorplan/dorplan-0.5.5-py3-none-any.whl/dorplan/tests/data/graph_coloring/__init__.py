from cornflow_client import (
    get_empty_schema,
    ApplicationCore,
    InstanceCore,
    SolutionCore,
    ExperimentCore,
)
from cornflow_client.core.tools import load_json
from typing import List, Dict
import os


try:
    from .solvers import OrToolsCP, PulpMip
    from .core import Instance, Solution, Experiment
except ImportError as e:
    print(e)

    class GraphColoring(ApplicationCore):
        name = "graph_coloring"
        instance = InstanceCore
        solution = SolutionCore
        solvers = dict(experiment=ExperimentCore)
        schema = get_empty_schema(solvers=["experiment"])

        @property
        def test_cases(self) -> List[Dict]:
            return [dict()]

else:

    class GraphColoring(ApplicationCore):
        name = "graph_coloring"
        instance = Instance
        solution = Solution
        solvers = dict(ortools=OrToolsCP, pulp=PulpMip)
        schema = load_json(
            os.path.join(os.path.dirname(__file__), "schemas/config.json")
        )

        @property
        def test_cases(self) -> List[Dict]:

            file_dir = os.path.join(os.path.dirname(__file__), "data")
            get_file = lambda name: os.path.join(file_dir, name)
            return [
                {
                    "name": "gc_4_1",
                    "instance": Instance.from_txt_file(get_file("gc_4_1")).to_dict(),
                    "description": "Example data with 4 pairs",
                },
                {
                    "name": "gc_50_1",
                    "instance": Instance.from_txt_file(get_file("gc_50_1")).to_dict(),
                    "description": "Example data with 50 pairs",
                },
            ]
