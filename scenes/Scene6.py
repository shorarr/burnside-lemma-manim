from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *

class Sc6(Scene):

    def construct(self):

        # Заголовок
        title = Text(
            "Идея Бернсайда",
            font_size=40
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Подпись
        caption_lines = VGroup(
            Text("Нужно для каждого преобразования посчитать,", font_size=28),
            Text("сколько раскрасок оно оставляет неподвижными.", font_size=28),
            Text("(какие повороты и отражения не меняют раскраску)", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        caption_lines.next_to(title, DOWN, buff=0.6)

        # побуквенное появление
        for line in caption_lines:
            self.play(AddTextLetterByLetter(line), run_time=1.2)

        self.wait(2)

        # формула
        left_text = Text(
            "Число различных раскрасок =",
            font_size=36
        )

        right_formula = MathTex(
            r"\frac{1}{|G|}",
            r"\sum_{g \in G}",
            r"|X^g|"
        )

        right_formula.scale(1.2)
        formula_group = VGroup(left_text, right_formula).arrange(RIGHT, buff=0.3)
        formula_group.next_to(caption_lines, DOWN, buff=1)

        self.play(Write(formula_group))
        self.wait(1)

        # ---------- Подписи к формуле ----------

        # части формулы
        frac_part = right_formula[0]  # 1 / |G|
        sum_part = right_formula[1]  # сумма
        xg_part = right_formula[2]  # |X^g|

        g_math = MathTex(r"|G|")
        g_text = Text(" — число преобразований", font_size=26)
        g_caption = VGroup(g_math, g_text).arrange(RIGHT, buff=0.2)

        sum_text = Text("Cуммируем по всем преобразованиям", font_size=26)

        xg_math = MathTex(r"|X^g|")
        xg_text = Text(" — число неподвижных раскрасок", font_size=26)
        xg_caption = VGroup(xg_math, xg_text).arrange(RIGHT, buff=0.2)

        # анимация
        self.play(FadeOut(caption_lines))
        self.play(formula_group.animate.next_to(title, DOWN, buff=1))

        g_caption.next_to(formula_group, DOWN, buff=0.5)
        sum_text.next_to(g_caption, DOWN, buff=0.5)
        xg_caption.next_to(sum_text, DOWN, buff=0.5)

        # |G|
        self.play(frac_part.animate.set_color(YELLOW))
        self.play(FadeIn(g_caption))
        self.wait(0.5)
        self.play(frac_part.animate.set_color(WHITE))

        # сумма
        self.play(sum_part.animate.set_color(YELLOW))
        self.play(FadeIn(sum_text))
        self.wait(0.5)
        self.play(sum_part.animate.set_color(WHITE))

        # |X^g|
        self.play(xg_part.animate.set_color(YELLOW))
        self.play(FadeIn(xg_caption))
        self.wait(1)
        self.play(xg_part.animate.set_color(WHITE))

        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])