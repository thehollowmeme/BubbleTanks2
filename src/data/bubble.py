from constants import BUBBLE_COLOR, BUBBLE_COLOR_2
from utils import scaled_body, HF


BUBBLES = {
    "tiny": {
        "radius": HF(13),
        "health": 1,
        "body": scaled_body([[15, 2.5, BUBBLE_COLOR, 0, 0, True, 14, True, False]])
    },
    "small": {
        "radius": HF(17),
        "health": 1,
        "body": scaled_body([[17, 3.6, BUBBLE_COLOR, 0, 0, True, 16, True, False]])
    },
    "medium": {
        "radius": HF(24),
        "health": 5,
        "body": scaled_body([[24, 4, BUBBLE_COLOR, 0, 0, True, 11, True, False]])
    },
    "big": {
        "radius": HF(34),
        "health": 25,
        "body": scaled_body([[34, 4, BUBBLE_COLOR_2, 0, 0, True, 16, True, False]])
    }
}

BUBBLE_MAX_VEL = HF(0.7)
BUBBLE_ACC = HF(0.0024)


__all__ = [

    "BUBBLES",
    "BUBBLE_MAX_VEL",
    "BUBBLE_ACC"

]
