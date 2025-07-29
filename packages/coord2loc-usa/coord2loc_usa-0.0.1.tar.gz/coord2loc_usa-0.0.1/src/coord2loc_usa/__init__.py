from importlib import resources
from importlib.abc import Traversable
from typing import Tuple

from .data import METADATA_FILENAME, POLYGONS_FILENAME


def get_data() -> Tuple[str, Traversable, Traversable]:
    return (
        "USA",
        resources.files("coord2loc_usa.data").joinpath(POLYGONS_FILENAME),
        resources.files("coord2loc_usa.data").joinpath(METADATA_FILENAME),
    )
