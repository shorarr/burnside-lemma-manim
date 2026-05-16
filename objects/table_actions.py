from manim import *
from config import *

table1 = Table(
            [
                ["Элемент", "e", r"\tau", r"\tau^2", r"\tau^3", r"\tau^4", r"\tau^5"],
                ["Перест.", "e", "(123456)", "(135)(246)", "(14)(25)(36)", "(153)(264)", "(654321)"],
            ],
            include_outer_lines=True,
            element_to_mobject=lambda x: (
                Text(x, font_size=32)
                if any(c.isalpha() and ord(c) > 127 for c in x)
                else MathTex(x).scale(1.2)
            ),
            line_config={
                "stroke_width": 3
            }
        )

table2 = Table(
            [
                ["Элемент", r"\sigma", r"\sigma\tau", r"\sigma\tau^2", r"\sigma\tau^3", r"\sigma\tau^4",
                 r"\sigma\tau^5"],
                ["Перест.", "(16)(25)(34)", "(15)(24)", "(14)(23)(56)", "(13)(46)", "(12)(36)(45)", "(26)(35)"]
            ],
            include_outer_lines=True,
            element_to_mobject=lambda x: (
                Text(x, font_size=32)
                if any(c.isalpha() and ord(c) > 127 for c in x)
                else MathTex(x).scale(1.2)
            ),
            line_config={
                "stroke_width": 3
    }
        )

max_width = max(table1.width, table2.width)
table1.scale_to_fit_width(max_width)
table2.scale_to_fit_width(max_width)

action_table = VGroup(table1, table2).arrange(DOWN, buff = 0.4)