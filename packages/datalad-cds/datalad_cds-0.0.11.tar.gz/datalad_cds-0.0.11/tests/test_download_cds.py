import json
import os
from typing import Union

import datalad.api as da
import pytest

import datalad_cds

request_dict = {
    "dataset": "reanalysis-era5-pressure-levels",
    "sub-selection": {
        "variable": "temperature",
        "pressure_level": "1000",
        "product_type": "reanalysis",
        "date": "2017-12-01/2017-12-31",
        "time": "12:00",
        "format": "grib",
    },
}


@pytest.mark.parametrize("cds_request", [request_dict, json.dumps(request_dict)])
def test_download_cds(cds_request: Union[str, dict], empty_dataset: da.Dataset) -> None:
    dataset = empty_dataset
    dataset.download_cds(
        cds_request,
        path="download.grib",
    )
    actual_request = datalad_cds.spec.Spec.from_json(
        (dataset.pathobj / "download.grib").read_text()
    )
    if isinstance(cds_request, dict):
        expected_request = datalad_cds.spec.Spec.from_dict(cds_request)
    elif isinstance(cds_request, str):
        expected_request = datalad_cds.spec.Spec.from_json(cds_request)
    assert actual_request == expected_request


@pytest.mark.parametrize("cds_request", [request_dict, json.dumps(request_dict)])
def test_download_cds_lazy(
    cds_request: Union[str, dict], empty_dataset: da.Dataset
) -> None:
    dataset = empty_dataset
    dataset.download_cds(
        cds_request,
        path="download.grib",
        lazy=True,
    )
    assert (
        os.readlink(dataset.pathobj / "download.grib")
        == ".git/annex/objects/5J/pV/URL--cds&cv1-eyJkYXRhc2V0IjoicmVhbmFs-77566133ebfe9220aefbeed5a58b6972/URL--cds&cv1-eyJkYXRhc2V0IjoicmVhbmFs-77566133ebfe9220aefbeed5a58b6972"
    )
