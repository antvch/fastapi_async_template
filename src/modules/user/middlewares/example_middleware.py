from fastapi import Request, Response

from exceptions import NotFoundError


def example_middleware(request: Request, response: Response):
    """
    Пример middleware.

    :param request: HTTP запрос
    :type request: Request

    :param response: Ответ
    :type response: Response

    :raises NotFoundError: ошибка в middleware
    """
    if 'example' in request.query_params:
        raise NotFoundError('Ошибка в middleware')
