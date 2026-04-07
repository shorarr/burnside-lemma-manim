from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots


class Sc8(Scene):

    def construct(self):

        # заголовок
        title = Text(
            "Поворот на 60°",
            font_size=36
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # основная формула
        formula = MathTex(
            r"e = (123456)"
        )

        formula.next_to(title, DOWN, buff=0.5)

        self.play(Write(formula))
        self.wait(1)

        # Шестиугольник
        hex_dots = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_dots.random_coloring()
        hex_dots.scale(0.8)

        self.play(FadeIn(hex_dots))
        self.wait(0.5)

        # Подсветка точек
        animations = []
        for dot in hex_dots.dots:
            glow = dot.copy().scale(2).set_opacity(0.4)

            animations.append(
                Succession(
                    FadeIn(glow),
                    FadeOut(glow)
                )
            )

        self.play(*animations, lag_ratio=0, run_time=1)

        self.wait(0.5)
        self.play(
            Rotate(hex_dots, angle=-PI / 3),
            run_time=2,
        )

        animations = []
        for dot in hex_dots.dots:
            glow = dot.copy().scale(2).set_opacity(0.4)

            animations.append(
                Succession(
                    FadeIn(glow),
                    FadeOut(glow)
                )
            )
        self.play(*animations, lag_ratio=0, run_time=1)

        # Текст
        text1 = Paragraph(
            "Чтобы раскраска не изменилась",
                  "все бусины в цикле должны быть одного цвета.",
            font_size=28,
            alignment="center",
        ).to_edge(DOWN)

        self.play(FadeIn(text1))
        self.wait(1)

        # Перекрашивание в 1 цвет
        hex_dots.set_coloring(DOT_BLUE)
        self.wait(1)
        hex_dots.set_coloring(DOT_GREEN)
        self.wait(1)
        hex_dots.set_coloring(DOT_RED)
        self.wait(1)

        self.play(
            Rotate(hex_dots, angle=-PI / 3),
            run_time=2,
        )
        self.wait(2)

        # Подпись
        text2 = Text(
            "Аналогично для поворотов на -60°, 300° и т.д.",
            font_size=26
        ).to_edge(DOWN, buff=1)

        self.play(FadeOut(text1))
        self.wait(0.5)
        self.play(Write(text2))
        self.play(
            Rotate(hex_dots, angle=-5 * PI / 3),
            run_time=2,
        )
        self.wait(1.5)

        # Очистка
        self.play(
            FadeOut(formula),
            FadeOut(text2)
        )

        self.wait(0.5)

        # Формула цикл
        cycle_text = Text("1 цикл", font_size=26)

        cycle_formula = MathTex(
            r"\Rightarrow 3^1"
        ).scale(0.8)

        text_formula = VGroup(cycle_text, cycle_formula)
        text_formula.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)

        # Формула
        xe_math = MathTex(r"|X^\tau| = 3")
        xe_math.scale(0.8)

        # Общий блок
        full_formula = VGroup(text_formula, xe_math)
        full_formula.arrange(RIGHT, buff=1, aligned_edge=DOWN)

        full_formula.to_edge(DOWN, buff=1.25)
        full_formula.set_x(0)

        self.play(Write(text_formula))
        self.play(Write(xe_math))


        # Финальный текст
        final_text = Text(
            "В этом случае есть всего 3 варианта раскраски",
            font_size=26
        )

        final_text.next_to(xe_math, DOWN, buff=0.3)
        final_text.center()
        final_text.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(final_text))
        self.wait(2)