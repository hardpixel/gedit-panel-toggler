import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gedit', '3.0')

from gi.repository import GObject, Gtk, Gedit


class PanelTogglerWindowActivatable(GObject.Object, Gedit.WindowActivatable):

  window = GObject.property(type=Gedit.Window)

  def __init__(self):
    GObject.Object.__init__(self)

    self._header_bar    = None
    self._bottom_panel  = None
    self._side_panel    = None
    self._panel_sidebar = None
    self._left_button   = None
    self._bottom_button = None

  def do_activate(self):
    self.add_icon_path()

    self._header_bar    = self.window.get_titlebar().get_children()[-1]
    self._bottom_panel  = self.window.get_bottom_panel()
    self._side_panel    = self.window.get_side_panel()
    self._panel_sidebar = self._bottom_panel.get_parent().get_parent().get_children()[-1]
    self._button_box    = Gtk.Box()
    self._left_button   = Gtk.Button.new_from_icon_name('left-panel-symbolic', Gtk.IconSize.BUTTON)
    self._bottom_button = Gtk.Button.new_from_icon_name('bottom-panel-symbolic', Gtk.IconSize.BUTTON)

    self._button_box.get_style_context().add_class('linked')
    self._bottom_button.connect('clicked', self.on_bottom_button_activated)
    self._left_button.connect('clicked', self.on_left_button_activated)

    self._header_bar.pack_end(self._button_box)
    self._button_box.pack_end(self._bottom_button, True, True, 0)
    self._button_box.pack_end(self._left_button, True, True, 1)

    self._button_box.show_all()
    self._panel_sidebar.hide()

  def add_icon_path(self):
    theme = Gtk.IconTheme.get_default()
    path  = "%s/icons" % os.path.dirname(__file__)

    Gtk.IconTheme.append_search_path(theme, path)

  def do_deactivate(self):
    self._button_box.destroy()
    self._panel_sidebar.show()

  def on_left_button_activated(self, _button):
    status = not self._side_panel.get_property('visible')
    self._side_panel.set_property('visible', status)

  def on_bottom_button_activated(self, _button):
    status = not self._bottom_panel.get_property('visible')
    self._bottom_panel.set_property('visible', status)
