from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivy.graphics import Triangle, Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior

class ToggleButton(MDToggleButton, MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)


class Separator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.width, dp(1))


def popup(title, info):
    dialog_content = info
    close_button = MDRaisedButton(
        text="Close",
        on_release=lambda x: error_dialog.dismiss()
    )
    error_dialog = MDDialog(
        title=title,
        text=dialog_content,
        buttons=[close_button]
    )
    error_dialog.open()

def dropdown(caller, items_list):
    def menu_callback(selected_item):
        caller.text = selected_item
        menu.dismiss()

    menu_items = [
        {
            "text": item,
            "viewclass": "OneLineListItem",
            "height": dp(56),
            "on_release": lambda x=item: menu_callback(x),
        } for item in items_list
    ]

    menu = MDDropdownMenu(
        caller=caller,
        items=menu_items,
        width_mult=4,
    )

    return menu


class TriangleButton(ButtonBehavior, Widget):
    def __init__(self, vertices, on_release, **kwargs):
        super(TriangleButton, self).__init__(**kwargs)
        self.vertices = vertices #[x1, y1, x2, y2, x3, y3]

        x_coords = vertices[::2]
        y_coords = vertices[1::2]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        self.pos = (min_x, min_y)
        self.size = (max_x - min_x, max_y - min_y)

        self.opacity = 0
        # with self.canvas:
        #     self.color = Color(0, 1, 0, 1)
        #     self.triangle = Triangle(points=self.vertices)
        self.on_release = on_release

    def collide_point(self, x, y):
        return self.point_in_triangle((x, y), self.vertices)

    def point_in_triangle(self, pt, tri_points):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        x1, y1, x2, y2, x3, y3 = tri_points
        b1 = sign(pt, (x1, y1), (x2, y2)) < 0.0
        b2 = sign(pt, (x2, y2), (x3, y3)) < 0.0
        b3 = sign(pt, (x3, y3), (x1, y1)) < 0.0

        return (b1 == b2) and (b2 == b3)
