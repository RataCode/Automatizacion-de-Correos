from librerias.lib import *

status, mensajes = imap.select("INBOX")
mensajes = int(mensajes[0])
for i in range(mensajes, 1, -1):
    try:
        res, mensaje = imap.fetch(str(i), "(RFC822)")
    except:
        break
    for respuesta in mensaje:
        if isinstance(respuesta, tuple):
            mensaje = email.message_from_bytes(respuesta[1])
            from_ = mensaje.get("From")
            if "correo@gmail.es" in from_:
            # if "no-responder@boe.es" in from_:
                subject = decode_header(mensaje["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                if mensaje.is_multipart():
                    for part in mensaje.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload()[0].get_payload(decode=True).decode('latin-1').replace("\r\n"," ").replace("- ","").replace("  "," ")
                            titulo = re.findall( r'Título: (.*?) Departamento:', body, re.DOTALL)
                            departamento = re.findall( r'Departamento: (.*?) Publicación:', body, re.DOTALL)
                            publicacion = re.findall( r'Publicación: (.*?) Ver documento:', body, re.DOTALL)
                            fecha = re.findall(r'Publicación:.*?(\d{2}/\d{2}/\d{4}).*?Ver documento:', body,re.DOTALL)
                            formatted_dates = [datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d') for date in fecha]
                            documento=re.findall(r'Ver documento: (.*?)\s+\d+\.  Título:', body, re.DOTALL)
                            documento.append(re.findall( r'[^"]*Ver documento: (.*?)  Muchas', body, re.DOTALL)[0])

                            for i in range(0, len(titulo)):
                                normativa_collection.update_many({"Titulo":titulo[i]}, {"$set":{"Fecha":formatted_dates[i],"Departamento":departamento[i],"Publicacion":publicacion[i],"Documento":documento[i]}},upsert=True)                        
                        except:
                            pass
imap.close()
imap.logout()