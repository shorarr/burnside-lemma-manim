from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots


class Sc1(Scene):

    def construct(self):

        # Заголовок
        title = Paragraph(
            "Задача:\n"
            "сколько различных бус можно составить из 6 бусинок,\n"
            "если каждая может быть красной, зелёной или синей?",
            font_size=24,
            color=PRIMARY_COLOR,
            alignment="center",
            line_spacing = 1.1
        ).move_to(ORIGIN)

        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.7).to_edge(UP))
        self.wait(1)

        # Шестиугольник с точками
        hex_dots = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)

        self.play(Create(hex_dots), run_time=1.0)
        self.wait(1)

        # Демонстрация 3 разных раскрасок
        self.play(*[dot.animate.set_color(DOT_RED) for dot in hex_dots.dots], run_time=0.1)
        self.wait(1)

        self.play(*[dot.animate.set_color(DOT_GREEN) for dot in hex_dots.dots], run_time=0.1)
        self.wait(1)

        self.play(*[dot.animate.set_color(DOT_BLUE) for dot in hex_dots.dots], run_time=0.1)
        self.wait(1.5)

        for _ in range(8):
            self.play(hex_dots.animate.random_coloring(), run_time=0.01)
            self.wait(0.25)
        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_GREEN, DOT_RED, DOT_BLUE, DOT_GREEN])

        self.wait(2)
        self.play(FadeOut(title))
        self.play(
            hex_dots.animate.scale(0.7).to_edge(UP)
        )

        # Подпись цветов
        colors_text1 = MathTex(
            r"C = \{red, green, blue\}",
            font_size=36
        ).next_to(hex_dots, DOWN, buff=0.8)

        colors_text2 = MathTex(
            r"C = \{r, g, b\}",
            font_size=36
        ).next_to(hex_dots, DOWN, buff=0.8)

        self.play(Write(colors_text1))
        self.wait(1)
        self.play(FadeTransform(colors_text1, colors_text2))

        # |C| = 3
        card_text = MathTex(
            r"|C| = 3",
            font_size=48
        ).next_to(colors_text1, DOWN, buff=0.6)

        self.play(Write(card_text))
        self.wait(1)

        # Переменные
        left = MathTex(r"\{x_1, x_2, x_3, x_4, x_5, x_6\},", font_size=36)
        where = Text("где", font_size=24)
        right = MathTex(r"x_k \in C")

        line = VGroup(left, where, right).arrange(RIGHT, buff=0.3)
        line.next_to(card_text, DOWN, buff=0.6)
        self.play(Write(line))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Лемма Бернсайда
        lemma = Paragraph(
            "Лемма Бернсайда\n"
            "число уникальных комбинаций равно среднему числу объектов,\n"
            "которые не меняются при каждом возможном действии (повороте/отражении)",
            font_size=24,
            color=PRIMARY_COLOR,
            alignment="center",
            line_spacing=1.5
        ).move_to(ORIGIN)
        lemma[0].scale(1.5)

        self.play(Write(lemma), run_time=4)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])