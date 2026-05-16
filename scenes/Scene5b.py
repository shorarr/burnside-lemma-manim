from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots
from objects.axis import main_axis

class Sc5b(Scene):

    def construct(self):
        hex_dots = HexDots(
            dot_colors=DOT_COLORS,
            radius=HEX_RADIUS,
            dot_radius=DOT_RADIUS
        )
        hex_dots.set_coloring([DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED, DOT_RED])

        self.play(FadeIn(hex_dots))
        self.wait(1)

        # Индексы
        labels = VGroup()

        labels = hex_dots.get_labels()
        old_labels = labels.copy()

        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.1))
        self.wait(1)

        for label in labels:
            label.set_z_index(10)

        for i, label in enumerate(labels):
            label.add_updater(
                lambda m, i=i: m.move_to(hex_dots.dots[i].get_center())
            )

        self.play(
            old_labels.animate.set_opacity(0.3).scale(1.4)
        )
        self.wait(0.5)

        self.wait(0.5)

        self.play(
            Rotate(hex_dots, angle=-PI / 3),
            run_time=2,
        )

        self.wait(1)

        left_group = VGroup(hex_dots, labels, old_labels)

        self.play(left_group.animate.to_edge(LEFT))
        self.wait(1)

        # Второй шестиугольник
        hex2 = HexDots(
            dot_colors=DOT_COLORS,
            radius=HEX_RADIUS,
            dot_radius=DOT_RADIUS
        )
        hex2.set_coloring([DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED, DOT_RED])

        # индексы
        old_labels2 = old_labels.copy()
        old_labels2.move_to(hex2, ORIGIN)

        hex2g = VGroup(hex2, old_labels2)
        hex2g.to_edge(RIGHT)

        labels2 = hex2.get_labels()

        self.play(FadeIn(hex2g), FadeIn(labels2))
        self.wait(1)

        new_positions = []

        for i in range(6):
            prev_index = (i - 1) % 6
            new_positions.append(old_labels2[prev_index].get_center())

        self.play(
            *[
                old_labels2[i].animate.move_to(new_positions[i])
                for i in range(6)
            ],
            run_time=2
        )

        self.wait(1)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Третий шестиугольник (отражения)

        hex3 = HexDots(
            dot_colors=DOT_COLORS,
            radius=HEX_RADIUS,
            dot_radius=DOT_RADIUS
        )
        hex3.set_coloring([DOT_RED, DOT_BLUE, DOT_RED, DOT_RED, DOT_BLUE, DOT_RED])
        old_labels.move_to(hex3, ORIGIN)

        hex3g = VGroup(hex3, old_labels)
        hex3g.to_edge(LEFT)

        hex3g2 = hex3g.copy()
        hex3g2.to_edge(RIGHT)

        labels3 = hex3.get_labels()
        for label in labels3:
            label.set_z_index(10)

        for i, label in enumerate(labels3):
            label.add_updater(
                lambda m, i=i: m.move_to(hex3.dots[i].get_center())
            )

        labels4 = hex3g2[0].get_labels()

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
            run_time=1
        )

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
            hex3g2[1][mapping[i]].get_center()
            for i in range(6)
        ]

        self.play(
            *[
                hex3g2[1][i].animate.move_to(new_positions[i])
                for i in range(6)
            ],
            run_time=1
        )
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])