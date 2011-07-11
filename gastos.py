import sys
import sqlite3

dbfile='gastos.db'


#======================================
def main(args):
    try:
        conn=sqlite3.connect(dbfile)
        cur=conn.cursor()

        cur.execute('SELECT * FROM datos')
        for row in cur:
            print 'fecha: %s | concepto: %s | valor: %f | grupo: %s | descripcion: %s' % row


    except Exception,e:
        print e


#======================================
if __name__=='__main__':
    main(sys.argv)

