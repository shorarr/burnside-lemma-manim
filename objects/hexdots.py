from manim import *
from config import *
from itertools import product
import numpy as np

class HexDots(VGroup):

    def __init__(self, colors=None):
        super().__init__()

        self.hexagon = RegularPolygon(
            n=6,
            radius=HEX_RADIUS,
            color=PRIMARY_COLOR
        )

        vertices = self.hexagon.get_vertices()

        start_vertex = sorted(vertices, key=lambda p: (-p[1], p[0]))[0]
        start_index = next(
            i for i, v in enumerate(vertices)
            if np.allclose(v, start_vertex)
        )
        ordered_vertices = list(vertices[start_index:]) + list(vertices[:start_index])
        ordered_vertices = ordered_vertices[::-1]
        ordered_vertices = ordered_vertices[5:] + ordered_vertices[:5]

        # точки на вершинах
        self.dots = VGroup()

        for vertex in ordered_vertices:
            dot = Dot(
                point=vertex,
                radius=DOT_RADIUS,
                color=PRIMARY_COLOR
            )
            self.dots.add(dot)

        self.add(self.hexagon, self.dots)

        if colors:
            self.set_coloring(colors)

    # перекрасить точки
    def set_coloring(self, colors):

        if len(colors) == 1:
            colors = colors * 6

        elif 2 <= len(colors) <= 5:
            raise ValueError("Были указаны цвета не для всех точек")

        elif len(colors) != 6:
            raise ValueError("Количество цветов должно быть 1 или 6")

        for dot, color in zip(self.dots, colors):
            dot.set_color(color)

    # случайная раскраска
    def random_coloring(self):
        import random

        colors = [ random.choice(DOT_COLORS) for _ in range(6) ]
        self.set_coloring(colors)

    # поворот
    def rotate_hex(self, angle):
        self.rotate(angle)

    # отражение относительно оси
    def reflect_vertical(self):
        self.flip(RIGHT)

    # перебор всех уникальных раскрасок
    def all_unique_colorings(self):

        seen = set()

        for coloring in product(DOT_COLORS, repeat=6):

            orbit = []

            # повороты
            for k in range(6):
                rotated = coloring[k:] + coloring[:k]
                orbit.append(rotated)

            # отражения + повороты
            reversed_col = coloring[::-1]
            for k in range(6):
                reflected = reversed_col[k:] + reversed_col[:k]
                orbit.append(reflected)

            canonical = min(orbit)

            if canonical not in seen:
                seen.add(canonical)
                yield list(canonical)