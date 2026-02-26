from fastapi import FastAPI
from .routers import router  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Синопсис протокола API")


app.include_router(router)



@app.middleware("http")
async def log_request_path(request, call_next):
    print(f"FastAPI received path: {request.url.path}")
    response = await call_next(request)
    return response

origins = [
    "http://localhost:5173",               # для локальной разработки
    "http://127.0.0.1:5173",
    "https://alexto-ip.github.io",          # продакшен-фронтенд

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)