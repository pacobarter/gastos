# -- coding: utf-8 --
# =============================================================================
'''
Created on 09/08/2011

@author: raul
'''
import sys
import gtk
import gobject
import pango

import db

def not_implemented(self):
    print 'Not implemented'


# =============================================================================
#    MAIN WND
#
class MainWnd:
    gui_file='main_wnd_2.glade'

    # -----------------------------------------------------------------------
    #   CONSTRUCTOR
    #
    def __init__(self):
        # init data
        self.db_connection=None
        
        self.data_cmbData=('Variable','Fijo','Ingreso','Conceptos','Grupos')
        
        self.columns = (
            ('id','fecha','concepto','grupo','valor','descripcion'), 
            ('id','fecha','mensual','concepto','valor'), 
            ('id','fecha','ingreso'), 
            ('id','nombre','descripcion'), 
            ('id','nombre','descripcion')
        )
        
        self.models=(
            gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING),
            gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_FLOAT),
            gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_FLOAT),
            gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING),
            gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING)
        )
        
        self.methods={
            'new'     : (not_implemented, not_implemented, not_implemented, not_implemented, not_implemented),
            'edit'    : (not_implemented, not_implemented, not_implemented, not_implemented, not_implemented),
            'delete'  : (not_implemented, not_implemented, not_implemented, not_implemented, not_implemented),
            'show_all': (not_implemented, db.Fijo.listAll, db.Ingreso.listAll, db.Concept.listAll, db.Group.listAll)
        }
        
        # open DB
        self.open_db()

        # build GUI
        self.builder = gtk.Builder()
        self.builder.add_from_file(MainWnd.gui_file)
        
        # - create object vars
        self.window  = self.builder.get_object('wndMain')
        self.cmbData = self.builder.get_object('cmbData')
        self.tvwData = self.builder.get_object('tvwData')
        self.status = self.builder.get_object('statusbar')

        # - init structures
        self.cmbbox_init(self.cmbData, self.data_cmbData)
        self.reinit_tblData()

        # - modify fonts
        self.set_gui_fonts()
        
        # - show all
        self.window.show_all()
        
        # - connect signals
        self.builder.connect_signals(self)

    
    # -----------------------------------------------------------------------
    #   UTILS
    #
    def open_db(self):
        self.db_connection=db.dbOpen()

    def set_gui_fonts(self):
        font=pango.FontDescription('monospace 8')
        self.tvwData.modify_font(font)

    def cmbbox_getSelected(self, cmb):
        return cmb.get_active()

    def cmbbox_init(self, cmb, init_data):
        cell = gtk.CellRendererText()
        cmb.pack_start(cell,True)
        cmb.add_attribute(cell, 'text', 0)

        for txt in init_data:
            cmb.append_text(txt)
            
        if len(init_data)>0:
            cmb.set_active(0)

    def reinit_tblData(self):
        id=self.cmbbox_getSelected(self.cmbData)
        tvw=self.tvwData
        
        # quitar las columnas anteriores
        for c in tvw.get_columns():
            tvw.remove_column(c)
        
        # añadir las nuevas columnas
        colId=0
        for c in self.columns[id]:
            col = gtk.TreeViewColumn(c, gtk.CellRendererText(), text=colId)
            col.set_resizable(True)
            col.set_sort_column_id(colId)
            
            tvw.append_column(col)

            colId += 1

        tvw.set_model(self.models[id])

    def exec_method(self, id, mthd):
        if mthd:
            lst=mthd(self.db_connection)
            if lst:
                self.listst_rebuild(self.models[id], lst)

    def listst_rebuild(self, list_store, list_data):
        list_store.clear()
        for item in list_data:
            list_store.append(item.toList())
        

    # -----------------------------------------------------------------------
    #   EVENTS
    #
    def on_wndMain_destroy(self,widget):
        sys.exit(0)

    def on_cmbData_changed(self, widget):
        #print 'selected: ', widget.get_active()
        self.reinit_tblData()

    def on_btnNuevo_clicked(self, widget):
        id=self.cmbbox_getSelected(self.cmbData)
        mthd=self.methods['new'][id]
        self.exec_method(id, mthd)

    def on_btnEditar_clicked(self, widget):
        id=self.cmbbox_getSelected(self.cmbData)
        mthd=self.methods['edit'][id]
        self.exec_method(id, mthd)

    def on_btnBorrar_clicked(self, widget):
        id=self.cmbbox_getSelected(self.cmbData)
        mthd=self.methods['delete'][id]
        self.exec_method(id, mthd)

    def on_btnShowAll_clicked(self, widget):
        id=self.cmbbox_getSelected(self.cmbData)
        mthd=self.methods['show_all'][id]
        self.exec_method(id, mthd)

# =============================================================================
#    MAIN 
#
if __name__ == '__main__':
    wnd = MainWnd()
    gtk.main()
