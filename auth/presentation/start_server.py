from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from auth.presentation.routers import tokens

app = FastAPI()
app.include_router(tokens.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.3.11", "http://192.168.3.11:1000", "http://192.168.3.11:1002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.3.11", port=1001)
