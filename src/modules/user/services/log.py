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

        f = open("storage/log.txt", "w")
        f.write(now.strftime("%d.%m.%Y %H:%M:%S") + "\n")
        f.write(message + "\n\n")
        f.close()