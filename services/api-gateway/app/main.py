from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import scan
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="ScamShield API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
