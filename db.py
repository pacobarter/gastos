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
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Fijo.tableName,)

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
    def findConcept(cls, db_connection, concept):
        sql='SELECT * FROM %s WHERE id_concept=' % (Fijo.tableName,concept.id)
        
        

    @classmethod
    def findDate(cls, db_connection, date):
        pass

    @classmethod
    def findMensual(cls, db_connection, date, is_mensual):
        pass
        
    def __init__(self, id, mensual, concept, value, date):
        self.id=id
        self.mensual=mensual
        self.concept=concept
        self.value=value
        self.date=date
    
    def __str__(self):
        if self.mensual==True:
            return '[%d] %s (%s; mensual) %.2f Eur' % (self.id, self.concept.name, self.date, self.value)
        else:
            return '[%d] %s (%s;   anual) %.2f Eur' % (self.id, self.concept.name, self.date, self.value)

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
            
    def __init__(self, id, name, description):
        self.id=id
        self.name=name
        self.description=description
    
    def __str__(self):
        return '[%d] %-15s, %s' % (self.id, self.name, self.description)
    

# =============================================================================
def main():
    conn=dbOpen()
    
#     lstG=Group.listAll(conn)
#     for g in lstG:
#         print g
    
#    print lstG[2].name
    
#    print '"OCIO" ID =>',Group.findID(conn,'OCIO')
    
#     lstC=Concept.listAll(conn)
#     for c in lstC:
#         print c
    
#    lstF=Fijo.listAll(conn)
#    for f in lstF:
#        print f

#    print Concept.fromName(conn,'Seguro coche Hyundai')

    lstC=Concept.likeName(conn,'coche')
    for c in lstC:
        print c
    
###############################################################################    
if __name__=='__main__':
    main()
