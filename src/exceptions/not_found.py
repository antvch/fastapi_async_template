class NotFoundError(Exception):
    def __init__(self, message: str = 'Запись не найдена'):
        self.message = message
