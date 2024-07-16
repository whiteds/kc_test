import socket
import time
import random

def generate_dummy_data(command):
    """명령어에 따라 더미 데이터를 무작위로 생성"""
    if command == "P001MOD":
        response = f"D017001,{random.randint(1, 10)},{random.randint(100, 999)},{random.randint(300, 400)},{random.randint(20, 30)}"
    elif command == "P001ST1":
        response = f"D120001,{random.randint(300, 500)},{random.randint(100, 300)},{random.randint(50, 100)},{random.randint(10, 20)}"
    elif command == "P001ST2":
        response = f"D222001,{random.randint(300, 400)},{random.randint(300, 400)},{random.randint(300, 400)},{random.randint(500, 700)},{random.randint(50, 60)}"
    elif command == "P001ST3":
        response = f"D321001,{random.randint(100, 200)},{random.randint(100, 200)},{random.randint(100, 200)},{random.randint(30, 50)}"
    elif command == "P001ST4":
        response = f"D419001,{random.randint(50, 100)},{random.randint(0, 100000)},{random.randint(20, 40)}"
    elif command == "P001ST6":
        response = f"D612001,{random.randint(0, 1)},{random.randint(0, 1)},{random.randint(0, 1)},{random.randint(5, 15)}"
    else:
        response = "UNKNOWN COMMAND"

    return response

def main():
    host = '0.0.0.0'  # 로컬 호스트
    port = 65432        # 사용할 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("COM3 포트에 성공적으로 연결되었습니다.")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"{addr}에서 연결되었습니다.")

            buffer = ""

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                buffer += data.decode('latin-1')
                while '\n' in buffer:  # 개행 문자를 기준으로 명령어를 분리
                    line, buffer = buffer.split('\n', 1)
                    command = line.strip()
                    if command in ["P001MOD", "P001ST1", "P001ST2", "P001ST3", "P001ST4", "P001ST6"]:
                        print(f"수신한 명령어: {command}")
                        response = generate_dummy_data(command)
                        client_socket.sendall(f"{response}\r\n".encode())
                        print(f"송신한 데이터: {response}")

            client_socket.close()
            print(f"{addr}의 연결이 종료되었습니다.")

    except KeyboardInterrupt:
        print("사용자에 의해 서버가 중단되었습니다.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
