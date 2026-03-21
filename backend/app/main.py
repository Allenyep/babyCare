from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine
from app.db import Base
from app.api import babies, parents, tasks, knowledge, scheduler, fatigue

app = FastAPI(
    title=settings.APP_NAME,
    description="智能家庭育儿助手 - 基于智能分配和负载均衡的育儿管理平台",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {
        "message": "Welcome to BabyCare API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "babies": "/api/v1/babies",
            "parents": "/api/v1/parents",
            "tasks": "/api/v1/tasks",
            "knowledge": "/api/v1/knowledge",
            "scheduler": "/api/v1/scheduler",
            "fatigue": "/api/v1/fatigue"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(babies.router, prefix="/api/v1")
app.include_router(parents.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(scheduler.router, prefix="/api/v1")
app.include_router(fatigue.router, prefix="/api/v1")
