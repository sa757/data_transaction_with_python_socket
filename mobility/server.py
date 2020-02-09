import socket
import select
import pickle

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3525

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket] # 추후 고객 추가될 곳

clients = {}
transactions= []

sdir = './status.pkl'

with open(sdir, 'wb') as p:
    pickle.dump(transactions, p)

def receive_message(client_socket):
    try:
        # recv(bufsize) -- 한 번에 수신할 수 있는 최대 데이터양
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {
        "header": message_header,
        "data": client_socket.recv(message_length)
        }

    except:
        return False

while True:
    # select.select(읽기위해 대기중, 쓰기 위해 대기중, 예외 상태 대기중)
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # 소켓을 순환하며 정보 업데이트
    for notified_socket in read_sockets:
        # 서버 소켓 자신인 경우 이하 실행(리스트 맨 앞 위치하기 때문에 항상 맨 처음 실행 됨)
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept() # 항상 허용

            user = receive_message(client_socket) # 메세지 수신

            if user is False: # False 발생해도 일단 실행
                continue

            sockets_list.append(client_socket) # 허용한 고객소켓을 리스트에 추가

            clients[client_socket] = user # 고객 딕셔너리에 메세지 저장

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else: # 고객 소켓인 경우 이하 실행
            message = receive_message(notified_socket) # 메세지 받고
            if message is False: # 내용 없으면 이하 실행
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket) # 리스트에서 고객 소켓 삭제(연결 중단)
                del clients[notified_socket] # 고객 딕셔너리에서도 삭제
                continue

            user = clients[notified_socket] # 고객 딕셔너리에서 해당 고객 정보 가져옴
            print(f"Received message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}") # 해당 고객 헤더, 데이터 출력

            # 현재 서비스 사용중인 전체 고객 출력
            transactions.append([user, message])

            with open(sdir, 'wb') as p:
                pickle.dump(transactions, p)

            with open(sdir, 'rb') as p:
                out = pickle.load(p)
                print(out) # 조회용
            # 현재 서비스 중인 전체 택시 출력
            # 매칭 결과 출력

            # 매칭결과 고객 전송
            # 매칭결과 택시 전송

            # # 이하 받은 데이터 전 고객에게 공유
            # for client_socket in clients: # clients의 key를 떨군다.
            #     if client_socket != notified_socket: # 공유할때 문자 보낸 사람은 제외
            #         client_socket.send(user['header']+user['data']+message['header']+message['data'])

    # 예외 상태의 소켓을 떨굼
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket) # 리스트에서 고객 소켓 삭제(연결 중단)
        del clients[notified_socket] # 고객 딕셔너리에서도 삭제
