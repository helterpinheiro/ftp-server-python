'''
Devs: Helter Pinheiro, Julio Cesar, Gustavo Roberth
cliente simples FTP
inicio: 15/11/2019
'''
import socket
import sys
import os
import struct 

HOST =  '127.0.0.1' #endereco ip do servidor
PORT = 6000 #porta onde esta o servidor
'''
socket.AF_INET = socket ip
socket.SOCK_STREAM = tipo TCP
'''
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''
def upload(arquivo):
    #vamos testar se o arquivo existe mesmo 
    try:
        conteudo = open(arquivo, "rb")
    #caso nao exista
    except:
        print "Arquivo inexistente, verifique novamente!!"
'''
print '\nBem-vindo ao FTP Cliente'
print '\n** LISTA DE COMANDOS DO CLIENTE **\n\n'
print 'CON - Iniciar conexao\n'
print 'UPLD - Upload\n'
print 'DWL - Download\n'



#funcao connection
def connection():
    dest = (HOST,PORT)
    print "Enviando uma requisicao ao servidor..."
    try:
        #cliente se conectou ao destino
        cliente.connect(dest)
        print "Sucesso ao conectar..."
    except:
        print "Erro ao conectar..."

while True:
    aux = raw_input('\nEntre com um comando:\n')
    if aux[:3].upper() == "CON":
        connection()
    break
