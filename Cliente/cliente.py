'''
Devs: Helter Pinheiro
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
#menu inicial do cliente
print ('\nBem-vindo ao FTP Cliente')
print ('\n** LISTA DE COMANDOS DO CLIENTE **\n')
print ('CON - Iniciar conexao\n')
print ('UPLD - Upload \n')
print ('DWLD - Download\n')
print ('LIST - Listar diretorio\n')

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
        #envia a mensagem com a requisicao UPLD para o servido
        #enviamos a mensagem codificada em utf-8
        cliente.send(msg.encode("utf-8"))
        print ("Enviando requisicao...")
    except:
        print ("Erro ao enviar requisicao...")
    #abre o arquivo passado pra ler
    arq = open(nome_arquivo,'rb')
    print ("Abrindo Arquivo...")
    #envia o tamanho do arquivo pra funcao upld do servidor
    cliente.send(struct.pack("h",sys.getsizeof(arq)))
    '''
    o cliente esta enviando o nome do arquivo para que se possa
    criar um arquivo com o nome igual na pasta do servidor
    '''
    cliente.send(nome_arquivo)
    cliente.recv(1024)
    #Enviando o arquivo 
    try:
       print ("Enviando...")
       for i in arq:
        cliente.send(i)   
    except:
        print("Erro ao enviar os arquivos...")
    arq.close()

#funcao download do cliente
def download(nome_arquivo):
    print "Download arquivo...{}".format(nome_arquivo)
    #requisicao do download
    msg = "DWLD"
    try:
        #envia a requisicao de download em utf-8
        cliente.send(msg.encode("utf-8"))
        print("Enviando requisicao...")
    except:
        print "Erro ao enviar requisicao..."
    #abre um arquivo no na pasta do cliente
    arq = open(nome_arquivo,'wb')
    #o cliente envia o nome do arquivo pra que a funcao download
    #do servidor possa procurar o arquivo em sua pasta
    cliente.send(nome_arquivo)
    #recebe o tamanho do arquivo do servidor
    size_arq = struct.unpack("h",cliente.recv(2))[0]
    print("tamanho do aqruivo...{}".format(size_arq))
    recebidos = 0
    #recebendo o arquivo
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
    #envia a requisicao LIST
    msg = "LIST"
    try:
        cliente.send(msg.encode("utf-8"))
        print("Enviando requisicao...")
    except:
        print "Erro ao enviar requisicao..."
    #recebe o tamanho do diretorio
    len_dir = struct.unpack("h", cliente.recv(2))[0]
    print('Tamanho do diretorio...{}'.format(len_dir))
    print ('Arquivos:')
    recebido = 0
    '''
    recebe o tamanho do arquivo
    recebe o arquivo
    envia uma requisicao 'ok' para sinalizar que o arquivo foi bem revebido
    '''
    while recebido < int(len_dir):
        buffer = struct.unpack("i",cliente.recv(4))[0]
        arch = cliente.recv(buffer)
        print("\t{}".format(arch))
        cliente.send("ok")
        recebido = recebido + 1
#funcao que troca os diretorios
def _cd(diretorio):
    #enviando a requisicao CD
    msg = "CD"
    try:
        cliente.send(msg.encode("utf-8"))
    except:
        print('Erro de comando...')
    #recebeu a requisicao '1' de confirmacao
    cliente.recv(1024)
    #envia o diretorio que quer entrar
    #se voce colocar .. retorna o diretorio anterior
    try:
        cliente.send(diretorio)
    except:
        print ('Nao foi possivel acessar o diretorio')

#laco infinito que espera os comandos passados pelo usuario
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
    
    elif aux[:2].upper() == "CD":
        _cd(aux[3:])
    
    elif aux[:4].upper() == "CD..":
        cd()
    
    elif aux[:4].upper() == "QUIT":
        quit()
        break
    aux = None

    
