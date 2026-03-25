import asyncio
from fastapi import FastAPI
from app.api.xhs import router as xhs_router
from app.core.database import Base, engine
from app.core.browser_pool import browser_pool, _pw_executor
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(xhs_router)


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(_pw_executor, browser_pool.start)


@app.on_event("shutdown")
async def shutdown():
    _pw_executor.shutdown(wait=False, cancel_futures=True)


@app.get("/")
def root():
    return {"message": "xhs playwright service running"}
