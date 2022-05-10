
import random
from winreg import REG_QWORD
from flask import Flask, redirect, render_template,url_for, request
from database import baseD

app=Flask(__name__)


@app.route('/')
def inicio():
    error_user=""
    error_pin=""
    error_email=""
    pin=""
    email=""
    return render_template('index.html',error_user=error_user,error_pin=error_pin ,error_email=error_email,pin=pin,email=email)


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
        
        if opcion=='3':
            cod=request.args.get('cod')
            tipo=request.args.get('t')
            nombre=request.args.get('name')
            email=request.args.get('email')
            
            
        return render_template('view_admin.html',opcion=opcion,data_create=["","","",""] ,data=["","","","",""],error="",data_update=[cod,tipo,nombre,email])
    
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
                if data:
                    return render_template('view_admin.html',opcion='2',data=data,error=error)
                else:
                    error="El codigo no se encuentra en base de datos"
                    return render_template('view_admin.html',opcion='2', data=[(cod,"","","","")],error=error)
            else:
                error="El campo no puede quedar vacio"
                return render_template('view_admin.html',opcion='2', data=["","","","",""],error=error)         

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
        if not email:
            error_email="Debe ingresar un correo valido!"
            return render_template('index.html',error_pin=error_pin ,error_email=error_email,error_user=error_user,pin=pin,email=email) 
        elif not pin:
            error_pin= "Debe ingresar un PIN valido!" 
            return render_template('index.html',error_pin=error_pin,error_user=error_user,error_email=error_email,pin=pin,email=email ) 
        else:
            
            conn=baseD()
            data=conn.valida_usuario(email=email, pin=pin)
            if data==0 or not data:
                error_user="El usuario no se encuentra registrado!"
                
                return render_template('index.html',error_user=error_user,error_pin=error_pin ,error_email=error_email,pin=pin,email=email )
                              
            else:
                
                return render_template("login_user.html", data=data[0])
        
            
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
    app.run(port=3000,debug=True)
    
    
    
    