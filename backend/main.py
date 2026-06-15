from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .database import Base, engine
from .middleware import APIKeyMiddleware
from .routes import roles, permissions, role_permissions, user_roles, query

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RBAC Platform",
    description="Centralized Role-Based Access Control",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(APIKeyMiddleware)

app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(role_permissions.router)
app.include_router(user_roles.router)
app.include_router(query.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "RBAC Platform API"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="RBAC Platform",
        version="1.0.0",
        description="Centralized Role-Based Access Control",
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
