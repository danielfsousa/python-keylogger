import ftplib, sys

def enviar_arquivo(arquivo, nome):

    HOST = #HOST ADDRESS
    LOGIN = #LOGIN
    SENHA = #SENHA

    try:
        file = open(arquivo,'rb')
    except FileNotFoundError as e:
        raise FileNotFoundError("O arquivo nao foi encontrado")

    session = ftplib.FTP(HOST, LOGIN, SENHA)
    session.cwd("kl")
    session.storbinary("STOR " + nome, file)
    file.close()
    session.quit()

    return "ftp://" + HOST + "/kl/" + nome
