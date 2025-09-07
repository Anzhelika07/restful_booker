from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
import requests


class APIError(Exception):
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


def is_5xx_error(exception):
    """Проверяет, является ли исключение 5xx ошибкой сервера"""
    return isinstance(exception, APIError) and exception.status_code >= 500


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception(is_5xx_error)  # Используем retry_if_exception вместо retry_if_exception_type
)
def make_request_with_retry(request_func, *args, **kwargs):
    from utils.logger import log_request, log_response

    # Логируем запрос
    method = kwargs.get('method', 'GET')
    url = args[0] if args else kwargs.get('url')
    headers = kwargs.get('headers', {})
    data = kwargs.get('json', kwargs.get('data'))

    log_request(method, url, headers, data)

    # Выполняем запрос
    response = request_func(*args, **kwargs)

    # Логируем ответ
    log_response(response)

    # Проверяем статус код
    if not response.ok:
        raise APIError(
            f"API request failed with status {response.status_code}",
            status_code=response.status_code,
            response=response
        )

    return response