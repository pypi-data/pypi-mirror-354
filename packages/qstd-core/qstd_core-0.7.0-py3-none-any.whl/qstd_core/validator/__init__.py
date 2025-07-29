import typing

from pydantic import BaseModel

from .enums import TargetNameType
from .ValidatorABS import ValidatorABS
from .ValidatorPydantic import ValidatorPydantic
from .ValidatorMarshmallow import ValidatorMarshmallow
from .types import SchemaType
from ..marshmallow import Schema


TPM = typing.TypeVar("TPM", bound=BaseModel)


@typing.overload
def validator_factory(
    *,
    schema: typing.Type[TPM],
    target: TargetNameType,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
) -> ValidatorPydantic[TPM]: ...


@typing.overload
def validator_factory(
    *,
    schema: Schema,
    target: TargetNameType,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
) -> ValidatorMarshmallow: ...


def validator_factory(
    *,
    schema: SchemaType,
    target: TargetNameType,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
) -> ValidatorABS:
    if isinstance(schema, Schema):
        return ValidatorMarshmallow(schema, target, pass_data=pass_data, docs=docs)
    elif issubclass(schema, BaseModel):
        return ValidatorPydantic(schema, target, pass_data=pass_data, docs=docs)
    else:
        raise NotImplementedError()


def body(
    schema: typing.Type[SchemaType],
    *,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
):
    return validator_factory(schema=schema, target=TargetNameType.BODY, pass_data=pass_data, docs=docs)


def query(
    schema: typing.Type[SchemaType],
    *,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
):
    return validator_factory(schema=schema, target=TargetNameType.QUERY, pass_data=pass_data, docs=docs)


def params(
    schema: typing.Type[SchemaType],
    *,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
):
    return validator_factory(schema=schema, target=TargetNameType.PARAMS, pass_data=pass_data, docs=docs)


def validate(
    schema: typing.Type[SchemaType],
    *,
    target: TargetNameType = TargetNameType.UNION,
    payload: dict,
    pass_data: typing.Optional[bool] = True,
    docs: typing.Optional[bool] = True
):
    return validator_factory(schema=schema, target=target, pass_data=pass_data, docs=docs).validate(payload)

