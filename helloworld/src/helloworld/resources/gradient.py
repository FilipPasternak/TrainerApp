from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import ListProperty


class Gradient(Widget):
    color_start = ListProperty([0.2, 0.2, 0.2, 1])
    color_end = ListProperty([0.7, 0.7, 0.7, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.rects = []
            steps = 150
            for i in range(steps):
                ratio = i / float(steps - 1)
                r = self.color_start[0] * (1 - ratio) + self.color_end[0] * ratio
                g = self.color_start[1] * (1 - ratio) + self.color_end[1] * ratio
                b = self.color_start[2] * (1 - ratio) + self.color_end[2] * ratio
                Color(r, g, b, 1)
                rect = Rectangle(size=self.size, pos=self.pos)
                self.rects.append(rect)

        self.bind(size=self.update_rectangles, pos=self.update_rectangles)

    def update_rectangles(self, *args):
        height_per_rect = self.height / len(self.rects)
        for i, rect in enumerate(self.rects):
            rect.size = (self.width, height_per_rect)
            rect.pos = (self.x, self.y + i * height_per_rect)
