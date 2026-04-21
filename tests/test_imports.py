# Check here that package imports well.

import sys
import types
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Fake eurostat
fake_eurostat = types.ModuleType("eurostat")
fake_eurostat.get_data_df = lambda dataset: None
sys.modules["eurostat"] = fake_eurostat

# Fake ineapy
fake_ineapy = types.ModuleType("ineapy")


class FakeINEConsultor:
    def get_table_data(self, id_table):
        return []


fake_ineapy.INEConsultor = FakeINEConsultor
sys.modules["ineapy"] = fake_ineapy

# Fake plotnine
fake_plotnine = types.ModuleType("plotnine")


def _fake_plotnine_function(*args, **kwargs):
    return None


fake_plotnine.ggplot = _fake_plotnine_function
fake_plotnine.aes = _fake_plotnine_function
fake_plotnine.geom_line = _fake_plotnine_function
fake_plotnine.geom_point = _fake_plotnine_function
fake_plotnine.labs = _fake_plotnine_function
fake_plotnine.theme_minimal = _fake_plotnine_function
fake_plotnine.theme = _fake_plotnine_function
fake_plotnine.element_text = _fake_plotnine_function
fake_plotnine.scale_x_continuous = _fake_plotnine_function
fake_plotnine.scale_y_continuous = _fake_plotnine_function
sys.modules["plotnine"] = fake_plotnine


def test_import_cleaning():
    import data_cleaning.cleaning
    assert data_cleaning.cleaning is not None


def test_import_analysis():
    import analysis.analysis
    assert analysis.analysis is not None


def test_import_main():
    import main
    assert main is not None


def test_import_main_eurostat():
    import main_eurostat
    assert main_eurostat is not None


def test_import_main_ine():
    import main_ine
    assert main_ine is not None