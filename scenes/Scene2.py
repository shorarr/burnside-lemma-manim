from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots
from objects.axis import main_axis

class Sc2(Scene):

    def construct(self):
        # надпись сверху
        title = Text(
            'Что значит "различные" и "одинаковые" раскраски?',
            font_size=36
        ).to_edge(UP)

        self.play(AddTextLetterByLetter(title), run_time=1)
        self.wait(1)

        # шестиугольник
        colors1 = [DOT_RED, DOT_BLUE, DOT_RED, DOT_RED, DOT_RED, DOT_RED]
        colors2 = [DOT_BLUE, DOT_RED, DOT_RED, DOT_RED, DOT_RED, DOT_RED]

        hex_left = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_right = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_left.set_coloring(colors1)
        hex_right.set_coloring(colors2)

        hex_left.shift(LEFT * 3)
        hex_right.shift(RIGHT * 3)

        self.play(
            FadeIn(hex_left),
            FadeIn(hex_right)
        )

        self.wait(1)

        self.play(
            Rotate(hex_right, -PI/3),
            run_time=2
        )

        self.wait(1)

        # Текст снизу
        text_equal = Text(
            "Одинаковые раскраски",
            font_size=36
        ).to_edge(DOWN)

        self.play(AddTextLetterByLetter(text_equal), run_time=1)

        self.wait(1)
        self.play(
            Rotate(hex_right, PI / 3),
            run_time=0.5
        )
        self.play(FadeOut(text_equal))

        # Отражение относительно оси
        axis = main_axis

        axis.set_length(hex_right.get_height() * 1.2)
        axis.move_to(hex_right)

        self.play(Create(axis))

        self.play(
            hex_right.animate.flip(axis=axis.get_unit_vector()),
            run_time=1
        )

        self.wait(1)

        text_equal2 = Text(
            "Одинаковые раскраски",
            font_size=36
        ).to_edge(DOWN)
        self.wait(1)
        self.play(
            hex_right.animate.flip(axis=axis.get_unit_vector()),
            run_time=0.5
        )

        self.play(AddTextLetterByLetter(text_equal2), run_time=1)


        self.play(FadeOut(axis),FadeOut(text_equal2))
        hex_right.set_coloring([DOT_BLUE, DOT_BLUE, DOT_RED, DOT_RED, DOT_RED, DOT_RED])

        for _ in range(6):
            self.play(
                Rotate(hex_right, -PI/3),
                run_time=0.5
            )
            self.wait(0.5)

        text_equal3 = Text(
            "А эти две - различные",
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