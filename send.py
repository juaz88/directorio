from ast import keyword
from cgitb import html
from operator import concat
import smtplib

from email.mime.text import MIMEText

from SMTPEmail import SMTP


class send_email():

	def notificar (self,pin,send_mail,contact_name):
		
		
		mensaje=(f"""<h1> Hola {contact_name},</h1> <hr> <p> Te informamos que se ha generado un nuevo PIN para acceder a tus certificados:</p><br> <p><h2>Usuario: {send_mail} </h2>  <br> <h2>PIN: {pin} </h2> <hr></p>
			<p> Consulta tus certificados accediendo a la pagina  <a href="www.indugevi.com">www.indugevi.com</a> </p>  """)
		
		try:
			
			formato = MIMEText(mensaje,'html')
			formato['From']="JUAN DAVID DIAZ"
			formato['To']=contact_name
			formato['Subject']="Certificado tributario"

			serv=smtplib.SMTP('smtp.gmail.com',587)
			serv.starttls()
			serv.login('juaz8888@gmail.com','Economia88')
			serv.sendmail(from_addr="juaz8888@gmail.com",to_addrs=send_mail,msg=formato.as_string())
			serv.quit()
		
			return ("Notificacion exitosa")
		except:
			return("Ha ocurrido un error!")
