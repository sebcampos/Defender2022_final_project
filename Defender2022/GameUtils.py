from pygame import mouse


class MouseHandler:
    @staticmethod
    def clicked_on(coordinates, size):
        mouse_x, mouse_y = mouse.get_pos()
        x, y = coordinates
        width, height = size
        width += x
        height += y
        if x <= mouse_x <= width and y <= mouse_y <= height:
            return True
        return False

    @staticmethod
    def hovered_over(coordinates, size):
        mouse_x, mouse_y = mouse.get_pos()
        x, y = coordinates
        width, height = size
        width += x
        height += y
        if x <= mouse_x <= width and y <= mouse_y <= height:
            return True
        return False
