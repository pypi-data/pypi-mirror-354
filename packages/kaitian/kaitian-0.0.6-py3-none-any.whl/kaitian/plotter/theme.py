from __future__ import annotations

import importlib.resources as import_resources
import json
import pathlib
from typing import Literal

from matplotlib import font_manager

with import_resources.path(
    f"{__package__}.static", "LXGWNeoXiHeiPlus.ttf"
) as font_file:
    font = font_manager.FontProperties(fname=pathlib.Path(font_file))  # type: ignore


def get_colormap(
    theme: Literal["science", "sharp", "nature", "purple"] = "science",
) -> list[str]:
    with import_resources.path(
        f"{__package__}.static", f"cm_{theme}.json"
    ) as font_file:
        colormap = json.load(open(font_file))
    return colormap


def get_font(
    fontsize: float
    | Literal[
        "xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"
    ] = "medium",
) -> font_manager.FontProperties:
    with import_resources.path(
        f"{__package__}.static", "LXGWNeoXiHeiPlus.ttf"
    ) as font_file:
        font = font_manager.FontProperties(
            fname=pathlib.Path(font_file),  # type: ignore
            size=fontsize,
        )
    return font


class Theme:
    def __init__(
        self,
        theme: Literal["science", "sharp", "nature", "purple"] = "science",
        fontsize: float
        | Literal[
            "xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"
        ] = "medium",
    ) -> None:
        self.colormap = get_colormap(theme)
        self._total = len(self.colormap)
        self._idx = 0
        self.font = get_font(fontsize)

    def get_color(self) -> str:
        color = self.colormap[int(self._idx % self._total)]
        self._idx += 1
        return color
