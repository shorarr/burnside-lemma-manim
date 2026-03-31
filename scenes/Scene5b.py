from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from objects.hexdots import HexDots
from objects.axis import main_axis

class Sc5b(Scene):

    def construct(self):
        hex_dots = HexDots([DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED, DOT_RED])

        self.play(FadeIn(hex_dots))
        self.wait(1)

        # Индексы
        labels = VGroup()

        for i, dot in enumerate(hex_dots.dots):
            label = MathTex(str(i + 1)).scale(0.7)
            label.next_to(dot, direction=OUT, buff=0.2)
            labels.add(label)

        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.1))
        self.wait(1)

        old_labels = labels.copy()

        self.play(
            old_labels.animate.set_opacity(0.3).scale(1.4)
        )
        self.wait(0.5)

        new_labels = labels.copy()
        self.play(
            ReplacementTransform(labels, new_labels, run_time=0.02),
        )

        #self.play(FadeIn(new_labels), run_time=0.02)
        self.wait(0.5)

        group_to_rotate = VGroup(hex_dots, new_labels)

        self.play(
            Rotate(group_to_rotate, angle=-PI / 3),
            run_time=2,
        )

        for label in new_labels:
            self.play(label.animate.rotate(PI / 3), run_time=0.2)



        self.wait(1)

        left_group = VGroup(hex_dots, new_labels, old_labels)

        self.play(left_group.animate.to_edge(LEFT))
        self.wait(1)

        # Второй шестиугольник
        hex2 = HexDots()
        hex2.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED])

        # индексы
        old_labels2 = old_labels.copy()
        old_labels2.move_to(hex2, ORIGIN)

        hex2g = VGroup(hex2, old_labels2)
        hex2g.to_edge(RIGHT)

        labels2 = VGroup()

        for i, dot in enumerate(hex2.dots):
            label = MathTex(str(i + 1)).scale(0.7)
            label.next_to(dot, direction=OUT, buff=0.2)
            labels2.add(label)

        self.play(FadeIn(hex2g), FadeIn(labels2))
        self.wait(1)

        new_positions = []

        for i in range(6):
            prev_index = (i + 1) % 6
            new_positions.append(hex2.dots[prev_index].get_center())

        self.play(
            *[
                labels2[i].animate.move_to(new_positions[i])
                for i in range(6)
            ],
            run_time=2
        )

        self.wait(1)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Третий шестиугольник (отражения)

        hex3 = HexDots()
        hex3.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED])
        old_labels.move_to(hex3, ORIGIN)

        hex3g = VGroup(hex3, old_labels)
        hex3g.to_edge(LEFT)

        hex3g2 = hex3g.copy()
        hex3g2.to_edge(RIGHT)

        labels3 = VGroup()
        for i, dot in enumerate(hex3.dots):
            label = MathTex(str(i + 1)).scale(0.7)
            label.next_to(dot, direction=OUT, buff=0.2)
            labels3.add(label)

        labels4 = VGroup()
        for i, dot in enumerate(hex3g2[0].dots):
            label = MathTex(str(i + 1)).scale(0.7)
            label.next_to(dot, direction=OUT, buff=0.2)
            labels4.add(label)

        self.play(FadeIn(hex3g), FadeIn(labels3))
        self.wait(1)

        # ось
        axis = main_axis

        axis.set_length(hex3.get_height() * 1.2)
        axis.move_to(hex3)

        axis2 = axis.copy()
        axis2.move_to(hex3g2)

        self.play(Create(axis))

        # отражение
        self.play(
            hex3.animate.flip(UP),
            labels3.animate.flip(UP),
            run_time=1
        )

        for label in labels3:
            self.play(label.animate.flip(UP), run_time=0.2)
        self.wait(1)

        self.play(FadeIn(hex3g2), FadeIn(labels4), FadeIn(axis2))
        self.wait(1)

        mapping = {
            0: 1,
            1: 0,
            2: 5,
            5: 2,
            3: 4,
            4: 3
        }

        new_positions = [
            hex3g2[0].dots[mapping[i]].get_center()
            for i in range(6)
        ]

        self.play(
            *[
                labels4[i].animate.move_to(new_positions[i])
                for i in range(6)
            ],
            run_time=1
        )
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])