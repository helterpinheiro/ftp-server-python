'''
Devs: Helter Pinheiro, Julio Cabral, Gustavo Roberth
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
    #recebendo o arquivo
    file_name = connection.recv(1024)
    
    #criando um arqivo com o mesmo nome do arquivo de upload
    arq = open('/home/helter/Desktop/Cherno/FTP-SERVER/Servidor/Arquivos/{}'.format(file_name),'wb')
    recebidos = 0
    '''
    Enquanto o numero de bytes recebidos for menor que o 
    tamanho do arquivo, ele vai continuar enviando
    '''
    connection.send("1")
    #enquanto o recebidos for menor que o tamanho do arquivo
    #ele vai continuar recebendo o arquivo
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
    #recebe o nome do arquivo
    file_name = connection.recv(1024)
    print(file_name)
    try:
        #abre o arquivo pra leitura
        print("Abrindo arquivo...")
        arq = open('/home/helter/Desktop/Cherno/FTP-SERVER/Servidor/Arquivos/{}'.format(file_name),'rb')
    except:
        print("Erro ao abrir o arquivo")
    #Envia o tamanho do arquivo pro cliente
    connection.send(struct.pack("h",sys.getsizeof(arq)))
    #enviando o arquivo
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
    #enviando o tamanho do diretorio 
    connection.send(struct.pack("h",len(lista)))
    #percorre a lista enviando o diretorio pro cliente
    '''
    Primeiro se envia o tamanho do arquivo que ta na lista
    depois se envia o arquivo
    logo apos se recebe um ok sinalizando que o envio ocorreu bem
    '''
    for i in lista:
        connection.send(struct.pack("i",sys.getsizeof(i)))
        connection.send(i)
        connection.recv(1024)
    print ('Diretorio enviado com sucesso!')

def _cd():
    #enviando uma requisicao afirmando que a funcao esta ativa
    connection.send("1")
    my_folder = connection.recv(1024)
    print 'diretorio...{}'.format(my_folder)
    #os.chdir faz a mudanca de diretorio
    try:
        os.chdir(my_folder)
        print(os.getcwd())
    except:
        print('Diretorio nao reconhecido...')


def quit():
    connection.close()
    servidor.close()
    os.execl(sys.executable, sys.executable, *sys.argv)


#laco infinito que espera sempre as requisicoes
while True:
    print ("\nEsperando por instrucoes...")
    #recebe as requisicoes das funcoes do cliente
    data = connection.recv(1024)
    #recebe e decodifica de utf-8
    data.decode("utf-8")
    print ("\nRecebendo instrucoes...", data)
    if data == "UPLD":
        upload() 
    elif data == "DWLD":
        download()
    elif data == "LIST":
        _list()
    elif data == "CD":
        _cd()
    elif data == "CD..":
        cd()
    elif data == "QUIT":
        quit()
        break
    else:
        print ("Comando nao reconhecido")

