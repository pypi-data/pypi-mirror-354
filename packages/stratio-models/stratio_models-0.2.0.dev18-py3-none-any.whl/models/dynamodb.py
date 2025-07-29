from enum import Enum

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


class DynamoModel:
    @classmethod
    def from_dynamo_object(cls, dynamo_object: dict):
        python_dict = dynamo_to_python(dynamo_object)
        return cls(**python_dict)

    def to_dynamo_object(self):
        return python_to_dynamo(self.__dict__)


def dynamo_to_python(dynamo_object: dict) -> dict:
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in dynamo_object.items()}


def dynamo_list_to_python(dynamo_object: list[dict]) -> list[dict]:
    return [dynamo_to_python(item) for item in dynamo_object]


def python_to_dynamo(python_object: dict) -> dict:
    serializer = TypeSerializer()

    def to_serializable(val):
        if isinstance(val, Enum):  # noqa: F821
            return val.value
        return val

    return {k: serializer.serialize(to_serializable(v)) for k, v in python_object.items()}
