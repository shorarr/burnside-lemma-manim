from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from objects.hexdots import HexDots
from objects.axis import main_axis

class Sc2(Scene):

    def construct(self):
        # надпись сверху
        title = Text(
            'Что значит "различные" раскраски?',
            font_size=36
        ).to_edge(UP)

        self.play(AddTextLetterByLetter(title), run_time=1)
        self.wait(1)

        # шестиугольник
        colors=[DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED, DOT_RED]

        hex_left = HexDots(colors)
        hex_right = HexDots(colors)

        hex_left.shift(LEFT * 3)
        hex_right.shift(RIGHT * 3)

        self.play(
            FadeIn(hex_left),
            FadeIn(hex_right)
        )

        self.wait(1)

        self.play(
            Rotate(hex_right, -PI),
            run_time=2
        )

        self.wait(1)

        # Текст снизу
        text_equal = Text(
            "Эти две раскраски считаются одинаковыми",
            font_size=36
        ).to_edge(DOWN)

        self.play(AddTextLetterByLetter(text_equal), run_time=1)

        self.wait(1)
        self.play(FadeOut(text_equal))

        # Отражение относительно оси
        axis = main_axis

        axis.set_length(hex_right.get_height() * 1.2)
        axis.move_to(hex_right)

        self.play(Create(axis))
        reflected = hex_right.copy().flip(UP)

        self.play(
            Transform(hex_right, reflected),
            run_time=1
        )

        self.wait(1)

        text_equal2 = Text(
            "Эти две раскраски тоже считаются одинаковыми",
            font_size=36
        ).to_edge(DOWN)

        self.play(AddTextLetterByLetter(text_equal2), run_time=1)

        self.wait(1)
        self.play(FadeOut(axis),FadeOut(text_equal2))
        self.play(
            Rotate(hex_right, -PI/2),
            run_time=2
        )

        text_equal3 = Text(
            "А эти две - нет",
            font_size=36
        ).to_edge(DOWN)

        self.play(AddTextLetterByLetter(text_equal3), run_time=1)
        self.wait(1)
        self.play(
            FadeOut(text_equal3),
            FadeOut(title)
        )

        hexes = VGroup (hex_left, hex_right)
        self.play(
            hexes.animate.to_edge(UP)
        )

        final_text = Paragraph(
            "Отождествляются раскраски,\n",
            "совпадающие при поворотах и отражениях.",
            font_size=36,
            color = PRIMARY_COLOR,
            alignment = "center",
        ).to_edge(DOWN)

        self.play(Write(final_text), run_time=2)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])