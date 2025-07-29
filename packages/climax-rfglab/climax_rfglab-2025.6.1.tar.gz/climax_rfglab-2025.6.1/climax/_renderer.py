from functools import cache
from typing import Union, Tuple

import numpy
import skimage.transform as sktr
from rich.segment import Segment
from rich.style import Style

def _get_color(pixel: Union[numpy.ndarray, Tuple[int, int, int]]) -> str:
    return f"rgb({pixval[pixel[0]]},{pixval[pixel[1]]},{pixval[pixel[2]]})"

pix_val_ints = range(256)  # Assuming pixel values are in the range 0-255, which is true for color maps.
pixval = [f"{theint}" for theint in pix_val_ints]

@cache # replacing calls to _get_color with _get_gray(self.image[y, x]) speeds up rendering by 33%.
def _get_gray(pixel: int) -> str:
    return f"rgb({pixval[pixel]},{pixval[pixel]},{pixval[pixel]})"


class Renderer:
    """
    Base class for renderers.
    """

    def __init__(
        self,
        image: numpy.ndarray,
    ) -> None:
        self.image = image.astype(int)
        self._get_pix_fn = _get_gray if self.image.ndim == 2 else _get_color

    def render(self, resize: tuple[int, int] | None) -> list[Segment]:
        """
        Render an image to Segments.
        """

        if resize:
            self.image = sktr.resize(self.image, resize, 0, preserve_range=True)

        segments = []

        for y in self._get_range():
            this_row: list[Segment] = []

            this_row += self._render_line(
                line_index=y
            )
            this_row.append(Segment("\n", None))

            # TODO: Double-check if this is required - I've forgotten...
            if not all(t[1] == "" for t in this_row[:-1]):
                segments += this_row

        return segments

    def _get_range(self) -> range:
        """
        Get the range of lines to render.
        """
        raise NotImplementedError

    def _render_line(
        self, line_index: int
    ) -> list[Segment]:
        """
        Render a line of pixels.
        """
        raise NotImplementedError


class HalfcellRenderer(Renderer):
    """
    Render an image to half-height cells.
    """

    def render(self, resize: tuple[int, int] | None) -> list[Segment]:
        # because each row is 2 lines high, so we need to make sure the height is even
        target_height = resize[0] if resize else self.image.shape[0]
        if target_height % 2 != 0:
            target_height += 1

        if self.image.shape[0] != target_height:
            resize = (
                (target_height, resize[1]) if resize else (target_height, self.image.shape[1])
            )

        return super().render(resize)

    def _get_range(self) -> range:
        return range(0, self.image.shape[0], 2)

    def _render_line(
        self, line_index: int
    ) -> list[Segment]:
        line = []
        for x in range(self.image.shape[1]):
            line.append(self._render_halfcell(x=x, y=line_index))
        return line

    def _render_halfcell(self, *, x: int, y: int) -> Segment:
        colors = []

        # get lower pixel, render lower pixel use foreground color, so it must be first
        lower_color = self._get_pix_fn(self.image[y + 1, x])
        colors.append(lower_color or "")

        # get upper pixel, render upper pixel use background color, it is optional
        upper_color = self._get_pix_fn(self.image[y, x])
        if upper_color:
            colors.append(upper_color or "")

        style = Style.parse(" on ".join(colors))
        # use lower halfheight block to render if lower pixel is not transparent
        return Segment("▄" if lower_color else " ", style)