"""Entry point for frontend app and backend api."""

import sys

import uvicorn


def run_backend():
    """Run the backend API server.

    This function starts the FastAPI application using Uvicorn.
    """
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)


def run_frontend():
    pass


if __name__ == "__main__":
    # Pilih backend/frontend sesuai argumen atau kebutuhan
    # Contoh: python src/main.py frontend
    if len(sys.argv) > 1 and sys.argv[1] == "frontend":
        run_frontend()
    else:
        run_backend()
