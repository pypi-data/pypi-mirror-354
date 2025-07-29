import typing

from marshmallow import ValidationError, Schema

from . import TargetNameType
from .exceptions import SchemaValidationException
from .ValidatorABS import ValidatorABS
from ..logger import app_core_logger


logger = app_core_logger.getChild(__name__)

TP = typing.TypeVar('TP', bound=dict)
TR = typing.TypeVar('TR', bound=dict)


class ValidatorMarshmallow(ValidatorABS, typing.Generic[TR]):
    schema: Schema

    @typing.overload
    def validate(self, payload: typing.List[TP]) -> typing.List[TR]: ...

    @typing.overload
    def validate(self, payload: TP) -> TR: ...

    def validate(self, payload: typing.Union[dict, list]) -> typing.Union[dict, list]:
        try:
            return self.schema.load(payload)
        except ValidationError as ex:
            raise self.errors_mapper(ex.messages)

    @classmethod
    def _marshmallow_errors_dict_mapper(
        cls,
        errors: dict,
        mapped_errors: typing.List[SchemaValidationException.SchemaValidationItemException],
        paths: typing.List[str]
    ):
        for key, value in errors.items():
            _local_paths = [*paths]
            if isinstance(value, dict):
                cls._marshmallow_errors_dict_mapper(value, mapped_errors, [*paths, str(key)])
            else:
                mapped_errors.append(cls.validation_error(','.join(value), [*_local_paths, str(key)]))
        return mapped_errors

    def errors_mapper(self, errors) -> SchemaValidationException:
        errors_list: typing.List[SchemaValidationException.SchemaValidationItemException] = []
        try:
            for key, value in errors.items():
                # Custom validators
                if key == '_schema':
                    key = ''
                if isinstance(value, list):
                    errors_list.append(self.validation_error(','.join(value), [str(key)]))
                elif isinstance(value, dict):
                    self._marshmallow_errors_dict_mapper(value, errors_list, [str(key)])
                else:
                    errors_list.append(self.validation_error(str(value), [str(key)]))
        except Exception as exc:
            logger.error(f'Failed parse validation exception for marshmallow: {exc}')

        return SchemaValidationException(self.target_name, errors_list)

    @classmethod
    def validation_error(cls, message: str, location: typing.List[str]):
        return SchemaValidationException.SchemaValidationItemException(
            message,
            location=location
        )

    def get_schema_fields(self):
        return list(self.schema.fields.keys()) if self.target_name == TargetNameType.PARAMS else []

