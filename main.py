
from distutils.log import error
from email.mime import base
import os

import random
from flask import Flask,send_file, redirect, render_template,url_for, request
from database import baseD
from send import send_email
from werkzeug.utils import secure_filename

app=Flask(__name__)


@app.route('/')
def inicio():
    error_user=""
    error_pin=""
    error_email=""
    pin=""
    email=""
    error_send=""
    return render_template('index.html',error_user=error_user,error_pin=error_pin ,error_email=error_email,pin=pin,email=email,error_send=error_send)


@app.route('/view_admin',methods=['get','post'])
def admin():
    return render_template('view_admin.html')
    
@app.route('/login_admin', methods=['get','post'])
def login_admin():
    user=""
    clave=""
    if request.method=="POST":
        
        if request.form['user'] and request.form['clave']:
            user=request.form['user'] 
            clave=request.form['clave']
            conn=baseD()
            data=conn.login_admin(user,clave)
            print(data)
            if data==0 or not data:
                error="El usuario no se encuentra registrado!"    
                return render_template('login_admin.html',error=error, user=user, clave=clave)
            else:
                return admin()
        else:
            error="Las credenciales no son correctas"    
            return render_template('login_admin.html',error=error,user=user, clave=user)
    else:
        return render_template('login_admin.html',error="",user=user, clave=clave)
    
@app.route('/legal')  
def legal():
    return render_template('login_admin.html',error="",user="", clave="")

@app.route('/portal_admin', methods=['POST','GET'])
def p_admin():
    if request.method=='GET':
        opcion=request.args.get('opcion')
        cod=""
        tipo=""
        nombre=""
        email=""
        error=""
        if opcion=='3':
            cod=request.args.get('cod')
            tipo=request.args.get('t')
            nombre=request.args.get('name')
            email=request.args.get('email')
            error=""
        
        
        if opcion=='4':
            cod=request.args.get('cod')
            tipo=request.args.get('t')
            nombre=request.args.get('name')
            email=request.args.get('email')
            send=send_email()
            data=baseD().consulta_directorio(cod)
            pin=data[0][4]
            error=send.notificar(pin,email,nombre)
                
            
            
        return render_template('view_admin.html',opcion=opcion,data_create=["","","",""] ,data=["","","","",""],error=error,data_update=[cod,tipo,nombre,email])
    
    if request.method=="POST":
        #Procedimiento para el formulario nuevo directorio
        data_create=[]
        conn=baseD()
        if request.form['id_form']=="new_dir":
            error=""
            tipo=request.form['tipo']
            if tipo=="":
                error=error + "Tipo vacio\n"    
            data_create.append(tipo)
            documento=request.form['documento']
            data_create.append(documento)
            if documento=="":
                error =error + " Documento vacio\n"
            else:
                dct=conn.consulta_directorio(cod=documento) 
                if len(dct)>0:
                    error="El documento ya existe en la base de datos.\n"
            nombre=request.form['nombre']
            data_create.append(nombre)
            if nombre=="":
                error=error + " Nombre vacio\n"
            email=request.form['email']
            data_create.append(email)
            if email=="":
                error=error + " Email vacio\n"
            
            
            
            if error=="":    
                pin=genera_pin(documento,email)               
                
                conn.nuevo_directorio(cod=documento,tipo=tipo,nombre=nombre,email=email,pin=pin) 
                return render_template('view_admin.html',opcion='1',error=error,data_create=["","","",""])
            else:
                print(data_create)    
                return render_template('view_admin.html',opcion='1',error=error,data_create=data_create)
               
            
        if request.form['id_form']=="search_dir":
            error=""
            if request.form['cod']!="":
                cod=request.form['cod']
                conn=baseD()
                data=conn.consulta_directorio(cod=cod)
                data_doc=baseD().consulta_document(cod=cod)
                print(data_doc)
                if data:
                    return render_template('view_admin.html',opcion='2',data=data,error=error,data_doc=data_doc)
                else:
                    error="El codigo no se encuentra en base de datos"
                    return render_template('view_admin.html',opcion='2', data=[(cod,"","","","")],error=error,data_doc=data_doc)
            else:
                error="El campo no puede quedar vacio"
                return render_template('view_admin.html',opcion='2', data=["","","","",""],error=error,data_doc=data_doc)         

        if request.form['id_form']=='update':
            error=""
            conn=baseD()
            cod=request.form['cod']
            tipo=request.form['tipo']
            nombre=request.form['nombre']
            email=request.form['email']
            
            if nombre=="":
                error=error + "Nombre vacío "
            if email=="":
                error=error + "email vacío " 
            
            if error !="":    
                return render_template('view_admin.html',opcion='3',error=error,data_update=[cod,tipo,nombre,email])    
            else:
                pin=genera_pin(cod,email)
                error=conn.actualizar_directorio(cod=cod,tipo=tipo,nombre=nombre,email=email,pin=pin)
                
                if error:
                    return error
                else:
                    
                    return render_template('view_admin.html',opcion='2',data=["","","","",""],error="")   
        
                
@app.route('/user',methods=['GET', 'POST'])
def user():
    if request.method=='POST':
        email=request.form['email']
        pin=request.form['pin']
        error_email=""
        error_pin=""
        error_user=""
        error_send=""
        if not email:
            error_email="Debe ingresar un correo valido!"
            return render_template('index.html',error_pin=error_pin ,error_email=error_email,error_user=error_user,pin=pin,email=email,error_send=error_send) 
        elif not pin:
            error_pin= "Debe ingresar un PIN valido!" 
            return render_template('index.html',error_pin=error_pin,error_user=error_user,error_email=error_email,pin=pin,email=email,error_send=error_send ) 
        else:
            
            conn=baseD()
            data=conn.valida_usuario(email=email, pin=pin)
            
            if data==0 or not data:
                error_user="El usuario no se encuentra registrado!"
                
                return render_template('index.html',error_user=error_user,error_pin=error_pin ,error_email=error_email,pin=pin,email=email,error_send=error_send )
                              
            else:
                cod=data[0][0]
                data_doc=baseD().consulta_document(cod=cod)
                return render_template("login_user.html", data=data[0],data_doc=data_doc)
        

@app.route('/uploader',methods=['POST'])
def upload():
    if request.method=="POST":
        cod=request.form['cod']
        f=request.files['archivo']
        nombre=cod +"_" + f.filename
        filename=secure_filename(nombre) 
        
        try:
            
            document=baseD().add_document(filename=filename,cod_dir=cod)
            data=baseD().consulta_directorio(cod=cod)
            data_doc=baseD().consulta_document(cod=cod)
            if document==True:
                
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                return render_template('view_admin.html',opcion='2',data=data,error="",error_add="",data_doc=data_doc)
                
               
            else:
                return render_template('view_admin.html',opcion='2',data=data,error="",error_add="El archivo ya existe en la base de datos",data_doc=data_doc)
             
            
        except:
            return "Ha ocurrido un error!"
    
@app.route('/download', methods=['GET'])
def download():
    if request.method=="GET":
        file_name=request.args.get('file_name')    
        ruta="./certificados/"+file_name
        return send_file(ruta,as_attachment=True)

@app.route('/delete',methods=['GET'])
def delete_doc():
    if request.method=="GET":
        cod_doc=request.args.get('cod_doc')
        file_name=request.args.get('file_name')
        cod=request.args.get('cod')
        ruta="./certificados/"
        error_add=""
        dlt=baseD().delete_document(cod_doc=cod_doc)
        if dlt==True:
            
            borrar=ruta+file_name
            try:
                os.remove(borrar)
            except:
                dlt=baseD().delete_document(cod_doc=cod_doc)
                data=baseD().consulta_directorio(cod=cod)
                data_doc=baseD().consulta_document(cod=cod)    
                return render_template('view_admin.html',opcion='2',data=data,error="",error_add=error_add,data_doc=data_doc)
                           
        else:
                
            error_add="Upss!! No se pudo borrar el documento"
            
            
        data=baseD().consulta_directorio(cod=cod)
        data_doc=baseD().consulta_document(cod=cod)    
        return render_template('view_admin.html',opcion='2',data=data,error="",error_add=error_add,data_doc=data_doc)
         
@app.route('/solicitud',methods=['POST'])
def solicitud():
    
    if request.method=="POST":
        error_send=""
        nombre=request.form['nombre']
        print(nombre)
        email_send=request.form['email_send']
        documento=request.form['documento']
        mensaje=request.form['mensaje']
        if nombre=="":
            error_send=error_send+"error"
        if not email_send:
            error_send=error_send+"error"
        if not documento:
            error_send=error_send+"error"
        if not mensaje:
            mensaje=""
            
        if error_send!="":
            return render_template('index.html',error_pin="" ,error_email="",error_user="",pin="",email="",error_send="Ingrese todos los datos requeridos")              
        else:
            
            solic=send_email().solicitud(nombre,email_send,documento,mensaje)
            return solic   
        #nombre,email,documento,mensaje         
    else:
        return render_template('index.html',error_pin="" ,error_email="",error_user="",pin="",email="",error_send="¡No se pude enviar su solicitud!")       
           
#--------------------------METODOS SIN MARCADOR ------------------------------                        
def genera_pin(documento,email):
    cadena=documento+email
    lista=[]
    for i in cadena:
        lista.append(i)    
    
    pin=""
    secuencia=random.sample(lista,5)
    for i in secuencia:
        pin=pin+i
        
    return(pin)         
       


    


if __name__=='__main__':
    
    app.config['UPLOAD_FOLDER']="./certificados"
    app.run(port=3000,debug=True)
    
    
    