from fastapi import FastAPI
from routers.status import router as status_router

app = FastAPI()

app.include_router(status_router, prefix="/status")
