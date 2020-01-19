# python object를 보내는 방법

import socket
import time
import pickle

HEADERSIZE = 10

# 소켓 네트워크 형식, 스트리밍 형식 데이터 받음.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 서버 컴퓨터명과 포트 설정
s.bind((socket.gethostname(), 3525))
# 최대 5개의 클라이언트로부터 접속 허용
s.listen(5)

while True:
    # 접속 허용. 따로 조건 없음.
    clientsocket, address = s.accept()
    # 서버에 메세지 보여줌
    print(f"Connection from {address} has been established!")

    # 클라이언트에 보낼 피클로 보낼 임의의 binary object
    d = {1:'Hey', 2:'There'}
    msg = pickle.dumps(d)

    # 보낼 메세지 앞에 메세지 길이 + 빈 공간 HEADERSIZE 만큼 삽입하고 보냄
    msg = bytes(f"{len(msg):<{HEADERSIZE}}","utf-8") + msg
    # 클라이언트에 메세지 보냄
    clientsocket.send(msg)

""" video #2
import socket
import time

HEADERSIZE = 10

# 소켓 네트워크 형식, 스트리밍 형식 데이터 받음.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 서버 컴퓨터명과 포트 설정
s.bind((socket.gethostname(), 3525))
# 최대 5개의 클라이언트로부터 접속 허용
s.listen(5)

while True:
    # 접속 허용. 따로 조건 없음.
    clientsocket, address = s.accept()
    # 서버에 메세지 보여줌
    print(f"Connection from {address} has been established!")
    # 클라이언트에 메세지 보냄
    msg = "welcome to sa757's local server"
    # 보낼 메세지 앞에 메세지 길이 + 빈 공간 HEADERSIZE 만큼 삽입하고 보냄
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    # 클라이언트에 메세지 보냄
    clientsocket.send(bytes(msg, "utf-8"))

    while True:
        # 3초마다 깨어나서 데이터 보냄.
        time.sleep(3)
        # 현재 시각 메세지 만들기
        msg = f"The time is! {time.time()}"
        # 현재시각 메세지를 헤더를 달아서 보내기.
        msg = f"{len(msg):<{HEADERSIZE}}" + msg # fixed lengh 10 characters
        clientsocket.send(bytes(msg, "utf-8"))
"""


""" video #1
import socket
# 소켓 네트워크 형식, 스트리밍 형식 데이터 받음.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 서버 컴퓨터명과 포트 설정
s.bind((socket.gethostname(), 3525))
# 최대 5개의 클라이언트로부터 접속 허용
s.listen(5)

while True:
    # 접속 허용. 따로 조건 없음.
    clientsocket, address = s.accept()
    # 서버에 메세지 보여줌
    print(f"Connection from {address} has been established!")
    # 클라이언트에 메세지 보냄
    clientsocket.send(bytes("welcome to sa757's local server", "utf-8"))
    # 연결 종료
    clientsocket.close()
"""
