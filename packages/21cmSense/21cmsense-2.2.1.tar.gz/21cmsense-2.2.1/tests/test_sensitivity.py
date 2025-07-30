"""Test the sensitivity module."""

import warnings
from functools import wraps

import numpy as np
import pytest
from astropy import units
from astropy.cosmology.units import littleh
from spiceypy.utils.exceptions import SpiceUNKNOWNFRAME

from py21cmsense import GaussianBeam, Observation, Observatory, PowerSpectrum, theory
from py21cmsense.sensitivity import Sensitivity


def skip_on(exception, reason="Default reason"):
    # Func below is the real decorator and will receive the test function as param
    def decorator_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Try to run the test
                return f(*args, **kwargs)
            except exception:
                # If exception of given type happens
                # just swallow it and raise pytest.Skip with given reason
                pytest.skip(reason)

        return wrapper

    return decorator_func


@pytest.fixture(scope="module")
def bm():
    return GaussianBeam(150.0 * units.MHz, dish_size=14 * units.m)


@pytest.fixture(scope="module", params=["earth", "moon"])
def wd(request):
    return request.param


@pytest.fixture(scope="module")
def observatory(bm, wd):
    return Observatory(
        antpos=np.array([[0, 0, 0], [14, 0, 0], [28, 0, 0], [70, 0, 0]]) * units.m,
        beam=bm,
        world=wd,
    )


@pytest.fixture(scope="module")
def observation(observatory):
    return Observation(observatory=observatory)


def test_units(observation):
    ps = PowerSpectrum(observation=observation)

    assert ps.horizon_buffer.to("littleh/Mpc").unit == littleh / units.Mpc
    assert ps.k1d.to("littleh/Mpc").unit == littleh / units.Mpc
    assert isinstance(ps.power_normalisation(0.1 * littleh / units.Mpc), float)
    assert ps.horizon_limit(10).to("littleh/Mpc").unit == littleh / units.Mpc


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_sensitivity_2d(observation):
    ps = PowerSpectrum(observation=observation)
    sense_thermal = ps.calculate_sensitivity_2d(thermal=True, sample=False)
    sense_full = ps.calculate_sensitivity_2d()
    assert all(np.all(sense_thermal[key] <= sense_full[key]) for key in sense_thermal)

    with pytest.raises(ValueError, match="Either thermal or sample must be True"):
        ps.calculate_sensitivity_2d(thermal=False, sample=False)


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_sensitivity_2d_grid(observation, caplog):
    ps = PowerSpectrum(observation=observation)
    sense_ungridded = ps.calculate_sensitivity_2d(thermal=True, sample=True)
    kperp = np.array([x.value for x in sense_ungridded]) * next(iter(sense_ungridded.keys())).unit
    sense = ps.calculate_sensitivity_2d_grid(
        kperp_edges=np.linspace(kperp.min().value, kperp.max().value, 10) * kperp.unit,
        kpar_edges=ps.k1d,
    )
    assert sense.shape == (9, len(ps.k1d) - 1)


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_sensitivity_1d_binned(observation):
    ps = PowerSpectrum(observation=observation)
    assert np.all(ps.calculate_sensitivity_1d() == ps.calculate_sensitivity_1d_binned(ps.k1d))
    kbins = np.linspace(0.1, 0.5, 10) * littleh / units.Mpc
    sense1d_sample = ps.calculate_sensitivity_1d_binned(k=kbins)
    assert len(sense1d_sample) == len(kbins)


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_plots(observation):
    # this is a dumb test, just checking that it doesn't error.
    ps = PowerSpectrum(observation=observation)
    sense2d = ps.calculate_sensitivity_2d()
    ps.plot_sense_2d(sense2d)


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_sensitivity_optimistic(observation):
    ps = PowerSpectrum(observation=observation, foreground_model="optimistic")
    assert ps.horizon_limit(10.0) > ps.horizon_limit(5.0)


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_sensitivity_foreground_free(observation):
    ps = PowerSpectrum(observation=observation, foreground_model="foreground_free")
    assert ps.horizon_limit(10.0) == 0


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_infs_in_trms(observation):
    # default dumb layout should have lots of infs..
    assert np.any(np.isinf(observation.Trms))
    ps = PowerSpectrum(observation=observation)
    ps.calculate_sensitivity_2d()
    # merely get through the calculations...


def test_write_to_custom_filename(observation, tmp_path):
    out = tmp_path / "outfile.h5"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ps = PowerSpectrum(observation=observation)
        out2 = ps.write(filename=out)
    assert out2 == out


def test_load_yaml_bad():
    with pytest.raises(
        ValueError,
        match="yaml_file must be a string filepath or a raw dict from such a file",
    ):
        Sensitivity.from_yaml(1)

    rng = np.random.default_rng(1234)
    with pytest.raises(ImportError, match="Could not import"):
        PowerSpectrum.from_yaml(
            {
                "plugins": ["this.is.not.a.module"],
                "observatory": {
                    "antpos": rng.random((20, 3)) * units.m,
                    "beam": {
                        "class": "GaussianBeam",
                        "frequency": 150 * units.MHz,
                        "dish_size": 14 * units.m,
                    },
                },
            }
        )


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_systematics_mask(observation):
    ps = PowerSpectrum(
        observation=observation,
        systematics_mask=lambda kperp, kpar: np.zeros(len(kpar), dtype=bool),
    )
    assert len(ps.calculate_sensitivity_2d()) == 0


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_track(observatory):
    """Test that setting `track` is the same as setting lst_bin_width."""
    obs1 = Observation(observatory=observatory, lst_bin_size=1 * units.hour)
    obs2 = Observation(observatory=observatory, track=1 * units.hour)

    assert np.all(obs1.uv_coverage == obs2.uv_coverage)


def test_clone(observation):
    ps = PowerSpectrum(
        observation=observation,
    )

    ps2 = ps.clone()
    assert ps2 == ps


@skip_on(SpiceUNKNOWNFRAME, "Unknown FRAME (flaky exception)")
def test_at_freq(observation):
    ps = PowerSpectrum(observation=observation, theory_model=theory.EOS2016Bright())
    ps2 = ps.at_frequency(0.9 * observation.frequency)

    assert ps2.frequency == 0.9 * observation.frequency
    with pytest.warns(UserWarning, match="Extrapolating above the simulated theoretical"):
        assert ps.calculate_significance() != ps2.calculate_significance()


def test_bad_theory(observation):
    with pytest.raises(ValueError, match="The theory_model must be an instance of TheoryModel"):
        PowerSpectrum(observation=observation, theory_model=3)
