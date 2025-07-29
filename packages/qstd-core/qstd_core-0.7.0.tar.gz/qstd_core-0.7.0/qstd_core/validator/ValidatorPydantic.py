import typing

from pydantic import BaseModel, ValidationError

from . import TargetNameType
from .ValidatorABS import ValidatorABS
from .exceptions import SchemaValidationException


T = typing.TypeVar('T', bound=BaseModel)


class ValidatorPydantic(ValidatorABS, typing.Generic[T]):
    schema: typing.Type[T]

    def validate(self, payload: dict) -> T:
        try:
            return self.schema.parse_obj(payload)
        except ValidationError as ex:
            raise self.errors_mapper(ex)

    def errors_mapper(self, ex: ValidationError):
        errors_list = []
        for error in ex.errors():
            location = list(error['loc'])
            if len(location) != 0:
                field_name = location[len(location) - 1]
            else:
                field_name = ''
            errors_list.append(
                SchemaValidationException.SchemaValidationItemException(
                    self.format_error_message(error['msg'], field_name),
                    location=location
                )
            )
        return SchemaValidationException(
            self.target_name,
            errors_list
        )

    @classmethod
    def format_error_message(cls, message: str, field_name: str) -> str:
        return message.replace('{field_name}', field_name)

    def get_schema_fields(self):
        return list(self.schema.__fields__.keys()) if self.target_name == TargetNameType.PARAMS else []
