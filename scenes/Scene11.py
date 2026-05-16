from manim import *
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots
from objects.axis import main_axis

class Sc11(Scene):

    def construct(self):

        # Заголовок
        title = Text(
            "Отражение относительно оси (через вершины)",
            font_size=36
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Основные формулы
        formula_big = MathTex(
            r"\sigma\tau^5 = (",
            "1", r")(",
            "4", r")(",
            "2", r"\,", "6",
            r")(",
            "3", r"\,", "5",
            r")"
        )
        formula_big25 = MathTex(
            r"\sigma\tau^3 = (",
            "2", r")(",
            "5", r")(",
            "1", r"\,", "3",
            r")(",
            "4", r"\,", "6",
            r")"
        ).scale(1.2).to_edge(LEFT, buff=1)
        formula_big36 = MathTex(
            r"\sigma\tau = (",
            "3", r")(",
            "6", r")(",
            "1", r"\,", "5",
            r")(",
            "2", r"\,", "4",
            r")"
        ).scale(1.2).to_edge(LEFT, buff=1)

        formula_big.scale(2)
        formula_big.move_to(ORIGIN)

        self.play(Write(formula_big))
        self.wait(1)

        # Циклы для подсветки
        fixed1 = formula_big[1]
        fixed2 = formula_big[3]

        cycle1 = [formula_big[5], formula_big[7]]   # 2 6
        cycle2 = [formula_big[9], formula_big[11]]  # 3 5

        # Стрелки
        def make_pair_arrow(a, b):
            return CurvedArrow(
                a.get_top(),
                b.get_top(),
                angle=-PI / 2,
                stroke_width=2
            )

        def make_pair_arrow_bottom(a, b):
            return CurvedArrow(
                b.get_bottom(),
                a.get_bottom(),
                angle=-PI / 2,
                stroke_width=2
            )

        arrows = VGroup(
            make_pair_arrow(*cycle1),
            make_pair_arrow(*cycle2),
        )

        arrows_bottom = VGroup(
            make_pair_arrow_bottom(*cycle1),
            make_pair_arrow_bottom(*cycle2),
        )

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2))
        self.play(LaggedStart(*[Create(a) for a in arrows_bottom], lag_ratio=0.2))

        # Подсветка
        self.play(Indicate(fixed1), scale_factor=1.1, run_time=0.5)
        self.play(Indicate(fixed2), scale_factor=1.1, run_time=0.5)# неподвижные

        for cycle in [cycle1, cycle2]:
            self.play(
                Indicate(cycle[0], scale_factor=1.1),
                Indicate(cycle[1], scale_factor=1.1),
                run_time=0.5
            )

        self.wait(1)

        formula_with_arrows = VGroup(formula_big, arrows, arrows_bottom)

        self.play(
            formula_with_arrows.animate.scale(0.6).to_edge(LEFT, buff=1),
            run_time=1.5
        )

        # Шестиугольник
        hex_dots = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_GREEN]*2)
        hex_dots.to_edge(RIGHT, buff=1)

        self.play(FadeIn(hex_dots))

        labels = hex_dots.get_labels()
        old_labels = labels.copy()

        for label in labels:
            label.set_z_index(10)

        for i, label in enumerate(labels):
            label.add_updater(
                lambda m, i=i: m.move_to(hex_dots.dots[i].get_center())
            )
        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.1))



        self.play(
            old_labels.animate.set_opacity(0.3).scale(1.3)
        )
        self.wait(0.5)

        hex_g = VGroup(hex_dots)
        hex_g.save_state()

        # Ось
        def make_axis(i, j):
            axis = main_axis.copy()

            p1 = hex_dots.dots[i].get_center()
            p2 = hex_dots.dots[j].get_center()

            axis.put_start_and_end_on(p1, p2)
            axis.scale(1.2, about_point=axis.get_center())
            axis.set_z_index(-1)

            return axis

        # Праы для оси
        configs = [
            ((0, 3), (1, 5), (2, 4)),  # ось 1–4
            ((1, 4), (2, 0), (3, 5)),  # ось 2–5
            ((2, 5), (0, 4), (1, 3)),  # ось 3–6
        ]

        axes = [
            make_axis(0, 3),
            make_axis(1, 4),
            make_axis(2, 5),
        ]

        counter = 1
        # анимация
        for axis, conf in zip(axes, configs):

            if counter == 2:
                self.play(FadeTransform(formula_with_arrows, formula_big25))
                #self.remove(formula_with_arrows)
            elif counter == 3:
                self.play(FadeTransform(formula_big25, formula_big36))
                #self.remove(formula_big25)

            fixed = conf[0]
            pairs = conf[1:]

            self.play(Create(axis))

            # подсветка неподвижных
            self.play(
                Indicate(hex_dots.dots[fixed[0]]),
                Indicate(hex_dots.dots[fixed[1]])
            )

            self.wait(0.5)

            # подсветка пар
            for i, j in pairs:
                self.play(
                    Indicate(hex_dots.dots[i]),
                    Indicate(hex_dots.dots[j]),
                    run_time=0.5
                )

            # отражение
            self.play(
                hex_g.animate.flip(axis=axis.get_unit_vector()),
                run_time=1
            )

            self.wait(0.5)
            self.play(FadeOut(axis))

            self.play(Restore(hex_g), run_time=0.8)
            counter += 1

        # Объяснение
        text_fixed = Text("2 неподвижные точки, 2 пары точек", font_size=28).to_edge(DOWN)
        self.play(FadeIn(text_fixed))
        self.wait(2)

        self.play(FadeOut(text_fixed))

        # Формулы
        cycle_text = Text("4 цикла", font_size=26)
        cycle_formula = MathTex(r"\Rightarrow 3^4").scale(0.8)

        text_formula = VGroup(cycle_text, cycle_formula)
        text_formula.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)

        xe_math = MathTex(r"|X^{\sigma}| = 3^4").scale(0.8)

        full_formula = VGroup(text_formula, xe_math)
        full_formula.arrange(RIGHT, buff=1)
        full_formula.to_edge(LEFT, buff=1)
        full_formula.next_to(formula_with_arrows, DOWN, buff=0.8)

        self.play(Write(text_formula))
        self.play(Write(xe_math))

        self.wait(2)

        self.clear()