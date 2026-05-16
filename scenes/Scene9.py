from manim import *
import sys
import os
import random

from typing_extensions import runtime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots


class Sc9(Scene):

    def construct(self):

        # заголовок
        title = Text(
            "Поворот на 120°",
            font_size=36
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Основная формула
        formula = MathTex(r"\tau^2 = (135)(246)")
        formula.next_to(title, DOWN, buff=0.5)

        self.play(Write(formula))
        self.wait(2)

        formula_big = MathTex(
            r"\tau^2 = (",
            "1", r"\,", "3", r"\,", "5",
            r")(",
            "2", r"\,", "4", r"\,", "6",
            r")"
        )

        formula_big.scale(2)
        formula_big.move_to(ORIGIN)

        self.play(Transform(formula, formula_big))
        self.wait(1)

        # Выделение цифр из формулы
        cycle1 = [formula_big[1], formula_big[3], formula_big[5]]  # 1 3 5
        cycle2 = [formula_big[7], formula_big[9], formula_big[11]]  # 2 4 6

        # Стрелки для формулы
        arrows1 = VGroup()

        for i in range(2):
            arrows1.add(
                CurvedArrow(
                    cycle1[i].get_top(),
                    cycle1[i + 1].get_top(),
                    angle=-PI / 2,
                    stroke_width=2
                )
            )

        arrow_last1 = CurvedArrow(
            cycle1[2].get_bottom(),
            cycle1[0].get_bottom(),
            angle=-PI / 2,
            stroke_width=2
        )

        arrows2 = VGroup()

        for i in range(2):
            arrows2.add(
                CurvedArrow(
                    cycle2[i].get_top(),
                    cycle2[i + 1].get_top(),
                    angle=-PI / 2,
                    stroke_width=2
                )
            )

        arrow_last2 = CurvedArrow(
            cycle2[2].get_bottom(),
            cycle2[0].get_bottom(),
            angle=-PI / 2,
            stroke_width=2
        )

        # Анимация формулы
        self.play(LaggedStart(*[Create(a) for a in arrows1], lag_ratio=0.15))
        self.play(Create(arrow_last1))

        self.play(LaggedStart(*[Create(a) for a in arrows2], lag_ratio=0.15))
        self.play(Create(arrow_last2))

        self.wait(1)

        # Подсветка
        for cycle in [cycle1, cycle2]:
            for i in range(3):
                next_i = (i + 1) % 3

                self.play(
                    Indicate(cycle[i], scale_factor=1.1),
                    Indicate(cycle[next_i], scale_factor=1.1),
                    run_time=0.5
                )

        self.wait(1)
        formula_with_arrows = VGroup(formula_big, arrows1, arrows2, arrow_last1, arrow_last2)

        self.remove(formula)
        self.play(
            formula_with_arrows.animate
            .scale(0.6)
            .to_edge(LEFT, buff=1),
            run_time=1.5
        )

        # Шестиугольник
        hex_dots = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE])
        hex_dots.to_edge(RIGHT, buff=1)

        self.play(FadeIn(hex_dots))
        self.wait(0.5)

        # Индексы
        labels = hex_dots.get_labels()
        old_labels = labels.copy()

        for label in labels:
            label.set_z_index(10)

        for i, label in enumerate(labels):
            label.add_updater(
                lambda m, i=i: m.move_to(hex_dots.dots[i].get_center())
            )

        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.1))
        self.wait(1)

        self.play(
            old_labels.animate.set_opacity(0.3).scale(1.3)
        )
        self.wait(0.5)

        p1 = hex_dots.dots[0].get_center()
        p2 = hex_dots.dots[2].get_center()
        p3 = hex_dots.dots[4].get_center()

        arrow1 = Arrow(
            p1, p2,
            buff=0,
            color=DOT_RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12
        )

        arrow2 = Arrow(
            p2, p3,
            buff=0,
            color=DOT_RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12
        )

        arrow3 = Arrow(
            p3, p1,
            buff=0,
            color=DOT_RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.12
        )

        triangle_arrows = VGroup(arrow1, arrow2, arrow3)
        triangle_arrows.scale(0.8, about_point=hex_dots.get_center())

        # Треугольники 2
        triangle_arrows_green = (
            triangle_arrows.copy()
            .rotate(-PI / 3, about_point=hex_dots.get_center())
            .set_color(DOT_BLUE)
        )

        self.play(Create(triangle_arrows))
        self.wait(0.25)
        self.play(Create(triangle_arrows_green))
        self.wait(0.5)

        for _ in range(1):
            self.play(
                Rotate(hex_dots, angle=-2 * PI / 3),
                run_time=1
            )
            self.wait(0.5)

        self.wait(0.5)

        # Красить независимо
        text1 = Text(
            "Каждый цикл можно красить независимо",
            font_size=28
        ).to_edge(DOWN)

        self.play(FadeOut(triangle_arrows_green))
        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE])
        triangle_arrows_green.set_color(WHITE)
        self.play(triangle_arrows.animate.set_color(WHITE), runtime=0.5)

        self.play(FadeIn(text1))

        # рандомный цикл 1
        for _ in range(5):
            for i in [0, 2, 4]:
                c = hex_dots.dots[i].get_color()
                hex_dots.dots[i].set_color(
                    random.choice([x for x in DOT_COLORS if ManimColor(x) != c])
                )
            self.wait(0.3)

        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE])
        self.play(FadeOut(triangle_arrows))
        self.play(FadeIn(triangle_arrows_green))

        # рандомный цикл 2
        for _ in range(5):
            for i in [1, 3, 5]:
                c = hex_dots.dots[i].get_color()
                hex_dots.dots[i].set_color(
                    random.choice([x for x in DOT_COLORS if ManimColor(x) != c])
                )
            self.wait(0.3)

        self.wait(1)

        self.play(FadeOut(text1))

        # формулы конец
        cycle_text = Text("2 цикла", font_size=26)
        cycle_formula = MathTex(r"\Rightarrow 3^2").scale(0.8)

        text_formula = VGroup(cycle_text, cycle_formula)
        text_formula.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)

        xe_math = MathTex(r"|X^{\tau^2}| = 3^2").scale(0.8)

        full_formula = VGroup(text_formula, xe_math)
        full_formula.arrange(RIGHT, buff=1, aligned_edge=DOWN)
        full_formula.to_edge(LEFT, buff=1)
        full_formula.next_to(formula_with_arrows, DOWN, buff=0.8)

        self.play(Write(text_formula))
        self.play(Write(xe_math))

        self.wait(2)

        # Аналогично
        analog_text = Text(
            "Аналогично для τ⁴",
            font_size=30
        ).to_edge(DOWN, buff=0.8)

        formula_with_arrows2 = formula_with_arrows.copy()
        formula_with_arrows2.next_to(formula_with_arrows, UP, buff=0.5)

        formula_with_arrows2[0].become(
            MathTex(
                r"\tau^4 = (",
                "1", r"\,", "5", r"\,", "3",
                r")(",
                "2", r"\,", "6", r"\,", "4",
                r")"
            )
            .scale(1.2)
            .move_to(formula_with_arrows2[0])
        )
        formula_with_arrows2.move_to(ORIGIN).to_edge(LEFT, buff=1)

        self.wait(1)
        for _ in range(1):
            self.play(
                Rotate(hex_dots, angle=2 * PI / 3),
                run_time=0.5
            )
            self.wait(0.5)
        self.play(Write(analog_text))
        self.play(
            formula_with_arrows.animate.next_to(
                formula_with_arrows2, UP, buff=0.5
            ),
            FadeIn(formula_with_arrows2),
        )

        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE, DOT_RED, DOT_BLUE])

        self.wait(0.5)

        self.play(
            Rotate(hex_dots, angle=-4 * PI / 3),
            run_time=2
        )

        self.wait(2)

        self.clear()