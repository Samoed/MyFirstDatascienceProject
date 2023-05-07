from PySide6.QtCore import QPointList
from pynput.mouse import Button, Controller

mouse = Controller()


def action_mouse(mouse_values: dict[str, str], label: str, is_start: bool = True) -> None:
    action = mouse_values.get(label, None)
    if action is None:
        return
    # TODO create enum for actions
    match action:
        case "Mouse move":
            return
        case "Left mouse (LMB)":
            button = Button.left
        case "Right mouse":
            button = Button.right
        case _:
            return
    if is_start:
        mouse.press(button)
    else:
        mouse.release(button)


def move_mouse(mouse_values: dict[str, str], point_history: QPointList, label: str) -> None:
    action = mouse_values.get(label, "None")
    if action == "None" or len(point_history) <= 2 or (point_history[-1].x() + point_history[-1].y()) == 0 or (
            point_history[-2].x() + point_history[-2].y()) == 0:
        return
    diff_x = point_history[-1].x() - point_history[-2].x()
    diff_y = point_history[-1].y() - point_history[-2].y()
    print(diff_x, diff_y)
    mouse.move(diff_x, diff_y)
