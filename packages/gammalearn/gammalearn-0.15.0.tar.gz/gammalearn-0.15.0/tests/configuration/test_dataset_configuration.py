from pathlib import Path

from pytest import FixtureRequest
from ruamel.yaml import YAML

from gammalearn.configuration.dataset import MemoryLSTDatasetConfiguration


def test_MemoryLSTDatasetConfiguration(request: FixtureRequest):
    current_dir = Path(request.path).parent.resolve()
    example_config_path = current_dir / "resources/MemoryLSTDatasetConfiguration.yaml"

    with open(example_config_path, "r") as example_config_f:
        yaml = YAML(typ="safe")
        example_config = yaml.load(example_config_f)

    MemoryLSTDatasetConfiguration.model_validate(example_config)
