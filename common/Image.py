from gi.repository import Gdk
class Image(Gdk.Paintable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save_to_file(self, path: str) -> None:
        pass
