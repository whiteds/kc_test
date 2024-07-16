import serial
import httpx
import time
from datetime import datetime

API_URL = "http://dev.recs.kr:8002/data/recv/data"
COMMANDS = ["P001MOD", "P001ST1", "P001ST2", "P001ST3", "P001ST4", "P001ST6"]
SERIAL_PORT = '/dev/serial0'
BAUDRATE = 115200

def read_from_serial(ser):
    if ser.in_waiting:
        return ser.readline().decode('latin-1').strip()
    return None

def send_to_api(data):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    payload = {
        "data": data,
        "timestamp": timestamp
    }
    response = httpx.post(API_URL, json=payload)
    print(f"Sent data: {payload} | Response: {response.status_code}")

def connect_serial(port, baudrate):
    while True:
        try:
            ser = serial.Serial(port, baudrate=baudrate, timeout=1)
            print(f"{port} 포트에 성공적으로 연결되었습니다.")
            return ser
        except serial.serialutil.SerialException as e:
            print(f"{port} 포트에 연결할 수 없습니다: {e}")
            print("5초 후 다시 시도합니다...")
            time.sleep(5)

def main():
    ser = None
    try:
        ser = connect_serial(SERIAL_PORT, BAUDRATE)

        while True:
            all_responses = []
            for command in COMMANDS:
                print(f"명령어 송신: {command}")
                ser.write(f"{command}\r\n".encode())  # 명령어 전송

                # 응답 대기 및 읽기
                time.sleep(0.3)  # 장치가 응답을 보낼 시간을 줌
                response = read_from_serial(ser)
                if response:
                    print(f"수신한 데이터: {response}")
                    all_responses.append(response)

            if all_responses:
                combined_response = ",".join(all_responses)
                send_to_api(combined_response)

            time.sleep(1)  # 1초 대기

    except KeyboardInterrupt:
        print("사용자에 의해 프로그램이 중단되었습니다.")
    finally:
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
