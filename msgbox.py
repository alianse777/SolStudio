#    SolStudio
#    Copyright (C) 2017  alainse777

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk

def alert(parent = None, title="", text=""):
    dialog = Gtk.Dialog(title, parent, 0)
    dialog.set_default_size(150, 100)
    dialog.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#FAFAFA"))
    label = Gtk.Label()
    label.set_markup('<span foreground="#494941" face="sans">' + text + '</span>')
    box = dialog.get_content_area()
    box.add(label)
    btn = dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
    btn.set_relief(2)
    box.show_all()
    dialog.run()
    dialog.destroy()

def confirm(parent=None, title="", text=""):
    dialog = Gtk.Dialog(title, parent, 0)

    dialog.set_default_size(150, 100)
    dialog.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
    label = Gtk.Label()
    label.set_markup('<span foreground="#494941" face="sans">' + text + '</span>')
    box = dialog.get_content_area()
    box.add(label)
    box.show_all()
    btn1 = dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
    btn1.set_relief(2)
    btn2 = dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
    btn2.set_relief(2)
    result = False
    response = dialog.run()
    dialog.destroy()
    if response == Gtk.ResponseType.OK:
        result = True
    elif response == Gtk.ResponseType.CANCEL:
        result = False
    return result

if __name__ == "__main__":
    confirm(title='', text="test")
