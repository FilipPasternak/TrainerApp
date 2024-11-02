from helloworld.common.common_page import CommonPage

class DevPage(CommonPage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self.path = path

    def on_kv_post(self, base_widget):
        pass
