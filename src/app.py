import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Templete API", description="Solufit Microservice Network", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

if __name__ == "__main__":
    if os.getenv("DEBUG") == "True":
        uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True, log_config="log_config_debug.yaml")
    else:
        uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True, log_config="log_config.yaml")
