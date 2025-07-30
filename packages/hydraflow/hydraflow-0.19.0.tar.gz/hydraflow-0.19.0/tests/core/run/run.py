from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import hydraflow

if TYPE_CHECKING:
    from mlflow.entities import Run


@dataclass
class Size:
    width: int = 0
    height: int = 0


@dataclass
class Config:
    count: int = 1
    name: str = "a"
    size: Size = field(default_factory=Size)


@hydraflow.main(Config)
def app(run: Run, cfg: Config):
    pass


if __name__ == "__main__":
    app()
