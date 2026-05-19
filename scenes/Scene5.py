from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots

class Sc5(Scene):

    def construct(self):

        # Заголовок
        title = Text(
            "Как действует группа",
            font_size=40
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Определение
        definition = Text(
            "Композиция — это фундаментальная операция,\n"
            "определяющая структуру группы, при которой к двум элементам\n"
            "применяется правило, возвращающее третий элемент той же группы",
            font_size=32,
            t2w={"Композиция": BOLD}
        )

        definition.set_width(config.frame_width - 2)
        definition.move_to(ORIGIN)

        self.play(FadeIn(definition))
        self.wait(4)
        self.play(FadeOut(definition))

        # Первая формула
        formula = MathTex(r"\tau \cdot \tau = \tau^2")
        formula.scale(1.2)
        new_formula = MathTex(r"\tau \tau = \tau^2")
        new_formula.scale(1.2)
        new_formula.move_to(formula)

        formula.next_to(title, DOWN, buff=1)

        self.play(Write(formula))
        self.wait(1)

        # пояснение
        explanation = Text(
            "(поворот на 60° + поворот на 60° = поворот на 120°)",
            font_size=28
        )

        explanation.next_to(formula, DOWN, buff=0.5)

        self.play(Write(explanation))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(explanation),
            formula.animate.scale(1.5).move_to(ORIGIN),
            #Transform(formula, new_formula, run_time=2)
        )

        self.wait(0.5)

        caption = Text('Стандартная запись композиции', font_size=24)
        caption.next_to(formula, DOWN, buff=0.4)
        self.play(Write(caption))
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


        ##################### Часть 2 #####################

        tau_formula = MathTex(r"\tau = (123456)")
        tau_formula.move_to(ORIGIN)
        tau_formula.shift(UP * 2)

        self.play(Write(tau_formula))
        self.wait(1)

        top_row = VGroup(*[
            MathTex(str(i)) for i in range(1, 7)
        ]).arrange(RIGHT, buff=0.8)

        top_row.next_to(tau_formula, DOWN, buff=0.8)

        bottom_values = [2, 3, 4, 5, 6, 1]

        bottom_row = VGroup(*[
            MathTex(str(i)) for i in bottom_values
        ]).arrange(RIGHT, buff=0.8)

        bottom_row.next_to(top_row, DOWN, buff=0.8)

        self.play(Write(top_row))
        self.play(Write(bottom_row))
        self.wait(1)

        arrows = VGroup(*[
            Arrow(
                top_row[i].get_bottom(),
                bottom_row[i].get_top(),
                buff=0.1,
                stroke_width=1
            )
            for i in range(6)
        ])

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != tau_formula])
        self.play(tau_formula.animate.move_to(ORIGIN))

        # большая формула
        tau_formula2 = MathTex(r"\tau = (1 \, 2 \, 3 \, 4 \, 5 \, 6)")
        tau_formula2.scale(2)
        tau_formula2.move_to(ORIGIN)

        self.play(Transform(tau_formula, tau_formula2))
        self.wait(1)

        digits = tau_formula2[0][3:9]

        top_arrows = VGroup()

        for i in range(5):
            arrow = CurvedArrow(
                digits[i].get_top(),
                digits[i + 1].get_top(),
                angle=-PI / 2
            )
            top_arrows.add(arrow)

        self.play(LaggedStart(*[Create(a) for a in top_arrows], lag_ratio=0.15))
        self.wait(1)

        bottom_arrow = CurvedArrow(
            digits[5].get_bottom(),
            digits[0].get_bottom(),
            angle=-PI / 2
        )

        self.play(Create(bottom_arrow))
        self.wait(1)

        for i in range(6):
            next_i = (i + 1) % 6

            self.play(
                digits[i].animate.set_color(YELLOW),
                digits[next_i].animate.set_color(YELLOW),
                run_time=0.3
            )

            self.play(
                digits[i].animate.set_color(WHITE),
                digits[next_i].animate.set_color(WHITE),
                run_time=0.2
            )
        self.wait(1)

        text_again = Paragraph(
            "Ещё раз воздействуем элементом τ \n"
            "(поворот на 60)",
            font_size=26
        ).to_edge(LEFT, buff=0.8)

        tau_formula = MathTex(r"\tau = (1\;2\;3\;4\;5\;6)", font_size=60)
        tau_formula.next_to(text_again, UP, buff=0.8).align_to(text_again, LEFT)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )
        self.play(Write(tau_formula))
        self.wait(0.5)

        # шестиугольник
        hex_dots = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_dots.set_coloring([DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED, DOT_RED])
        hex_dots.to_edge(RIGHT, buff=1.5)

        labels_tau = hex_dots.get_labels()
        old_labels_tau = labels_tau.copy()

        for label in labels_tau:
            label.set_z_index(10)
        for i, label in enumerate(labels_tau):
            label.add_updater(
                lambda m, i=i: m.move_to(hex_dots.dots[i].get_center())
            )

        self.play(FadeIn(hex_dots))
        self.play(LaggedStart(*[Write(l) for l in labels_tau], lag_ratio=0.1))
        self.play(old_labels_tau.animate.set_opacity(0.3).scale(1.3))
        self.wait(0.5)

        # первое вращение на 60°
        self.play(
            Rotate(hex_dots, angle=-PI / 3),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(Write(text_again))
        self.wait(0.5)

        # второе вращение на 60°
        self.play(
            Rotate(hex_dots, angle=-PI / 3),
            run_time=1.5
        )
        self.wait(0.5)

        # MathTex с отдельными индексами, чтобы можно было адресовать цифры
        tau2_formula = MathTex(
            r"\tau^2 = (",
            "1", r"\,", "2", r"\,", "3", r"\,", "4", r"\,", "5", r"\,", "6",
            r")", font_size=60
        )
        digit_idx = {1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 11}

        tau2_formula.next_to(text_again, DOWN, buff=0.8).align_to(tau_formula, LEFT)

        self.play(Write(tau2_formula))
        self.wait(0.3)

        # Стрелки сверху
        arrows_top = VGroup()
        top_pairs = [(1, 3), (2, 4), (3, 5)]
        for a, b in top_pairs:
            arrows_top.add(
                CurvedArrow(
                    tau2_formula[digit_idx[a]].get_top() + UP * 0.05,
                    tau2_formula[digit_idx[b]].get_top() + UP * 0.05,
                    angle=-PI / 2,
                    stroke_width=2,
                    tip_length=0.12
                )
            )

        # Стрелки снизу
        arrows_bottom = VGroup()
        bottom_pairs = [(5, 1), (6, 2)]
        for a, b in bottom_pairs:
            arrows_bottom.add(
                CurvedArrow(
                    tau2_formula[digit_idx[a]].get_bottom() + DOWN * 0.05,
                    tau2_formula[digit_idx[b]].get_bottom() + DOWN * 0.05,
                    angle=-PI / 2,
                    stroke_width=2,
                    tip_length=0.12
                )
            )

        self.play(
            LaggedStart(*[Create(a) for a in arrows_top], lag_ratio=0.2),
            run_time=1.2
        )
        self.play(
            LaggedStart(*[Create(a) for a in arrows_bottom], lag_ratio=0.3),
            run_time=0.8
        )
        self.wait(2)

        tau2_cycles = MathTex(
            r"\tau^2 = (1\;3\;5)(2\;4\;6)", font_size=60
        ).move_to(tau2_formula).align_to(tau_formula, LEFT)

        self.play(
            FadeOut(arrows_top),
            FadeOut(arrows_bottom),
            Transform(tau2_formula, tau2_cycles)
        )
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])