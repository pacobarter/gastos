# -- coding: utf-8 --
# =============================================================================
#                                                                            
#   list.py                                                              
#   (c) 2011 rjimenez                                                        
#                                                                            
#   Utilidades para listar contenido de BBDD                                                              
#                                                                            
# ============================================================================= 

import sqlite3

dbName='gastos.db'

tableNames=['concepts','groups','fijo','variable']

# =============================================================================
def listAll(connection):
    cur=connection.cursor()
    
    for table in tableNames:
        printTableRAW(cur,table)

    cur.close()

def printTableRAW(cursor, table_name):
    cursor.execute('SELECT * FROM %s' % table_name)

    print 'Table:',table_name
    print '------------------------'
    i=1
    for row in cursor:
        print '%2d: %s' % (i,row)
        i=i+1
        
    if i==1:
        print '<empty>'

    print ''        


def main():
    conn=sqlite3.connect(dbName)
    
    listAll(conn)
    
###############################################################################    
if __name__=='__main__':
    main()
