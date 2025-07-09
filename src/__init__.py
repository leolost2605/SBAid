import sys

# import gi
#
# gi.require_version("Gtk", "4.0")
# gi.require_version("Adw", "1")
# gi.require_version("Shumate", "1")
# from gi.repository import GLib, Gtk
# from gi.repository import Adw
# from gi.repository import Shumate

# class MyApplication(Adw.Application):
#     def __init__(self):
#         super().__init__(application_id="io.github.leolost2605.SBAid")
#         GLib.set_application_name('SBAid')
#
#     def do_activate(self):
#         shumate_map = Shumate.SimpleMap()
#         shumate_map.set_vexpand(True)
#         shumate_map.set_map_source(Shumate.RasterRenderer.new_from_url("https://tile.openstreetmap.org/{z}/{x}/{y}.png"))
#
#         box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, vexpand=True)
#         box.append(Adw.HeaderBar())
#         box.append(shumate_map)
#
#         window = Adw.ApplicationWindow(application=self, title="SBAid")
#         window.set_content(box)
#         window.present()


# app = MyApplication()
# exit_status = app.run(sys.argv)
print("Hello World")
sys.exit(0)