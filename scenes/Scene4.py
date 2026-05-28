from manim import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import *
from objects.table_actions import *

class Sc4(Scene):

    def construct(self):

        # Заголовок
        title_math = MathTex("G =")
        title_text = Text(
            "группа симметрий правильного шестиугольника",
            font_size=36
        )

        title = VGroup(title_math, title_text).arrange(RIGHT, buff=0.3)
        title.to_edge(UP)

        subtitle = Text(
            "Диэдральная группа D12",
            font_size=28
        ).next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle))

        self.wait(1)

        # Полная запись группы
        group_full = MathTex(
            r"G = \{",
            r"e,", r"\tau,", r"\tau^2,", r"\tau^3,", r"\tau^4,", r"\tau^5,",
            r"\sigma,", r"\sigma\tau,", r"\sigma\tau^2,", r"\sigma\tau^3,", r"\sigma\tau^4,", r"\sigma\tau^5",
            r"\}"
        ).scale(0.9)

        group_full.next_to(subtitle, DOWN, buff=0.7)

        self.play(Write(group_full))

        self.wait(1)

        # Подписи
        e_part = MathTex("(e)")
        e_text = Text("— без изменений", font_size=28)

        tau_part = MathTex(r"(\tau)")
        tau_text = Text("— поворот на 60°", font_size=28)

        sigma_part = MathTex(r"(\sigma)")
        sigma_text = Text("— отражение относительно оси", font_size=28)

        e_line = VGroup(e_part, e_text).arrange(RIGHT, buff=0.2)
        tau_line = VGroup(tau_part, tau_text).arrange(RIGHT, buff=0.2)
        sigma_line = VGroup(sigma_part, sigma_text).arrange(RIGHT, buff=0.2)

        captions = VGroup(e_line, tau_line, sigma_line).arrange(DOWN, aligned_edge=LEFT)
        captions.next_to(group_full, DOWN, buff=0.6)

        self.play(FadeIn(captions))

        self.wait(2)

        # Упрощение
        group_size = MathTex(r"|G| = 12").scale(1.5)
        group_size_caption = Text("Порядок группы (количество элементов)", font_size=28)
        g_size = VGroup(group_size, group_size_caption).arrange(DOWN, buff=0.6)
        group_size.move_to(ORIGIN)

        self.play(
            FadeOut(captions, title, subtitle),
            Transform(group_full, g_size)
        )

        self.wait(2)
        self.play(group_full.animate.scale(0.8).to_edge(DOWN, buff=1.5))

        # Заголовок 2
        table_title = Text(
            "Таблица поворотов и симметрий",
            font_size=32
        ).to_edge(UP, buff=0.8)

        self.wait(1)
        self.play(FadeIn(table_title))

        # Таблица
        table = action_table

        table.scale(0.5)
        table.next_to(table_title, DOWN, buff=0.4)

        self.play(FadeIn(table))

        description = Text(
            "Все элементы группы D12 и их запись в циклическом виде",
            font_size=32
        ).to_edge(DOWN, buff=1.5)

        self.play(FadeOut(group_full, run_time=1), FadeIn(description, run_time=1))

        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])