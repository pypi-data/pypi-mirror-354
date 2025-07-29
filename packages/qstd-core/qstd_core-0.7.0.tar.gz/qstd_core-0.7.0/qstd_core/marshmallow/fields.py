import enum
from typing import AnyStr

import typing
from marshmallow import fields, ValidationError


def custom_field_factory(field_cls: typing.Type[fields.Field]):
    class CustomField(field_cls):
        _field_name = None
        deprecated = None
        meta_one_of: list
        base_openapi_schema: dict = dict()

        default_error_messages = {
            "required": "{field_name} is required field.",
            "null": "{field_name} can not be empty.",
            "validator_failed": "Invalid value.",
        }

        @property
        def name(self):
            return self._field_name

        @name.setter
        def name(self, value):
            self._field_name = self.data_key or value
            for validation in self.get_validation():
                validation.field_name = self._field_name

        def __init__(
            self,
            *args,
            transform=None,
            transform_after=None,
            description: str = None,
            meta_one_of=None,
            deprecated=None,
            example=None,
            **kwargs
        ):
            super().__init__(*args, **kwargs)
            self._transform = transform
            self._transform_after = transform_after
            self.description = description
            self.meta_one_of = meta_one_of
            self.deprecated = deprecated
            self.example = example

        def get_validation(self):
            if self.validate is None:
                return []
            elif type(self.validate) is list:
                return self.validate
            else:
                return [self.validate]

        def transform(self, value):
            if self._transform is not None:
                if isinstance(self._transform, list):
                    for f in self._transform:
                        value = f(value)
                else:
                    value = self._transform(value)
            return value

        def transform_after(self, value):
            if self._transform_after is not None:
                if isinstance(self._transform_after, list):
                    for f in self._transform_after:
                        value = f(value)
                else:
                    value = self._transform_after(value)
            return value

        def make_error(self, key: str, **kwargs) -> ValidationError:
            return super().make_error(key, field_name=self._field_name, **kwargs)

        def _deserialize(self, value, attr, data, **kwargs) -> AnyStr:
            return self.transform_after(super()._deserialize(self.transform(value), attr, data, **kwargs))

        def _serialize(self, value, attr, obj, **kwargs) -> AnyStr:
            return self.transform_after(super().serialize(self.transform(value), attr, obj, **kwargs))

        def openapi_schema(self):
            if hasattr(self, 'nested'):
                schema = self.nested.openapi_schema()
            elif hasattr(self, 'inner'):
                schema = self.base_openapi_schema.copy()
                schema['items'] = self.inner.openapi_schema()
            else:
                schema = self.base_openapi_schema.copy()
            schema['nullable'] = self.allow_none
            if self.dump_default:
                schema['default'] = self.dump_default
            elif self.missing != fields.missing_:
                schema['default'] = self.missing
            if self.example is not None:
                schema['example'] = self.example
            if self.deprecated is not None:
                schema['deprecated'] = self.deprecated
            if self.description is not None:
                schema['description'] = self.description
            if hasattr(self, 'enum') and hasattr(self, 'by_value'):
                if issubclass(self.enum, enum.Enum):
                    schema['enum'] = list(
                        map(lambda e: e.value if self.by_value else e.name, self.enum)
                    )
                elif isinstance(self.enum, list):
                    schema['enum'] = self.enum
            for v in self.get_validation():
                schema.update(v.openapi_schema())
            if self.meta_one_of is not None:
                schema['oneOf'] = [one_of.openapi_schema() for one_of in self.meta_one_of]
            return schema

    return CustomField


class Field(custom_field_factory(fields.Field)):
    """
    For typing
    """


class Raw(custom_field_factory(fields.Raw)):
    base_openapi_schema = dict(type='object')


class Nested(custom_field_factory(fields.Nested)):
    default_error_messages = {"type": "{filed_name} contain invalid data type"}
    base_openapi_schema = dict(type='object')
    #
    # def openapi_schema(self):
    #     schema = self.nested.openapi_schema()
    #     schema['nullable'] = self.allow_none
    #     if self.dump_default:
    #         schema['default'] = self.dump_default
    #     elif self.missing != fields.missing_:
    #         schema['default'] = self.missing
    #     if self.example is not None:
    #         schema['example'] = self.example
    #     if self.deprecated is not None:
    #         schema['deprecated'] = self.deprecated
    #     if self.description is not None:
    #         schema['description'] = self.description
    #     return schema


class Pluck(custom_field_factory(fields.Pluck)):
    base_openapi_schema = dict(type='object')


class List(custom_field_factory(fields.List)):
    default_error_messages = {"invalid": "{field_name} are not a valid list."}
    base_openapi_schema = dict(type='array')


class Tuple(custom_field_factory(fields.Tuple)):
    base_openapi_schema = dict(type='array')


class String(custom_field_factory(fields.String)):
    default_error_messages = {
        "invalid": "{field_name} must be string.",
        "invalid_utf8": "{field_name} must be utf-8 string."
    }
    base_openapi_schema = dict(type='string')


class UUID(custom_field_factory(fields.UUID)):
    base_openapi_schema = dict(type='string', format='uuid')


class Number(custom_field_factory(fields.Number)):
    default_error_messages = {
        "invalid": "{field_name} must be number.",
        "too_large": "Number too large."
    }
    base_openapi_schema = dict(type='number')


class Integer(custom_field_factory(fields.Integer)):
    default_error_messages = {"invalid": "{field_name} must be integer."}
    base_openapi_schema = dict(type='integer')


class Float(custom_field_factory(fields.Float)):
    default_error_messages = {
        "special": "Special numeric values (nan or infinity) are not permitted.",
        "invalid": "{field_name} must be a float number.",
        "too_large": "Number too large."
    }
    base_openapi_schema = dict(type='number')


class Decimal(custom_field_factory(fields.Decimal)):
    base_openapi_schema = dict(type='number')


class Boolean(custom_field_factory(fields.Boolean)):
    default_error_messages = {"invalid": "{field_name} must be boolean."}
    base_openapi_schema = dict(type='boolean')


class DateTime(custom_field_factory(fields.DateTime)):
    default_error_messages = {
        "invalid": "Invalid date.",
        "format": '"{input}" cannot be formatted as a date.'
    }
    base_openapi_schema = dict(type='string', format='date-time')


class NaiveDateTime(custom_field_factory(fields.NaiveDateTime)):
    base_openapi_schema = dict(type='string', format='date-time')


class AwareDateTime(custom_field_factory(fields.AwareDateTime)):
    base_openapi_schema = dict(type='string', format='date-time')


class Time(DateTime):
    base_openapi_schema = dict(type='string', format='date-time')


class Date(DateTime):
    base_openapi_schema = dict(type='string', format='date')


class TimeDelta(custom_field_factory(fields.TimeDelta)):
    base_openapi_schema = dict(type='number')


class Mapping(custom_field_factory(fields.Mapping)):
    base_openapi_schema = dict(type='object', additionalProperties=True)


class Dict(custom_field_factory(fields.Dict)):
    pass


class Url(custom_field_factory(fields.Url)):
    base_openapi_schema = dict(type='string', format='url')


class Email(custom_field_factory(fields.Email)):
    base_openapi_schema = dict(type='string', format='email')


class IP(custom_field_factory(fields.IP)):
    base_openapi_schema = dict(
        type='string',
        oneOf=[dict(type='string', format='ipv4'), dict(type='string', format='ipv6')]
    )


class IPv4(custom_field_factory(fields.IPv4)):
    base_openapi_schema = dict(type='string', format='ipv4')


class IPv6(custom_field_factory(fields.IPv6)):
    base_openapi_schema = dict(type='string', format='ipv6')


class IPInterface(custom_field_factory(fields.IPInterface)):
    base_openapi_schema = dict(type='string')


class IPv4Interface(custom_field_factory(fields.IPv4Interface)):
    base_openapi_schema = dict(type='string')


class IPv6Interface(custom_field_factory(fields.IPv6Interface)):
    base_openapi_schema = dict(type='string')


class Enum(custom_field_factory(fields.Enum)):
    default_error_messages = {
        "unknown": "{field_name} must be one of: {choices}.",
    }
    base_openapi_schema = dict(type='string')


class Method(custom_field_factory(fields.Method)):
    base_openapi_schema = dict(type='string')


class Function(custom_field_factory(fields.Function)):
    base_openapi_schema = dict(type='string')


class Constant(custom_field_factory(fields.Constant)):
    base_openapi_schema = dict(type='string')


class Inferred(custom_field_factory(fields.Inferred)):
    pass


# Aliases
URL = Url
Str = String
Bool = Boolean
Int = Integer
