"""Entrypoint utama FastAPI app. Memastikan .env ter-load sebelum import lain.

Hasan Maki and Copilot
"""

from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src._version import __version__ as version
from src.backend.core.app_exception import register_exception_handlers
from src.backend.core.app_lifespan import lifespan
from src.backend.core.app_logging import setup_app_logging
from src.backend.core.app_router import register_routers

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

# Setup logging
setup_app_logging()
version = version.split(" ")[0]

# FastAPI app
app = FastAPI(
    title="modkit-otoplus",
    version=version,
    description="Localhost untuk menjembatani antara otomax dan addon addon otoplus,transaksi ke addon akan di parse dan di restruktur sebelum akhir nya di kembalikan ke otomax",
    lifespan=lifespan,
)

# Setup app
register_routers(app)
register_exception_handlers(app)


@app.get("/")
def root() -> dict[str, str]:
    """Endpoint root untuk health check aplikasi.

    Returns:
        dict[str, str]: Pesan status aplikasi.

    Hasan Maki and Copilot
    """
    return {"message": "modkit-otoplus up & running"}


if __name__ == "__main__":
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)
