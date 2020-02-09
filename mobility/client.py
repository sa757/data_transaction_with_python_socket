# 코드 응용시 아래 링크 참고 : 서버 + Reader용 클라이언트 + 챗 클라이언트2
# https://youtu.be/ytu2yV3Gn1I?list=PLQVvvaa0QuDdzLB_0JSTTcl8E8jsJLhR5&t=1189
import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3525

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # 메세지 수신 차단 해제

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    #message = ""

    if message: # if message is not empty
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True: # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header): # if username_header is empty
                print("Connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

    except IOError as e: # 예외 처리
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e: # 예외처리
        print("General error", str(e))
        sys.exit()
