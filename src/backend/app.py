import uvicorn
from fastapi import FastAPI

from src._version import __version__ as version
from src.backend.core.app_exception import register_exception_handlers
from src.backend.core.app_lifespan import lifespan
from src.backend.core.app_logging import setup_app_logging
from src.backend.core.app_router import register_routers

# Setup logging
setup_app_logging()
version = version.split(" ")[0]

# FastAPI app
app = FastAPI(
    title="modkit-otoplus",
    version=version,
    description="Menjembatani transaksi antara otomax dan addon addon otoplus.",
    lifespan=lifespan,
)

# Setup app
register_routers(app)
register_exception_handlers(app)


@app.get("/")
def root():
    return {"message": "modkit-otoplus up & running"}


if __name__ == "__main__":
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)
