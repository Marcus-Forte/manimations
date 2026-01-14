from manim import *

class RectangleWithText(VGroup):
    def __init__(self, text: str, color: ParsableManimColor, font_size=28, padding=0.28, **kwargs):
        super().__init__(**kwargs)
        msg = Text(text, font_size=font_size)
        rect = SurroundingRectangle(msg, color=color, buff=padding)
        self.add(rect, msg)
