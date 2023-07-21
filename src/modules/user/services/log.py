from datetime import datetime


class Log:
    @staticmethod
    def to_file(
        message: str
    ):
        """
        Запись сообщения в файл

        :param message: Сообщение для логирования
        """
        now = datetime.now()

        with open("storage/log.txt", "a") as f:
            f.write(f'{now.strftime("%d.%m.%Y %H:%M:%S")}: {message} \n')