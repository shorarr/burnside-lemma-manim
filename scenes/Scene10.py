from manim import *
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots


class Sc10(Scene):

    def construct(self):

        # Заголовок
        title = Text(
            "Поворот на 180°",
            font_size=36
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        formula = MathTex(r"\tau^3 = (14)(25)(36)")
        formula.next_to(title, DOWN, buff=0.5)

        self.play(Write(formula))
        self.wait(2)

        # Формула расписанная
        formula_big = MathTex(
            r"\tau^3 = (",
            "1", r"\,", "4",
            r")(",
            "2", r"\,", "5",
            r")(",
            "3", r"\,", "6",
            r")"
        )

        formula_big.scale(2)
        formula_big.move_to(ORIGIN)

        self.play(Transform(formula, formula_big))
        self.wait(1)

        # Пары для стрелочек
        cycle1 = [formula_big[1], formula_big[3]]
        cycle2 = [formula_big[5], formula_big[7]]
        cycle3 = [formula_big[9], formula_big[11]]

        # стрелки
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
            make_pair_arrow(*cycle3),
        )

        arrows_bottom = VGroup(
            make_pair_arrow_bottom(*cycle1),
            make_pair_arrow_bottom(*cycle2),
            make_pair_arrow_bottom(*cycle3),
        )

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2))
        self.play(LaggedStart(*[Create(a) for a in arrows_bottom], lag_ratio=0.2))
        self.wait(1)

        # Подсветка
        for cycle in [cycle1, cycle2, cycle3]:
            self.play(
                Indicate(cycle[0], scale_factor=1.1),
                Indicate(cycle[1], scale_factor=1.1),
                run_time=0.5
            )

        self.wait(1)

        # Сдвиг влево
        formula_with_arrows = VGroup(formula_big, arrows, arrows_bottom)

        self.remove(formula)
        self.play(
            formula_with_arrows.animate.scale(0.6).to_edge(LEFT, buff=1),
            run_time=1.5
        )

        # Шестиугольник
        hex_dots = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_GREEN]*2)
        hex_dots.to_edge(RIGHT, buff=1)

        self.play(FadeIn(hex_dots))
        self.wait(0.5)

        labels = hex_dots.get_labels()
        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.1))
        self.wait(1)

        old_labels = labels.copy()
        for label in labels:
            label.set_z_index(10)

        for i, label in enumerate(labels):
            label.add_updater(
                lambda m, i=i: m.move_to(hex_dots.dots[i].get_center())
            )

        self.play(
            old_labels.animate.set_opacity(0.3).scale(1.3)
        )
        self.wait(0.5)

        hex_g = VGroup(hex_dots)
        hex_g.save_state()

        # Стрелочки для вершин
        def make_diameter(i, j, color=WHITE):
            return DoubleArrow(
                hex_dots.dots[i].get_center(),
                hex_dots.dots[j].get_center(),
                buff=0,
                color=color,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12
            )

        diam1 = make_diameter(0, 3).scale(0.8)
        diam2 = make_diameter(1, 4).scale(0.8)
        diam3 = make_diameter(2, 5).scale(0.8)

        # Анимация основная
        for diam in [diam1, diam2, diam3]:
            # показать стрелку
            self.play(Create(diam))
            self.wait(0.3)

            self.play(
                Rotate(hex_g, angle=PI),
                run_time=2
            )

            self.wait(0.5)
            self.play(FadeOut(diam))

            # вернуть всё как было
            self.play(Restore(hex_g), run_time=1)

        # Независимая перекраска
        text1 = Text(
            "Каждый цикл можно красить независимо",
            font_size=28
        ).to_edge(DOWN)

        self.play(FadeIn(text1))
        self.wait(1)

        text1 = Text(
            "Каждый цикл можно красить независимо",
            font_size=28
        ).to_edge(DOWN)

        self.play(FadeIn(text1))

        pairs = [
            (0, 3),  # 1–4
            (1, 4),  # 2–5
            (2, 5)  # 3–6
        ]

        pairs_with_arrows = [
            ((0, 3), diam1),
            ((1, 4), diam2),
            ((2, 5), diam3),
        ]

        # Смены цвета пары
        def recolor_pair(i, j):
            for _ in range(5):
                ci = hex_dots.dots[i].get_color()
                c_new = random.choice([x for x in DOT_COLORS if ManimColor(x) != ci])
                hex_dots.dots[i].set_color(c_new)
                hex_dots.dots[j].set_color(c_new)

                self.wait(0.3)

        for (i, j), diam in pairs_with_arrows:

            self.play(Create(diam))

            # подсветка точек
            self.play(
                Indicate(hex_dots.dots[i], scale_factor=1.1),
                Indicate(hex_dots.dots[j], scale_factor=1.1),
                run_time=0.5
            )

            recolor_pair(i, j)

            self.wait(0.3)
            self.play(FadeOut(diam))

            hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_GREEN] * 2)
            self.wait(0.3)


        self.play(FadeOut(text1))

        self.play(FadeOut(text1))

        # Формулы конец
        cycle_text = Text("3 цикла", font_size=26)
        cycle_formula = MathTex(r"\Rightarrow 3^3").scale(0.8)

        text_formula = VGroup(cycle_text, cycle_formula)
        text_formula.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)

        xe_math = MathTex(r"|X^{\tau^3}| = 3^3").scale(0.8)

        full_formula = VGroup(text_formula, xe_math)
        full_formula.arrange(RIGHT, buff=1)
        full_formula.to_edge(LEFT, buff=1)
        full_formula.next_to(formula_with_arrows, DOWN, buff=0.8)

        self.play(Write(text_formula))
        self.play(Write(xe_math))

        self.wait(2)

        self.clear()