import configparser
import codecs
import os
import io

pwd = os.path.dirname(os.path.abspath(__file__))
print(pwd)
pwd1 = os.path.dirname(pwd)
print(pwd1)
proDir = os.path.split(pwd1)[0]
configPath = os.path.join(proDir, 'config\config.ini')
print(configPath)


class ReadConfig:
    def __init__(self):
        fd = io.open(configPath, "r", encoding='utf-8')
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='utf-8')

    def get_login(self, name):
        value = self.cf.get('login', name)
        return value

    def get_selection(self, name):
        value = self.cf.get('selection', name)
        return value

    def get_db(self, name):
        value = self.cf.get('db', name)
        return value

    def get_browserType(self, name):
        value = self.cf.get('browserType', name)
        return value


if __name__ == '__main__':
    print(ReadConfig().get_login('username'))