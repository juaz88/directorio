import smtplib
import ssl
import getpass

username="jeaxcorp@gmail.com"
psw="Economia88"

# context= ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(username,psw)
#     print("iniciaste sesion")
#     desteinatario="juas8888@gmail.com"
#     mensaje="Hoja luan este mensaje te lo hago llegar por PYTHON"
#     server.sendmail(username,desteinatario,mensaje)
#     print("mensaje enviado")
    
server=smtplib
server.SMTP_SSL(host="smyp.gmail.com",port=465)    
#server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)

server.login(username,psw)

server.sendmail(
  username, 
  "juaz8888@gmail.com", 
  "Hola juan este mensaje te lo hago llegar por PYTHON")

server.quit()

