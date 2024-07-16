import socket
import httpx
import time
from datetime import datetime

API_URL = "http://dev.recs.kr:8002/data/recv/data"
COMMANDS = ["P001MOD", "P001ST1", "P001ST2", "P001ST3", "P001ST4", "P001ST6"]
SERVER_ADDRESS = '192.168.0.74'
SERVER_PORT = 65432

def send_to_api(data):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    payload = {
        "data": data,
        "timestamp": timestamp
    }
    response = httpx.post(API_URL, json=payload)
    print(f"Sent data: {payload} | Response: {response.status_code}")

def main():
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        print(f"{SERVER_ADDRESS}:{SERVER_PORT}에 성공적으로 연결되었습니다.")

        while True:
            all_responses = []
            for command in COMMANDS:
                print(f"명령어 송신: {command}")
                client_socket.sendall(f"{command}\n".encode())  # 명령어 전송

                # 응답 대기 및 읽기
                time.sleep(0.5)  # 서버가 응답을 보낼 시간을 줌
                response = client_socket.recv(1024).decode('latin-1').strip()
                if response:
                    print(f"수신한 데이터: {response}")
                    all_responses.append(response)

            if all_responses:
                combined_response = ",".join(all_responses)
                send_to_api(combined_response)

            time.sleep(1)  # 1초 대기

    except socket.error as e:
        print(f"{SERVER_ADDRESS}:{SERVER_PORT}에 연결할 수 없습니다: {e}")
    except KeyboardInterrupt:
        print("사용자에 의해 프로그램이 중단되었습니다.")
    finally:
        if client_socket:
            client_socket.close()

if __name__ == "__main__":
    main()
