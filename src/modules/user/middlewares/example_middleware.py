from fastapi import Request, Response
from ..exceptions.not_found import NotFoundException

def example_middleware(request: Request, response: Response):
    """
    Пример middleware
    """
    if "example" in request.query_params:
        raise NotFoundException("Ошибка в middleware")