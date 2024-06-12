import imaplib
import email
from email.header import decode_header
import re
from librerias.Utilities import *

username = "correo@gmail.com"
password = 'password'
imap = imaplib.IMAP4_SSL('smtp.correo.com')
imap.login(username, password)

cliente = connect_db('basededatos')
client_local = connect_db('')

client = cliente

normativa_collection = client.base.Normativa