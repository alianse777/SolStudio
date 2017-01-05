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

import os
import random
import subprocess as sp
from gi.repository import Gtk, Gdk
from msgbox import *
from solidity import *
import tempfile

GAS = 300000 # Gas price
PATH = os.path.dirname(os.path.realpath(__file__))

def highlightText(buffer, searchStr, color, N):
    buffer.create_tag("syntax"+str(N), foreground=color)
    start, end = buffer.get_bounds()
    finished = False

    while finished == False:
        res = start.forward_search(searchStr, Gtk.TextSearchFlags.TEXT_ONLY)
        if not res:
            finished = True
        else:
            matchStart, matchEnd = res
            buffer.apply_tag_by_name("syntax"+str(N), matchStart, matchEnd)
            start = matchEnd
    
class GUI():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.xml")
        self.win = self.builder.get_object("window_main")
        self.win.connect("delete-event", self.exit)
        self.win.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        self.win.show_all()
        self.prefix = "SolStudio"
        self.ws = 0 # TODO: workspaces
        self.ctrl = False
        self.completion = True
        self.saved = [True]
        self.buff = [None]
        self.FILE = [None]
        self.ident = 0
        self.connect()
        self.check_solc()
        self.reopen() # check for the last opened file
        Gtk.main()

    def reopen(self):
        try:
            with open(PATH + "/.latest") as fl:
                filename = fl.readline().strip()
            if os.path.isfile(filename):
                self.FILE[self.ws] = filename
                self.load()
            else:
                self.new(None)
        except OSError:
            self.new(None)

    def connect(self):
        # Connect function
        self.win.connect('key_release_event', self.on_key_pressed)
        # File menu
        self.builder.get_object("menu_file_new").connect("activate", self.new)
        self.builder.get_object("menu_file_open").connect("activate", self.open)
        self.builder.get_object("menu_file_save").connect("activate", self.save)
        self.builder.get_object("menu_file_save-as").connect("activate", self.save_as)
        self.builder.get_object("menu_file_exit").connect("activate", self.exit)
        
        #Edit menu
        self.builder.get_object("menu_edit_format").connect("activate",self.format)
        self.builder.get_object("menu_edit_cut").connect("activate", self.cut)
        self.builder.get_object("menu_edit_copy").connect("activate", self.copy)
        self.builder.get_object("menu_edit_paste").connect("activate", self.paste)
        
        #View menu
        self.builder.get_object("menu_view_gas").connect("activate", self.show_gas)
        
        #Compile button
        self.builder.get_object("compile_button").connect("pressed", self.compile)
        
        #Copy web3 button
        self.builder.get_object("button_copy").connect("pressed", self.copy_web3)
        
        #Buffer
        self.buff[self.ws] = self.builder.get_object("code")
        self.buff[self.ws].connect("changed", self.changed)
        
        self.tags = get_tags(self.buff[self.ws])
        self.cb =Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        # END Connect function        
        
    def copy_web3(self, obj):
        web3 = self.builder.get_object("web3")
        text = web3.get_text(web3.get_start_iter(), web3.get_end_iter(), False)
        self.cb.set_text(text, -1)
        
    def check_solc(self):
        try:
            ver = sp.check_output(['solc', '--version']).split(b'\n')[1].split(b" ")[1]
            self.builder.get_object("solc_version").set_text(ver.decode())
        except FileNotFoundError:
            alert(parent=self.win, title="Error!", text="solc compiler not found!")
            os._exit(1)
        
    def exit(self, *argv):
        if self.FILE[self.ws]:
            with open(PATH + "/.latest", "w") as fl:
                fl.write(self.FILE[self.ws])
        if not self.saved[self.ws]:
            if confirm(title="Unsaved file", text="Save file before exit?"):
                self.save(None)
        Gtk.main_quit()
        
    def new(self, obj):
        self.FILE[self.ws] = None
        self.buff[self.ws].set_text("pragma solidity ^0.4.0;\n")
        self.win.set_title(self.prefix + " - Unsaved " + str(self.ws))

    def format(self, obj):
        # format identation
        buff = self.buff[self.ws]
        text = format(buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False))
        buff.set_text(text)
        
    def open(self, obj):
        openfile = self.builder.get_object("open_file_dialog")
        destroy = lambda obj: openfile.hide()
        openfile.connect("delete-event", destroy)
        openfile.show_all()
        def open_file(obj):
            self.FILE[self.ws] = openfile.get_filename()
            if self.FILE[self.ws]:
                openfile.hide()
                self.load()
                self.win.set_title(self.prefix + " - " + os.path.basename(self.FILE[self.ws]))
        self.builder.get_object("button_open_cancel").connect("pressed", destroy)
        self.builder.get_object("button_open").connect("pressed", open_file)
        
    def load(self):
        try:
            with open(self.FILE[self.ws], "r") as fl:
                data = fl.read()
            buf = self.buff[self.ws]
            buf.set_text(data)
            self.saved[self.ws] = True
            self.win.set_title(self.prefix + " - " + os.path.basename(self.FILE[self.ws]))
        except:
            alert(title="Error!", text="Cannot open file!")
            
    def save(self, obj):
        buf = self.buff[self.ws]
        if self.FILE[self.ws]:
            try:
                with open(self.FILE[self.ws], "w") as fl:
                    fl.write(buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False))
                    self.saved[self.ws] = True
                    self.win.set_title(self.prefix + " - " + os.path.basename(self.FILE[self.ws]))
            except:
                alert(parent=self.win, title="Error!", text="Cannot save file!")
        else:
            self.save_as(None)
        
    def save_as(self, obj):
        if True: # will be implemented
            dialog = self.builder.get_object("save_as_dialog")
            destroy = lambda obj: dialog.hide()
            self.builder.get_object("button_save_as_cancel").connect("pressed", destroy)
            dialog.show_all()
            def save(obj):
                filename = dialog.get_filename()
                if filename:
                    buf = self.buff[self.ws]
                    allowed = True
                    if os.path.exists(filename):
                        allowed = confirm(text="Already exists. Do you want to overwrite?", 
                            title= 'Already exists', parent=self.win
                        )
                    if allowed:
                        with open(filename, "w") as fl:
                            fl.write(buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False))
                            self.saved[self.ws] = True
                        self.FILE[self.ws] = filename
                        self.win.set_title(self.prefix + " - " + os.path.basename(self.FILE[self.ws]))
                        dialog.hide()
            self.builder.get_object("button_save_as_ok").connect("pressed", save)
    
    def changed(self, obj):
        # -- on file changed --
        self.apply_tags()
        self.saved[self.ws] = False
        if self.FILE[self.ws]:
            self.win.set_title(self.prefix + " - " + os.path.basename(self.FILE[self.ws]) + "*")

    def apply_tags(self):
        #self.buff[self.ws].remove_all_tags(self.buff[self.ws].get_start_iter(), self.buff[self.ws].get_end_iter())
        N = 0
        for tag in self.tags:
            for kw in tag[0]:
                highlightText(self.buff[self.ws], kw, tag[1], N)
                N += 1
    
    def compile(self, obj):
        if self.FILE[self.ws]:
            data = compile(self.FILE[self.ws],
                use_std=self.builder.get_object("include_std").get_active(),
                optimize=self.builder.get_object("optimize").get_active())
            if(len(data) == 2):
                self.builder.get_object("bytecode").set_text(data[0])
                buf = self.builder.get_object("web3")
                buf.set_text(data[1])
            else:
                self.builder.get_object("bytecode").set_text("")
                buf = self.builder.get_object("web3")
                buf.set_text(data)
            
    def show_gas(self, obj):
        if self.FILE[self.ws]:
            out = sp.check_output(["solc --gas " + self.FILE[self.ws]], shell=True).decode()
            alert(title="Gas info", text=out, parent=self.win)
    
    def copy(self, obj):
        self.buff[self.ws].copy_clipboard(self.cb)
        
    def cut(self, obj):
        self.buff[self.ws].cut_clipboard(self.cb, True)
        
    def paste(self, obj):
        self.buff[self.ws].paste_clipboard(self.cb, None, True)
    
    def on_key_pressed(self, win, e):
        key = e.keyval
        ctrl = self.ctrl
        if chr(key).lower() == 'o' and ctrl:
            self.open(None)
        if chr(key).lower() == 's' and ctrl:
            self.save(None)
        if chr(key).lower() == 'a' and ctrl:
            self.save_as(None)
        if chr(key) == '(':
            buff = self.buff[self.ws]
            cur = buff.get_iter_at_mark(buff.get_insert()).get_offset()
            buff.insert_at_cursor(")")
            pos = buff.get_start_iter()
            pos.set_offset(cur)
            buff.place_cursor(pos)
            
        if chr(key) == '{':
            self.ident += 1
            buff = self.buff[self.ws]
            cur = buff.get_iter_at_mark(buff.get_insert()).get_offset()
            buff.insert_at_cursor("\n" + "    "*self.ident + "\n}")
            pos = buff.get_start_iter()
            pos.set_offset(cur + self.ident*4 + 1)
            buff.place_cursor(pos)
            self.ident = 0
        self.ctrl = e.state == (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK)


def compile(filename, use_std=False, optimize=True):
    path = tempfile.gettempdir() + "/" + str(random.randint(100, 10000)) + "-SOLC.bin"
    p = sp.Popen(["solc --abi " + filename + ";exit 0"], shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    result = p.communicate()
    if not result[0]:
        return result[1].decode()
    data = result[0].split(b'\n')
    if not data[0]:
        del data[0]
    if not data[-1]:
        del data[-1]
    contractName = data[0].replace(b"=======", b"").strip().decode()
    abi = data[2].decode()
    cmd = "solc --bin -o " + path + " " + filename
    if use_std:
        cmd += " --add-std"
    if optimize:
        cmd += " --optimize"
    os.system(cmd)
    bytecode = ''.join(map(lambda x: chr(x), open(path + "/" + contractName + ".bin","rb").read()))
    WEB3 = "var " + contractName + "Contract = web3.eth.contract(" + abi + ");\n"
    WEB3 += "var " + contractName + " = " + contractName + "Contract.new({\n"
    WEB3 += "from:eth.accounts[0],\n"
    WEB3 += "data: '0x" + bytecode + "',\n"
    WEB3 += "gas: '" + str(GAS) + "'\n"
    WEB3 += """}, function (e, contract){
console.log(e, contract); \n if (typeof contract.address !== 'undefined') {
console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
}
});"""
    return bytecode, WEB3
if __name__ == "__main__":
    GUI()
