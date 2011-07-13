# -- coding: utf-8 --

import sys
import gtk
import db

gui_file='main_wnd.glade'

class MainWnd:

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gui_file)
        
        self.window             = self.builder.get_object('wndMain')
        
        self.btnOpenDB          = self.builder.get_object('btnOpenDB')
        self.btnListAllConcepts = self.builder.get_object('btnListAllConcepts')
        self.btnListAllGroups   = self.builder.get_object('btnListAllGroups')
        
        self.textOut            = self.builder.get_object('textOut')
        self.textbufferOut      = self.builder.get_object('textbufferOut')
        
        self.window.show_all()

        self.builder.connect_signals(self)

        self.db_connection=None


    def addLog(self, txt):
        self.textbufferOut.insert_at_cursor(txt + '\n')

    def setLog(self, txt):
        self.textbufferOut.set_text(txt)

    def clearLog(self):
        self.setLog('')

    def on_btnOpenDB_clicked(self, widget):
        self.clearLog()
        self.db_connection=db.dbOpen()
        self.addLog('DB opened')

    def on_btnListAllConcepts_clicked(self, widget):
        self.clearLog()
        
        lstC=db.Concept.listAll(self.db_connection)
        if len(lstC)>0:
            for c in lstC:
                self.addLog(str(c))
        else:
            self.setLog('<empty>')


    def on_btnListAllGroups_clicked(self, widget):
        self.clearLog()
        
        lstG=db.Group.listAll(self.db_connection)
        if len(lstG)>0:
            for g in lstG:
                self.addLog(str(g))
        else:
            self.setLog('<empty>')
        
        
    def on_wndMain_destroy(self,widget):
        sys.exit(0)


if __name__ == '__main__':
    wnd = MainWnd()
    gtk.main()
