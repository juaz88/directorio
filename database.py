from mimetypes import init
import queue
import sqlite3

class baseD():
   
    
        
    def nuevo_directorio(self,cod,tipo,nombre,email,pin):
        conn=sqlite3.connect('bd.db')    
        cur=conn.cursor()
        data=(cod,tipo,nombre,email,pin)
        query="INSERT INTO DIRECTORIO (COD,TIPO,NOMBRE,EMAIL,PIN) VALUES (?,?,?,?,?)"
        cur.execute(query,data)
        conn.commit()
        conn.close()
        return("datos ingresados con exito")

    def consulta_directorio(self, cod):
        
        conn=sqlite3.connect('bd.db')    
        cur=conn.cursor()    
        query=f"SELECT * FROM DIRECTORIO WHERE COD={cod}"
        cur.execute(query)
        data=cur.fetchall()
        return (data)
    
    def valida_usuario(self,email,pin):
        conn=sqlite3.connect('bd.db')
        cur=conn.cursor()
        try:
            query=f"SELECT * FROM DIRECTORIO WHERE EMAIL='{email}' AND PIN='{pin}'"
            cur.execute(query)
            data=cur.fetchall()
            return data
        except:
            return 0
            
     