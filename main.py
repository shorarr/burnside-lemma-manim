from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from objects.hexdots import HexDots


class Sc1(Scene):

    def construct(self):

        # Шестиугольник с точками
        hex_dots = HexDots()

        self.play(Create(hex_dots))
        self.wait(1)

        # Демонстрация 3 разных раскрасок
        self.play(*[dot.animate.set_color(DOT_RED) for dot in hex_dots.dots], run_time =0.1)
        self.wait(1)

        self.play(*[dot.animate.set_color(DOT_GREEN) for dot in hex_dots.dots], run_time =0.1)
        self.wait(1)

        self.play(*[dot.animate.set_color(DOT_BLUE) for dot in hex_dots.dots], run_time =0.1)
        self.wait(1.5)

        self.play(hex_dots.animate.random_coloring(), run_time=0.01)
        self.wait(1)

        for _ in range(5):
            self.play(hex_dots.animate.random_coloring(), run_time=0.01)
            self.wait(1)

        self.wait(2)