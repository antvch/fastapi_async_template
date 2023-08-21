from datetime import datetime


class LogsService:
    def __init__(self):
        self.filepath = 'storage/log.txt'

    def to_file(self, message: str):
        """
        Записывает сообщение в лог-файл.

        :param message: Сообщение для логирования
        :type message: str
        """
        now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        with open(self.filepath, 'a') as log_file:
            log_file.write(f'{now}: {message} \n')
