from manim import *
from itertools import product
import numpy as np
import random


class HexDots(VGroup):
    def __init__(
        self,
        colors=None,
        radius=2,
        dot_radius=0.08,
        polygon_color=WHITE,
        dot_colors=(RED, GREEN, BLUE)
    ):
        super().__init__()

        self.radius = radius
        self.dot_radius = dot_radius
        self.polygon_color = polygon_color
        self.available_colors = list(dot_colors)

        # Hexagon
        self.hexagon = RegularPolygon(
            n=6,
            radius=self.radius,
            color=self.polygon_color
        )

        # vertices alignment
        vertices = self.hexagon.get_vertices()
        start_vertex = sorted(vertices, key=lambda p: (-p[1], p[0]))[0]

        start_index = next(
            i for i, v in enumerate(vertices)
            if np.allclose(v, start_vertex)
        )

        ordered_vertices = list(vertices[start_index:]) + list(vertices[:start_index])

        # clockwise
        ordered_vertices = ordered_vertices[::-1]
        ordered_vertices = ordered_vertices[1:] + ordered_vertices[:1]

        # Dots
        self.dots = VGroup()

        for vertex in ordered_vertices:
            dot = Dot(
                point=vertex,
                radius=self.dot_radius,
                color=self.polygon_color
            )
            self.dots.add(dot)

        self.add(self.hexagon, self.dots)

        # начальная раскраска
        if colors is not None:
            self.set_coloring(colors)

    # Painting

    def set_coloring(self, colors):

        if len(colors) == 1:
            colors = colors * 6

        elif 2 <= len(colors) <= 5:
            raise ValueError("Нужно задать либо 1 цвет, либо все 6")

        elif len(colors) != 6:
            raise ValueError("Количество цветов должно быть 1 или 6")

        for dot, color in zip(self.dots, colors):
            dot.set_color(color)

    def random_coloring(self):
        colors = [random.choice(self.available_colors) for _ in range(6)]
        self.set_coloring(colors)

    # Indexes (labels)

    def get_labels(self, scale=0.7, buff=0.2):
        labels = VGroup()

        center = self.get_center()

        for i, dot in enumerate(self.dots):
            direction = dot.get_center() - center
            direction = direction / np.linalg.norm(direction)

            label = MathTex(str(i + 1)).scale(scale)
            label.move_to(dot.get_center() + direction * buff * 5)

            labels.add(label)

        return labels

    # Group actions

    def rotate_hex(self, angle):
        self.rotate(angle)

    def reflect_vertical(self):
        self.flip(RIGHT)

    # Permutation

    def permute_coloring(self, permutation):

        colors = [dot.get_color() for dot in self.dots]
        new_colors = [colors[i] for i in permutation]
        self.set_coloring(new_colors)

    # Get all unique colorings

    def generate_unique_colorings(self):

        seen = set()

        for coloring in product(self.available_colors, repeat=6):

            orbit = []

            for k in range(6):
                rotated = coloring[k:] + coloring[:k]
                orbit.append(rotated)

            reversed_col = coloring[::-1]
            for k in range(6):
                reflected = reversed_col[k:] + reversed_col[:k]
                orbit.append(reflected)

            canonical = min(orbit)

            if canonical not in seen:
                seen.add(canonical)
                yield list(canonical)

    # Rotation and reflection

    def animate_rotation(self, angle=PI/3, run_time=2):
        return Rotate(self, angle=angle, run_time=run_time)

    def animate_reflection(self, run_time=2):
        return ApplyMethod(self.flip, RIGHT, run_time=run_time)