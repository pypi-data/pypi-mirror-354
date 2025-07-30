import gammalearn
from importlib.metadata import version as runtime_version


def test_version_is_defined():
    assert runtime_version("gammalearn") != "0.0.0"


def test_version_init():
    """test that gammalearn.__version__ is accessible
    """
    assert gammalearn.__version__ == runtime_version("gammalearn")