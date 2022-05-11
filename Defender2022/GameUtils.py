from pygame import mouse, draw, font, image, transform
from Colors import WHITE
from os import path


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


class ContinueButton:
    coords = None
    size = None
    x = None
    y = None
    width = None
    height = None
    small_font = None
    text = None
    text_coords = None

    @classmethod
    def __init__(cls, screen_width, screen_height):
        cls.coords = (screen_width / 100 * 45, screen_height / 100 * 90)
        cls.size = (screen_width / 100 * 10, screen_height / 100 * 10)
        cls.x = cls.coords[0]
        cls.y = cls.coords[1]
        cls.width = cls.size[0]
        cls.height = cls.size[1]
        cls.height = cls.size[1]
        cls.small_font = font.SysFont('Corbel', 35)
        cls.text = cls.small_font.render('Play', True, WHITE)
        cls.text_coords = cls.calculate_center(cls.x, cls.x + cls.width, cls.y, cls.y + cls.height)

    @classmethod
    def init(cls, screen_width, screen_height):
        return cls(screen_width, screen_height)

    @staticmethod
    def add(screen, color):
        draw.rect(screen, color, [ContinueButton.x, ContinueButton.y, ContinueButton.width, ContinueButton.height])

    @staticmethod
    def calculate_center(x1, x2, y1, y2):
        x = (x1 + x2) / 2
        x -= (x / 100 * 2)
        y = (y1 + y2) / 2
        return x, y


class SideScroller:
    bgx = 0
    background = None

    @classmethod
    def __init__(cls, screen_width, screen_height):
        cls.background = image.load("assets" + path.sep + "Level1.jpg")
        cls.background = transform.scale(cls.background, (screen_width*3, screen_height))

    @classmethod
    def init(cls, screen_width, screen_height):
        return cls(screen_width, screen_height)