import enum


class TargetNameType(str, enum.Enum):
    QUERY = 'query',
    BODY = 'body',
    PARAMS = 'params'
    UNION = 'union'
