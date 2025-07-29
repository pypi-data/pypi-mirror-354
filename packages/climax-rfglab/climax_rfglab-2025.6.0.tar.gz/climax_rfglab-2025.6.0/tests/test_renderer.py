# image renderer widget tests.
# for coverage, run:
# coverage run -m pytest -s
# or if you want to include branches:
# coverage run --branch -m pytest
# followed by:
# coverage report -i


import numpy

from climax._renderer import HalfcellRenderer, _get_color
from climax._imagepanel import ImagePanel


def test_halfcell_renderer_basic():
    img = numpy.zeros((4, 4, 3), dtype=int)
    renderer = HalfcellRenderer(img)
    segments = renderer.render(None)
    assert segments  # Should produce some segments

def test_halfcell_renderer_with_fixture():
    image = numpy.random.rand(100, 100)
    renderer = HalfcellRenderer(ImagePanel.map_image(image))

    segments = renderer.render(None)
    assert segments  # Should produce some segments
    assert len(segments) == (image.shape[0] * image.shape[1] // 2) + (image.shape[0] // 2)  # Each row is half-height and separated by a carriage return character.

def test_halfcell_renderer_with_empty_image():
    image = numpy.zeros((0, 0, 3), dtype=int)  # Empty image
    renderer = HalfcellRenderer(image)
    segments = renderer.render(None)
    assert segments == []  # Should produce no segments for an empty image

def test_get_color_basic():
    assert _get_color((0, 0, 0)) == "rgb(0,0,0)"
    assert _get_color((255, 255, 255)) == "rgb(255,255,255)"
    assert _get_color((128, 64, 32)) == "rgb(128,64,32)"
