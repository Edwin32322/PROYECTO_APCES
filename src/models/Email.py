from email.message import EmailMessage
import ssl
from flask import current_app
from ..services.AuthService import AuthService
import smtplib
from decouple import config

class Email:
    def __init__(self, email_emisor=config("EMAIL"), email_contrasena=config("EMAIL_PASSWORD")):
        self.email_emisor = email_emisor
        self.email_contrasena = email_contrasena
            
    def enviar_correo_recuperar_contrasena(self, email_receptor):
        usuario = AuthService.get_by_email(email_receptor)
        token = current_app.config['SERIALIZER'].dumps({'user_id': usuario.id_Usuario})
        em = EmailMessage()
        
        asunto = "Recuperación de contraseña"

        cuerpo = f"""
            <html>
                <body>
                    <p><strong>Hola,</strong></p>
                    <p>Hemos recibido una solicitud para recuperar tu contraseña. Tienes 60 minutos para realizar el cambio de contraseña.</p>
                        <ol>
                            <li>Accede al siguiente link: <a href='http://127.0.0.1:5900/recuperarContraseña/{usuario.id_Usuario}/{token}'>Recuperar Contraseña</li>
                            <li>Llena los campos con la nueva contraseña de tu preferencia</li>
                            <li>Confirma el envío</li>
                        </ol>
                    <p>Apces - Sena</p>
                    <p>
                        **********************NO RESPONDER - Mensaje Generado Automáticamente**********************
                        Este correo es únicamente informativo y es de uso exclusivo del destinatario(a), puede contener información privilegiada y/o confidencial. Si no es usted el destinatario(a) deberá borrarlo inmediatamente. 
                        Queda notificado que el mal uso, divulgación no autorizada, alteración y/o  modificación malintencionada sobre este mensaje y sus anexos quedan estrictamente prohibidos y pueden ser legalmente sancionados.
                        El SENA  no asume ninguna responsabilidad por estas circunstancias
                    <p/>
                </body>
            </html>
        """
        
        em['From'] = self.email_emisor
        em['To'] = email_receptor
        em['Subject'] = asunto
        
        em.add_alternative(cuerpo, subtype='html')  # Establecer el contenido HTML
        contexto = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
                smtp.login(self.email_emisor, self.email_contrasena)
                smtp.sendmail(self.email_emisor, email_receptor, em.as_string())
                return True
                
        except Exception as ex:
            raise ex
