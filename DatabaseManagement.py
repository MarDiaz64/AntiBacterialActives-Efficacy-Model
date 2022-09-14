import pandas as pd
import sqlite3
class DBManager:
    @classmethod
    def insert(cls,actives,dilution,hardness,dirty,ph,efficacy,idd):
        conn = sqlite3.connect('LocalSQL.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO data
                          (id,DDAC,BKC,Citric,Dilution,DDACppm,BKCppm,Citricppm,Hardness,Dirty,PH,Efficacy) 
                           VALUES 
                          (?,?,?,?,?,?,?,?,?,?,?,?)""",\
                        (idd,actives[0],actives[1],actives[2],dilution,\
                         (actives[0]*10000/dilution),(actives[1]*10000/dilution),(actives[2]*10000/dilution),\
                         hardness,dirty,ph,efficacy))
        conn.commit()
        conn.close()
    @classmethod    
    def getCleanedData(cls):
        conn = sqlite3.connect('LocalSQL.db')
        cursor = conn.cursor()
        data= pd.read_sql_query("SELECT * from data", conn)
        conn.commit()
        conn.close()
        return data.drop(columns=['ID','DDAC','BKC','Dilution','Citric'])
    
    #general usage for getting data, may be used at a later updates
    #@classmethod
    #def performQuery(cls,query): 
        #conn = sqlite3.connect('LocalSQL.db')
        #cursor = conn.cursor()
        #out = cursor.execute(query)
        #conn.commit()
        #cursor.close()
        #return out

