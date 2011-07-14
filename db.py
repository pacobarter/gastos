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
#         CREATE TABLE ingresos ( 
#             id      INTEGER  PRIMARY KEY AUTOINCREMENT
#                              NOT NULL
#                              UNIQUE,
#             date    DATETIME NOT NULL,
#             sueldo1 REAL     NOT NULL,
#             sueldo2 REAL     NOT NULL 
#         );
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
#-- Clase que encapsula un elemento de la tabla 'ingresos'
#
#-----------------------------------------------------------------------------------------------
class Ingreso:
    tableName       = 'ingresos'
    idx_ID          = 0
    idx_date        = 1
    idx_sueldo1     = 2
    idx_sueldo2     = 3

    @classmethod
    def __listFromSQL(cls, db_connection, sql):
        cur=None

        try:
            cur=db_connection.cursor()
            cur.execute(sql)

            ret=[]
            for r in cur:
                i=Ingreso(r[Ingreso.idx_ID],r[Ingreso.idx_date],r[Ingreso.idx_sueldo1],r[Ingreso.idx_sueldo2])            
                ret.append(i)
            
            return ret

        except:
            return []
            
        finally:
            if cur:
                cur.close()

    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Ingreso.tableName,)

        return Ingreso.__listFromSQL(db_connection,sql)

    @classmethod
    def findDate(cls, db_connection, date): 
        # 'date' como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE date="%s"' % (Ingreso.tableName,date)

        return Ingreso.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateRange(cls, db_connection, date_start, date_end): 
        # 'date's como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE date>="%s" AND date<="%s"' % (Ingreso.tableName,date_start,date_end)

        return Ingreso.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateSup(cls, db_connection, date_max):
        # 'date' como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s WHERE AND date<="%s"' % (Ingreso.tableName,date_max)

        return Ingreso.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateInf(cls, db_connection, date_min):
        # 'date' como string, en la forma 'YYYY-MM-DD'
        sql='SELECT * FROM %s AND WHERE date>="%s"' % (Ingreso.tableName,date_max)
        
        return Ingreso.__listFromSQL(db_connection,sql)


    def __init__(self, id, date, sueldo1, sueldo2):
        self.id=id
        self.date=date
        self.sueldo1=sueldo1
        sefl.sueldo2.sueldo2

    def total(self):
        return self.sueldo1+self.sueldo2

    def __str__(self):
        return '[%d] (%s) %.2f Eur' % (self,id, self.date, self.total())

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
        cur=None
        
        try:
            cur=db_connection.cursor()
            cur.execute(sql)

            ret=[]
            for r in cur:
                c=Concept.fromID(db_connection, r[Fijo.idx_idConcept])
                
                if not c:
                    raise Exception()
                    
                f=Fijo(r[Fijo.idx_ID],r[Fijo.idx_mensual],c,r[Fijo.idx_value],r[Fijo.idx_date])            
                ret.append(f)
            
            return ret        

        except:
            return []
            
        finally:
            if cur:
                cur.close()

    @classmethod
    def __listFromSQLConcept(cls, sql, concept):
        cur=None
        
        try:
            cur=db_connection.cursor()
            cur.execute(sql)
    
            ret=[]
            for r in cur:
                f=Fijo(r[Fijo.idx_ID],r[Fijo.idx_mensual],concept,r[Fijo.idx_value],r[Fijo.idx_date])            
                ret.append(f)
            
            return ret        

        except:
            return []
            
        finally:
            if cur:
                cur.close()


    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Fijo.tableName,)

        return Fijo.__listFromSQL(db_connection,sql)
        
    @classmethod
    def findConcept(cls, db_connection, concept):
        sql='SELECT * FROM %s WHERE id_concept=%d' % (Fijo.tableName,concept.id)

        return Fijo.__listFromSQLConcept(sql,concept)
      

    @classmethod
    def findDate(cls, db_connection, date, is_mensual): 
        # 'date' como string, en la forma 'YYYY-MM-DD'
        if is_mensual==True:
            sql='SELECT * FROM %s WHERE mensual=1 AND date="%s"' % (Fijo.tableName,date)
        else:
            sql='SELECT * FROM %s WHERE mensual=0 AND date="%s"' % (Fijo.tableName,date)

        return Fijo.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateRange(cls, db_connection, date_start, date_end, is_mensual): 
        # 'date's como string, en la forma 'YYYY-MM-DD'
        if is_mensual==True:
            sql='SELECT * FROM %s WHERE mensual=1 AND date>="%s" AND date<="%s"' % (Fijo.tableName,date_start,date_end)
        else:
            sql='SELECT * FROM %s WHERE mensual=0 AND date>="%s" AND date<="%s"' % (Fijo.tableName,date_start,date_end)

        return Fijo.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateSup(cls, db_connection, date_max, is_mensual):
        # 'date' como string, en la forma 'YYYY-MM-DD'
        if is_mensual:
            sql='SELECT * FROM %s WHERE mensual=1 AND date<="%s"' % (Fijo.tableName,date_max)
        else:
            sql='SELECT * FROM %s WHERE mensual=0 AND date<="%s"' % (Fijo.tableName,date_max)

        return Fijo.__listFromSQL(db_connection,sql)

    @classmethod
    def findDateInf(cls, db_connection, date_min, is_mensual):
        # 'date' como string, en la forma 'YYYY-MM-DD'
        if is_mensual==True:
            sql='SELECT * FROM %s mensual=1 AND WHERE date>="%s"' % (Fijo.tableName,date_max)
        else:
            sql='SELECT * FROM %s mensual=0 AND WHERE date>="%s"' % (Fijo.tableName,date_max)
        
        return Fijo.__listFromSQL(db_connection,sql)


    @classmethod
    def findAllMensual(cls, db_connection):
        sql='SELECT * FROM %s WHERE mensual=1' % (Fijo.tableName,)
            
        return Fijo.__listFromSQL(db_connection,sql)
        
    @classmethod
    def findAllAnual(cls, db_connection):
        sql='SELECT * FROM %s WHERE mensual=0' % (Fijo.tableName,)
            
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
    def __oneFromSQL(cls, db_connection, sql):
        cur=None
        
        try:
            cur=db_connection.cursor()
            cur.execute(sql)

            r=cur.fetchone()
            return Concept(r[Concept.idx_ID],r[Concept.idx_Name],r[Concept.idx_Description])
        
        except Exception:
            return None
            
        finally:
            if cur:
                cur.close()

    @classmethod
    def __listFromSQL(cls, db_connection, sql):
        cur=None
        
        try:
            cur=db_connection.cursor()
            cur.execute(sql)

            ret=[]
            for r in cur:
                ret.append(Concept(r[Concept.idx_ID],r[Concept.idx_Name],r[Concept.idx_Description]))
    
            return ret

        except:
            return []

        finally:
            if cur:
                cur.close()

    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Concept.tableName,)

        return Concept.__listFromSQL(db_connection,sql)

    @classmethod
    def findID(cls, db_connection, name):
        sql='SELECT ID FROM %s WHERE name="%s"' % (Concept.tableName, name)

        try:
            return Concept.__oneFromSQL(db_connection,sql).id
        except:
            return -1

    @classmethod
    def fromID(cls, db_connection, id):
        sql='SELECT * FROM %s WHERE ID=%d' % (Concept.tableName, id)
        
        return Concept.__oneFromSQL(db_connection,sql)

    @classmethod
    def fromName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name="%s"' % (Concept.tableName, name)

        return Concept.__oneFromSQL(db_connection,sql)

    @classmethod
    def likeName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name LIKE "%%%s%%"' % (Concept.tableName, name)

        return Concept.__listFromSQL(db_connection,sql)

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
    def __oneFromSQL(cls, db_connection, sql):
        cur=None
        
        try:
            cur=db_connection.cursor()
            cur.execute(sql)

            r=cur.fetchone()
            return Group(r[Group.idx_ID],r[Group.idx_Name],r[Group.idx_Description])
        
        except Exception as e:
            return None
            
        finally:
            if cur:
                cur.close()

    @classmethod
    def __listFromSQL(cls, db_connection, sql):
        cur=None
        
        try:
            cur=db_connection.cursor()
            cur.execute(sql)

            ret=[]
            for r in cur:
                ret.append(Group(r[Group.idx_ID],r[Group.idx_Name],r[Group.idx_Description]))
    
            return ret

        except:
            return []

        finally:
            if cur:
                cur.close()

    
    @classmethod
    def listAll(cls, db_connection):
        sql='SELECT * FROM %s' % (Group.tableName,)
        
        return Group.__listFromSQL(db_connection,sql)

    @classmethod
    def findID(cls, db_connection, name):
        sql='SELECT ID FROM %s WHERE name="%s"' % (Group.tableName, name)

        g=Group.__oneFromSQL(db_connection,sql)
        
        if g:
            return g.id
        else:
            return -1
            
    @classmethod
    def fromID(cls, db_connection, id):
        sql='SELECT * FROM %s WHERE ID=%d' % (Group.tableName, id)

        return Group.__oneFromSQL(db_connection,sql)

    @classmethod
    def fromName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name="%s"' % (Group.tableName, name)

        return Group.__oneFromSQL(db_connection,sql)

    @classmethod
    def likeName(cls, db_connection, name):
        sql='SELECT * FROM %s WHERE name LIKE "%%%s%%"' % (Group.tableName, name)
        
        return Group.__listFromSQL(db_connection,sql)

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

#     print 'all mensual:'
#     lstF=Fijo.findAllMensual(conn)
#     for f in lstF:
#         print f
#     print '--'

#     print 'all anual:'
#     lstF=Fijo.findAllAnual(conn)
#     for f in lstF:
#         print f
#     print '--'

#     c=Concept.fromName(conn,'Seguro coche Hyundai')
#     if not c:
#         print 'Concept not found!'
#     else:
#         lstF=Fijo.findConcept(conn,c)
#         for f in lstF:
#             print f

#     lstF=Fijo.findDate(conn,'2011-05-01', False)
#     for f in lstF:
#         print f
 
#     lstF=Fijo.findDateRange(conn,'2011-01-01','2011-09-01', False)
#     for f in lstF:
#         print f

    lstF=Fijo.findDateRange(conn,'2011-01-01','2011-09-01', True)
    for f in lstF:
        print f

#     lstF=Fijo.findDateSup(conn,'2011-06-01', False)
#     for f in lstF:
#         print f

#     lstF=Fijo.findDateSup(conn,'2011-06-01', True)
#     for f in lstF:
#         print f

# -->
    
    
###############################################################################    
if __name__=='__main__':
    main()
