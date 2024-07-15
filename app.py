import httpx
import asyncio
from datetime import datetime
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

async def call_dummy_and_post():
    while True:
        commands = ["P001MOD", "P001ST1", "P001ST2", "P001ST3", "P001ST4", "P001ST6"]
        all_dummy_data = [generate_dummy_data(command) for command in commands]
        combined_data = ",".join(all_dummy_data)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data = {
            "data": combined_data,
            "timestamp": timestamp
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("http://dev.recs.kr:8002/data/recv/data", json=data)
                print(f"Sent data: {data} | Response: {response.status_code}")
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
                print(f"Error details: {exc}")
        await asyncio.sleep(10)

async def main():
    await call_dummy_and_post()

if __name__ == "__main__":
    asyncio.run(main())
