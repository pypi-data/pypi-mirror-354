# src/stratio/models/__init__.py
from pydantic import BaseModel

from .bootstrap import BootstrapItem
from .cluster import Cluster, ClusterBase, ClusterMetadata, EC2Item, EKSItem, Infrastructure, InfrastructureList
from .customer import Subscriber, SubscriberBase, SubscriberList
from .dynamodb import DynamoModel, dynamo_list_to_python, dynamo_to_python
from .logs import StreamItem
from .repositories import Chart, UploadResult

__all__ = [
    "BootstrapItem",
    "Cluster",
    "ClusterBase",
    "ClusterMetadata",
    "Infrastructure",
    "InfrastructureList",
    "EC2Item",
    "EKSItem",
    "Subscriber",
    "SubscriberBase",
    "StreamItem",
    "SubscriberList",
    "Chart",
    "UploadResult",
    "DynamoModel",
    "controllers",
    "globals",
    "dynamo_to_python",
    "dynamo_list_to_python",
    "Error",
]


class Error(BaseModel):
    source: str
    error: str
