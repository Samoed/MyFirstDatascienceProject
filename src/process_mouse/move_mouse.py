from pynput.mouse import Button, Controller
from PySide6.QtCore import QPointList
from src.process_mouse.mouse_enum import MouseEnum

mouse = Controller()


def action_mouse(mouse_values: dict[str, str], label: str, is_start: bool = True) -> None:
    action = mouse_values.get(label, None)
    if action is None:
        return

    match action:
        case MouseEnum.move_mouse | MouseEnum.none:
            return
        case MouseEnum.left_click:
            button = Button.left
        case MouseEnum.right_click:
            button = Button.right
        case _:
            return
    if is_start:
        mouse.press(button)
    else:
        mouse.release(button)


def move_mouse(mouse_values: dict[str, str], point_history: QPointList, label: str) -> None:
    action = mouse_values.get(label, "None")
    if (
        action == "None"
        or len(point_history) <= 2
        or (point_history[-1].x() + point_history[-1].y()) == 0
        or (point_history[-2].x() + point_history[-2].y()) == 0
    ):
        return
    diff_x = point_history[-1].x() - point_history[-2].x()
    diff_y = point_history[-1].y() - point_history[-2].y()
    mouse.move(diff_x, diff_y)
