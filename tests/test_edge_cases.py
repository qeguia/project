# Test:
# - empty input
# - invalid input
# - boundary values
# - exceptions


import sys
import types
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Fake external dependencies so imports from cleaning.py work
fake_eurostat = types.ModuleType("eurostat")
fake_eurostat.get_data_df = lambda dataset: None
sys.modules["eurostat"] = fake_eurostat

fake_ineapy = types.ModuleType("ineapy")


class FakeINEConsultor:
    def get_table_data(self, id_table):
        return []


fake_ineapy.INEConsultor = FakeINEConsultor
sys.modules["ineapy"] = fake_ineapy

from data_cleaning.cleaning import prepare_hpi_long
from analysis.analysis import (
    get_country_series,
    build_country_comparison_dataset,
    get_ine_national_series,
)


def test_get_country_series_raises_for_missing_country():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT"],
        "year": [2020, 2020],
        "hpi": [110, 100],
    })

    with pytest.raises(ValueError):
        get_country_series(df_long, "FR")


def test_build_country_comparison_dataset_raises_for_same_country():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT"],
        "year": [2020, 2020],
        "hpi": [110, 100],
    })

    with pytest.raises(ValueError):
        build_country_comparison_dataset(df_long, "ES", "ES")


def test_prepare_hpi_long_drops_invalid_hpi_values():
    df = pd.DataFrame({
        "geo": ["ES"],
        "purchase": ["TOTAL"],
        "unit": ["I10_A_AVG"],
        "2020": ["not_a_number"],
        "2021": [115],
    })

    result = prepare_hpi_long(df)

    assert len(result) == 1
    assert result.iloc[0]["year"] == 2021
    assert result.iloc[0]["hpi"] == 115


def test_get_ine_national_series_returns_empty_when_input_empty():
    df_ine = pd.DataFrame(columns=["region", "dwelling", "year", "value"])

    result = get_ine_national_series(df_ine)

    assert result.empty


def test_get_ine_national_series_returns_full_dataset_if_no_national_row():
    df_ine = pd.DataFrame({
        "region": ["Madrid", "Cataluña"],
        "dwelling": ["Total", "Total"],
        "year": [2020, 2020],
        "value": [110, 108],
    })

    result = get_ine_national_series(df_ine)

    assert len(result) == 2
    assert set(result["region"]) == {"Madrid", "Cataluña"}