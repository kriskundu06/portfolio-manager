from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.portfolio import router as portfolio_router
from backend.app.routes.performance import router as performance_router
from backend.app.routes.comparison import router as comparison_router


app = FastAPI(
    title="AI Portfolio Manager",
    description="PPO-based multi-asset portfolio management API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://portfolio-manager-taupe-pi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "PPO Market Baseline"
    }


app.include_router(portfolio_router)
app.include_router(performance_router)
app.include_router(comparison_router)