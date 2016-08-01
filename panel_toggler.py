from gi.repository import GObject, Gtk, Gedit, Gdk

import os

class CutLineWindowActivatable(GObject.Object, Gedit.WindowActivatable):

	window = GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		path = os.path.dirname(__file__)
		hbar = self.find_widget_by_id(self.window, "headerbar")

		image = Gtk.Image.new_from_file(path + "/icons/gedit-view-bottom-pane-symbolic.svg")
		self.bottom_button = Gtk.Button(image=image)
		self.bottom_button.connect('clicked', self.on_bottom_pane_button_activated)
		self.bottom_button.show()
		hbar.pack_end(self.bottom_button)

		image = Gtk.Image.new_from_file(path + "/icons/gedit-view-left-pane-symbolic.svg")
		self.left_button = Gtk.Button(image=image)
		self.left_button.connect('clicked', self.on_left_pane_button_activated)
		self.left_button.show()
		hbar.pack_end(self.left_button)

		self.panel_sidebar = self.find_widget_by_id(self.window, "bottom_panel_sidebar")
		self.panel_sidebar.hide()

	def do_deactivate(self):
		self.left_button.destroy()
		self.bottom_button.destroy()
		self.panel_sidebar.show()

	def on_left_pane_button_activated(self, action=None, user_data=None):
		panel = self.window.get_side_panel()
		status = not panel.get_property("visible")
		panel.set_property("visible", status)

	def on_bottom_pane_button_activated(self, action=None, user_data=None):
		panel = self.window.get_bottom_panel()
		status = not panel.get_property("visible")
		panel.set_property("visible", status)

	def find_widget_by_id(self, widget, id):
		if Gtk.Buildable.get_name(widget) == id: return widget
		if not hasattr(widget, "get_children"): return None

		for child in widget.get_children():
			ret = self.find_widget_by_id(child, id)
			if ret: return ret
		return None
