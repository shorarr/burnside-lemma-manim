from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from objects.hexdots import HexDots

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
            Transform(formula, new_formula, run_time=2)
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
        self.play(*[FadeOut(mob) for mob in self.mobjects])