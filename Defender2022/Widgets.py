from pygame import mouse, draw, font, image, transform, Rect, Color
from constants import GameConstants, Colors
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


class Widget(GameConstants, Rect):
    def __init__(self, *args, **kwargs):
        x = self.SCREEN_WIDTH / 100 * args[0]
        y = self.SCREEN_HEIGHT / 100 * args[1]
        width = self.SCREEN_WIDTH / 100 * args[2]
        height = self.SCREEN_HEIGHT / 100 * args[3]
        super().__init__(x, y, width, height, **kwargs)

    def get_size(self):
        return self.left, self.top, self.right, self.bottom

    def is_over(self):
        pos = mouse.get_pos()
        if self.collidepoint(pos[0], pos[1]):
            return True
        return False

    @staticmethod
    def calculate_center(x1, x2, y1, y2):
        x = (x1 + x2) / 2
        x -= (x / 100 * 2)
        y = (y1 + y2) / 2
        return x, y


class TableWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = [kwargs['columns']] + kwargs['data']
        self.base_font = font.Font(None, 32)

    def add(self, screen, color):
        draw.rect(screen, color, self)
        current_x = self.x + (self.x / 100 * 20)
        increment_x = current_x / 100 * 60
        current_y = self.y + self.y
        increment_y = current_y / 100 * 50
        for tup in self.lst:
            for txt in tup:
                text_surface = self.base_font.render(str(txt), True, Colors.WHITE)
                screen.blit(text_surface, (current_x, current_y))
                current_x += increment_x
            current_x = self.x + (self.x / 100 * 20)
            current_y += increment_y


class TextBox(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_active = Color('lightskyblue3')
        self.color_passive = Colors.LIGHTER
        self.color = self.color_passive
        self.text_surface = None
        self.active = False
        self.base_font = font.Font(None, 32)
        self.user_text = "Click here to enter name"

    def set_active_status(self, active: bool = True):
        self.active = active
        if self.active:
            self.color = self.color_active
            self.user_text = ""
        elif not self.active:
            self.color = self.color_passive

    def add(self, screen, color):
        draw.rect(screen, color, self)
        self.text_surface = self.base_font.render(self.user_text, True, Colors.WHITE)
        screen.blit(self.text_surface, (self.x + 5, self.y + 5))
        self.w = max(100, self.text_surface.get_width() + 10)


class Title(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_active = Color('lightskyblue3')
        self.base_font = font.SysFont('Corbel', 35)
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
                word_surface = font_text.render(word, True, color)
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


class PlayButton(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.small_font = font.SysFont('Corbel', 35)
        self.text = self.small_font.render('Play', True, Colors.WHITE)
        self.text_coords = self.calculate_center(self.x, self.x + self.width, self.y, self.y + self.height)

    def add(self, screen, color):
        draw.rect(screen, color, self)
        screen.blit(self.text, self.text_coords)


class ScoreWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = 0
        self.time_score = None
        self.start_time = time.time()
        self.small_font = font.SysFont('Corbel', 35)
        self.number = self.small_font.render(str(self.score), True, Colors.WHITE)
        self.number_coords = (self.x / 100 * 50, self.y / 100 * 3)
        self.timer = self.small_font.render("00:00:00", True, Colors.WHITE)
        self.timer_coords = (self.x / 100 * 90, self.y / 100 * 3)

    def update_score(self):
        self.score += 1
        self.number = self.small_font.render(str(self.score), True, Colors.WHITE)

    def show(self, screen):
        screen.blit(self.number, self.number_coords)
        screen.blit(self.timer, self.timer_coords)

    def update_time(self):
        end_time = time.time()
        current_time = self.time_convert(end_time - self.start_time)
        self.time_score = current_time
        self.timer = self.small_font.render(current_time, True, Colors.WHITE)

    def final_score(self):
        return self.score, self.time_score

    @staticmethod
    def time_convert(sec):
        minute = sec // 60
        sec = sec % 60
        hours = minute // 60
        minute = minute % 60
        return f"{str(int(hours)).rjust(2, '0')}:{str(int(minute)).rjust(2, '0')}:{str(int(sec)).rjust(2, '0')}"


class SideScroller(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgx = 0
        self.level = 1
        self.surf = image.load("assets" + path.sep + "Level1.jpg")
        self.surf = transform.scale(self.surf, (self.x, self.y))

    def add(self, screen):
        screen.blit(self.surf, (self.bgx, 0))

    def slide(self):
        self.bgx -= 1
        if self.bgx <= -self.SCREEN_WIDTH * 2:
            self.bgx = 0
            self.next_level()

    def next_level(self):
        if self.level == 5:
            self.level = 1
            self.surf = image.load("assets" + path.sep + "Level1.jpg")
        self.level += 1
        self.surf = image.load("assets" + path.sep + str(self.level) + ".jpg")
