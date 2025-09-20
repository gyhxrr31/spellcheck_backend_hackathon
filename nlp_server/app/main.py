from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.health.router import router as health_router
from routers.process.router import router as process_router
from routers.spellcheck.router import router as spellcheck_router

import uvicorn

app = FastAPI(
    title="NLP Server API",
    description="Microservice for processing native language",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(process_router)
app.include_router(spellcheck_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app)