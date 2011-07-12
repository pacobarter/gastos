# -- coding: utf-8 --
# =============================================================================
#                                                                            
#   db.py                                                              
#   (c) 2011 rjimenez                                                        
#                                                                            
#   Clase que encapsula el acceso a la BBDD                                                              
#                                          
#   Esquema de la BBDD:
#         
#         CREATE TABLE concepts ( 
#             id          INTEGER        PRIMARY KEY
#                                        NOT NULL
#                                        UNIQUE,
#             name        VARCHAR( 30 )  NOT NULL
#                                        UNIQUE,
#             description VARCHAR( 80 ) 
#         );
#         
#         CREATE TABLE groups ( 
#             id          INTEGER        PRIMARY KEY
#                                        NOT NULL
#                                        UNIQUE,
#             name        VARCHAR( 30 )  NOT NULL
#                                        UNIQUE,
#             description VARCHAR( 80 ) 
#         );
#         
#         CREATE TABLE fijo ( 
#             id         INTEGER  PRIMARY KEY
#                                 NOT NULL
#                                 UNIQUE,
#             mensual    BOOLEAN  NOT NULL,
#             id_concept INTEGER  NOT NULL,
#             value      REAL     NOT NULL,
#             date       DATETIME NOT NULL 
#         );
#         
#         CREATE TABLE variable ( 
#             id          INTEGER        PRIMARY KEY AUTOINCREMENT
#                                        NOT NULL
#                                        UNIQUE,
#             date        DATETIME       NOT NULL,
#             id_concept  INTEGER        NOT NULL,
#             id_group    INTEGER        NOT NULL,
#             value       REAL           NOT NULL,
#             description VARCHAR( 80 ) 
#         );
#
# ============================================================================= 

import sqlite3
import datetime as dt

dbName='gastos.db'

def dbOpen():
    return sqlite3.connect(dbName)

#
#-- Clase que encapsula un elemento de la tabla 'fijo'
#
#-----------------------------------------------------------------------------------------------
class Fijo:
    tableName       = 'fijo'
    idx_ID          = 0
    idx_mensual     = 1
    idx_idConcept   = 2
    idx_value       = 3
    idx_date        = 4

    @classmethod
    def __listFromSQL(cls, db_connection, sql):
        cur=db_connection.cursor()
        cur.execute(sql)

        ret=[]
        for r in cur:
            c=Concept.fromID(db_connection, r[Fijo.idx_idConcept])
            f=Fijo(r[Fijo.idx_ID],r[Fijo.idx_mensual],c,r[Fijo.idx_value],r[Fijo.idx_date])            
            ret.append(f)
        
        cur.close()
        return ret        

    @classmethod
    def __listFromSQLConcept(cls, sql, concept):
        cur=db_connection.cursor()
        cur.execute(sql)

        ret=[]
        for r in cur:
            f=Fijo(r[Fijo.idx_ID],r[Fijo.idx_mensual],concept,r[Fijo.idx_value],r[Fijo.idx_date])            
            ret.append(f)
        
        cur.close()
        return ret        

    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Fijo.tableName,)

        return Fijo.__listFromSQL(db_connection,sql)
        
    @classmethod
    def findConcept(cls, db_connection, concept):
        sql='SELECT * FROM %s WHERE id_concept=%d' % (Fijo.tableName,concept.id)

        return Fijo.__listFromSQLConcept(sql,concept)
      

    @classmethod
    def findDate(cls, db_connection, date): 
        # 'date' como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE date="%s"' % (Fijo.tableName,date)

        return Fijo.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateRange(cls, db_connection, date_start, date_end): 
        # 'date's como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE date>="%s" AND date<="%s"' % (Fijo.tableName,date_start,date_end)

        return Fijo.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateSup(cls, db_connection, date_max):
        # 'date' como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE date<="%s"' % (Fijo.tableName,date_max)

        return Fijo.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateInf(cls, db_connection, date_min):
        # 'date' como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE date>="%s"' % (Fijo.tableName,date_max)

        return Fijo.__listFromSQL(db_connection,sql)


    @classmethod
    def findMensual(cls, db_connection, is_mensual):
        if is_mensual:
            sql='SELECT * FROM %s WHERE mensual="true"' % (Fijo.tableName,)
        else:
            sql='SELECT * FROM %s WHERE mensual="false"' % (Fijo.tableName,)
            
        return Fijo.__listFromSQL(db_connection,sql)
        
        
    def __init__(self, id, mensual, concept, value, date):
        self.id=id
        self.mensual=mensual
        self.concept=concept
        self.value=value
        self.date=date
    
    def __str__(self):
        if self.mensual==True:
            return '[%d] %-25s (%s; mensual) %.2f Eur' % (self.id, self.concept.name, self.date, self.value)
        else:
            return '[%d] %-25s (%s;   anual) %.2f Eur' % (self.id, self.concept.name, self.date, self.value)

#
#-- Clase que encapsula un elemento de la tabla 'concepts'
#
#-----------------------------------------------------------------------------------------------
class Concept:
    tableName       = 'concepts'
    idx_ID          = 0
    idx_Name        = 1
    idx_Description = 2

    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Concept.tableName,)

        cur=db_connection.cursor()
        cur.execute(sql)
        
        ret=[]
        for r in cur:
            ret.append(Concept(r[Concept.idx_ID],r[Concept.idx_Name],r[Concept.idx_Description]))
        
        cur.close()
        
        return ret

    @classmethod
    def findID(cls, db_connection, name):
        sql='SELECT ID FROM %s WHERE name="%s"' % (Concept.tableName, name)

        cur=db_connection.cursor()
        cur.execute(sql)

        try:
            return cur.fetchone()[Concept.idx_ID]
        except:
            return -1

    @classmethod
    def fromID(cls, db_connection, id):
        sql='SELECT * FROM %s WHERE ID=%d' % (Concept.tableName, id)

        cur=db_connection.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        
        return Concept(id,row[Concept.idx_Name],row[Concept.idx_Description])

    @classmethod
    def fromName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name="%s"' % (Concept.tableName, name)

        cur=db_connection.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        
        return Concept(row[Concept.idx_ID],name,row[Concept.idx_Description])

    @classmethod
    def likeName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name LIKE "%%%s%%"' % (Concept.tableName, name)

        cur=db_connection.cursor()
        cur.execute(sql)

        lst=[]
        for r in cur:
            lst.append(Concept(r[Concept.idx_ID],r[Concept.idx_Name],r[Concept.idx_Description]))            
        
        return lst

    def __init__(self, id, name, description):
        self.id=id
        self.name=name
        self.description=description
        
    def __str__(self):
        return '[%d] %-25s, %s' % (self.id, self.name, self.description)
    
#
#-- Clase que encapsula un elemento de la tabla 'groups'
#
#-----------------------------------------------------------------------------------------------
class Group:
    tableName       = 'groups'
    idx_ID          = 0
    idx_Name        = 1
    idx_Description = 2

    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Group.tableName,)

        cur=db_connection.cursor()
        cur.execute(sql)
        
        ret=[]
        for r in cur:
            ret.append(Group(r[Group.idx_ID],r[Group.idx_Name],r[Group.idx_Description]))
        
        cur.close()
        
        return ret

    @classmethod
    def findID(cls, db_connection, name):
        sql='SELECT ID FROM %s WHERE name="%s"' % (Group.tableName, name)

        cur=db_connection.cursor()
        cur.execute(sql)

        try:
            return cur.fetchone()[Group.idx_ID]
        except:
            return -1
            
    @classmethod
    def fromName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name="%s"' % (Group.tableName, name)

        cur=db_connection.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        
        return Group(row[Group.idx_ID],name,row[Group.idx_Description])

    @classmethod
    def likeName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name LIKE "%%%s%%"' % (Group.tableName, name)

        cur=db_connection.cursor()
        cur.execute(sql)

        lst=[]
        for r in cur:
            lst.append(Group(r[Group.idx_ID],r[Group.idx_Name],r[Group.idx_Description]))            
        
        return lst

    def __init__(self, id, name, description):
        self.id=id
        self.name=name
        self.description=description
    
    def __str__(self):
        return '[%d] %-15s, %s' % (self.id, self.name, self.description)
    

# =============================================================================
def main():
    conn=dbOpen()

# <-- Tests for 'Group'
    
#     lstG=Group.listAll(conn)
#     for g in lstG:
#         print g
    
#    print lstG[2].name
    
#    print '"OCIO" ID =>',Group.findID(conn,'OCIO')
    
# -->

# <-- Tests for 'Concept'

#     lstC=Concept.listAll(conn)
#     for c in lstC:
#         print c
    
#     lstC=Concept.likeName(conn,'coche')
#     for c in lstC:
#         print c
    
#     print Concept.fromName(conn,'Seguro coche Hyundai')

# -->

# <-- Tests for 'Fijo'

#     lstF=Fijo.listAll(conn)
#     for f in lstF:
#         print f

#     lstF=Fijo.findMensual(conn,False)
#     for f in lstF:
#         print f

#     c=Concept.fromName(conn,'Seguro coche Hyundai')
#     if not c:
#         print 'Concept not found!'
#     else:
#         lstF=Fijo.findConcept(conn,c)
#         for f in lstF:
#             print f

#     lstF=Fijo.findDate(conn,'2011-05-01')
#     for f in lstF:
#         print f
 
#     lstF=Fijo.findDateRange(conn,'2011-01-01','2011-09-01')
#     for f in lstF:
#         print f

    lstF=Fijo.findDateSup(conn,'2011-06-01')
    for f in lstF:
        print f

# -->
    
    
###############################################################################    
if __name__=='__main__':
    main()
