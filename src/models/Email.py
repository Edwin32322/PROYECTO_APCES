from email.message import EmailMessage
import ssl
from pathlib import Path
from flask import current_app

from ..services.AuthService import AuthService
import smtplib
from decouple import config

class Email:
    def __init__(self, email_emisor=config("EMAIL"), email_contrasena=config("EMAIL_PASSWORD")):
        self.email_emisor = email_emisor
        self.email_contrasena = email_contrasena
        
    def enviar_correo_general(self, user):
        em = EmailMessage()
        
        asunto = "Creación de Usuario en APCES"

        cuerpo = f"""
            <html>
                <body>
                    <p><strong>Hola,</strong></p>
                    <p>El siguiente correo es para informarle que se ha creado un usuario con su direccion de correo en el aplicativo APCES. Los datos de su usuario son los siguientes</p>
                    <ul>
                        <li>Usuario: {user.nombre_Usuario} </li>
                        <li>Contraseña: {user.contrasena_Usuario}</li>
                    </ul>
                    <p><strong>Recuerde no compartir su usuario a nadie que no sea se confianza</strong></p>
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
        em['To'] = user.correo_Usuario
        em['Subject'] = asunto
        
        em.add_alternative(cuerpo, subtype='html')  # Establecer el contenido HTML
        contexto = ssl.create_default_context()


        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
                smtp.login(self.email_emisor, self.email_contrasena)
                smtp.sendmail(self.email_emisor, user.correo_Usuario, em.as_string())
                return True

        except Exception as ex:
            raise ex

            
    def enviar_correo_recuperar_contrasena(self, email_receptor):
        usuario = AuthService.get_by_email(email_receptor)
        token = current_app.config['SERIALIZER'].dumps({'user_id': usuario.id_Usuario})
        em = EmailMessage()
        
        asunto = "Recuperación de contraseña"

        cuerpo = f"""
            <html>
                <body>
                    <p><strong>Hola,</strong></p>
                    <p>Hemos recibido una solicitud para recuperar tu contraseña. Tienes 5 minutos para realizar el cambio de contraseña, de lo contrario, se cancelará la petición.</p>
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
        
    def enviar_plan_mejora_e_info_llamado(self,llamadoObj):
        em = EmailMessage()
        asunto = "LLAMADO DE ATENCIÓN REGISTRADO - APCES"

        cuerpo = f"""
            <html>
                <body>
                    <p><strong>Hola,</strong></p>
                    <p>El siguiente correo es para informarle que usted ha recibido un llamado de atención y por tanto deberá cumplir con el plan de mejora adjunto</p>
                    <ul>
                        <li>Nombre del instructor quien realiza el llamado: {llamadoObj.nombre_Instructor} </li>
                        <li>Motivo: {llamadoObj.motivo}</li>
                    </ul>
                    <p><strong>Debe presentar el plan de mejora al instructor correspondiente</strong></p>
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
        em['To'] = llamadoObj.correo_Aprendiz
        em['Subject'] = asunto
        nombre_adjunto = 'LLamado_Atencion.pdf'

            
        em.add_alternative(cuerpo, subtype='html')  # Establecer el contenido HTML
        em.add_attachment(llamadoObj.plan_Mejora, maintype='application', subtype='octet-stream', filename=nombre_adjunto)
        contexto = ssl.create_default_context()


        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
                smtp.login(self.email_emisor, self.email_contrasena)
                smtp.sendmail(self.email_emisor, llamadoObj.correo_Aprendiz, em.as_string())
                return True

        except Exception as ex:
            raise ex
    
    def enviar_citacion_participantes(self,citacion):
        citacion.correo_Citacion = citacion.correo_Citacion.split(', ')
        em = EmailMessage()
        asunto = "CITACIÓN COMÍTE EVALUACIÓN Y SEGUIMIENTO - PARTICIPANTES"

        cuerpo = f"""
            <html>
                <body>
                    <p><strong>Hola,</strong></p>
                    <p>El siguiente correo es para informarle de la citación del comíte de evaluación y seguimiento que se desarrollará en:</p>
                    <ul>
                        <li>Fecha: {citacion.fecha_Citacion}</li>
                        <li>Hora: {citacion.hora_Citacion}</li>
                        <li>Centro de formación: Calle 52</li>
                        Por favor, asistir.
                        **********************NO RESPONDER - Mensaje Generado Automáticamente**********************
                        Este correo es únicamente informativo y es de uso exclusivo del destinatario(a), puede contener información privilegiada y/o confidencial. Si no es usted el destinatario(a) deberá borrarlo inmediatamente. 
                        Queda notificado que el mal uso, divulgación no autorizada, alteración y/o  modificación malintencionada sobre este mensaje y sus anexos quedan estrictamente prohibidos y pueden ser legalmente sancionados.
                        El SENA  no asume ninguna responsabilidad por estas circunstancias
                    <p/>
                </body>
            </html>
        """
        em['From'] = self.email_emisor
        em['To'] = citacion.correo_Citacion
        em['Subject'] = asunto
            
        em.add_alternative(cuerpo, subtype='html')  # Establecer el contenido HTML

        contexto = ssl.create_default_context()


        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
                smtp.login(self.email_emisor, self.email_contrasena)
                smtp.sendmail(self.email_emisor, citacion.correo_Citacion, em.as_string())
                return True

        except Exception as ex:
            raise ex