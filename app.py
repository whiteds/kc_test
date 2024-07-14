import httpx
import asyncio
from datetime import datetime

def generate_dummy_data(command):
    """명령어에 따라 더미 데이터를 생성"""
    if command == "P001MOD":
        response = "^D017001,3,0100,380,24"
    elif command == "P001ST1":
        response = "^D120001,400,0200,0080,18"
    elif command == "P001ST2":
        response = "^D222001,380,379,381,600,55"
    elif command == "P001ST3":
        response = "^D321001,0118,0119,0118,38"
    elif command == "P001ST4":
        response = "^D419001,0078,0000100,31"
    elif command == "P001ST6":
        response = "^D612001,0,0,0,10"
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

        await asyncio.sleep(10)

async def main():
    await call_dummy_and_post()

if __name__ == "__main__":
    asyncio.run(main())
