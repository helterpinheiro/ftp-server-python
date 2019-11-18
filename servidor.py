'''
Devs: Helter Pinheiro, Julio Cesar, Gustavo ROberth
Servidor simples FTP
inicio: 15/11/2019
'''
import socket
import sys
import os
import struct 

print '\nBem-vindo ao servidor FTP \nEsperando conexao...\n'
HOST = '127.0.0.1' #endereco ip do servidor
PORT = 6000 #porta onde esta o servidor

'''
socket.AF_INET = socket ip
socket.SOCK_STREAM = tipo TCP
'''
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST,PORT)
servidor.bind(orig)
servidor.listen(1) #suporta uma maquina

connection, cliente = servidor.accept()

print 'Conectado por', cliente
