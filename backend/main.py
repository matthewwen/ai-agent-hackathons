from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()

ALLOWED_IP = "10.214.209.4"
@app.middleware("http")
async def check_ip_address(request: Request, call_next):
    client_ip = request.client.host
    is_production  = os.getenv("PRODUCTION", "false") == "true"

    if is_production and client_ip != ALLOWED_IP:
        raise HTTPException(status_code=403, detail="Forbidden: Access denied")

    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}