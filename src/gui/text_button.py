from gui.text import Text
from gui.scaling_button import ScalingButton
from data.colors import *
from utils import H


class TextButton(ScalingButton):
    def __init__(self, x, y, texts, font, font_size, min_alpha, sound_player, w=H(700)):
        super().__init__(x, y, w, H(80), 0.88, min_alpha, texts, sound_player)

        self.text_widget = Text(self.w//2, 0, font, font_size, WHITE, 1)
        self.zoom_area.h = H(60)
        self.zoom_area.centery = self.y

    def set_text(self, text):
        self.text_widget.set_text(text)
        self.render_surface()


class DoubleTextButton(ScalingButton):
    def __init__(self, x, y, texts, value, font, font_size, min_alpha, sound_player):
        super().__init__(x, y, H(700), H(90), 0.88, min_alpha, texts, sound_player)

        self.text_widget = Text(self.w // 2 - H(40), H(20), font, font_size, WHITE, 2)
        self.value_widget = Text(self.w // 2 + H(40), H(20), font, font_size, WHITE, 0)
        self.set_value(value)

    def set_value(self, value):
        self.value_widget.set_text(value)
        self.render_surface()

    def render_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        self.value_widget.draw(self.surface)
        self.set_alpha()
        self.set_scaled_surface()

__all__ = ["TextButton", "DoubleTextButton"]
