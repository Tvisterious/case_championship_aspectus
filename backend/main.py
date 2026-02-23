from fastapi import FastAPI
from backend.routers import router

app = FastAPI(title="Синопсис протокола API")

# Подключаем все эндпоинты
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)