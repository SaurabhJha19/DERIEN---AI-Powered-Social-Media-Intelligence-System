from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, users, posts, network

app = FastAPI(
    title="DERIEN Intelligence API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(network.router)
