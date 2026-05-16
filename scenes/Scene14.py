from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from my_manim_plugins import HexDots


class Sc14(Scene):

    def construct(self):

        # --- Вопрос ---
        question = Text(
            "Изначальная задача: сколько различных бус можно составить\n"
            "из 6 бусинок, если каждая может быть красной, синей или зелёной?\n",
            font_size=32,
            line_spacing=1.4
        ).move_to(ORIGIN)

        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question))
        self.wait(0.3)

        # --- Центральный шестиугольник ---
        hex_main = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS)
        hex_main.set_coloring(DOT_BLUE)
        hex_main.scale(0.8)
        hex_main.move_to(ORIGIN)

        self.play(FadeIn(hex_main))
        self.wait(0.3)

        # --- Быстрый перебор всех раскрасок на центральном шестиугольнике ---
        colorings = list(hex_main.generate_unique_colorings())  # 92 раскраски

        def update_colors(mob, alpha):
            index = int(alpha * (len(colorings) - 1))
            mob.set_coloring(colorings[index])

        self.play(
            UpdateFromAlphaFunc(
                hex_main,
                update_colors
            ),
            run_time=6,
            rate_func=smooth
        )

        self.wait(0.3)

        COLS = 12          # 13 колонок => 8 строк (92 = 13*7 + 1)
        AVAILABLE_WIDTH = 13.0   # чуть меньше полного экрана
        AVAILABLE_HEIGHT = 5.8   # высота под сетку

        rows = (len(colorings) + COLS - 1) // COLS  # = 8

        H_SPACING = AVAILABLE_WIDTH / (COLS - 1)
        V_SPACING = AVAILABLE_HEIGHT / (rows - 1)

        # Масштаб: берём меньшее из двух направлений с небольшим запасом
        SMALL_SCALE = min(H_SPACING, V_SPACING) * 0.13

        start_x = -AVAILABLE_WIDTH / 2
        start_y = AVAILABLE_HEIGHT / 2 + 0.6   # смещаем вверх, оставляя место тексту

        small_hexes = VGroup()

        for i, coloring in enumerate(colorings):
            col = i % COLS
            row = i // COLS

            h = HexDots(dot_colors=DOT_COLORS, radius=HEX_RADIUS, dot_radius=DOT_RADIUS*2)
            h.set_coloring(coloring)
            h.scale(SMALL_SCALE)
            h.move_to(np.array([
                start_x + col * H_SPACING,
                start_y - row * V_SPACING,
                0
            ]))
            small_hexes.add(h)

        # Убираем центральный шестиугольник, показываем сетку
        self.play(FadeOut(hex_main))

        # Появление по очереди (lag_ratio даёт эффект «волны»)
        self.play(
            LaggedStart(
                *[FadeIn(h) for h in small_hexes],
                lag_ratio=0.04,
                run_time=5
            )
        )

        self.wait(0.5)

        # --- Ответ ---
        answer = Text(
            "Ответ: 92 уникальных раскраски (комбинации бус)",
            font_size=30
        ).to_edge(DOWN, buff=0.8)

        self.play(Write(answer))
        self.wait(1.5)

        # --- Вывод ---
        conclusion = Text(
            "Это и есть применение леммы Бернсайда.",
            font_size=28
        ).next_to(answer, DOWN, buff=0.25)

        self.play(FadeIn(conclusion))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])