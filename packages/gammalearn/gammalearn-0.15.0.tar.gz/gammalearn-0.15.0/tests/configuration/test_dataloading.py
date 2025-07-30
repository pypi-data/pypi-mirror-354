from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import FixtureRequest
from ruamel.yaml import YAML

from gammalearn.configuration.dataloading import DataloadingConfiguration


def test_WrongDatasetTypeDataloadingConfiguration(request: FixtureRequest):
    current_dir = Path(request.path).parent.resolve()
    example_config_path = current_dir / "resources/WrongDatasetTypeDataloadingConfiguration.yaml"

    with open(example_config_path, "r") as example_config_f:
        yaml = YAML(typ="safe")
        example_config = yaml.load(example_config_f)

    with pytest.raises(ValidationError):
        DataloadingConfiguration.model_validate(example_config)


def test_DataloadingConfiguration(request: FixtureRequest):
    current_dir = Path(request.path).parent.resolve()
    example_config_path = current_dir / "resources/DataloadingConfiguration.yaml"

    with open(example_config_path, "r") as example_config_f:
        yaml = YAML(typ="safe")
        example_config = yaml.load(example_config_f)

    DataloadingConfiguration.model_validate(example_config)
