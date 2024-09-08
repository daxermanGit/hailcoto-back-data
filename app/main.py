from fastapi import FastAPI
from app.routers import item
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.include_router(item.router, prefix="/item", tags=["item"])

origins = [
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API for Prediction actions given a item info"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)