from dorplan.tests.data.graph_coloring import GraphColoring
from dorplan.app import DorPlan


def test_open_app_gui():
    DorPlan(GraphColoring, {})
    return 1


if __name__ == "__main__":
    test_open_app_gui()
