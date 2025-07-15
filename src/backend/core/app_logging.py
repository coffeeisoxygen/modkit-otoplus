from src.mlog.mylog import patch_uvicorn_loggers, setup_logging


def setup_app_logging():
    """Setup logging for the application."""
    setup_logging()
    patch_uvicorn_loggers()
