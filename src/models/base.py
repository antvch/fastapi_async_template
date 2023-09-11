from typing import Any, Iterable

from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()


class DatabaseModel(metaclass=DeclarativeMeta):
    __abstract__ = True
    __mapper_args__ = {'eager_defaults': True}

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():  # noqa: WPS110
            setattr(self, key, value)

    registry = mapper_registry
    metadata = mapper_registry.metadata

    def as_dict(
            self,
            include: Iterable | None = None,
            exclude: Iterable | None = None,
    ) -> dict[Any, Any]:
        """
        Возвращает модель в виде словаря.

        :param include: Список полей, которые нужно включить
        :param exclude: Список полей, которые нужно исключить

        :returns: dict
        """
        return self._get_attributes(include=include, exclude=exclude)

    def __str__(self) -> str:
        attributes = '|'.join(
            str(column_value)
            for field_name, column_value in self._get_attributes().items()
        )
        return f'<{self.__class__.__qualname__} {attributes}>'  # noqa: WPS237

    def _get_attributes(
            self,
            include: Iterable | None = None,
            exclude: Iterable | None = None,
    ) -> dict[Any, Any]:
        if include == exclude and include is not None:
            raise ValueError('Only exclude or include, not both')
        if include is not None:
            return {field_name: column_value
                    for field_name, column_value in self.__dict__.items()
                    if not field_name.startswith('_') and field_name in include
                    }
        if exclude is not None:
            return {field_name: column_value
                    for field_name, column_value in self.__dict__.items()
                    if not field_name.startswith('_') and field_name not in exclude
                    }
        return {field_name: column_value
                for field_name, column_value in self.__dict__.items()
                if not field_name.startswith('_')
                }
