"""Modul service_result.py

Modul ini berfungsi sebagai gerbang utama untuk menangani hasil operasi service di backend.

- Kelas ServiceResult membungkus hasil operasi service, baik success maupun exception.
- Fungsi handle_result digunakan untuk mengelola hasil tersebut, melempar exception jika gagal, atau mengembalikan value jika sukses.
- Exception yang dilempar akan terstruktur dan dapat ditangani oleh handler FastAPI, sehingga frontend dapat menerima response error yang konsisten.

Cocok digunakan untuk seluruh service layer pada aplikasi ini.

Hasan Maki and Copilot
"""

import inspect
from typing import Any

from src.backend.exceptions.cst_exception import AppExceptionError
from src.mlog.mylog import logger


class ServiceResult:
    def __init__(self, arg: Any):
        if isinstance(arg, AppExceptionError):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
        self.value = arg

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        # NOTE : Handle any cleanup if necessary
        # Currently, this method is empty as per the original code
        pass


def caller_info() -> str:
    """Get information about the caller function."""
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult, log_success: bool = False):
    """Handle the result of a service operation."""
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    else:
        if log_success:
            logger.info(f"Success result from {caller_info()}")
        with result as result_value:
            return result_value
