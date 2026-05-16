from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots


class Sc7(Scene):

    def construct(self):

        # заголовок
        title = Text(
            "Тождественное преобразование (e)",
            font_size=36
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # основная формула
        formula = MathTex(
            r"e = (1)(2)(3)(4)(5)(6)"
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

        # Текст
        text1 = Text(
            "Все раскраски сохраняются на своих местах",
            font_size=28
        ).to_edge(DOWN)

        self.play(FadeIn(text1))
        self.wait(1)

        # Поворот на 360
        self.play(
            Rotate(hex_dots, angle=2 * PI),
            run_time=2
        )

        self.wait(0.5)

        # Подпись
        text2 = Text(
            "Аналогично для поворотов на 360°, 720° и т.д.",
            font_size=26
        ).to_edge(DOWN)

        self.play(FadeOut(text1))
        self.wait(0.5)
        self.play(Write(text2))
        self.wait(1.5)

        # Очистка
        self.play(
            FadeOut(formula),
            FadeOut(text2)
        )

        self.wait(0.5)
        self.play(hex_dots.animate.scale(1.25))



        self.wait(0.5)

        # Формула X^e
        xe_math = MathTex(r"|X^e| = 3^6")
        xe_math.to_edge(DOWN, buff=1)

        self.play(Write(xe_math))

        # Перебор всех раскрасок
        colorings = list(hex_dots.generate_unique_colorings())

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

        # Финальный текст
        final_text = Text(
            "В этом случае все возможные раскраски уникальны",
            font_size=26
        )

        final_text.next_to(xe_math, DOWN, buff=0.3)

        self.play(FadeIn(final_text))
        self.wait(2)

        self.clear()