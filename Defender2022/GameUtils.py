from pygame import mouse, draw, font, image, transform
from Colors import WHITE
from os import path
import time


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
    foo = None

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
        cls.foo = "X"

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


class ScoreWidget:
    def __init__(self, screen_width, screen_height):
        self.coords = (0, 0)
        self.size = (screen_width, screen_height / 100 * 2)
        self.x = self.coords[0]
        self.y = self.coords[1]
        self.width = self.size[0]
        self.height = self.size[1]
        self.height = self.size[1]
        self.score = 0
        self.start_time = time.time()
        self.small_font = font.SysFont('Corbel', 35)
        self.number = self.small_font.render(str(self.score), True, WHITE)
        self.number_coords = (screen_width / 100 * 50, screen_height / 100 * 3)
        self.timer = self.small_font.render("00:00:00", True, WHITE)
        self.timer_coords = (screen_width / 100 * 90, screen_height / 100 * 3)

    def update_score(self):
        self.score += 1
        self.number = self.small_font.render(str(self.score), True, WHITE)

    def update_time(self):
        end_time = time.time()
        current_time = self.time_convert(end_time - self.start_time)
        self.timer = self.small_font.render(current_time, True, WHITE)

    @staticmethod
    def time_convert(sec):
        minute = sec // 60
        sec = sec % 60
        hours = minute // 60
        minute = minute % 60
        return f"{str(int(hours)).rjust(2, '0')}:{str(int(minute)).rjust(2, '0')}:{str(int(sec)).rjust(2,'0')}"


class SideScroller:
    bgx = 0
    background = None
    level = 1

    @classmethod
    def __init__(cls, screen_width, screen_height, level="Level1.jpg"):
        cls.background = image.load("assets" + path.sep + level)
        cls.background = transform.scale(cls.background, (screen_width * 3, screen_height))

    @classmethod
    def next_level(cls):
        if cls.level == 5:
            cls.level = 1
            return
        cls.level += 1
        return "Level"+str(cls.level)+".jpg"

    @classmethod
    def init(cls, screen_width, screen_height, level="Level1.jpg"):
        return cls(screen_width, screen_height, level=level)
