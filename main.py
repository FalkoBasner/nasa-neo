from fastapi import FastAPI

from nasa_neo.routers.neo import router as neo_router

app = FastAPI()
app.include_router(neo_router)


@app.get("/health")
def health():
    return {"status": "ok"}
