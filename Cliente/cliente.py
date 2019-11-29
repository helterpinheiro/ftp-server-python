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
PORT = 6010#porta onde esta o servidor
'''
socket.AF_INET = socket ip
socket.SOCK_STREAM = tipo TCP
'''
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ('\nBem-vindo ao FTP Cliente')
print ('\n** LISTA DE COMANDOS DO CLIENTE **\n')
print ('CON - Iniciar conexao\n')
print ('UPLD - Upload\n')
print ('DWLD - Download\n')



#funcao connection
def connection():
    dest = (HOST,PORT)
    print ("Enviando uma requisicao ao servidor...")
    try:
        #cliente se conectou ao destino
        cliente.connect(dest)
        print ("Sucesso ao conectar...")
    except:
        print ("Erro ao conectar...")

#funcao upload do cliente
def upload(nome_arquivo):
    
    print ("Upload do Arquivo...")
    msg = "UPLD"
    try:
        cliente.send(msg.encode("utf-8"))
        print ("Enviando requisicao...")
    except:
        print ("Erro ao enviar requisicao...")
    arq = open(nome_arquivo,'rb')
    print ("Abrindo Arquivo...")
    cliente.send(struct.pack("h",sys.getsizeof(arq)))
    '''
    o cliente esta enviando o nome do arquivo para que se possa
    criar um arquivo com o nome igual na pasta do servidor
    '''
    cliente.send(nome_arquivo)
    cliente.recv(1024)
    try:
       print ("Enviando...")
       for i in arq:
        cliente.send(i)   
    except:
        print("Erro ao enviar os arquivos...")
    arq.close()

def download(nome_arquivo):
    print "Download arquivo...{}".format(nome_arquivo)
    msg = "DWLD"
    try:
        cliente.send(msg.encode("utf-8"))
        print("Enviando requisicao...")
    except:
        print "Erro ao enviar requisicao..."
    
    arq = open(nome_arquivo,'wb')
    cliente.send(nome_arquivo)
    size_arq = struct.unpack("h",cliente.recv(2))[0]
    print("tamanho do aqruivo...{}".format(size_arq))
    recebidos = 0
    try:
        while recebidos < size_arq:
            dados = cliente.recv(1024)
            arq.write(dados)
            recebidos += 1024
        arq.close()
        print('Saindo...')
    except:
        print("Erro no download...")

def _list():
    print('Listando diretorios...')
    msg = "LIST"
    try:
        cliente.send(msg.encode("utf-8").strip())
        print("Enviando requisicao...")
    except:
        print "Erro ao enviar requisicao..."
    
    len_dir = struct.unpack("h", cliente.recv(2))[0]
    print('Tamanho do diretorio...{}'.format(len_dir))
    print ('Arquivos:')
    recebido = 0
    while recebido < int(len_dir):
        buffer = struct.unpack("i",cliente.recv(4))[0]
        arch = cliente.recv(buffer)
        print("\t{}".format(arch))
        cliente.send("ok")
        recebido = recebido + 1

while True:
    aux = raw_input('\nEntre com um comando:\n')
    if aux[:3].upper() == "CON":
        connection()
    
    elif aux[:4].upper() == "UPLD":
        upload(aux[5:])
    
    elif aux[:4].upper() == "DWLD":
        download(aux[5:])
    
    elif aux[:4].upper() == "LIST":
        _list()
    
    elif aux[:4].upper() == "QUIT":
        quit()
        break
    aux = None

    
