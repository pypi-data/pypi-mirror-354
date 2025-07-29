from ..config import *

class BaseScene:
    def __init__(self):
        self.game = None
        self.name = None
        self.display_surface = None

    def get_image(self,path,*args,**kwargs):
        if not self.game:
            raise RuntimeError("\n\nDo not call 'get_image()' in '__init__'. Wait until the scene is fully initialized (e.g., in 'on_create()').")

        return self.game.asset_manager.get_image(kwargs.get("all-scenes",self.name), path)

    def on_create(self):
        pass

    def on_event(self,event):
        pass

    def on_update(self):
        pass

    def on_render(self):
        pass

    def on_close(self):
        pass