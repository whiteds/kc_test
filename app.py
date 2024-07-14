import httpx
import asyncio
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

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
            response = await client.post("http://dev.recs.kr:8002/data/recv/data", json=data)
            print(f"Sent data: {data} | Response: {response.status_code}")
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(call_dummy_and_post())

@app.get("/")
async def root():
    return {"message": "FastAPI 서버가 실행 중입니다. 10초마다 외부 API를 호출합니다."}
