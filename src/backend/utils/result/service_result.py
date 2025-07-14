from src.mlog.cst_logging import logger
import inspect

from src.backend.utils.exceptions.app_exceptions import AppExceptionError


class ServiceResult(object):
    def __init__(self, arg):
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
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult, log_success: bool = False):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    else:
        if log_success:
            logger.info(f"Success result from {caller_info()}")
        with result as result_value:
            return result_value
