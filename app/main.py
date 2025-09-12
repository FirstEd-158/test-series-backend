from fastapi import FastAPI
from app.database import init_db
from app.routers import auth_routes, user_routes, hello_routes, domain_routes, subject_routes

app = FastAPI(title="FirstEd website", version='1.0')

@app.on_event("startup")
async def on_startup():
  await init_db()

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(hello_routes.router)
app.include_router(domain_routes.router)
app.include_router(subject_routes.router)
