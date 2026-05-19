from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots
from objects.table_actions import action_table
from objects.axis import main_axis


class Sc13(Scene):

    def construct(self):

        # Заголовок
        title = Text(
            "Подсчет по лемме Бернсайда",
            font_size=36
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Таблица
        table = action_table.scale(0.4).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(table))
        self.wait(1)
        self.play(FadeOut(title))

        # Шестиугольник
        hex_dots = HexDots(
            dot_colors=DOT_COLORS,
            radius=HEX_RADIUS,
            dot_radius=DOT_RADIUS
        )
        hex_dots.set_coloring([DOT_RED, DOT_BLUE, DOT_GREEN]*2)
        hex_dots.scale(0.75)
        hex_dots.next_to(table, UP, buff=1)

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
        self.wait(1)
        self.play(
            old_labels.animate.set_opacity(0.3).scale(1.4)
        )
        self.wait(0.5)

        hex_g = VGroup(hex_dots)
        hex_g.save_state()

        table1, table2 = action_table

        cells1 = table1.get_entries()
        cells2 = table2.get_entries()

        # индексы:
        # 0–6 первая строка
        # 7–13 вторая строка

        def do_rotation(angle):
            self.play(
                Rotate(hex_g, angle=angle),
                run_time=1
            )

        def do_reflection(axis_vector):
            self.play(
                hex_g.animate.flip(axis=axis_vector),
                run_time=1
            )

        # Повороты

        rotations = [
            (1, 0),          # e
            (2, -PI/3),      # τ
            (3, -2*PI/3),    # τ²
            (4, PI),         # τ³
            (5, -4*PI/3),    # τ⁴
            (6, -5*PI/3),    # τ⁵
        ]

        for cell_index, angle in rotations:

            self.play(Indicate(cells1[cell_index], scale_factor=1.7))

            if angle != 0:
                do_rotation(angle)

            self.wait(1)

            self.play(Restore(hex_g), run_time=0.5)

        # Ось

        p1 = (hex_dots.dots[0].get_center() + hex_dots.dots[5].get_center()) / 2
        p2 = (hex_dots.dots[2].get_center() + hex_dots.dots[3].get_center()) / 2

        axis = main_axis.copy()
        axis.put_start_and_end_on(p1, p2)
        axis.scale(1.4, about_point=axis.get_center())
        axis.set_z_index(-1)

        reflection_configs = [
            (7, ((0,1),(3,4))),  # σ
            (8, ((1,2),(4,5))),  # στ
            (9, ((2,3),(5,0))),  # στ²
            (10, ((0,1),(3,4))), # στ³
            (11, ((1,2),(4,5))), # στ⁴
            (12, ((2,3),(5,0))), # στ⁵
        ]

        self.play(Create(axis))

        for i, (cell_index, _) in enumerate(reflection_configs):

            # подсветка ячейки (вторая таблица!)
            self.play(Indicate(cells2[cell_index - 6], scale_factor=1.7))

            # отражение
            self.play(
                hex_g.animate.flip(axis=axis.get_unit_vector()),
                run_time=1
            )

            self.wait(0.5)

            # вернуть назад
            self.play(Restore(hex_g), run_time=0.5)

            self.wait(0.3)

            # повернуть ось (кроме последней итерации)
            if i < len(reflection_configs) - 1:
                self.play(
                    axis.animate.rotate(PI / 6, about_point=hex_dots.get_center()),
                    run_time=0.7
                )


        # финальная формула
        self.play(FadeOut(hex_g, labels, old_labels, axis))
        self.play(table.animate.to_edge(UP, buff=1))
        formula = MathTex(
            r"\frac{1}{12}\Big(",
            r"3^6",
            r"+ 2\cdot 3",
            r"+ 2\cdot 3^2",
            r"+ 3\cdot 3^4",
            r"+ 4\cdot 3^3",
            r"\Big)"
        )

        formula.scale(0.9)
        formula.to_edge(DOWN, buff=2)
        result = MathTex(r"= 92")
        formula.shift(LEFT * result.width)
        result.next_to(formula, RIGHT, buff=0.5)

        self.play(Write(formula))
        self.wait(1)



        final_text = Text("92 уникальные раскраски", font_size=24)
        final_text.to_edge( DOWN, buff=1)

        self.play(Write(result))
        self.play(Write(final_text))
        self.wait(2)

        self.clear()