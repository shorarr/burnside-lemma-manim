from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from objects.hexdots import HexDots

class Sc3(Scene):

    def construct(self):

        # формулы
        C_formula = MathTex(
            r"C = \{r, g, b\}"
        ).move_to(ORIGIN)

        X_formula = MathTex(
            r"X = \{(x_1, x_2, x_3, x_4, x_5, x_6)\ |\ x_i \in C\}"
        ).next_to(C_formula, UP, buff=1.2)

        xi = MathTex(r"x_i", font_size=32)
        text1 = Text("— цвет", font_size=20)
        i_part = MathTex(r"i", font_size=32)
        text2 = Text("-й бусинки", font_size=20)

        caption = VGroup(xi, text1, i_part, text2).arrange(RIGHT, buff=0.15).next_to(C_formula, DOWN, buff=0.25)

        count_formula = MathTex(r"|X| = 3^6 = 729")
        count_txt = Text("Количество всех возможных комбинаций", font_size=20)
        count_text = VGroup(count_formula, count_txt).arrange(DOWN, buff=0.15)

        count_text.next_to(caption, DOWN, buff=1.2)

        self.play(Write(X_formula))
        self.wait(0.5)

        self.play(Write(C_formula))
        self.wait(0.5)

        self.play(FadeIn(caption))
        self.wait(1)

        self.play(Write(count_formula))
        self.wait(1)

        self.play(FadeIn(count_txt))
        self.wait(1)

        # убираем лишнее

        self.play(
            FadeOut(X_formula),
            FadeOut(C_formula),
            FadeOut(caption)
        )

        self.play(
            count_text.animate.to_edge(UP)
        )

        self.wait(1)

        # шестиугольник

        hex_dots = HexDots()
        self.play(FadeIn(hex_dots))
        self.wait(1)

        # перебор всех раскрасок

        colorings = list(hex_dots.all_unique_colorings())

        def update_colors(mob, alpha):
            index = int(alpha * (len(colorings) - 1))
            mob.set_coloring(colorings[index])

        self.play(
            UpdateFromAlphaFunc(
                hex_dots,
                update_colors
            ),
            run_time=6,
            rate_func=smooth
        )

        self.wait(2)
        # оставляем 1 раскраску

        example = [DOT_RED, DOT_GREEN, DOT_BLUE, DOT_RED, DOT_GREEN, DOT_BLUE]

        hex_dots.set_coloring(example)

        self.wait(1)

        self.play(
            Rotate(
                hex_dots,
                angle=-PI,
                run_time=2
            )
        )

        self.wait(1)

        # последний текст

        final_text = Paragraph(
            "Но некоторые раскраски совпадают,\n",
            "значит уникальных - меньше 729",
            font_size=24,
            color=PRIMARY_COLOR,
            alignment="center",
        )

        final_text.to_edge(DOWN)

        self.play(Write(final_text))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])