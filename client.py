# python object를 받는 방법

import socket
import pickle
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), 3525))

while True:
    full_msg = b""
    new_msg = True
    while True:
        # 메시지 받음(받은 메세지 저장할 buffer 메모리)
        msg = s.recv(10)
        if new_msg:
            # 새로 받은 메세지 길이 출력(길이 + 빈공간 부분임)
            print(f"new message length : {msg[:HEADERSIZE]}")
            # 메세지 길이 할당
            msglen = int(msg[:HEADERSIZE])
            # False로 변경
            new_msg = False
        # full_msg에 업데이트
        full_msg += msg
        # 풀메세지 길이(41) - 10 = 31 이므로 현재는 msglen과 항상 같음
        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            # 메세지 출력
            print(full_msg[HEADERSIZE:])

            # 받은 피클 열어서 내용물 보기
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            # 신규 메세지 True로 변경
            new_msg = True
            # 전체 메세지 초기화
            full_msg = b""
    print(full_msg)

""" video #2
# 헤더를 포함한 데이터를 받아서 적재해두다가
# 특정 조건에 적합하면 적재한 데이터 전체 출력하고
# 다시 처음부터 시작하는 프로세스.
# 헤더  + 데이터를 같이 보내는게 2번째 영상의 포인트
import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((socket.gethostname(), 3525))

while True:
    full_msg = ""
    new_msg = True
    while True:
        # 메시지 받음(받은 메세지 저장할 buffer 메모리)
        msg = s.recv(10)
        if new_msg:
            # 새로 받은 메세지 길이 출력(길이 + 빈공간 부분임)
            print(f"new message length : {msg[:HEADERSIZE]}")
            # 메세지 길이 할당
            msglen = int(msg[:HEADERSIZE])
            # False로 변경
            new_msg = False
        # full_msg에 업데이트
        full_msg += msg.decode('utf-8')
        # 풀메세지 길이(41) - 10 = 31 이므로 현재는 msglen과 항상 같음
        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            # 메세지 출력
            print(full_msg[HEADERSIZE:])
            # 신규 메세지 True로 변경
            new_msg = True
            # 전체 메세지 초기화
            full_msg = ""
    print(full_msg)
"""

""" video #1
import socket
# 소켓 네트워크 형식, 스트리밍 형식 데이터 받음.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 접속할 서버 컴퓨터명과 포트 설정
s.connect((socket.gethostname(), 3525))

full_msg = ""
while True:
    # 메시지 받음(받은 메세지 저장할 buffer 메모리)
    msg = s.recv(8)
    # 메시지가 너무 짧으면 멈춤
    if len(msg) <= 0:
        break
    # 받은 메세지 저장해둠.
    full_msg += msg.decode("utf-8")
# 전체 메시지 출력
print(full_msg)

"""
