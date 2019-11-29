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
PORT = 6010 #porta onde esta o servidor

'''
socket.AF_INET = socket ip
socket.SOCK_STREAM = tipo TCP
'''
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST,PORT)
servidor.bind(orig)
servidor.listen(1) #suporta uma maquina

connection, cliente = servidor.accept()

print "Conectado por", cliente

def upload():
    print ("Recebendo ...")
    #recebe o tamanho do arquivo em bytes
    size_arq = struct.unpack("h",connection.recv(2))[0]
    print ('Tamanho do arquivo enviado...',size_arq)
    #recebendo o nome do arquivo
    file_name = connection.recv(1024)
    
    #criando um arqivo com o mesmo nome do arquivo de upload
    arq = open('/home/helter/Desktop/Cherno/FTP-SERVER/Servidor/Arquivos/{}'.format(file_name),'wb')
    recebidos = 0
    '''
    Enquanto o numero de bytes recebidos for menor que o 
    tamanho do arquivo, ele vai continuar enviando
    '''
    connection.send("1")
    while recebidos < size_arq:
        print("estou aqui")
        dados = connection.recv(1024)
        arq.write(dados)
        recebidos += 1024
        print("e agora aqui")
    arq.close()
    print('Saindo...')

def download():
    print ("Enviando arquivo...")
    file_name = connection.recv(1024)
    print(file_name)
    try:
        print("Abrindo arquivo...")
        arq = open('/home/helter/Desktop/Cherno/FTP-SERVER/Servidor/Arquivos/{}'.format(file_name),'rb')
    except:
        print("Erro ao abrir o arquivo")
    #size_arq = ("h",sys.getsizeof(arq))
    connection.send(struct.pack("h",sys.getsizeof(arq)))

    try:
        for i in arq:
            connection.send(i)
    except:
        print ("Erro ao enviar os arquivos...")
    arq.close()

def _list():
    print ('Listando...')
    #listdir retorna uma lista com os arquivos do diretorio atual
    #getcwd retorna o diretorio atual
    lista = os.listdir(os.getcwd())
    connection.send(struct.pack("h",len(lista)))
    for i in lista:
        connection.send(struct.pack("i",sys.getsizeof(i)))
        connection.send(i)
        connection.recv(1024)
    print ('Diretorio enviado com sucesso!')
    

def quit():
    connection.close()
    servidor.close()
    os.execl(sys.executable, sys.executable, *sys.argv)



while True:
    print ("\nEsperando por instrucoes...")
    '''
    aux = raw_input()
    if aux[:4].upper() == "QUIT":
        quit()
        break
    '''
    data = connection.recv(1024)
    data.decode("utf-8")
    print ("\nRecebendo instrucoes...", data)
    if data == "UPLD":
        upload() 
    elif data == "DWLD":
        download()
    elif data == "LIST":
        _list()
    elif data == "QUIT":
        quit()
        break
    else:
        print ("Comando nao reconhecido")

