from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .middleware import APIKeyMiddleware
from .routes import roles, permissions, role_permissions, user_roles, query

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="RBAC Platform",
    description="Centralized Role-Based Access Control",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API key middleware
app.add_middleware(APIKeyMiddleware)

# Include routers
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(role_permissions.router)
app.include_router(user_roles.router)
app.include_router(query.router)

# Health check endpoint (no auth required)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "RBAC Platform API"}