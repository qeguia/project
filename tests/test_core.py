# Tests of main functions or classes.


import sys
import types
from pathlib import Path

import pandas as pd

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

from data_cleaning.cleaning import (
    clean_eurostat_data,
    prepare_hpi_long,
    clean_ine_data,
)
from analysis.analysis import (
    get_spain_series,
    get_country_series,
    get_eu_average,
    build_spain_vs_eu_dataset,
    build_country_comparison_dataset,
    get_ine_national_series,
)


def test_clean_eurostat_data_removes_freq_and_renames_geo():
    raw = pd.DataFrame({
        "freq": ["A", "A"],
        "geo\\TIME_PERIOD": ["ES", "PT"],
        "purchase": ["TOTAL", "TOTAL"],
        "unit": ["I10_A_AVG", "I10_A_AVG"],
        "2020": [110, 105],
    })

    result = clean_eurostat_data(raw)

    assert "freq" not in result.columns
    assert "geo" in result.columns
    assert "geo\\TIME_PERIOD" not in result.columns
    assert len(result) == 2


def test_prepare_hpi_long_filters_and_reshapes_data():
    df = pd.DataFrame({
        "geo": ["ES", "PT", "FR"],
        "purchase": ["TOTAL", "TOTAL", "OTHER"],
        "unit": ["I10_A_AVG", "I10_A_AVG", "I10_A_AVG"],
        "2020": [110, 105, 999],
        "2021": [115, 107, 999],
    })

    result = prepare_hpi_long(df)

    assert list(result.columns) == ["geo", "year", "hpi"]
    assert set(result["geo"]) == {"ES", "PT"}
    assert set(result["year"]) == {2020, 2021}
    assert len(result) == 4


def test_get_spain_series_returns_only_es():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT", "ES"],
        "year": [2020, 2020, 2021],
        "hpi": [110, 105, 115],
    })

    result = get_spain_series(df_long)

    assert all(result["geo"] == "ES")
    assert len(result) == 2


def test_get_country_series_returns_selected_country():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT", "FR"],
        "year": [2020, 2020, 2020],
        "hpi": [110, 105, 120],
    })

    result = get_country_series(df_long, "pt")

    assert len(result) == 1
    assert result.iloc[0]["geo"] == "PT"


def test_get_eu_average_computes_mean_by_year():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT", "EU27_2020", "ES", "PT"],
        "year": [2020, 2020, 2020, 2021, 2021],
        "hpi": [110, 100, 999, 120, 130],
    })

    result = get_eu_average(df_long)

    assert set(result["year"]) == {2020, 2021}
    assert all(result["geo"] == "EU Avg")

    value_2020 = result[result["year"] == 2020]["hpi"].iloc[0]
    value_2021 = result[result["year"] == 2021]["hpi"].iloc[0]

    assert value_2020 == 105
    assert value_2021 == 125


def test_build_spain_vs_eu_dataset_contains_es_and_eu_avg():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT", "ES", "PT"],
        "year": [2020, 2020, 2021, 2021],
        "hpi": [110, 100, 120, 130],
    })

    result = build_spain_vs_eu_dataset(df_long)

    assert set(result["geo"]) == {"ES", "EU Avg"}
    assert len(result) == 4


def test_build_country_comparison_dataset_returns_two_countries():
    df_long = pd.DataFrame({
        "geo": ["ES", "PT", "FR", "ES", "PT", "FR"],
        "year": [2020, 2020, 2020, 2021, 2021, 2021],
        "hpi": [110, 100, 120, 115, 105, 125],
    })

    result = build_country_comparison_dataset(df_long, "es", "pt")

    assert set(result["geo"]) == {"ES", "PT"}
    assert len(result) == 4


def test_get_ine_national_series_returns_national_rows_when_present():
    df_ine = pd.DataFrame({
        "region": ["Nacional", "Madrid", "Cataluña"],
        "dwelling": ["Total", "Total", "Total"],
        "year": [2020, 2020, 2020],
        "value": [100, 110, 108],
    })

    result = get_ine_national_series(df_ine)

    assert len(result) == 1
    assert "Nacional" in result["region"].iloc[0]


def test_clean_ine_data_filters_and_selects_needed_columns():
    df_ine = pd.DataFrame({
        "name_table": [
            "Nacional. Media anual. Vivienda total.",
            "Madrid. Media anual. Vivienda nueva.",
            "Madrid. Trimestral. Vivienda total.",
        ],
        "unidad": ["Índice", "Índice", "Índice"],
        "year": [2020, 2020, 2020],
        "value": [100, 110, 999],
    })

    result = clean_ine_data(df_ine)

    assert list(result.columns) == ["region", "dwelling", "year", "value"]
    assert len(result) == 2
    assert set(result["region"]) == {"Nacional", "Madrid"}