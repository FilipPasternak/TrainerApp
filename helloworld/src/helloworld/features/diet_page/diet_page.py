from helloworld.common.common_page import CommonPage


class DietPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path

    def on_kv_post(self, base_widget):
        pass
        # import helloworld.common.actions as actions
        #
        # main_box = toga.Box(style=Pack(direction='column'))
        #
        # diet_label = toga.Label('This is the Diet Page', style=Pack(padding=10))
        # main_box.add(diet_label)
        #
        # create_button(box=main_box,
        #               action=actions.go_to_start_page,
        #               label='Go to Start page',
        #               style=Pack(padding=5))
        #
        # self.main_window.content = main_box


