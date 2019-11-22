'''
Devs: Helter Pinheiro, Julio Cesar, Gustavo ROberth
Servidor simples FTP
inicio: 15/11/2019
'''
import socket
import sys
import os
import struct 

print ('\nBem-vindo ao   servidor FTP \nEsperando conexao...\n')
HOST = '127.0.0.1' #endereco ip do servidor
PORT = 6011 #porta onde esta o servidor

'''
socket.AF_INET = socket ip
socket.SOCK_STREAM = tipo TCP
'''
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST,PORT)
servidor.bind(orig)
servidor.listen(1) #suporta uma maquina

connection, cliente = servidor.accept()

print ('Conectado por', cliente)

def upload():
    print ("Recebendo ...")
    file = 'file_output.txt'
    size_arq = struct.unpack("h",connection.recv(2))[0]
    print ('Tamanho do arquivo enviado...',size_arq)
    arq = open(file,'wb')
    recebidos = 0
    aux = 20
    '''
    Enquanto o numero de bytes recebidos for menor que o 
    tamanho do arquivo, ele vai continuar enviando
    '''
    while recebidos < size_arq:
        dados = connection.recv(1024)
        arq.write(dados)
        recebidos += 1024
    arq.close()
    
    print('Saindo...')


while True:
    print ("\nEsperando por instrucoes...")
    data = connection.recv(1024)
    data.decode("utf-8").strip()
    print ("\nRecebendo instrucoes...", data)

    if data == "UPLD":
        upload() 
    elif data[:4].upper() == "QUIT":
        quit()
        break
    else:
        print ("Comando nao reconhecido")
