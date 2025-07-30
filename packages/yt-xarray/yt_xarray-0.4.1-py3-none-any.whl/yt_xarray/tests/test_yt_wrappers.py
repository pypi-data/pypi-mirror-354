import os
import os.path

import pytest
from yt.data_objects.static_output import Dataset as ytDataset

from yt_xarray.sample_data import load_random_xr_data


def get_xr_ds() -> ytDataset:
    fields = {
        "temperature": ("x", "y", "z"),
        "pressure": ("x", "y", "z"),
        "precip": ("x", "y", "z"),
    }
    dims = {"x": (0, 1, 15), "y": (0, 1, 10), "z": (0, 1, 15)}
    ds = load_random_xr_data(fields, dims, length_unit="m")
    return ds


@pytest.mark.parametrize("viz_method", ["SlicePlot", "ProjectionPlot"])
def test_2d_volume_plots(tmp_path, viz_method):
    xr_ds = get_xr_ds()
    func = getattr(xr_ds.yt, viz_method)
    slc = func("x", "temperature")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    fname = str(output_dir / f"yt_xarray_{viz_method}.png")
    slc.save(fname)

    assert os.path.isfile(fname)


def test_phase_plot(tmp_path):
    xr_ds = get_xr_ds()
    slc = xr_ds.yt.PhasePlot("pressure", "temperature", "temperature")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    fname = str(output_dir / "yt_xarray_PhasePlot.png")
    slc.save(fname)

    assert os.path.isfile(fname)


def test_profile_plot(tmp_path):
    xr_ds = get_xr_ds()
    slc = xr_ds.yt.ProfilePlot("pressure", "temperature", weight_field="precip")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    fname = str(output_dir / "yt_xarray_ProfilePlot.png")
    actual_name = slc.save(fname)[0]

    assert os.path.isfile(actual_name)
