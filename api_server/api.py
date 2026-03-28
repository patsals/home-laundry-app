from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import time


app = FastAPI(
        title="Laundry API Server"
)

API_VERSION = "v1"

@app.get("/")
async def root():
    return JSONResponse(
        status_code=200,
        content={"success": "you have arrived!"}
    )

@app.post(f"/api/{API_VERSION}/accelerometer_data")
async def post_accelerometer_data(request: Request):
    try:
        current_timestamp = time.time()
        current_timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_timestamp))
        data = await request.json()
        print(f"{current_timestamp_str} - {str(data)}")

        return JSONResponse(
                status_code=200,
                content={"success": "data received"}
            )

    except Exception as e:
        return JSONResponse(
                status_code=400,
                content={"failure": f"{str(type(e))}: {str(e)}"}
            )