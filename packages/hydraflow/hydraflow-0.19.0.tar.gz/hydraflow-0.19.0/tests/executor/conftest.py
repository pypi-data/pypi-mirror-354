from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from hydraflow.executor.conf import HydraflowConf


@pytest.fixture(scope="module")
def config(chdir):
    from hydraflow.executor.io import load_config

    def config(text: str):
        Path("hydraflow.yaml").write_text(text)
        cfg = load_config()
        Path("hydraflow.yaml").unlink()
        return cfg

    return config


@pytest.fixture(scope="module")
def args(config):
    def args(text: str):
        text = f"jobs:\n  a:\n    sets:\n      - all: {text}\n"
        cfg: HydraflowConf = config(text)
        return cfg.jobs["a"].sets[0].all

    return args
