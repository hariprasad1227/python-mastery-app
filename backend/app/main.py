"""
Python Mastery - Main FastAPI Application
Entry point for backend API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.db.session import init_db
from backend.app.api.runner import router as runner_router
from backend.app.api.progression import router as progression_router
from backend.app.api.mentor import router as mentor_router
from backend.app.api.auth import router as auth_router
from backend.app.api.projects import router as projects_router
from backend.app.api.interview import router as interview_router

# Initialize database schema and curriculum seeds
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade API for Python Mastery: Sandboxed execution, progression engine, and AI mentor."
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(runner_router, prefix=settings.API_PREFIX)
app.include_router(progression_router, prefix=settings.API_PREFIX)
app.include_router(mentor_router, prefix=settings.API_PREFIX)
app.include_router(projects_router, prefix=settings.API_PREFIX)
app.include_router(interview_router, prefix=settings.API_PREFIX)


from fastapi import Depends, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.db.session import get_db
from runner.runner import execute_learner_code

@app.get("/")
def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health/db")
def health_check_db(response: Response, db: Session = Depends(get_db)):
    """Health check validating live database connectivity."""
    try:
        db.execute(text("SELECT 1")).scalar()
        return {"status": "up", "database": "connected"}
    except Exception as exc:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "down", "error": str(exc)}


@app.get("/health/sandbox")
def health_check_sandbox(response: Response):
    """Health check verifying sandbox execution capability."""
    try:
        test_cases = [{"input": [2, 3], "expected": 5, "description": "health check"}]
        result = execute_learner_code(
            code="def add(a, b):\n    return a + b\n",
            entry_function_name="add",
            test_cases=test_cases,
            timeout_seconds=2.0
        )
        if result.get("passed"):
            return {
                "status": "up",
                "sandbox": "operational",
                "execution_time_ms": result.get("execution_time_ms", 0)
            }
        else:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {
                "status": "degraded",
                "error": result.get("stderr") or "Sandbox validation failed"
            }
    except Exception as exc:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "down", "error": str(exc)}


@app.get("/health")
def health_check(response: Response, db: Session = Depends(get_db)):
    """Composite health check for system monitoring."""
    db_ok = True
    db_err = None
    try:
        db.execute(text("SELECT 1")).scalar()
    except Exception as e:
        db_ok = False
        db_err = str(e)

    sandbox_ok = True
    sandbox_err = None
    try:
        res = execute_learner_code(
            code="def check():\n    return 42\n",
            entry_function_name="check",
            test_cases=[{"input": [], "expected": 42}],
            timeout_seconds=2.0
        )
        sandbox_ok = res.get("passed", False)
        if not sandbox_ok:
            sandbox_err = res.get("stderr") or "Validation test failed"
    except Exception as e:
        sandbox_ok = False
        sandbox_err = str(e)

    all_healthy = db_ok and sandbox_ok
    if not all_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "version": settings.VERSION,
        "components": {
            "database": {"status": "up" if db_ok else "down", "error": db_err},
            "sandbox": {"status": "up" if sandbox_ok else "down", "error": sandbox_err}
        }
    }

