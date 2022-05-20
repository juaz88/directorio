from mimetypes import init
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

    def add_document(self,filename,cod_dir):
        conn=sqlite3.connect('bd.db')    
        cur=conn.cursor()
        
        query=(f"SELECT COUNT(*) FROM DOCUMENTO WHERE NOMBRE_FILE='{filename}' AND COD_DIRECT='{cod_dir}'")
        cur.execute(query)
        result=cur.fetchall()
      
        if result[0][0]==0:
            data=(filename,cod_dir)
            query="INSERT INTO DOCUMENTO (NOMBRE_FILE,COD_DIRECT) VALUES (?,?)"
            cur.execute(query,data)
            conn.commit()
            conn.close() 
            return True
        else:
            conn.close() 
            return False
            
    def consulta_document(self,cod):
        try:
            conn=sqlite3.connect('bd.db')    
            cur=conn.cursor()    
            query=f"SELECT * FROM DOCUMENTO WHERE COD_DIRECT='{cod}'"
            cur.execute(query)
            data=cur.fetchall()
            return list(data)
        except:
            return 0        
        
    def delete_document(self,cod_doc):
        try:
            conn=sqlite3.connect('bd.db')    
            cur=conn.cursor()    
            query=f"DELETE FROM DOCUMENTO WHERE COD='{cod_doc}'"
            cur.execute(query)
            conn.commit()
            conn.close() 
            return True
        except:
            return False         
    
    def consulta_directorio(self, cod):
        try:
            conn=sqlite3.connect('bd.db')    
            cur=conn.cursor()    
            query=f"SELECT * FROM DIRECTORIO WHERE COD='{cod}'"
            cur.execute(query)
            data=cur.fetchall()
            return (data)
        except:
            return 0
        
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
            
    def login_admin(self,cod,clave):
        conn=sqlite3.connect('bd.db')
        cur=conn.cursor()
        try:
            query=f"SELECT * FROM USER WHERE COD='{cod}' AND CLAVE='{clave}'"
            cur.execute(query)
            data=cur.fetchall()
            return data
        except :
            return 0
    
    def actualizar_directorio(self,cod,tipo,nombre,email,pin):
        conn=sqlite3.connect('bd.db')
        cur=conn.cursor()
        try:
            query=f"UPDATE DIRECTORIO SET TIPO='{tipo}', NOMBRE='{nombre}', EMAIL='{email}', PIN='{pin}' WHERE COD='{cod}' "
            cur.execute(query)
            conn.commit()
            conn.close()
            return ""   
        except:
            return "ERROR...No se pudo actualizar intenta mas tarde"
