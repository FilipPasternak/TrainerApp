from helloworld.common.common_page import CommonPage

class StartPage(CommonPage):
    def __init__(self, path, **kw):
        super().__init__(path, **kw)
        self.path = path

    def on_kv_post(self, base_widget):
        pass


