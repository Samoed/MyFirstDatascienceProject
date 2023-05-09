from enum import Enum


class MouseEnum(str, Enum):
    none = "None"
    move_mouse = "Mouse move"
    left_click = "Left mouse"
    right_click = "Right mouse"
