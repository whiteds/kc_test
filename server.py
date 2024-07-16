import serial
import time
import random

def generate_dummy_data(command):
    """명령어에 따라 더미 데이터를 무작위로 생성"""
    if command == "P001MOD":
        response = f"^D017001,{random.randint(1, 10)},{random.randint(100, 999)},{random.randint(300, 400)},{random.randint(20, 30)}"
    elif command == "P001ST1":
        response = f"^D120001,{random.randint(300, 500)},{random.randint(100, 300)},{random.randint(50, 100)},{random.randint(10, 20)}"
    elif command == "P001ST2":
        response = f"^D222001,{random.randint(300, 400)},{random.randint(300, 400)},{random.randint(300, 400)},{random.randint(500, 700)},{random.randint(50, 60)}"
    elif command == "P001ST3":
        response = f"^D321001,{random.randint(100, 200)},{random.randint(100, 200)},{random.randint(100, 200)},{random.randint(30, 50)}"
    elif command == "P001ST4":
        response = f"^D419001,{random.randint(50, 100)},{random.randint(0, 100000)},{random.randint(20, 40)}"
    elif command == "P001ST6":
        response = f"^D612001,{random.randint(0, 1)},{random.randint(0, 1)},{random.randint(0, 1)},{random.randint(5, 15)}"
    else:
        response = "UNKNOWN COMMAND"

    return response

def main():
    ser = None
    try:
        # COM3 포트에 115200 baudrate로 연결
        ser = serial.Serial('COM3', baudrate=115200, timeout=1)
        print("COM3 포트에 성공적으로 연결되었습니다.")

        buffer = ""

        while True:
            if ser.in_waiting:
                buffer += ser.read(ser.in_waiting).decode('latin-1')
                while '\n' in buffer:  # 개행 문자를 기준으로 명령어를 분리
                    line, buffer = buffer.split('\n', 1)
                    command = line.strip()
                    if command in ["P001MOD", "P001ST1", "P001ST2", "P001ST3", "P001ST4", "P001ST6"]:
                        print(f"수신한 명령어: {command}")
                        response = generate_dummy_data(command)
                        ser.write(f"{response}\r\n".encode())
                        print(f"송신한 데이터: {response}")
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"COM3 포트에 연결할 수 없습니다: {e}")
    except KeyboardInterrupt:
        print("사용자에 의해 프로그램이 중단되었습니다.")
    finally:
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
