from pygame import mouse, draw, font, image, transform, Rect, Color
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


class TextBox(Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_active = Color('lightskyblue3')
        self.color_passive = Color('chartreuse4')
        self.color = self.color_passive
        self.text_surface = None
        self.active = False
        self.base_font = font.Font(None, 32)
        self.user_text = ""

    def set_active_status(self, active: bool = True):
        self.active = active
        if self.active:
            self.color = self.color_active
        elif not self.active:
            self.color = self.color_passive

    def add(self, screen, color):
        draw.rect(screen, color, self)
        self.text_surface = self.base_font.render(self.user_text, True, WHITE)
        screen.blit(self.text_surface, (self.x + 5, self.y + 5))
        self.w = max(100, self.text_surface.get_width() + 10)


class Title(Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_active = Color('lightskyblue3')
        self.base_font = font.Font(None, 50)
        self.title_txt = kwargs['text']

    def add(self, screen, color):
        draw.rect(screen, color, self)
        if self.title_txt == "":
            return
        self.blit_text(screen, self.title_txt, (self.x + 5, self.y + 5), self.base_font)
        self.w = max(100, screen.get_size()[0] / 2)

    @staticmethod
    def blit_text(surface, text, pos, font_text, color=Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font_text.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        max_length_line = []
        for line in words:
            for word in line:
                word_surface = font_text.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                max_length_line.append(word_width)
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        return max(max_length_line)


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
        self.time_score = None
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
        self.time_score = current_time
        self.timer = self.small_font.render(current_time, True, WHITE)

    @staticmethod
    def time_convert(sec):
        minute = sec // 60
        sec = sec % 60
        hours = minute // 60
        minute = minute % 60
        return f"{str(int(hours)).rjust(2, '0')}:{str(int(minute)).rjust(2, '0')}:{str(int(sec)).rjust(2, '0')}"


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
            return "Level1.jpg"
        cls.level += 1
        return "Level" + str(cls.level) + ".jpg"

    @classmethod
    def init(cls, screen_width, screen_height, level="Level1.jpg"):
        return cls(screen_width, screen_height, level=level)
